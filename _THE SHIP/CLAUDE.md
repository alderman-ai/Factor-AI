---
Run: "002"
---
# **CRASH!**

 We've landed on this strange planet. I wonder what awaits us in this **vast unknown**....

## The fence

**This working directory is fenced. Never read or edit files in
`_THE VAST UNKNOWN/`.** The fence outlives the engine: a dead engine's files
are still on disk, still off-limits, and the vault is gitignored so nothing
there re-enters the repo by accident.

The repo root is exempt from this — see root `CLAUDE.md`, "Root has no fences."
**That exemption belongs to the root working directory, not to the assistant.**
A session started here does not inherit it by having read about it. If engine
work is needed, it happens from root, in a different session.

## Boot check — the engine is a state, not an assumption

Do not assert whether an engine exists. **Check, then report which state you
are in.** Both are legal.

| State | How you know | What you do |
|---|---|---|
| **ENGINE PRESENT** | `.mcp.json` at repo root registers a server **and** its tool answers when called. | Report the sweep. Pick up the run. |
| **ENGINE ABSENT** | `.mcp.json` registers nothing. | Say so plainly. Read `_EJECT BUTTON/`. Stop. Do not go looking for a server. Absence is a state, not a fault. |
| **ENGINE FAULTED** | `.mcp.json` registers a server and the tool does **not** answer. | Stop and report loudly, with the exact failure. This is a real fault. |

The distinction that matters is the last two rows. *Registered but not
answering* is a defect. *Not registered* is normal between runs. Run 002 opened
by confusing them — commit `b460417`, "First contact fails: the engine was
never started, not broken."

This section replaced a hand-written paragraph describing one particular dead
engine. That paragraph was correct when written and would have rotted silently
the moment an engine landed. **Do not reintroduce a prose description of the
current engine here.** If the boot check needs richer output, change the check.

## Between runs

We are after the `RUN_002/BITER_ATTACK!!` tag and before the next
`SAME_SHIP_DIFFERENT_DAY` tag. There is no world to play until that tag lands.
`_EJECT BUTTON/` — the README, the Biter Attack Ritual, and the latest
`RUN-NNN-` documents — is where a session picks up what is in progress.

## Nothing disposable lives here

**Everything under `_THE SHIP/` is 100% durable. Nothing temporary spawns here.**
A run creates nothing in this folder, so nothing in this folder is ever deleted
at a run boundary. Run-lifetime objects live at repo root and are named so you
can see them — see `Hitchhiker's Guide/Ontology/The Crate.md`.

This is the rule that makes the invariant in `Commit Ritual.md` —
*"a scuttle commit must delete nothing under `_THE SHIP/`"* — true and
hook-enforceable for the first time.
