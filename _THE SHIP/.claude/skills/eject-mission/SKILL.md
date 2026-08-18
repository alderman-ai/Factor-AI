---
name: eject-mission
description: End the current RUN and open the gap before the next one. Files the assistant report, deregisters the engine, makes the Ship's one and only commit, runs the File Move Ritual, and stamps a blank New World Coordinates form. Never tags and never pushes. Triggers on /eject-mission, "end the run", "close out the run", "scuttle the run", "biter attack", "eject".
---

# eject-mission

One world has died. This walks the boundary out of it and stops before the next
one begins.

**It runs from either working directory — repo root or `_THE SHIP/` — and the
two copies of this file are byte-identical.** Every path below is resolved from
the repo root at runtime, so nothing here depends on where you started:

    R="$(git rev-parse --show-toplevel)"

That resolves identically from anywhere inside the repo. Use it. Do not write a
cwd-relative path into any step.

## What this skill is allowed to do

It absorbed `chart-course`, which no longer exists. That merge is the point:
**the commit and the file move can never be separated**, because nothing can
invoke one without the other. A report describing a state that no commit holds
is the exact flaw this ordering exists to prevent.

| It does | It never does |
|---|---|
| Files the assistant report | Plants a tag |
| Deregisters the engine | Pushes |
| **One** minimal commit | A second commit |
| Runs the File Move Ritual | Deletes `/The Guy/` or the crate |
| Stamps the blank form | Fills any field of that form |

**This is the only commit the Ship ever makes.** Not "the Ship avoids git" —
exactly one commit, from exactly one skill, never a tag and never a push. That
is a rule a hook can check; the softer version was not.

---

## Step 0 — the gate

Run these and report each as a plain yes/no with the evidence. Show the output.

    R="$(git rev-parse --show-toplevel)"
    ls "$R/_THE SHIP/Instrument Panel/"        # is there a live world form?
    ls "$R/_THE SHIP/_EJECT BUTTON/"           # was the toll already paid?
    git status --porcelain                     # anything half-staged?
    git tag -l                                 # where are we in the ledger?

**REFUSE and stop if any of these hold:**

| Condition | Why it refuses |
|---|---|
| No `New World NNN.md` on the Instrument Panel | There is no live run to end. The Panel holds exactly one live form; none means the last run already ended. |
| A report already exists for this run | This run was already ended. Doing it twice files a second toll and archives an already-archived form. |
| A merge, rebase, or cherry-pick is in progress | The Ship's one commit must be a clean, readable snapshot. |

Show the refusal and stop. **Do not create the form, rename anything, or edit a
document to make the gate pass.** Friction is the product.

### The run number comes from the form

`New World NNN.md` on the Panel is the authority. Run numbering is derived from
the forms — which is why the Atlas keeps every one of them forever. Do not read
a run number out of a `CLAUDE.md` frontmatter and trust it.

### What actually went wrong in run 002, corrected

An earlier version of this gate claimed run 002 launched out of a run that was
never closed. **That is false, and the autopsy disproved it** — run 001 *was*
closed, and `7fb5681`'s parent is exactly `RUN_001/BITER_ATTACK!!`.

What was missing was **the toll**. `_EJECT BUTTON/` did not exist until
`9864b76`, partway into run 002, so no report was ever filed for the run that
ended before it. The gate is right. Its reason is that the toll goes missing,
not the headstone. See `_EJECT BUTTON/RUN-002-Autopsy.md`.

---

## Step 1 — pay the toll

Write `$R/_THE SHIP/_EJECT BUTTON/RUN-NNN-Assistant-Report.md`.

**A reset is legal only once this file exists.** Pay the toll, then burn it —
the reset produces the resource rather than spending it.

Follow the shape of `RUN-002-Assistant-Report.md`, in the same folder. At
minimum it carries:

- **What the world failed at** — one sentence, at the top.
- **The failure**, with evidence. Commands and their real output.
- **What was discovered this run.**
- **Assistant errors this run.** Not optional. Failure-solution pairs are the
  point of the whole project, and an error the operator caught that the
  assistant did not is the most valuable kind there is.
- **Fence report** — what was and was not read, stated plainly.
- **Engine work items** — what needs a root session to fix.
- **Open decisions** — what nobody has ruled on yet.

Write it without hindsight. This is the dying run's own account, filed from
inside it. A later session may write `RUN-NNN-Autopsy.md` beside it with
hindsight this document cannot have. **Do not merge the two** — merging them
rewrites history.

## Step 2 — deregister the engine

Empty the `mcpServers` object in every `.mcp.json` that registers one:

    "$R/.mcp.json"                 # root
    "$R/_THE SHIP/.mcp.json"       # the Ship, if it exists

An engine is registered in both, because the Ship calls its **tools** while root
edits its **files**. Ending the run closes both doors.

Then confirm the tool no longer answers, and say so. Absence is a state, not a
fault — report it, do not go hunting for the server.

If a `.mcp.json` is already `{"mcpServers": {}}`, say so and move on. That is
not an error.

## Step 3 — the Ship's one commit

    git add -A
    git commit -m "<terse>"

**Minimal message on purpose.** This commit's only job is to freeze the state
the report describes, before the File Move Ritual destroys it. The narrative
commit comes later, in `Commit Ritual.md`, written by the operator at root.

**No tag. No push.** Both belong to the operator.

## Step 4 — move the files and stamp the next form

**Read `$R/_THE SHIP/_EJECT BUTTON/Biter Attack Ritual/File Move Ritual.md`
first.** Its *Undecided* table names artifacts that still have no rule. If this
transition touches one, stop and say which. Do not move it, and do not decide
for the operator.

Then run exactly this, once:

    python "$R/_THE SHIP/Instrument Panel/Ignition Codes/chart_course.py"

It archives every live form into `Atlas of Worlds/` and stamps the next blank
from the master template. Both halves, one run.

- Show the output verbatim.
- **If it prints REFUSED: stop.** Show the refusal exactly as printed. Do not
  create the folder, rename the file, or edit the template to make it pass. A
  name collision in the Atlas means a run number is being reused — a ledger
  fault, fixed in the ledger, never by renaming the file that tripped it.
- **Do not fill any field of the stamped form.** Filling happens in Obsidian,
  by the operator, and nowhere else.

## Step 5 — stop, and report what is left standing

Do not continue past this point. Report:

1. What the report said, in two lines.
2. What moved, and what was stamped.
3. **What still needs deleting, and by whom.** `/The Guy/` and the crate die
   with the run, but nothing has been specified to delete them — that row is
   still open in `File Move Ritual.md`. Name them. Do not remove them.
4. That the next move is the operator's: fill the form in Obsidian, then the
   repair period, then `Commit Ritual.md` at root for the scuttle commit, the
   `BITER_ATTACK!!` tag, the new-day commit, and `SAME_SHIP_DIFFERENT_DAY`.

---

## Running this from `_THE SHIP/`

Two things differ, and neither is a reason to work around anything:

- **`$R/.mcp.json` is outside the Ship's workspace.** Reaching it may prompt.
  If it is refused, report the refusal and stop — do not look for another way in.
- **The Ship's fence hook is live.** It blocks `_THE VAST UNKNOWN/` and
  `_THE SHIP/.claude/`. Nothing in this skill needs either. If the fence fires
  during an eject, the step is wrong, not the fence.

## Why this file exists twice

Cloud and mobile sessions are repo-root only, and changing directory on a phone
is painful. A run-boundary skill you cannot reach from where you actually work
is a skill that does not exist.

So it lives at both `.claude/skills/eject-mission/` and
`_THE SHIP/.claude/skills/eject-mission/`, **byte-identical**. Edit one, edit
the other in the same commit. `Instrument Panel/Ship Capabilities.md` records
the pair and the one-line command that checks they still match.
