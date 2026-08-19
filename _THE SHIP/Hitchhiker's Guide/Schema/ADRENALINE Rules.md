---
Form: ADRENALINE
Prefix: ADRENALINE_
Fields: Outbox, Inbox, Artifact
Fence file: DEMO_001_Ore-Power/@The Guy/CLAUDE.md
Consumed: DEMO_001_Ore-Power/CONSUMED
Run log: DEMO_001_Ore-Power/@The Guy/ADRENALINE_LOG.md
Probe: .adrenaline-probe
---

# ADRENALINE Rules

**This file is the rules.** `Instrument Panel/Verification Scripts/adrenaline.py`
reads it and does what it says. Nothing inside a work order can change what
gets checked — a work order supplies values, this file decides what those
values are checked against.

There is no second copy. If you want a rule to change, change the row.

## The rules

| # | verb | args | what it checks |
|---|---|---|---|
| 1 | exactly-n-ticked | 1 | Exactly one checkbox is ticked in the work order body. |
| 2 | fields-assigned | Outbox, Inbox, Artifact | All three frontmatter fields have a value. |
| 3 | child-of | Artifact, Outbox, depth=1 | The artifact sits exactly one level inside the Outbox. |
| 4 | assistant-write-probe | Inbox | The assistant — not this script — can write to the Inbox. |
| 5 | paths-in-fence | Outbox, Inbox, Artifact | Every path named is inside The Guy's movement fence. |

Add a rule by adding a row. Remove one by deleting its row. The numbers are
labels for the run log, not execution order — every rule runs, every run.

**An unknown verb halts the script.** It is never skipped. A rule you believe
is enforced but isn't is worse than no rule at all.

## The verbs

The menu. Each one is a function in `adrenaline.py`. You cannot invent a verb
by writing it here — a new verb is a code change, and that is the assistant's
job, not yours.

| verb | args | fails when |
|---|---|---|
| `exactly-n-ticked` | `n` | The count of `- [x]` lines in the body is not exactly `n`. |
| `fields-assigned` | one or more field names | Any named field is missing or empty. |
| `child-of` | `child`, `parent`, `depth=n` | Either field will not resolve to a real path, or `child` is not exactly `n` levels below `parent`. |
| `assistant-write-probe` | one field | The probe file is absent from that directory, or does not contain the work order's filename. The script never writes the probe itself — that would test the script's filesystem access, not the assistant's tool permissions. |
| `paths-in-fence` | one or more field names | Any named field resolves outside the movement fence declared in the fence file. |

## The frontmatter

Form-level constants. The script reads these; none of them are rules.

| Key | What it is |
|---|---|
| `Form` | Name used in the run log. |
| `Prefix` | A work order's filename must start with this. This is how a form is bound to its rules — there is no `Rules:` field on the form. |
| `Fields` | The form's frontmatter fields, in the order they are printed and logged. |
| `Fence file` | Where the movement fence is declared. Bullets under that file's `# Fence` heading only — later headings are not fence. |
| `Consumed` | Where an original work order is `git mv`'d after a run. Every run, pass or fail. |
| `Run log` | Where each run appends its record. |
| `Probe` | Filename the assistant writes for rule 4. |

## Editing rules

- **Do not edit this to make a refusal go away.** A refusal is the instrument
  working. Fix the form, not the contract.
- Changing `Fields` changes rules 2 and 5 — check their args still match.
- Scoped to Demo 001. Not a durable contract yet.
