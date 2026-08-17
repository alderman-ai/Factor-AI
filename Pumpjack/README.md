# Pumpjack

Knowledge enters this factory as **oil**, not ore.

Ore is discrete and gets *assembled* — countable items combined into bigger
items. That is the task line. Oil is continuous and gets *refined* — one
undifferentiated flow separated into distinct fractions. That is the
knowledge line, and this is its wellhead.

The pumpjack produces crude by sitting on the patch and running. It does not
decide what is valuable. Every session in this repo generates a transcript
whether anyone is paying attention or not, which is exactly the property that
makes it a pumpjack rather than a hand-swung pickaxe: **zero action, not just
zero friction.**

## What is here

```
Pumpjack/
  pumpjack.py       the machine
  crude/            verbatim JSONL, byte-for-byte. Never edited.
  transcripts/      readable, attributed renderings
```

Two artifacts per session, deliberately.

`crude/` is the source of truth. It is copied out of Claude Code's own storage
without alteration, because that storage lives outside this repo, is subject to
cleanup, and is invisible to git.

`transcripts/` is what a human or a refinery actually reads. It is lossy on
purpose — long tool results are clipped — and every clip is marked. A bad
render is therefore never a data loss; re-run the machine.

**Refining at the pumpjack would defeat the point of having a refinery.**
Nothing here sorts, categorises, or extracts lessons. That happens downstream.

## Running it

```
python pumpjack.py --project <encoded-project-dir> --date YYYY-MM-DD
```

`<encoded-project-dir>` is the folder name under `~/.claude/projects/` — the
working directory path with separators replaced by dashes. For example:

```
python pumpjack.py --project C--Users-alder-Desktop-Factor-AI-The-Ship --date 2026-08-17
```

Re-running is safe and idempotent for finished sessions: same input, same
output filenames, overwritten in place.

## Three things the first extraction taught us

**Reasoning is not in the crude, and no better script will recover it.** Each
thinking block is stored with an empty `thinking` field and a populated
`signature`. The signature is a protobuf blob whose payload is encrypted — its
only plaintext is metadata (model name, block type, a UUID). It exists so the
API can verify thinking blocks on replay, not so anyone can read them.

This was checked rather than assumed. A search across the whole of
`~/.claude/` for any file containing a non-empty `"thinking"` value returns
nothing — not in the project storage, not in `sessions/`, `cache/`,
`backups/`, or `history.jsonl`. Across the first three sessions: 100 thinking
blocks, 0 with retained text.

The consequence is structural. Transcripts hold what was said and done, never
what was thought, so a refinery has to derive lessons from visible output
alone — conclusions survive, the reasoning that produced them does not. Blocks
are counted in each transcript header so the absence stays visible rather than
silent. **If reasoning matters for a given decision, it has to be said out loud
in the session**, where it lands in the crude like anything else.

**Large tool results are not in the JSONL either.** Claude Code spills them to
`<session-id>/tool-results/toolu_*.txt` beside the transcript, and the JSONL
does not reference the path — the files are keyed by tool_use id and found by
convention. Copying only the JSONL silently drops them. Worse, the spill has a
size threshold, so a naive extractor works correctly right up until it doesn't:
of the first three sessions, two had spilled files and one had none. The
pumpjack now copies the whole sidecar directory alongside the crude and notes
the count in the transcript header.

**A live session cannot be finalised.** Extracting the currently-running
session copies a mid-session snapshot; the source file keeps growing after the
copy. Such a session needs re-extraction once it ends. This is the ordinary
state of a well that is still flowing, and it is the strongest argument for
making extraction a Stop hook rather than a thing you remember to run.

## Note on what gets published

This repo is public and crude is unedited. Extraction publishes everything said
in a session — dead ends, mistakes, asides. That is consistent with the
project's stated fallback of keeping full transcripts for building in public,
but it is automatic and unreviewed, and worth knowing before the machine runs
on its own.
