# Ignition Codes

The durable scripts. They survive every reset and must never depend on anything
that does not.

| Script | What it does |
|---|---|
| `chart_course.py` | Archives every live `New World NNN.md` into `Atlas of Worlds/` and stamps the next blank from the master template. Refuses rather than resolving — see `_EJECT BUTTON/Biter Attack Ritual/File Move Ritual.md` for the full refusal table. |
| `enter_hyperspeed.py` | Validates the filled world form against the schema and emits the crash-site JSON for the engine. |
| `pumpjack.py` | **The live copy.** Pulls Claude Code session transcripts out of its own storage into `SatNav/Incoming Transmissions/`. An older, different version is kept as inspiration at `Fireproof Safe/Ancient Artifacts/pumpjack.py` — that one is not run. |

## The rule that got learned here the hard way

**A durable script may not depend on a disposable anything.** Both loop skills
once called `_THE VAST UNKNOWN/.venv/Scripts/python.exe` — tooling that survives
every reset, reaching into the one directory guaranteed to be destroyed. Both
now use plain `python`.

The interpreter was only the visible half. `enter_hyperspeed.py` also imported
`yaml`, and the sole declaration of that dependency lived in the engine's
`pyproject.toml` — the disposable world's manifest carrying the durable Ship's
dependency, for a package the engine never imported itself. That was removed
rather than relocated: the frontmatter is parsed by hand now, and **these
scripts have no third-party dependencies at all.**

Keep it that way. A durable script that needs something installed is the same
fault as one that needs the planet mounted, only slower to notice.

## Refusals

Every script here stops rather than resolving a precondition. Show the refusal
exactly as printed and stop. Do not create the folder, rename the file, or edit
the template to make it pass. Friction is the product.
