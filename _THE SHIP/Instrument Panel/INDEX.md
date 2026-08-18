# Instrument Panel — INDEX

| Entry | What it is |
|---|---|
| `Ship Capabilities.md` | Every skill deployed in this repo, where it loads from, and what it does. Also the durable scripts. Read this instead of opening `.claude/skills/`. |
| `Atlas of Worlds/` | Every retired `New World NNN.md`. Permanent — a world's coordinates are never deleted. |
| `Ignition Codes/` | The durable scripts. `chart_course.py`, `enter_hyperspeed.py`, `pumpjack.py`. |
| `New World NNN.md` | The one live world form, when there is one. None right now. |

This file accretes. `README.md` does not.

**What used to be here:** `chart-course.md` and `enter-hyperspeed.md`, full
copies of their `.claude/skills/*/SKILL.md` bodies. They were hand-synced and
had already drifted. Replaced by `Ship Capabilities.md`, which describes the
skills without duplicating them.

`chart-course` itself no longer exists — `eject-mission` absorbed it, and is
deployed at both repo root and `_THE SHIP/` so it is reachable from cloud and
mobile sessions, which are root-only.
