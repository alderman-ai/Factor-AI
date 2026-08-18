# Ignition Codes

The durable scripts. They survive every reset and must never depend on anything
that does not.

| Script | What it does |
|---|---|
| `chart_course.py` | Archives every live `New World NNN.md` into `Atlas of Worlds/` and stamps the next blank from the master template. Refuses rather than resolving — see `_EJECT BUTTON/Biter Attack Ritual/File Move Ritual.md` for the full refusal table. |
| `enter_hyperspeed.py` | Validates the filled world form against the schema and emits the crash-site JSON for the engine. |
| `pumpjack.py` | **The live copy.** Pulls Claude Code session transcripts out of its own storage into `SatNav/Incoming Transmissions/`. An older, different version is kept as inspiration at `Fireproof Safe/Ancient Artifacts/pumpjack.py` — that one is not run. |

## The rule that got learned here the hard way

**A durable script may not invoke a disposable interpreter.** Both loop skills
once called `_THE VAST UNKNOWN/.venv/Scripts/python.exe` — tooling that survives
every reset, reaching into the one directory guaranteed to be destroyed.
`chart-course` has been fixed to plain `python`. `enter-hyperspeed` has not, and
is recorded as known drift in `Ship Capabilities.md`.

## Refusals

Every script here stops rather than resolving a precondition. Show the refusal
exactly as printed and stop. Do not create the folder, rename the file, or edit
the template to make it pass. Friction is the product.
