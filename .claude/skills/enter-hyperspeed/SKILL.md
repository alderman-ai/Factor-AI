---
name: enter-hyperspeed
description: Validate the filled New World Coordinates form on the Instrument Panel and emit the engine JSON into _THE VAST UNKNOWN/Crash Sites/. Terminal stage 03 (Process) of the loop. Triggers on /enter-hyperspeed, "enter hyperspeed", "launch the world", "process the coordinates".
---

# enter-hyperspeed

Run exactly this, from the repository root:

    python "_THE SHIP/Instrument Panel/Ignition Codes/enter_hyperspeed.py"

Rules:

- Show the script's output verbatim.
- If it prints REFUSED: stop. Show the refusal exactly as printed. Do not
  edit the form, the schema, or the script to make it pass, and do not
  fill empty fields yourself. The operator fixes their form in Obsidian;
  the fence stays where it is. Friction is the product.
- On success, report the crash-site path and the emitted JSON.
