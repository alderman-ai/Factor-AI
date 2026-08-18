"""enter-hyperspeed — punch the filled coordinates into the engine.

Terminal stage 03 of the loop (Process). Finds the one live New World form on
the Instrument Panel, validates its frontmatter against the coordinates schema,
and emits the JSON the engine consumes into _THE VAST UNKNOWN/Crash Sites/.
Refuses loudly, naming every violation. Never repairs input.
"""

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[3]
NW = re.compile(r"^New World (\d{3})\.md$")
DIFFICULTY = {"Easy", "Normal", "Hard"}
LENGTH = {"Quick", "Short", "Normal", "Long", "Epic"}
KNOWN_KEYS = {
    "Run",
    "Difficulty",
    "Length",
    "World Objective",
    "Learning Objective",
    "Version",
    "Version Date",
}


def refuse(precondition: str, observed: str) -> None:
    print(
        f"REFUSED\n  precondition: {precondition}\n  observed: {observed}",
        file=sys.stderr,
    )
    sys.exit(1)


INT = re.compile(r"^[+-]?\d+$")


def scalar(raw: str):
    """One frontmatter value, typed the way this form's schema expects.

    Deliberately narrow. A world form's frontmatter is flat `Key: value` and
    nothing else, so this handles exactly that and refuses the rest rather
    than guessing. Empty -> None, digits -> int, everything else -> str.
    """
    v = raw.strip()
    if v in ("", "null", "~"):
        return None
    if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
        return v[1:-1]
    if INT.match(v):
        return int(v)
    return v


def frontmatter(text: str, name: str) -> dict:
    """Parse the leading `---` block.

    Hand-rolled on purpose. This script is durable Ship tooling, and the only
    declaration of its former yaml dependency lived in the engine's
    pyproject.toml -- inside the disposable world. Durable tooling that needs
    the planet installed is the same fault as durable tooling that runs the
    planet's interpreter, only quieter. It now depends on nothing.

    The trade that buys: this is stricter than a YAML parser. Anything a world
    form has no business containing -- nesting, lists, anchors, multi-line
    values -- is REFUSED by line number instead of being silently accepted and
    reinterpreted. For a script whose entire job is refusing malformed forms,
    strict is the correct direction.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        refuse(f"{name} opens with a '---' frontmatter fence", "first line is not '---'")
    try:
        end = next(i for i, ln in enumerate(lines[1:], start=1) if ln.strip() == "---")
    except StopIteration:
        refuse(f"{name} frontmatter is closed by a second '---'", "no closing fence found")

    fm: dict = {}
    for n, ln in enumerate(lines[1:end], start=2):
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        if ln[:1] in (" ", "\t"):
            refuse(
                f"{name} frontmatter is flat `Key: value` lines",
                f"line {n} is indented -- nested values are not part of this schema: {ln!r}",
            )
        if ln.lstrip().startswith("- "):
            refuse(
                f"{name} frontmatter is flat `Key: value` lines",
                f"line {n} is a list item -- no field in this schema takes a list: {ln!r}",
            )
        if ":" not in ln:
            refuse(
                f"{name} frontmatter is flat `Key: value` lines",
                f"line {n} has no ':' separator: {ln!r}",
            )
        key, _, raw = ln.partition(":")
        key = key.strip()
        if not key:
            refuse(f"{name} frontmatter keys are non-empty", f"line {n}: {ln!r}")
        if key in fm:
            refuse(f"{name} declares each key once", f"line {n} repeats {key!r}")
        fm[key] = scalar(raw)
    return fm


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    root = ap.parse_args().root.resolve()

    panel = root / "_THE SHIP" / "Instrument Panel"
    crash = root / "_THE VAST UNKNOWN" / "Crash Sites"

    if not panel.is_dir():
        refuse("Instrument Panel exists", f"no directory at {panel}")

    live = sorted(p for p in panel.iterdir() if p.is_file() and NW.match(p.name))
    if len(live) != 1:
        refuse(
            "exactly one live New World form on the Instrument Panel",
            f"found {len(live)}: {[p.name for p in live]}",
        )
    src = live[0]
    file_run = int(NW.match(src.name).group(1))

    fm = frontmatter(src.read_text(encoding="utf-8"), src.name)

    problems = []
    unknown = set(fm) - KNOWN_KEYS
    if unknown:
        problems.append(f"unknown keys not in the schema: {sorted(unknown)}")

    run = fm.get("Run")
    if not isinstance(run, int) or isinstance(run, bool) or run < 1:
        problems.append(f"Run must be an integer >= 1, got {run!r}")
    elif run != file_run:
        problems.append(f"Run {run} does not match filename number {file_run:03d}")

    difficulty = fm.get("Difficulty")
    if difficulty not in DIFFICULTY:
        problems.append(f"Difficulty must be one of {sorted(DIFFICULTY)}, got {difficulty!r}")

    length = fm.get("Length")
    if length not in LENGTH:
        problems.append(f"Length must be one of {sorted(LENGTH)}, got {length!r}")

    world_obj = fm.get("World Objective")
    if not isinstance(world_obj, str) or not world_obj.strip():
        problems.append(f"World Objective must be a non-empty string, got {world_obj!r}")

    learn_obj = fm.get("Learning Objective")
    if learn_obj is not None and not isinstance(learn_obj, str):
        problems.append(f"Learning Objective must be a string or empty, got {learn_obj!r}")

    if problems:
        refuse("coordinates conform to the New World schema", "; ".join(problems))

    version = fm.get("Version")
    vdate = fm.get("Version Date")
    if isinstance(vdate, (datetime.date, datetime.datetime)):
        vdate = vdate.isoformat()

    out = crash / f"New World {run:03d}.json"
    if out.exists():
        refuse("no crash site already recorded for this run", f"{out} already exists")
    crash.mkdir(parents=True, exist_ok=True)

    payload = {
        "run": run,
        "difficulty": difficulty,
        "length": length,
        "world_objective": world_obj.strip(),
        "learning_objective": (learn_obj.strip() or None) if isinstance(learn_obj, str) else None,
        "template_version": version,
        "template_version_date": vdate,
        "source": src.relative_to(root).as_posix(),
        "extracted_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"hyperspeed: {out.relative_to(root)}")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
