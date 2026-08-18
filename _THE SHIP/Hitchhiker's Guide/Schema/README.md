# Schema

**Master forms that scripts consume.** These are machine contracts, not
documents. Break the shape and a script refuses rather than adapting.

| File | Consumed by | What happens if it is wrong |
|---|---|---|
| `New World Coordinates.md` | `Ignition Codes/chart_course.py` stamps a blank copy onto the Instrument Panel; `enter_hyperspeed.py` validates the filled result. | `chart_course.py` refuses if this file is missing or has no empty `Run:` slot. Shown verbatim, never worked around. |
| `The Guy.md` | Not yet wired to a script. | — |

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
