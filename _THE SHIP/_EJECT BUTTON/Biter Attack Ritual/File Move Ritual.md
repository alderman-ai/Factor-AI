# File Move Ritual

The file half of a run transition. Read alongside `Commit Ritual.md`.

**`Commit Ritual.md` governs what git does. This governs what moves on disk.**
Nothing here creates a commit, and nothing there moves a file. Where a step does
both, it is split across the two documents and each names the other.

Called by the `eject-mission` skill, which will not stamp a new world until this
document has been read and every artifact it touches has a rule.

`eject-mission` absorbed `chart-course`, which no longer exists. The merge
matters here: the Ship's one commit now happens **before** these moves, in the
same skill run. A report describing a state that no commit holds was the flaw
that ordering exists to prevent.

---

## What this solves

A run's death and a run's birth both move files, and the moves are not
symmetrical. Some artifacts are archived and kept forever, some die with the
world, some are written fresh.

Unwritten, the moves get made by hand and differently each time. That already
happened: `New World 002.md` was archived into `Atlas of Worlds/` by hand, while
`chart_course.py` — the thing whose job that is — had never been run. The result
looked identical and was not the same operation.

---

## The one established move

**`New World NNN.md`: `Instrument Panel/` → `Instrument Panel/Atlas of Worlds/`**

The Instrument Panel holds **exactly one live form** — the world currently being
charted or flown. The Atlas of Worlds holds **every form that has been retired**,
permanently. A world's coordinates are never deleted. They are the only surviving
record of what each run was asked to be, and the run numbering is derived from
them.

Executed by `_THE SHIP/Instrument Panel/Ignition Codes/chart_course.py`, which
archives every live form it finds before stamping the next one. **It is not a
hand move.** Doing it by hand produces the same directory listing and skips every
refusal below.

### Why move, not copy

The Panel must hold exactly one live form. A copy leaves the retired world on the
Panel beside the new one, and the next chart archives both.

### Refusals

The script stops rather than resolving any of these. Show the refusal exactly as
printed and stop. Do not create the folder, rename the file, or edit the template
to make it pass.

| Precondition | Refused when |
|---|---|
| Master template exists | no file at `_THE SHIP/Hitchhiker's Guide/Schema/New World Coordinates.md` |
| Instrument Panel exists | no such directory |
| Atlas of Worlds exists | no such directory |
| No name collision in the Atlas | a file of that name is already archived |
| Master has an empty `Run:` slot | nothing matches `^Run:` with an empty value |

A collision means a run number is being reused. That is a ledger fault, not a
file fault, and it gets fixed in the ledger — never by renaming the file that
tripped it.

---

## Decided

Rulings from batch request R2 and R3. Each row was in the *Undecided* table
below until it was ruled. Do not re-open one without saying so.

| Artifact | Rule | Ruled by |
|---|---|---|
| `_THE SHIP/The Guy/` | **Retired — nothing spawns in the Ship at all.** The Guy's home is repo root, alongside the crate. Nothing under `_THE SHIP/` is ever deleted at a boundary, so this ritual has no Ship-side deletion step. See `Hitchhiker's Guide/Ontology/The Crate.md`. | operator, R3 |
| `_THE VAST UNKNOWN/Crash Sites/New World NNN.json` | **Dies with the world. Not archived, not moved.** It is the engine's derived copy of a form whose master is already archived forever in `Instrument Panel/Atlas of Worlds/`. Archiving a derivation of a preserved source is how two sources of truth start. | assistant, R2 — operator may veto |
| `_THE VAST UNKNOWN/` itself | **A new engine replaces the dead one in place.** The directory is gitignored and untracked, so a replacement enters the repo on purpose (`git add -f`) or not at all. Landing beside it would leave two directories both plausibly live, and the engine has no INDEX to say which. | assistant, R2 — operator may veto |

The two assistant-ruled rows are marked because they were decided in Pass 4 of
a batch, not by the operator directly. They are live rules until vetoed, but
the authorship is on the record.

### What the Ship-side rule now buys

`Commit Ritual.md` asserts an invariant: *"a scuttle commit must delete nothing
under `_THE SHIP/`."* Until The Guy was retired, that invariant was false, and
the note below explains why no path-based hook could have enforced it.

**It is now true by construction.** A hook checking it can never fire a false
positive, because there is no legitimate case of a run deleting something in
the Ship. That hook has not been written yet.

---

## Undecided

Each row below is a real artifact that exists right now with no rule attached.
Until a row is decided, this ritual does not cover it, and **nothing may move it
silently.**

| Artifact | The open question |
|---|---|
| `_THE SHIP/_EJECT BUTTON/RUN-NNN-Assistant-Report.md` | Accumulates one per run into a flat folder. No archive directory exists for it, and none has been asked for. `RUN-NNN-Autopsy.md` now accumulates beside it, so the folder gains two files per run, not one. |
| `/C-THE SHIP-10` (the crate) | Created at server launch, lives at repo root. Whether it survives a run boundary or dies with the world is unstated. See `Ontology/The Crate.md`. |
| `/The Guy/` at repo root | Dies with the run, per the operator, who deleted it by hand this transition. What deletes it when it is not done by hand has never been specified. |
