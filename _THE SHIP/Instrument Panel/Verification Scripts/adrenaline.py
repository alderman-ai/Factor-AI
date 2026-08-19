#!/usr/bin/env python3
"""
adrenaline.py - executor for ADRENALINE work orders.

This file holds VERBS. The rules live in the Schema:

    _THE SHIP/Hitchhiker's Guide/Schema/ADRENALINE Rules.md

That file's table decides what is checked. This file decides what each verb
means. A work order decides nothing - it supplies values to be checked.

An unknown verb halts. It is never skipped: a rule the operator believes is
enforced but isn't is worse than no rule.

Two subcommands:
    inspect <work order>   read-only. runs every non-deferred rule, then
                           prints the probe path the assistant must write to.
    execute <work order>   re-runs those, adds the deferred probe rule, then
                           branches, routes, stamps, and consumes.
"""

import datetime
import os
import re
import shutil
import subprocess
import sys

RULES_FILE = "_THE SHIP/Hitchhiker's Guide/Schema/ADRENALINE Rules.md"

# Record format, not rules. Routing is recorded twice on purpose - the operator
# is comparing the two. ROUTE_KEY is a breadcrumb of basenames: compact,
# instantly verifiable, and the version that will visibly strain as hop counts
# grow. ROUTE_HEADING is the audit log: full paths, times, failed attempts too.
# The breadcrumb is derivable from the log, so a disagreement between them is
# evidence of tampering rather than a formatting quirk.
STAMP_KEY = "Successful"
ROUTE_KEY = "Route"
ROUTE_HEADING = "## Routing"


# ------------------------------------------------------------- utilities ----
def die(msg):
    print("HALT: " + msg)
    sys.exit(2)


def repo_root():
    d = os.path.abspath(os.path.dirname(__file__))
    while True:
        if os.path.isdir(os.path.join(d, ".git")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            die("cannot locate repo root (no .git found above this script)")
        d = parent


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def rel(root, path):
    return os.path.relpath(path, root).replace("\\", "/")


def split_frontmatter(text):
    """Return (ordered [(key, value)], body). No block -> ([], text)."""
    m = re.match(r"^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n?", text, re.S)
    if not m:
        return [], text
    pairs = []
    for line in m.group(1).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        pairs.append((k.strip(), v.strip()))
    return pairs, text[m.end():]


def render_frontmatter(pairs, body):
    lines = ["---"] + ["{}: {}".format(k, v) for k, v in pairs] + ["---", ""]
    return "\n".join(lines) + body


def resolve(root, path_value):
    """Resolve a form path. Literal first, then Obsidian-style implicit .md."""
    if not path_value:
        return None
    p = os.path.normpath(os.path.join(root, path_value))
    if os.path.exists(p):
        return p
    if os.path.exists(p + ".md"):
        return p + ".md"
    return None


def csv(value):
    return [v.strip() for v in value.split(",") if v.strip()]


# ---------------------------------------------------------- rules intake ----
def section(text, heading):
    m = re.search(r"^##[ \t]+" + re.escape(heading) + r"[ \t]*$(.*?)(?=^##[ \t]|\Z)",
                  text, re.M | re.S)
    return m.group(1) if m else None


def table_rows(text):
    """Yield cell lists for pipe-table rows, skipping the separator row."""
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip().strip("`").strip() for c in s.strip("|").split("|")]
        if cells and cells[0] and set(cells[0]) <= set("-: "):
            continue
        yield cells


def parse_args(value):
    """'Artifact, Outbox, depth=1' -> (['Artifact', 'Outbox'], {'depth': '1'})"""
    pos, kw = [], {}
    for tok in csv(value):
        tok = tok.strip("`").strip()
        if "=" in tok:
            k, v = tok.split("=", 1)
            kw[k.strip()] = v.strip()
        else:
            pos.append(tok)
    return pos, kw


def load_rules(root):
    path = os.path.join(root, RULES_FILE)
    if not os.path.isfile(path):
        die("rules file not found: {}".format(RULES_FILE))
    pairs, body = split_frontmatter(read(path))
    meta = dict(pairs)

    for key in ("Form", "Prefix", "Fields", "Fence file", "Consumed",
                "Run log", "Probe"):
        if not meta.get(key):
            die("rules file is missing frontmatter key: {}".format(key))

    block = section(body, "The rules")
    if block is None:
        die("rules file has no '## The rules' section")

    rules = []
    for cells in table_rows(block):
        if len(cells) < 3 or not cells[0].isdigit():
            continue
        num, verb, args = cells[0], cells[1], cells[2]
        if verb not in VERBS:
            die("unknown verb {!r} in rule {} of {}\n"
                "      A new verb is a code change, not a table edit. "
                "Nothing was run.".format(verb, num, RULES_FILE))
        pos, kw = parse_args(args)
        rules.append((num, verb, pos, kw))

    if not rules:
        die("rules table in {} has no rules".format(RULES_FILE))
    return meta, rules


# ----------------------------------------------------------------- fence ----
def fence_roots(root, fence_file):
    """Bullets under the fence file's '# Fence' heading, and nothing else.

    Later headings in that file - read/execute grants, notes - are deliberately
    NOT fence. Widening what The Guy may read must not quietly widen where ore
    is allowed to be."""
    path = os.path.join(root, fence_file)
    if not os.path.isfile(path):
        die("fence file not found: {}".format(fence_file))
    roots = [os.path.dirname(path)]  # "Your working directory"
    inside = False
    for line in read(path).splitlines():
        s = line.strip()
        if s.startswith("#"):
            inside = s.lstrip("#").strip().lower() == "fence"
            continue
        if inside and s.startswith("- "):
            roots.append(os.path.normpath(os.path.join(root, s[2:].strip())))
    return roots


def in_fence(path, roots):
    if path is None:
        return False
    p = os.path.abspath(path)
    for r in roots:
        r = os.path.abspath(r)
        if p == r or p.startswith(r + os.sep):
            return True
    return False


# ----------------------------------------------------------------- verbs ----
class Ctx(object):
    def __init__(self, root, meta, order_path, fields, body, roots):
        self.root = root
        self.meta = meta
        self.order_path = order_path
        self.fields = fields
        self.body = body
        self.roots = roots


def v_exactly_n_ticked(ctx, pos, kw):
    n = int(pos[0])
    got = len(re.findall(r"^\s*[-*]\s*\[[xX]\]", ctx.body, re.M))
    return got == n, "{} ticked, want {}".format(got, n)


def v_fields_assigned(ctx, pos, kw):
    missing = [f for f in pos if not ctx.fields.get(f, "")]
    if missing:
        return False, "missing: " + ", ".join(missing)
    return True, "{} of {} assigned".format(len(pos), len(pos))


def v_child_of(ctx, pos, kw):
    child_f, parent_f = pos[0], pos[1]
    depth = int(kw.get("depth", "1"))
    child = resolve(ctx.root, ctx.fields.get(child_f, ""))
    parent = resolve(ctx.root, ctx.fields.get(parent_f, ""))
    if child is None or parent is None:
        return False, "{} {}, {} {}".format(
            child_f, "ok" if child else "unresolved",
            parent_f, "ok" if parent else "unresolved")
    p = os.path.abspath(child)
    for _ in range(depth):
        p = os.path.dirname(p)
    ok = p == os.path.abspath(parent)
    return ok, "{} up from {} {} {}".format(
        depth, child_f, "==" if ok else "!=", parent_f)


def v_paths_in_fence(ctx, pos, kw):
    bad = [f for f in pos
           if ctx.fields.get(f, "")
           and not in_fence(os.path.normpath(
               os.path.join(ctx.root, ctx.fields[f])), ctx.roots)]
    if bad:
        return False, "out of fence: " + ", ".join(bad)
    return True, "all in fence"


def probe_path(ctx, field):
    where = ctx.fields.get(field, "")
    if not where:
        return None
    return os.path.normpath(os.path.join(ctx.root, where, ctx.meta["Probe"]))


def v_assistant_write_probe(ctx, pos, kw):
    """Deferred. The assistant must have created this probe with its Write
    tool. If this script wrote it, the script would be testing its own
    filesystem access, not the assistant's tool permissions - a different
    claim, and a false one."""
    p = probe_path(ctx, pos[0])
    if p is None:
        return False, "no {} assigned".format(pos[0])
    if not os.path.isfile(p):
        return False, "no probe at {}".format(rel(ctx.root, p))
    want = os.path.basename(ctx.order_path)
    got = read(p).strip()
    if got != want:
        return False, "probe says {!r}, expected {!r}".format(got, want)
    return True, "probe present and correct"


# verb -> (function, deferred). Deferred rules do not run during inspect,
# because inspect is read-only and the assistant has not acted yet.
VERBS = {
    "exactly-n-ticked": (v_exactly_n_ticked, False),
    "fields-assigned": (v_fields_assigned, False),
    "child-of": (v_child_of, False),
    "paths-in-fence": (v_paths_in_fence, False),
    "assistant-write-probe": (v_assistant_write_probe, True),
}


def run_rules(ctx, rules, include_deferred):
    results = []
    for num, verb, pos, kw in rules:
        fn, deferred = VERBS[verb]
        if deferred and not include_deferred:
            continue
        try:
            ok, detail = fn(ctx, pos, kw)
        except (IndexError, ValueError) as e:
            die("rule {} ({}) has bad args: {}".format(num, verb, e))
        results.append((num, verb, ok, detail))
    return results


# ----------------------------------------------------------- side effects ---
def stamp(path, value):
    text = read(path) if os.path.isfile(path) else ""
    pairs, body = split_frontmatter(text)
    pairs = [(k, v) for k, v in pairs if k != STAMP_KEY]
    pairs.append((STAMP_KEY, value))
    with open(path, "w", encoding="utf-8") as f:
        f.write(render_frontmatter(pairs, body))


def append_route(path, src_dir, dst_dir, via, ok):
    """Record one hop on the artifact, in both formats.

    Provenance is NOT verified here - the DoD audit at the Ship walks the full
    trail and decides whether the ore counts. A hop only testifies."""
    text = read(path) if os.path.isfile(path) else ""
    pairs, body = split_frontmatter(text)

    if ok:
        crumb = dict(pairs).get(ROUTE_KEY, "")
        hops = [h.strip() for h in crumb.split(">") if h.strip()]
        here = os.path.basename(src_dir.rstrip("/"))

        # A hop testifies only to what it did. If the trail does not already
        # end where this hop picked the artifact up, custody is unaccounted for
        # between the two - and that gap is recorded, never smoothed over.
        # Closing it silently would forge exactly the provenance the DoD audit
        # at the Ship exists to verify.
        if not hops:
            hops = [here]
        elif hops[-1] != here:
            hops += ["?", here]

        hops.append(os.path.basename(dst_dir.rstrip("/")))
        pairs = [(k, v) for k, v in pairs if k != ROUTE_KEY]
        pairs.append((ROUTE_KEY, " > ".join(hops)))

    entry = "- {} to {} {} via {} ({})".format(
        src_dir, dst_dir, datetime.datetime.now().strftime("%H%M"),
        via, "Success" if ok else "Failed")

    if ROUTE_HEADING in body:
        body = body.rstrip("\n") + "\n" + entry + "\n"
    else:
        body = body.rstrip("\n") + "\n\n" + ROUTE_HEADING + "\n\n" + entry + "\n"

    with open(path, "w", encoding="utf-8") as f:
        f.write(render_frontmatter(pairs, body))


def git_move(root, src, dest_dir):
    dest = "{}/{}".format(dest_dir.rstrip("/"), os.path.basename(src))
    r = subprocess.run(["git", "mv", rel(root, src), dest],
                       cwd=root, capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip(), dest


def write_log(ctx, results, actions, outcome):
    """Append one run record. Every path through this script - including the
    ones that refuse to do anything - lands here, so the failures are legible
    afterwards instead of only existing as terminal scrollback."""
    lines = ["",
             "## {}  {}  {}".format(
                 datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                 outcome, os.path.basename(ctx.order_path)),
             ""]
    for k in csv(ctx.meta["Fields"]):
        lines.append("- {}: `{}`".format(k, ctx.fields.get(k, "") or "<empty>"))
    lines += ["", "| # | verb | result | detail |", "|---|---|---|---|"]
    for num, verb, ok, detail in results:
        lines.append("| {} | {} | {} | {} |".format(
            num, verb, "PASS" if ok else "FAIL", detail))
    lines += ["", "| action | state | detail |", "|---|---|---|"]
    for label, state, detail in actions:
        lines.append("| {} | {} | {} |".format(label, state, detail))
    lines.append("")

    path = os.path.join(ctx.root, ctx.meta["Run log"])
    header_line = "" if os.path.isfile(path) else "# ADRENALINE run log\n"
    with open(path, "a", encoding="utf-8") as f:
        f.write(header_line + "\n".join(lines) + "\n")


def clear_probe(ctx, rules):
    for num, verb, pos, kw in rules:
        if verb == "assistant-write-probe":
            p = probe_path(ctx, pos[0])
            if p and os.path.isfile(p):
                os.remove(p)


# -------------------------------------------------------------- commands ----
def build_ctx(root, order_value):
    meta, rules = load_rules(root)

    order_path = resolve(root, order_value)
    if order_path is None:
        die("work order not found: {}".format(order_value))

    # Binding. A form is bound to its rules by filename, so a form the prefix
    # does not claim cannot be judged by these rules at all.
    name = os.path.basename(order_path)
    if not name.startswith(meta["Prefix"]):
        die("{!r} does not start with {!r}, so it is not a {} work order.\n"
            "      Nothing was checked and nothing was run."
            .format(name, meta["Prefix"], meta["Form"]))

    pairs, body = split_frontmatter(read(order_path))
    roots = fence_roots(root, meta["Fence file"])
    return Ctx(root, meta, order_path, dict(pairs), body, roots), rules


def report(results):
    for num, verb, ok, detail in results:
        print("  [{}] rule {}  {}  ({})".format(
            "PASS" if ok else "FAIL", num, verb, detail))


def print_header(ctx):
    print("Work order: {}".format(rel(ctx.root, ctx.order_path)))
    print("Rules:      {}".format(RULES_FILE))
    for k in csv(ctx.meta["Fields"]):
        print("  {:<10} {}".format(k + ":", ctx.fields.get(k, "") or "<empty>"))
    print()


def cmd_inspect(root, order_value):
    ctx, rules = build_ctx(root, order_value)
    print_header(ctx)
    report(run_rules(ctx, rules, include_deferred=False))
    print()

    deferred = [(n, p) for n, v, p, k in rules if v == "assistant-write-probe"]
    if not deferred:
        return
    num, pos = deferred[0]
    p = probe_path(ctx, pos[0])
    if p is None:
        print("Rule {} cannot be attempted: no {} assigned.".format(num, pos[0]))
        return
    if not in_fence(p, ctx.roots):
        # Never hand the assistant an instruction that breaches the fence.
        print("Rule {} cannot be attempted: the {} is outside the fence."
              .format(num, pos[0]))
        print("Do not write the probe. Run execute; rule {} fails there."
              .format(num))
        return
    print("Rule {} is yours to perform. Using your Write tool - not Bash, not"
          .format(num))
    print("this script - create:")
    print("  {}".format(rel(root, p)))
    print("containing exactly: {}".format(os.path.basename(ctx.order_path)))
    print("If the write is refused, do not work around it. Run execute anyway:")
    print("the missing probe is rule {} failing, and that is a real result."
          .format(num))


def cmd_execute(root, order_value):
    ctx, rules = build_ctx(root, order_value)
    results = run_rules(ctx, rules, include_deferred=True)

    print_header(ctx)
    report(results)
    print()

    all_ok = all(ok for _, _, ok, _ in results)
    actions = []       # every attempted side effect, performed or refused
    clear_probe(ctx, rules)

    def act(label, allowed, reason, do):
        """Perform a side effect, or record precisely why it was not."""
        if not allowed:
            actions.append((label, "REFUSED", reason))
            return False
        try:
            do()
        except OSError as e:
            actions.append((label, "ERROR", str(e)))
            return False
        actions.append((label, "DONE", reason))
        return True

    artifact = resolve(root, ctx.fields.get("Artifact", ""))
    if artifact is None:
        actions.append(("resolve artifact", "REFUSED",
                        "Artifact does not resolve to a file"))
    else:
        art_ok = in_fence(artifact, ctx.roots)
        via = os.path.basename(ctx.order_path)
        frm = ctx.fields.get("Outbox", "?")
        to = ctx.fields.get("Inbox", "?")

        if all_ok:
            dest = os.path.join(root, ctx.fields["Inbox"],
                                os.path.basename(artifact))
            copied = act("copy artifact to inbox",
                         not os.path.exists(dest),
                         rel(root, dest) if not os.path.exists(dest)
                         else "destination exists, refusing to overwrite",
                         lambda: shutil.copy2(artifact, dest))
            if copied:
                # The copy is what travels on, so the hop is recorded on it.
                act("route the copy", True, "{} > {}".format(frm, to),
                    lambda: append_route(dest, frm, to, via, True))
        elif art_ok:
            # Nothing travelled. The failed attempt is testified on the
            # original, which carries it into CONSUMED as the receipt.
            act("route the failed attempt", True, "logged as Failed",
                lambda: append_route(artifact, frm, to, via, False))

        # The stamp is a write to the artifact, so the fence governs it too.
        act("stamp artifact", art_ok,
            "Successful: {}".format("Yes" if all_ok else "No") if art_ok
            else "artifact is outside the fence",
            lambda: stamp(artifact, "Yes" if all_ok else "No"))

        if art_ok:
            moved, output, dest = git_move(root, artifact, ctx.meta["Consumed"])
            actions.append(("consume artifact",
                            "DONE" if moved else "ERROR",
                            dest if moved else output.replace("\n", " | ")))
        else:
            actions.append(("consume artifact", "REFUSED",
                            "artifact is outside the fence"))

    for label, state, detail in actions:
        print("  [{}] {}  ({})".format(state, label, detail))

    outcome = "SUCCESS" if all_ok else "REFUSED"
    if any(s == "ERROR" for _, s, _ in actions):
        outcome = "INCOMPLETE"
    print()
    print("OUTCOME: {}".format(outcome))
    write_log(ctx, results, actions, outcome)
    print("Logged   -> {}".format(ctx.meta["Run log"]))
    if outcome == "INCOMPLETE":
        sys.exit(3)


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("inspect", "execute"):
        print(__doc__)
        sys.exit(64)
    root = repo_root()
    (cmd_inspect if sys.argv[1] == "inspect" else cmd_execute)(root, sys.argv[2])


if __name__ == "__main__":
    main()
