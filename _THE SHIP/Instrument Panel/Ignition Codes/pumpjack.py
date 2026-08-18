#!/usr/bin/env python3
"""
Pumpjack -- extracts session transcripts from Claude Code storage into
_THE SHIP/SatNav/Incoming Transmissions/.

Claude Code writes sessions as JSONL into its own storage, outside this
repo, where they are subject to cleanup and invisible to git. This pulls
them in as readable markdown with a declared frontmatter header.

ONE artifact per session, by design change: the render only. The earlier
version also kept a byte-for-byte crude/ copy so a bad render was never a
data loss. That is gone, which has a consequence:

  Large tool results do NOT live in the JSONL. Claude Code spills them to
  <session-id>/tool-results/*.txt and the JSONL never references the path.
  With no crude, truncating them in the render destroys them. So this
  renderer does not truncate, and appends every sidecar file verbatim.

Reasoning is still unrecoverable. Claude Code stores thinking blocks with
their signature but strips the text. The header counts them; nothing can
bring them back. That absence is why /science exists.

Usage:
    python pumpjack.py                      # today, this repo
    python pumpjack.py --date 2026-08-17
    python pumpjack.py --session 09f8d4b0-5de6-41ad-b2f5-a3583d054bf9
    python pumpjack.py --all
"""

import argparse
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent

# _THE SHIP/Ignition Codes/ -> repo root. Asked of git rather than assumed,
# so moving this file one level does not silently write to the wrong tree.
REPO_ROOT = Path(
    subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=HERE, capture_output=True, text=True, check=True,
    ).stdout.strip()
)

OUT_DIR = REPO_ROOT / "_THE SHIP" / "SatNav" / "Incoming Transmissions"

SEP_FIELD = "\x1f"
SEP_REC = "\x1e"


def git(*args):
    r = subprocess.run(
        ["git", *args], cwd=REPO_ROOT, capture_output=True, text=True,
    )
    return r.stdout.strip() if r.returncode == 0 else ""


def encode_project(path):
    """Absolute path -> Claude Code's encoded project-storage directory name."""
    return re.sub(r"[:\\/.]", "-", str(path))


def local(iso_ts):
    """ISO-8601 (UTC or offset) -> local-time datetime."""
    return datetime.fromisoformat(iso_ts.replace("Z", "+00:00")).astimezone()


def run_boundaries():
    """
    [(run_number, opened_at)] for every run, oldest first.

    A run opens at its PROJECT_START (run 001) or SAME_SHIP_DIFFERENT_DAY
    (every run after). Dated by the *commit* the tag points at, not by when
    the tag was planted -- those differ whenever a boundary is tagged late,
    and the commit is the one that tells the truth about when the run began.
    """
    raw = git(
        "for-each-ref",
        "--format=%(refname:short)\t%(*committerdate:iso-strict)",
        "refs/tags",
    )
    out = []
    for line in raw.splitlines():
        if "\t" not in line:
            continue
        name, when = line.split("\t", 1)
        if "/" not in name or not name.startswith("RUN_"):
            continue
        head, leaf = name.split("/", 1)
        if not (leaf.startswith("PROJECT_START") or leaf.startswith("SAME_SHIP")):
            continue
        try:
            out.append((int(head.split("_")[1]), datetime.fromisoformat(when).astimezone()))
        except (IndexError, ValueError):
            continue
    return sorted(out, key=lambda x: x[1])


def run_for(started):
    """
    Which run was open when this session ran.

    Derived from the session's own start time rather than from the current
    tag state -- otherwise re-extracting an old session after a scuttle
    stamps it with today's run, which is how a ledger starts lying.
    """
    bounds = run_boundaries()
    if not bounds:
        return "001"
    current = bounds[0][0]
    for n, opened in bounds:
        if opened <= started:
            current = n
        else:
            break
    return "{:03d}".format(current)


def commits_in_window(start, end):
    """
    Commits authored inside the session window.

    Sessions cannot be joined to commits directly: the JSONL knows only the
    UUID, while the commit trailer carries the harness id (session_01...).
    Nothing records both, so the window is the only available join and it is
    ambiguous whenever two sessions overlap. That ambiguity is reported
    rather than hidden -- see build_frontmatter.
    """
    fmt = "--format=%h" + SEP_FIELD + "%s" + SEP_FIELD + "%b" + SEP_REC
    raw = git(
        "log", "--all",
        "--since=" + start.isoformat(),
        "--until=" + end.isoformat(),
        fmt,
    )
    out = []
    for rec in raw.split(SEP_REC):
        rec = rec.strip("\n")
        if not rec:
            continue
        parts = rec.split(SEP_FIELD)
        if len(parts) < 3:
            continue
        sha, subject, body = parts[0], parts[1], parts[2]
        m = re.search(r"^Claude-Session:\s*\S*?(session_\w+)\s*$", body, re.M)
        out.append({
            "sha": sha,
            "subject": subject,
            "trailer": m.group(1) if m else None,
        })
    return out


def tags_in_window(start, end):
    raw = git(
        "for-each-ref",
        "--format=%(refname:short)\t%(creatordate:iso-strict)",
        "refs/tags",
    )
    found = []
    for line in raw.splitlines():
        if "\t" not in line:
            continue
        name, when = line.split("\t", 1)
        try:
            ts = datetime.fromisoformat(when).astimezone()
        except ValueError:
            continue
        if start <= ts <= end:
            found.append(name)
    return sorted(found)


def science_in_window(session_uuid):
    """Science entries filed by this session, matched on the id they record."""
    if not OUT_DIR.is_dir():
        return []
    hits = []
    for f in sorted(OUT_DIR.glob("*.md")):
        head = f.read_text(encoding="utf-8", errors="replace")[:600]
        if session_uuid in head and "session_id" in head:
            hits.append(f.name)
    return hits


def yq(s):
    """Quote a scalar so YAML keeps it a string (001 must not become 1)."""
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def build_frontmatter(session_uuid, meta, start, end):
    cwd = Path(meta.get("cwd", str(REPO_ROOT)))
    try:
        rel = cwd.resolve().relative_to(REPO_ROOT).as_posix() or "."
    except ValueError:
        rel = cwd.as_posix()

    commits = commits_in_window(start, end)
    trailers = sorted({c["trailer"] for c in commits if c["trailer"]})

    fm = ["---"]
    fm.append("Run: " + yq(run_for(start)))
    fm.append("Working Directory: " + yq(rel))
    fm.append("Session UUID: " + yq(session_uuid))

    if len(trailers) == 1:
        fm.append("Claude Session: " + yq(trailers[0]))
    else:
        fm.append("Claude Session: null")
        if len(trailers) > 1:
            # Loud, not silent: overlapping sessions make the window join
            # unreliable, and the reader needs to know the commit list is a
            # superset rather than this session's own work.
            warning = "{} distinct sessions committed in this window".format(len(trailers))
            fm.append("Concurrency Warning: " + yq(warning))
            fm.append("Claude Sessions Seen:")
            for t in trailers:
                fm.append("  - " + yq(t))

    fm.append("Started: " + yq(start.isoformat()))
    fm.append("Ended: " + yq(end.isoformat()))
    fm.append("Git Branch: " + yq(meta.get("gitBranch", "?")))
    fm.append("Claude Code Version: " + yq(meta.get("version", "?")))

    if commits:
        fm.append("Commits:")
        for c in commits:
            fm.append("  - SHA: " + yq(c["sha"]))
            fm.append("    Subject: " + yq(c["subject"]))
    else:
        fm.append("Commits: []")

    planted = tags_in_window(start, end)
    if planted:
        fm.append("Tags Planted:")
        for t in planted:
            fm.append("  - " + yq(t))

    filed = science_in_window(session_uuid)
    if filed:
        fm.append("Science Filed:")
        for s in filed:
            fm.append("  - " + yq(s))

    fm.append("---")
    return "\n".join(fm)


def render_blocks(blocks, out):
    for b in blocks:
        btype = b.get("type")

        if btype == "text":
            out.append(b.get("text", "").rstrip())
            out.append("")

        elif btype == "thinking":
            text = b.get("thinking", "").strip()
            if not text:
                continue
            out.append("> [!note]- Thinking")
            for line in text.split("\n"):
                out.append("> " + line)
            out.append("")

        elif btype == "tool_use":
            body = json.dumps(b.get("input", {}), indent=2, ensure_ascii=False)
            out.append("**→ tool call: `" + str(b.get("name", "?")) + "`**")
            out.append("")
            out.append("```json")
            out.append(body)
            out.append("```")
            out.append("")

        elif btype == "tool_result":
            content = b.get("content", "")
            if isinstance(content, list):
                content = "\n".join(
                    c.get("text", "") if isinstance(c, dict) else str(c) for c in content
                )
            flag = " (error)" if b.get("is_error") else ""
            out.append("**← tool result" + flag + "**")
            out.append("")
            out.append("```")
            out.append(str(content).rstrip())
            out.append("```")
            out.append("")

        elif btype == "image":
            out.append("*[image omitted from render -- binary, not recoverable here]*")
            out.append("")


def count_thinking(turns, kept_only=False):
    total = 0
    for r in turns:
        content = r.get("message", {}).get("content")
        if not isinstance(content, list):
            continue
        for b in content:
            if not isinstance(b, dict) or b.get("type") != "thinking":
                continue
            if kept_only and not b.get("thinking", "").strip():
                continue
            total += 1
    return total


def render_session(records, session_uuid, source_path, sidecar_dir):
    turns = [r for r in records if r.get("type") in ("user", "assistant")]
    if not turns:
        return None, None

    stamped = [r for r in records if r.get("timestamp")]
    if not stamped:
        return None, None
    start = local(stamped[0]["timestamp"])
    end = local(stamped[-1]["timestamp"])

    meta = next((r for r in turns if r.get("cwd")), {})
    models = sorted({
        r["message"].get("model")
        for r in turns
        if r.get("type") == "assistant" and r.get("message", {}).get("model")
    })

    thinking_total = count_thinking(turns)
    thinking_kept = count_thinking(turns, kept_only=True)

    out = [build_frontmatter(session_uuid, meta, start, end), ""]
    out.append("# Session " + session_uuid[:8] + " — " + start.strftime("%Y-%m-%d"))
    out.append("")
    out.append("Attributed rendering of Claude Code session storage. Not edited for content.")
    out.append("")
    out.append("| | |")
    out.append("|---|---|")
    out.append("| Model(s) | " + (", ".join(models) if models else "?") + " |")
    out.append("| Turns | " + str(len(turns)) + " |")
    if thinking_total:
        out.append(
            "| Thinking blocks | {} ({} with retained text — Claude Code strips the rest) |".format(
                thinking_total, thinking_kept
            )
        )
    out.append("| Source | `" + str(source_path) + "` |")
    out.append("")
    out.append("---")
    out.append("")

    for r in turns:
        msg = r.get("message", {})
        if r.get("timestamp"):
            pretty = local(r["timestamp"]).strftime("%Y-%m-%d %H:%M:%S %z")
        else:
            pretty = "?"

        if r.get("type") == "user":
            label = "OPERATOR (meta)" if r.get("isMeta") else "OPERATOR"
        else:
            label = "CLAUDE (" + str(msg.get("model", "?")) + ")"

        out.append("### " + label + " · " + pretty)
        out.append("")
        content = msg.get("content")
        if isinstance(content, str):
            out.append(content.rstrip())
            out.append("")
        elif isinstance(content, list):
            render_blocks(content, out)
        out.append("---")
        out.append("")

    # Spilled tool results, verbatim. Without crude/ this appendix is the only
    # copy that ever enters the repo.
    if sidecar_dir and sidecar_dir.is_dir():
        files = sorted(p for p in sidecar_dir.iterdir() if p.is_file())
        if files:
            out.append("## Appendix — spilled tool results")
            out.append("")
            out.append(
                "{} result(s) too large for the JSONL. Claude Code wrote them to "
                "`{}` and never referenced the path. Reproduced verbatim.".format(
                    len(files), sidecar_dir
                )
            )
            out.append("")
            for p in files:
                out.append("### `" + p.name + "`")
                out.append("")
                out.append("```")
                out.append(p.read_text(encoding="utf-8", errors="replace").rstrip())
                out.append("```")
                out.append("")

    name = start.strftime("%Y-%m-%d_%H%M") + "_" + session_uuid[:8]
    return name, "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", help="Encoded dir under ~/.claude/projects/ (default: this repo)")
    ap.add_argument("--date", help="Local date to extract, YYYY-MM-DD (default: today)")
    ap.add_argument("--session", help="Extract one session UUID")
    ap.add_argument("--all", action="store_true", help="Extract every session in storage")
    args = ap.parse_args()

    project = args.project or encode_project(REPO_ROOT)
    src_dir = Path.home() / ".claude" / "projects" / project
    if not src_dir.is_dir():
        raise SystemExit("No such project storage: " + str(src_dir))

    want_date = None
    if not args.all and not args.session:
        want_date = args.date or datetime.now().strftime("%Y-%m-%d")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    extracted = []
    for jsonl in sorted(src_dir.glob("*.jsonl")):
        session_uuid = jsonl.stem
        if args.session and session_uuid != args.session:
            continue

        records = []
        for line in jsonl.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue

        stamped = [r for r in records if r.get("timestamp")]
        if not stamped:
            continue
        if want_date and local(stamped[0]["timestamp"]).strftime("%Y-%m-%d") != want_date:
            continue

        sidecar = src_dir / session_uuid / "tool-results"
        name, md = render_session(records, session_uuid, str(jsonl), sidecar)
        if md is None:
            continue

        dest = OUT_DIR / (name + ".md")
        dest.write_text(md, encoding="utf-8")
        extracted.append((dest.name, len(md)))

    if not extracted:
        target = args.session or want_date or "all sessions"
        print("Nothing extracted for " + str(target) + " in " + project)
        return

    print("Extracted {} session(s) to {}:\n".format(len(extracted), OUT_DIR))
    for name, size in extracted:
        print("  {}  -  {:,} bytes".format(name, size))


if __name__ == "__main__":
    main()
