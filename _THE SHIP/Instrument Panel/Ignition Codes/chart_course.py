"""chart-course — stamp a blank New World Coordinates form onto the Instrument Panel.

Terminal stage 01 of the loop (Generate). Copies the master template verbatim,
stamps the next run number, and archives the previous world's form into the
Atlas of Worlds first. Filling happens in Obsidian, never here.
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[3]
NW = re.compile(r"^New World (\d{3})\.md$")


def refuse(precondition: str, observed: str) -> None:
    print(
        f"REFUSED\n  precondition: {precondition}\n  observed: {observed}",
        file=sys.stderr,
    )
    sys.exit(1)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    root = ap.parse_args().root.resolve()

    master = root / "_THE SHIP" / "Hitchhiker's Guide" / "Template Schema" / "New World Coordinates.md"
    panel = root / "_THE SHIP" / "Instrument Panel"
    atlas = panel / "Atlas of Worlds"

    if not master.is_file():
        refuse("master template exists", f"no file at {master}")
    if not panel.is_dir():
        refuse("Instrument Panel exists", f"no directory at {panel}")
    if not atlas.is_dir():
        refuse("Atlas of Worlds exists", f"no directory at {atlas}")

    live = sorted(p for p in panel.iterdir() if p.is_file() and NW.match(p.name))
    known = [
        int(NW.match(p.name).group(1))
        for p in [*atlas.iterdir(), *live]
        if p.is_file() and NW.match(p.name)
    ]
    next_run = max(known, default=0) + 1

    text = master.read_text(encoding="utf-8")
    if not re.search(r"^Run:\s*$", text, flags=re.M):
        refuse(
            "master template has an empty 'Run:' slot to stamp",
            "no line matching '^Run:' with an empty value in the master",
        )
    stamped = re.sub(r"^Run:\s*$", f"Run: {next_run}", text, count=1, flags=re.M)

    for p in live:
        dest = atlas / p.name
        if dest.exists():
            refuse(
                "Atlas of Worlds has no file with the archived name",
                f"{dest} already exists",
            )
        shutil.move(str(p), str(dest))
        print(f"archived: {p.name} -> Atlas of Worlds/")

    out = panel / f"New World {next_run:03d}.md"
    out.write_text(stamped, encoding="utf-8")
    print(f"charted: {out.relative_to(root)}  (Run {next_run})")


if __name__ == "__main__":
    main()
