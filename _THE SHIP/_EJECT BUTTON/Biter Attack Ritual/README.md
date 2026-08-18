# Biter Attack Ritual

How a run dies. Two documents, split by what they touch.

| Document | Governs | Never does |
|---|---|---|
| `Commit Ritual.md` | git — the tag scheme, the commit order, how to navigate run boundaries afterwards | moves a file |
| `File Move Ritual.md` | disk — what is archived, what dies with the world, what is written fresh | creates a commit |

Read both before scuttling anything. Where a step does both jobs it is split
across the two, and each names the other.

## Why the split

Git never deletes anything, so preservation is free and is not the problem. The
problem is **navigation** — making run boundaries findable without reading the
whole log. `Commit Ritual.md` is the coordinate system for that.

The file moves are a separate problem with a separate failure mode: a move made
by hand produces the same directory listing as a move made by the script, and
skips every refusal. That already happened once, and `File Move Ritual.md`
exists because of it.

## Status

`File Move Ritual.md` still carries an *Undecided* table. Until a row there is
ruled, this ritual does not cover that artifact and **nothing may move it
silently.**
