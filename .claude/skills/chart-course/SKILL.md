---
name: chart-course
description: Drive the transition between runs. Verify the dead run was closed out, run the File Move Ritual, and stamp a blank New World Coordinates form onto the Instrument Panel from the master template. Terminal stage 01 (Generate) of the loop. Triggers on /chart-course, "chart a course", "spawn a new world form", "start the next run", "transition to the next run".
---

# chart-course

The between-runs driver. One world has died and the next has not been charted.
This skill walks that gap and refuses to cross it early.

**This skill gates. It does not automate.** Every git operation below belongs to
the operator and to `Commit Ritual.md`. Never run a commit, a tag, or a push from
here. Verify, report, stop.

## The sequence

| # | Step | Defined in | Performed by |
|---|---|---|---|
| 1 | Pay the toll — `RUN-NNN-Assistant-Report.md` | `Commit Ritual.md` | assistant |
| 2 | Scuttle the world, tag `RUN_00N/BITER_ATTACK!!` | `Commit Ritual.md` | operator |
| 3 | **Repair** — diagnose, fix, complete the rituals | *(not yet defined)* | both |
| 4 | **Move the files** | `File Move Ritual.md` | script, below |
| 5 | **Chart the course** — stamp the blank form | this skill | script, below |
| 6 | Fill the form | Obsidian | operator, alone |
| 7 | Land it — commit, tag `RUN_00M/SAME_SHIP_DIFFERENT_DAY` | `Commit Ritual.md` | operator |
| 8 | Launch | `/enter-hyperspeed` | assistant |

Both ritual documents live in `_THE SHIP/_EJECT BUTTON/Biter Attack Ritual/`.

Steps 4 and 5 are a single script run. Everything else this skill checks and
reports; it performs none of it.

## Before running anything

**Read `_THE SHIP/_EJECT BUTTON/Biter Attack Ritual/File Move Ritual.md` first.**
It governs every file this skill relocates, and its *Undecided* table names
artifacts that have no rule yet. If this transition touches one of those, stop
and say which one. Do not move it and do not decide for the operator.

Then verify steps 1 and 2 actually happened. Report each as a plain yes/no with
the evidence, and show the commands' output:

    git tag -l 'RUN_*/BITER_ATTACK!!'       # the dead run has a headstone
    ls "_THE SHIP/_EJECT BUTTON/"           # the toll was paid
    git status --porcelain                  # nothing half-staged or mid-surgery

**If the most recent run has no `BITER_ATTACK!!` tag, or no assistant report,
stop.** Charting a course out of a run that was never closed is exactly how run
002 launched — no gap, no diagnosis, no repair — and it died of the faults that
phase exists to catch.

Step 3 has no definition yet. Do not invent one. If repair work is still open,
say so and let the operator decide whether the transition proceeds.

## Then run exactly this, from the repository root

    python "_THE SHIP/Instrument Panel/Ignition Codes/chart_course.py"

Rules:

- Show the script's output verbatim.
- If it prints REFUSED: stop. Show the refusal exactly as printed. Do not
  create folders, rename files, or edit anything to make it pass. Friction
  is the product.
- Do not fill any of the spawned form's fields. Filling happens in
  Obsidian, by the operator, and nowhere else.
- Do not commit and do not tag. Report what moved and what was stamped, then
  hand back to the operator for step 6.
