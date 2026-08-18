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

import yaml

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


def frontmatter(text: str, name: str) -> dict:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        refuse(f"{name} opens with a '---' frontmatter fence", "first line is not '---'")
    try:
        end = next(i for i, ln in enumerate(lines[1:], start=1) if ln.strip() == "---")
    except StopIteration:
        refuse(f"{name} frontmatter is closed by a second '---'", "no closing fence found")
    try:
        fm = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as e:
        refuse(f"{name} frontmatter parses as YAML", str(e))
    if not isinstance(fm, dict):
        refuse(f"{name} frontmatter is a key/value mapping", f"parsed as {type(fm).__name__}")
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
