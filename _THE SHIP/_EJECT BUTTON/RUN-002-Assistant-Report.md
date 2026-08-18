# RUN-002 — Assistant Report

The toll for run 2. Filed 2026-08-18, before any scuttle.

What the world failed at: **the engine reported a thing that does not exist.**

---

## Sensor state at filing

| | |
|---|---|
| Guy | `the-guy` |
| Run | 002 |
| Visible | `Cryobay.md` (v1), `The Guy` (v1) — both first appearance Run-002 |
| Unknown contacts | 0 |

The fog is fully lifted on run 2. One of the two things behind it was real.

---

## The failure

`scan` reports `Cryobay.md` as `Visible: Yes, Version 1`. The file does not
exist anywhere on disk.

| Check | Result |
|---|---|
| Recursive search of `_THE SHIP/` | nothing |
| Operator's explorer, `_THE VAST UNKNOWN/` | nothing |
| `git ls-files "_THE VAST UNKNOWN/"` | `Crash Sites/New World 002.json`, `cartridge.json`, `pyproject.toml`, `schema.json`, `server.py` — no Cryobay |
| `git status --short --ignored` | `Crash Sites/Run 002 State.json`, `.venv/` — no Cryobay |

**Two sources of truth, already drifted.** `Run 002 State.json` carries the
Visible flag. The filesystem has never held the artifact. `scan` reads the
JSON, so the engine describes a world it cannot produce.

The correct behaviour was observed live in the same session: `observe` on
`The Guy` returned an explicit `spawned:` path and created
`_THE SHIP/The Guy/` on disk. The write-through works. Cryobay got the flag
without the file.

### Hypothesis — not verified

Cryobay was observed before commit `cd4342c` — *"No save ritual: the engine
writes through, and observe makes discovery real."* Write-through is recent.
An observe that predates it would flip Visible and materialise nothing, and
the state file would carry that flag forward uncorrected.

Unverified because confirming it means reading `server.py`, which is behind
the fence. Left unverified deliberately.

**If the hypothesis holds, this is not a bug in current code.** It is legacy
state from before the fix, still being reported as real — which is the worse
failure, because the engine looks healthy while lying.

---

## What was discovered this run

`The Guy` materialised at `_THE SHIP/The Guy/` — an **empty directory** with a
`.gitkeep`. Not a file. No content.

`guy_handle` has been a required parameter on every engine call since the
server came up, documented as *"unused until identity is designed."* Observing
it produced the slot, not the identity. The engine discovered that there is a
hole shaped like a decision, and left the decision open.

Note the split: `Cryobay.md` is world-side and named like a file. `The Guy` is
Ship-side and named like a folder. Discovery does not have one destination.

---

## Secondary findings

| Finding | Detail |
|---|---|
| `observe` is write-only | The engine can create things and has no tool that returns their contents. `scan` gives Name, Visible, First Appearance, Version — that is the entire read surface. |
| `observe` cannot be targeted | Its only parameter is `guy_handle`. It hits "the nearest unknown contact." You cannot aim it. |
| No pre-commit visibility | Nothing reveals a contact before committing to it. Irreversibility is by design; the absence of any preview is the consequence. |
| Spawn destination is unspecified | The Guy landed at Ship root. Whether that is intended, and whether the repo root or the Ship root is correct, has never been decided. |

---

## Assistant errors this run

Recorded because the failure-solution pairs are the point.

**1. Phantom capability.** Proposed `probe`, staged-observe, and a
type-but-not-content reveal as design options, listed close enough to the real
tools to read as inventory. The operator asked whether `probe` was available.
It was never real. *Hypotheticals stated in the same register as inventory
become phantom capabilities.*

**2. Elimination without the null case.** Searched the Ship, found nothing,
and concluded Cryobay "is in `_THE VAST UNKNOWN/`." Never considered that it
existed nowhere. The operator checked their own explorer and broke the
conclusion. *Eliminating one location does not confirm another when "absent"
is on the table.*

Both were caught by the operator, not by the assistant.

---

## Fence report

`_THE VAST UNKNOWN/` was not read. `server.py`, `cartridge.json`,
`schema.json`, and both state JSONs remain unopened by this session.
Diagnosis used file names, `git ls-files`, and `git status` only.

The desync was fully diagnosable from outside the fence. Holding it cost
nothing.

---

## Engine work items

Requires a session with the engine as working directory. The Ship cannot
reach in.

| # | Item | Why |
|---|---|---|
| 1 | **Reconciliation check** | `scan` must not report a thing it cannot produce. Either backfill the artifact or drop the flag — but never answer with both states at once. |
| 2 | **A reader** | `inspect(guy_handle, name)` returning contents for already-Visible things. Closes the write-only gap without touching fog or weakening irreversibility. |
| 3 | **Spawn destination, decided** | Ship root or repo root, stated explicitly rather than emergent. Applies to future spawns; relocating existing ones requires updating the state record in the same move or it desyncs again. |

Item 1 is the toll's actual finding. Items 2 and 3 are open design, not defects.

---

## Open decisions

- What goes in `The Guy/`. Currently empty by discovery, not by neglect.
- Whether `observe` should stay one-way.
- Whether world content should be readable through the engine at all, or
  remain operator-only by design.
