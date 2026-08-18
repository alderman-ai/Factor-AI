---
name: chart-course
description: Stamp a blank New World Coordinates form onto the Instrument Panel from the master template, archiving the previous world's form into the Atlas of Worlds. Terminal stage 01 (Generate) of the loop. Triggers on /chart-course, "chart a course", "spawn a new world form".
---

# chart-course

Run exactly this, from the repository root:

    "_THE VAST UNKNOWN/.venv/Scripts/python.exe" "_THE SHIP/Instrument Panel/Ignition Codes/chart_course.py"

Rules:

- Show the script's output verbatim.
- If it prints REFUSED: stop. Show the refusal exactly as printed. Do not
  create folders, rename files, or edit anything to make it pass. Friction
  is the product.
- Do not fill any of the spawned form's fields. Filling happens in
  Obsidian, by the operator, and nowhere else.
