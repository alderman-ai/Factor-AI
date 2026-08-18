# Ship Capabilities

Every skill deployed in this repo, what it does, and where it is loaded from.

**This page is a directory, not a copy.** It replaces the two full skill bodies
that used to sit in this folder — `chart-course.md` and `enter-hyperspeed.md`
were byte-identical duplicates of their `SKILL.md` files and had already begun
to drift. There is now exactly one copy of every skill, and it is the one Claude
Code actually loads.

## Where skills load from

Claude Code loads skills from `.claude/skills/` **relative to the working
directory the session was started in.** A session started at repo root sees the
root set. A session started at `_THE SHIP/` sees the Ship's set.

Right now that distinction is theoretical: **all four skills live at repo root
and `_THE SHIP/.claude/` does not exist.** Whether run rituals should move to a
Ship-local set — and what a root session should get when it types a Ship-owned
command — is an open decision (R6 of the batch request, returned for a new
proposal). Until it is ruled, this table has one column of homes, not two.

## Deployed skills

| Skill | Loaded from | Invoked by | What it does |
|---|---|---|---|
| `chart-course` | root | `/chart-course` | Drives the gap between runs. Verifies the dead run was actually closed out — headstone tag present, assistant report filed, working tree clean — then runs the File Move Ritual and stamps a blank `New World Coordinates` form onto this Panel. **Gates, does not automate:** it performs no commit, tag, or push, and it refuses to cross the gap if the previous run was never closed. |
| `enter-hyperspeed` | root | `/enter-hyperspeed` | Validates the filled `New World Coordinates` form on this Panel and emits the engine JSON into `_THE VAST UNKNOWN/Crash Sites/`. Refuses on an incomplete form and will not fill a field for you. Terminal stage 03 (Process) of the loop. |
| `science` | root | `/science`, or on the assistant's own initiative | Captures one lesson from the current session as a structured entry in `_THE SHIP/SatNav/Incoming Transmissions/`. Records who invoked it, why, and the lesson in full self-contained detail. This is the mechanism that feeds the Key Long-term Output; it is meant to be used generously. |
| `obsidian-sync` | root | `/obsidian-sync` | Forces a sync of the local vault through Obsidian Sync using the headless `ob` CLI. Hard-halts unless it is running in a local CLI session on the operator's desktop machine — never in a cloud or web session. |

## Durable scripts

Not skills. Invoked by name, or by a skill.

| Script | Path | What it does |
|---|---|---|
| `chart_course.py` | `Ignition Codes/` | Archives every live `New World NNN.md` into `Atlas of Worlds/` and stamps the next blank from the master template. Refuses rather than resolving; see `File Move Ritual.md`. |
| `enter_hyperspeed.py` | `Ignition Codes/` | Validates the filled form against the schema and emits the crash-site JSON. |
| `pumpjack.py` | `Ignition Codes/` | **The live copy.** Extracts Claude Code session transcripts out of its own storage and into `SatNav/Incoming Transmissions/`. A second, older copy exists at `Fireproof Safe/Ancient Artifacts/pumpjack.py` — that one is kept as inspiration, not run. |

## Known drift

`enter-hyperspeed` still invokes `_THE VAST UNKNOWN/.venv/Scripts/python.exe` —
the interpreter inside the disposable, scuttled world. `chart-course` was fixed
to plain `python`; this one was not. It has not been changed here because
nobody ruled on it. It has not bitten yet only because the scuttle used
`git rm --cached`, which left the venv sitting on disk.

**Swapping in plain `python` will not be enough.** The run-002 autopsy found a
second layer nobody had named: `enter_hyperspeed.py` imports `yaml`, and the
only place that dependency is declared is `_THE VAST UNKNOWN/pyproject.toml` —
the disposable world's manifest carrying the durable Ship's dependency, for a
package the engine itself never imports. Fixing the interpreter without moving
the declaration trades one failure for another. See
`_EJECT BUTTON/RUN-002-Autopsy.md`.
