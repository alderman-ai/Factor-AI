# File Move Ritual

The file half of a run transition. Read alongside `Commit Ritual.md`.

**`Commit Ritual.md` governs what git does. This governs what moves on disk.**
Nothing here creates a commit, and nothing there moves a file. Where a step does
both, it is split across the two documents and each names the other.

Called by the `chart-course` skill, which will not stamp a new world until this
document has been read and every artifact it touches has a rule.

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

## Undecided

Each row below is a real artifact that exists right now with no rule attached.
Until a row is decided, this ritual does not cover it, and **nothing may move it
silently.**

| Artifact | The open question |
|---|---|
| `_THE SHIP/The Guy/` | Dies with the run, per the operator. Empty since discovery. Nothing archives it, and no rule says what happens to it at the boundary. |
| `_THE VAST UNKNOWN/Crash Sites/New World NNN.json` | The engine's copy of the world. Left git at the scuttle, still on disk, behind the fence. Archived, deleted, or left where it lies? |
| `_THE SHIP/_EJECT BUTTON/RUN-NNN-Assistant-Report.md` | Accumulates one per run into a flat folder. No archive directory exists for it, and none has been asked for. |
| `_THE VAST UNKNOWN/` itself | Gitignored and on disk. Whether a new engine replaces the dead one in place, or lands beside it, is unstated. |

The Guy is the sharpest of these. It is the reason the invariant *"a scuttle
commit must delete nothing under `_THE SHIP/`"* is false and could never be
enforced by a hook: the Ship currently mixes durable and disposable in one
folder, so no path-based rule can tell them apart.
