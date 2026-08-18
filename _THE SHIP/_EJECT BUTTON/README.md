# _EJECT BUTTON

The reset ritual. Read before scuttling a run.

---

## What this solves

Git never deletes anything. A reset destroys the working tree, never the
history — every file the planet ever held stays in the commits that held it,
permanently.

So preservation is free and is not the problem. The problem is **navigation**:
making run boundaries findable without reading the whole log. This document is
the coordinate system.

**The Ship is the durable ledger. The planet is disposable.**

---

## The coordinate scheme

Annotated tags, namespaced per run, numbers zero-padded to three digits.

```
RUN_001/PROJECT_START
RUN_001/BITER_ATTACK!!
RUN_002/SAME_SHIP_DIFFERENT_DAY
RUN_002/BITER_ATTACK!!
RUN_003/SAME_SHIP_DIFFERENT_DAY
```

Every rule below was forced by git, not chosen:

| Rule | Why |
|---|---|
| No spaces in tag names | `fatal: 'BITER ATTACK!!' is not a valid tag name` — refs are paths on disk |
| Zero-pad to three digits | Tags sort alphabetically. `RUN_10` sorts *before* `RUN_3` |
| `RUN_00N` is a prefix, never a tag on its own | `fatal: cannot lock ref` — a ref can be a file or a directory, never both |
| The number is the run that **died** | `RUN_002/BITER_ATTACK!!` ends run 2. `RUN_003/SAME_SHIP_DIFFERENT_DAY` begins run 3 |
| No date in the name | Git already stores the tag date *and* the commit date. The run number exists nowhere else |

`!!` is legal in a git ref. Only spaces had to go.

### A run is a range, not a tag

A tag pins one commit. A run is the span between two pins. This is not a
limitation to work around — a run genuinely is a range, and git has first-class
syntax for ranges.

`RUN_001` is asymmetric by design: it opens on `PROJECT_START` because there was
no previous ship to be the same ship as. Every run after it opens on
`SAME_SHIP_DIFFERENT_DAY`.

---

## The ritual

Three commits, two tags, one push. Do not improvise the order.

**1. The toll.** File the entry naming what the world failed at. Lands in The
Ship. A reset is legal only after this entry exists — pay the toll, then burn
it. The reset produces the resource rather than spending it.

**2. The scuttle.** One commit. **Pure deletion, nothing else in it.** If a
deletion is mixed with additions the diff becomes unreadable, and being readable
is this commit's entire job. The commit message is the epitaph.

```bash
git rm -r --cached <planet paths>   # stage the removals
git commit                          # message = what the world failed at
git tag -a 'RUN_00N/BITER_ATTACK!!' -m '<what died and why>'
```

**3. The landing.** Scaffold the new world.

```bash
git commit
git tag -a 'RUN_00M/SAME_SHIP_DIFFERENT_DAY' -m '<what carried across>'
```

**4. Push the tags.** `git push` sends commits and **leaves tags behind.** A
ledger that never reaches GitHub is not public.

```bash
git push origin --tags
```

### The invariant

**A scuttle commit must delete nothing under `_THE SHIP/`.** This is mechanically
checkable and should become a hook rather than a promise.

---

## Navigation

| Question | Command |
|---|---|
| Every boundary, in order | `git runs` |
| Everything tagged in run 2 | `git tag -l 'RUN_002/*'` |
| The whole story of run 2 | `git log RUN_002/SAME_SHIP_DIFFERENT_DAY..RUN_002/BITER_ATTACK!!` |
| What run 2 built | `git diff RUN_002/SAME_SHIP_DIFFERENT_DAY RUN_002/BITER_ATTACK!! --stat` |
| Exactly what died | `git show RUN_002/BITER_ATTACK!!` |
| What The Ship carried across | `git diff RUN_002/BITER_ATTACK!! RUN_003/SAME_SHIP_DIFFERENT_DAY` |
| The repo as it stood at a boundary | Click the tag on GitHub |

Ranges exclude their left endpoint. To include the opening commit itself, add a
caret:

```bash
git log RUN_001/PROJECT_START^..RUN_001/BITER_ATTACK!!
```

### The measurement this gives away for free

`git diff RUN_00N/BITER_ATTACK!! RUN_00M/SAME_SHIP_DIFFERENT_DAY` is the
reset-cost instrument. A scuttle diff that **shrinks run over run** is the
ontology doing its job. One that stays the same size is the falsification.

No instrument had to be built. It only required planting the tags.

---

## The `git runs` alias

Lives in `.git/config`, which is **not committed** — it does not travel to
anyone who clones this repo. Recreate it with:

```bash
git config alias.runs "tag -l --sort=version:refname \
  --format='%(refname:short)%09%(*committerdate:short)%09%(subject)'"
```

`%(*committerdate)` is the date of the *commit the tag points at*, not the date
the tag was created. Those differ whenever a tag is planted late, and the commit
date is the one that tells the truth about the run.

---

## Current state

| Tag | Commit | Meaning |
|---|---|---|
| `RUN_001/PROJECT_START` | `24efdd4` | First commit whose root CLAUDE.md carries no Business motives section. Everything before it is pre-history: the pitch, not the work. |

No run has been scuttled yet.
