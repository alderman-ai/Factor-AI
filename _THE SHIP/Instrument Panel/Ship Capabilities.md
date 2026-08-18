# Ship Capabilities

Every skill deployed in this repo, what it does, and where it is loaded from.

**This page is a directory, not a copy.** It replaced the two full skill bodies
that used to sit in this folder — `chart-course.md` and `enter-hyperspeed.md`
were hand-synced duplicates of their `SKILL.md` files and had already drifted.
Nothing here restates a skill's body; it says what each one does and where it
loads from.

Where a skill *is* deployed twice, that is deliberate and stated, the copies are
byte-identical, and there is a command below that checks it.

## Where skills load from

Claude Code loads skills from `.claude/skills/` **relative to the working
directory the session was started in.** A root session sees the root set; a
session started at `_THE SHIP/` sees the Ship's set. Nothing is inherited.

That cuts against how the operator actually works: **cloud and mobile sessions
are repo-root only**, and changing directory on a phone is painful. A
run-boundary skill reachable only from the Ship would be unreachable most of
the time. So the run ritual is deployed at **both** levels rather than stubbed.

## Deployed skills

| Skill | Loaded from | Invoked by | What it does |
|---|---|---|---|
| `eject-mission` | **root and Ship** | `/eject-mission` | Ends the run and opens the gap before the next. Gates first, then files the assistant report, deregisters the engine, makes the Ship's one and only commit, runs the File Move Ritual and stamps the next blank form. **Never tags and never pushes.** Absorbed `chart-course`, so the commit and the file move cannot be separated. |
| `enter-hyperspeed` | root | `/enter-hyperspeed` | Validates the filled `New World Coordinates` form on this Panel and emits the engine JSON into `_THE VAST UNKNOWN/Crash Sites/`. Refuses on an incomplete form and will not fill a field for you. Terminal stage 03 (Process) of the loop. |
| `science` | root | `/science`, or on the assistant's own initiative | Captures one lesson from the current session into `_THE SHIP/SatNav/Incoming Transmissions/`. Feeds the Key Long-term Output; meant to be used generously. Ruled to be duplicated at both levels — a lesson cannot survive a `cd`, so a stub would be worthless. **Not yet duplicated.** |
| `obsidian-sync` | root | `/obsidian-sync` | Forces a sync of the local vault through the headless `ob` CLI. Hard-halts outside a local CLI session on the operator's desktop. Ruled to graduate to user level (`~/.claude/skills/`). **Not yet moved.** |

### The `eject-mission` pair

The two copies are **byte-identical**, and the skill is written to make that
possible: every path in it resolves from `git rev-parse --show-toplevel` at
runtime, so nothing is cwd-relative and neither copy needs adjusting.

Check they still match:

    diff .claude/skills/eject-mission/SKILL.md          "_THE SHIP/.claude/skills/eject-mission/SKILL.md"

Silence means they match. **Edit one, edit the other in the same commit.**

One thing holds this together for free: the Ship's fence hook blocks writes to
`_THE SHIP/.claude/`, so a Ship session **cannot** edit its own copy. Both
copies can only be changed from root, which is the one place a change can be
made to both at once. The self-protection rule turns out to double as a
sync guarantee.

## Durable scripts

Not skills. Invoked by name, or by a skill.

| Script | Path | What it does |
|---|---|---|
| `chart_course.py` | `Ignition Codes/` | Archives every live `New World NNN.md` into `Atlas of Worlds/` and stamps the next blank from the master template. Refuses rather than resolving; see `File Move Ritual.md`. |
| `enter_hyperspeed.py` | `Ignition Codes/` | Validates the filled form against the schema and emits the crash-site JSON. |
| `pumpjack.py` | `Ignition Codes/` | **The live copy.** Extracts Claude Code session transcripts out of its own storage and into `SatNav/Incoming Transmissions/`. A second, older copy exists at `Fireproof Safe/Ancient Artifacts/pumpjack.py` — that one is kept as inspiration, not run. |

## Enforcement

Not a skill. Runs whether or not anyone invokes it.

| Hook | Path | What it does |
|---|---|---|
| Ship fence | `_THE SHIP/.claude/hooks/ship_fence.py` | `PreToolUse` on Read, Edit, Write, NotebookEdit, Glob, Grep and Bash. Denies any filesystem access from a Ship session to `_THE VAST UNKNOWN/`, and any edit to the Ship's own `.claude/`. Registered in `_THE SHIP/.claude/settings.json`. |

It loads only in a session started at `_THE SHIP/`, because settings come from
the working directory's `.claude/`. A root session never sees it, which is how
root stays unfenced — by an absence, not by a permission.

It does not touch MCP tool calls. The Ship may call an engine's tools; it may
not read the engine's source. That distinction is the fence.

## Resolved drift

`enter-hyperspeed` used to invoke `_THE VAST UNKNOWN/.venv/Scripts/python.exe`
— durable tooling running on the disposable world's interpreter. It had not
bitten yet only because the scuttle used `git rm --cached`, which left the venv
on disk.

Fixed, and one layer deeper than the symptom. The run-002 autopsy found that
`enter_hyperspeed.py` imported `yaml`, and the only declaration of that
dependency was `_THE VAST UNKNOWN/pyproject.toml` — the disposable world's
manifest carrying the durable Ship's dependency, for a package the engine never
imported itself. Swapping the interpreter alone would have traded one failure
for a quieter one.

So the dependency was removed rather than relocated. `frontmatter()` now parses
the flat `Key: value` block by hand, and **the Ship's durable tooling has no
third-party dependencies at all.**

What that trade cost, stated plainly: the hand parser is stricter than YAML.
Nesting, list items, a line with no `:`, and a repeated key are each refused by
line number instead of being accepted and reinterpreted. For a script whose job
is refusing malformed forms, strict is the right direction — but it is a
behaviour change, so it was verified rather than assumed. Both real forms
(`New World 002.md` and the master template) parse identically to the old YAML
path, including `Run` staying an integer and empty fields staying empty.
