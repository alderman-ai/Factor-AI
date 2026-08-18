---
Run: "002"
---
# **CRASH!**

 We've landed on this strange planet. I wonder what awaits us in this **vast unknown**....

## The fence

**This working directory is fenced, and the fence is a hook, not this
paragraph.** `.claude/hooks/ship_fence.py` runs before every Read, Edit, Write,
Glob, Grep, and Bash call in a Ship session and denies:

| Target | Why |
|---|---|
| `_THE VAST UNKNOWN/` | The engine's files. The Ship knows the world through its MCP **tools** and never through the source behind them. |
| `_THE SHIP/.claude/` | Itself. The fenced party does not edit its own fence. Change it from the repo root. |

Root `CLAUDE.md` says root has no fences, and **you are reading that sentence
right now** — a Ship session loads both files, concatenated, root first. Neither
overrides the other. That is exactly why the rule is enforced by a hook instead
of asked for in prose: the hook does not care what this session has read.

If it fires, **show the denial and stop.** Do not rephrase the path, do not try
another tool, do not ask root to fetch it for you mid-session. Engine work
happens from the repo root, in a different session, on purpose.

MCP tool calls are not filesystem operations and never reach the hook. If an
engine is registered, calling it is play, not a breach.

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
