# Schema

**Master forms that scripts consume.** These are machine contracts, not
documents. Break the shape and a script refuses rather than adapting.

| File | Consumed by | What happens if it is wrong |
|---|---|---|
| `New World Coordinates.md` | `Ignition Codes/chart_course.py` stamps a blank copy onto the Instrument Panel; `enter_hyperspeed.py` validates the filled result. | `chart_course.py` refuses if this file is missing or has no empty `Run:` slot. Shown verbatim, never worked around. |
| `ADRENALINE Rules.md` | `Verification Scripts/adrenaline.py` reads its frontmatter and its `## The rules` table, and runs exactly what the table says. | `adrenaline.py` HALTs — missing file, missing frontmatter key, no rules table, or a verb the script has no function for. Nothing is checked and nothing is run. |
| `The Guy.md` | Listed here but **not on disk**. Either it was never written or it moved. Unresolved. | — |

## Editing rules

- **Do not edit a schema to make a refusal go away.** A refusal is the
  instrument working. Fix the form, not the contract.
- A schema change is a breaking change to every script that reads it. Say which
  scripts, in the commit message.

## Not this folder

`Fireproof Safe/Root level templates/` holds masters a **human** fills in by
hand, with nothing validating them. `Templates/` is a third, currently empty
thing, deliberately left alone.

`Untitled/` is an empty leftover directory from a rename. Left in place rather
than deleted — deleting is the operator's call.
