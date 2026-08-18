# Batch Request — CHANGELOG

Newest first. One entry per version. A version is cut, never edited in place —
`Batch Request v1.md` stays exactly as it was when v2 lands beside it.

---

## v1 — 2026-08-18

First master. Cut from the live batch at repo root after that batch's own R4
and R7 landed, so v1 already includes both changes rather than needing them
applied.

**Shape**

- Instructions: the four-pass cycle, what a `P` block owes the operator, the
  rule that fences hold during a batch, and the note that this file is a cut
  rather than the master.
- Ten slots, `R1` through `R10`, all empty.
- Three fenced blocks per slot with exactly one author each —
  `<operator_request>`, `<assistant_proposal>`, `<operator_approval>`.
- Five approval boxes per slot: APPROVED, APPROVED (Subagent), ADJUST, RETRY,
  DEFER.

**Carried in from the live batch**

- *R4 — the subagent box.* `APPROVED (Subagent)` added, with a backtick slot for
  a model name, plus the Instructions section covering what choosing it commits
  the assistant to: the subagent inherits none of the conversation so the slot
  must be made self-contained or the assistant says so instead of dispatching a
  guesser; the main session reports what it did rather than pasting its
  transcript; fences are restated in its prompt rather than assumed to carry.
- *R7 — the fence tag.* The assistant's block was tagged `<assistant_request>`,
  which read as though the assistant were making the request. Renamed to
  `<assistant_proposal>` throughout, and the Instructions block table gained a
  column naming each block's tag.

**Known open**

The archive destination for a finished batch is stated in the Instructions —
`Operator Inbox/Archived Intake Forms/` — but nothing moves it there
automatically. That is a hand move today.
