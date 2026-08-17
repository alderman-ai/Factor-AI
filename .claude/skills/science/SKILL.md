---
name: science
description: Capture a key lesson from the current session as a structured entry in The Lab's Global Inbox. Use when the operator says something is a lesson, a learning, or "make that a science" — and use it on your own initiative when a genuine lesson has just occurred (a wrong assumption corrected, a constraint discovered, a design decision that turned on a specific reason). Records who invoked it, why, and the lesson in full self-contained detail.
---

# Science

Capture a lesson while it is still in front of you.

The pumpjack already extracts every session transcript automatically, so this
skill is not for capture-in-general. It exists because **reasoning is not
retained in the crude** — Claude Code stores thinking blocks with their text
stripped, so transcripts hold what was said and done, never what was thought.
Anything that existed only as reasoning is gone unless it is written down
deliberately.

That is the whole job: say the reasoning out loud, in a structured way, before
it evaporates.

## When to invoke

**Operator-invoked** — they say "that's a lesson", "make that a science",
"capture that", or run `/science` directly.

**Assistant-invoked** — you decide, unprompted, because a genuine lesson just
occurred. Reasonable triggers:

- An assumption you stated confidently turned out to be wrong
- A constraint of the system or tooling was discovered by hitting it
- A design decision turned on a specific reason worth preserving
- Something failed in a way that will recur

Do not invoke for routine progress, for restating something already written
down, or to be agreeable. A lesson that could not change anyone's future
behaviour is not a lesson.

## What "invoked" means

Invoked means **who decided** to use this skill — assistant or operator — not
the mechanism that ran it.

If the operator says "hey let's make that a science" and the harness matches
this skill's description and runs it, that is **operator-invoked**. The
operator decided; the harness merely dispatched.

If you run it because you judged that a lesson had occurred, that is
**assistant-invoked**, even if you announce it first.

## Procedure

1. Read `template.md` in this skill directory. That is the exact structure to
   produce — do not improvise a different one.
2. Fill in the three frontmatter fields (see below) and answer all three
   questions *inside* their fenced blocks.
3. Write the result to `The Lab/Global Inbox/`, relative to the repository
   root. That is the repo containing the working directory Claude Code was
   started in, not necessarily the working directory itself.
4. Name the file `YYYY-MM-DD_HHMMSS.md` in local time. If that name already
   exists, append `-2`, `-3`, and so on. Seconds precision plus the collision
   check is what keeps parallel sessions from clobbering each other.
5. Tell the operator you filed it, and where.

Do not sort, categorise, tier, or colour the entry. Intake structure will be
derived later from a real corpus rather than guessed at now — templating ahead
of the data is exactly the failure this project is trying to avoid.

## The frontmatter fields

**`working_directory`** — the absolute path Claude Code was started in for this
session. Not the repository root, and not wherever the file happens to be
written. This repo is a set of sibling working directories on one machine, so
which one a lesson came from is part of the lesson. The pumpjack records this
same value in every transcript header, so the two agree and can be joined.

**`session_id`** — what makes an entry traceable back to source. Given an
entry, the readable transcript is
`Pumpjack/transcripts/<date>_<time>_<first 8 chars of session_id>.md` and the
unedited original is the matching file under `Pumpjack/crude/`. Routing in this
factory is declarative, so an item has to carry its own history — nothing about
the path it took records where it came from.

**`captured`** — local time, ISO 8601 with offset, e.g.
`2026-08-17T21:14:03+02:00`.

**Three questions, for now.** More get added when a real corpus shows what is
missing.
