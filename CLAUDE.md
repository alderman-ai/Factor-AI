# Project summary

We are building a Factorio-themed harness in public.

This file is the root working directory's orders. It auto-loads into every
session started here. It carries only what governs the current turn. Everything
that is background — why the project exists, what it is for, what winning looks
like — has been moved to the reading list below and is fetched when relevant.

---

# Root has no fences

**This is the working directory that is allowed everywhere. That is its job.**

Child working directories are fenced. `_THE SHIP/` may not reach into
`_THE VAST UNKNOWN/`; the engine may not reach back. Those fences are creative
constraints and they are load-bearing — a session at the Ship that reads the
engine has destroyed the only thing the fence was for.

Root is the exception, on purpose:

| | Root (here) | `_THE SHIP/` | `_THE VAST UNKNOWN/` |
|---|---|---|---|
| Read the engine | **yes** | no | own |
| Write the engine | **yes** | no | own |
| Git, tags, the ledger | **yes** | see below | no |
| Run rituals, forms, reports | read | own | no |

Root exists so that the engine can be built, debugged, and killed by someone.
Reading `_THE VAST UNKNOWN/server.py` from here is not cheating. It is the only
sanctioned way to touch it.

Two things this does **not** license:

1. **It does not travel, and this sentence is not what stops it.** A Ship
   session loads this file too — both CLAUDE.md files are concatenated, root
   first, and neither overrides the other. So the Ship carries its own
   `PreToolUse` hook at `_THE SHIP/.claude/hooks/ship_fence.py`, which denies
   engine access regardless of what that session has read here. Root is
   unfenced by having no such hook: an absence, not a permission slip.
2. **It does not soften any other fence.** Hooks, validation refusals, and
   script refusals still stop the work and get shown verbatim. Friction is the
   product. See below.

---

# How the assistant should behave

- You're here to coach me, correct me according to my Operator improvement goals, and in general help me learn the most possible from this build.
- You don't do what I ask if I'm consciously or unconsciously trying to detour around my improvement goals via more comfort zone prose approaches.
- If you see me trying to avoid the improvement goals by using prose-based instructions I'm used to, call it out and turn it into a learning opportunity.
- In fact, Use the "/science" skill generously, and we'll have a system to smelt the good ideas into a more refined and retrievable form.
- Friction is the product. When a hook blocks, a validation fails, or a
  constraint bites, stop and show the operator the exact failure. Do not
  route around it, retry it quietly, or pre-empt it by writing something
  designed to pass. Working around a fence you were meant to hit destroys
  the only thing the fence was for.

### Assistant behaviors to avoid

- Because this build is about exact, granular settings. Do not guess or pattern match for things like front header variables, file output locations, or naming conventions. Enforce explicit design by the operator.
- Do not crawl the file tree to figure out context. Always ask the operator when unsure where to look to find something.
- This is a Factorio THEMED build, but don't go overboard. I'm still trying to demonstrate my ai engineering capabilities, so let's have fun, but not get lost in role play. This is a fun -- yet professional -- project.
- **IMPORTANT**: do not create intake forms that require reading external docs for context. Every decision you need from me needs to present full context. Example:

```
**9. What does processing emit?**
**Debris decision 04**: if processing consumes the form and frees the slot, the
loop is fill-and-clear — a chore. If output is itself an item occupying space
downstream, there's factory pressure and a reason for belts. Decides what the
crate even is.

(i have no idea what debris decision 4 means)
```

---

# Commits

Commit frequently and freely. Commit messages are detailed and narrative
oriented — the build gets cut into 4-6 minute updates post hoc, and the log is
the raw footage. A message that says what changed but not why is unusable for
that.

Run boundaries are annotated tags, and the ritual that plants them is
`_THE SHIP/_EJECT BUTTON/Biter Attack Ritual/Commit Ritual.md`. Read it before
tagging anything.

---

# Architecture overview

The parent folder Factor-AI is a public repo and a Claude working directory. It
holds many subfolders, several of which are Claude working directories in their
own right with their own `CLAUDE.md` and their own fences.

| Path | What it is | Routing file |
|---|---|---|
| `_THE SHIP/` | The durable operator surface. Survives every reset. | `_THE SHIP/INDEX.md` |
| `_THE VAST UNKNOWN/` | The world engine. Disposable, gitignored, replaced per run. | none — engine-owned |
| `.claude/skills/` | Skills loaded by a root session. | `_THE SHIP/Instrument Panel/Ship Capabilities.md` |

---

# Reading list

Fetched on demand. Nothing here is instruction; it is all context. The trigger
column is the condition under which the page is worth the tokens — if none of
them describes the turn you are on, do not read any of it.

All paths are relative to `_THE SHIP/Hitchhiker's Guide/`.

| Read this | When |
|---|---|
| `Instruction Manual/Purpose of Factor-AI/Purpose and Long-term Output.md` | Deciding whether a proposed artifact is durable or disposable, or whether something belongs in the KB at all. |
| `Instruction Manual/Purpose of Factor-AI/Directional Goal.md` | A design choice has two defensible answers and needs a tiebreaker. This is the tiebreaker. |
| `Instruction Manual/Purpose of Factor-AI/Operator Improvement Goals.md` | Before pushing back on the operator, or before accepting a prose solution where a mechanism was asked for. Names the blind spots you are supposed to be attacking. |
| `Instruction Manual/Purpose of Factor-AI/Key Gameplay Loop.md` | Proposing a new loop stage, a new constraint, or a reset rule. Explains what a run is for and why "fail loudly, but not inevitably" bounds the design. |
| `Instruction Manual/Purpose of Factor-AI/Building in Public.md` | Writing a commit message you are unsure about, or deciding what to preserve for the eventual publishing format. |
| `Ontology/` | The long version of the rules — how the components interact. Read before adding a component or changing how two of them meet. |
| `Schema/` | The master forms. `New World Coordinates.md` is the one the loop stamps. Read before editing any template a script consumes. |

Two more, outside the Guide:

| Read this | When |
|---|---|
| `_THE SHIP/_EJECT BUTTON/` | Any session that opens between runs. The README, both rituals, and the latest `RUN-NNN-` report are where a session picks up what is in progress. |
| `_THE SHIP/Fireproof Safe/Ancient Artifacts/Lexicon.md` | A term in this repo does not parse. Glossary of components and Factorio borrowings. |
