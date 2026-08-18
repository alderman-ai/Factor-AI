---
Run: "002"
---
# **CRASH!**

 We've landed on this strange planet. I wonder what awaits us in this **vast unknown**.... 

## the-vast-unknown (MCP) — UNPLUGGED

- There is no world engine right now. When run 002 ended, its world and the
  server that ran it were removed from git tracking — they are still on disk —
  and `c980856` deleted `the-vast-unknown` from the repo-root `.mcp.json`, which
  is now empty. Do not call `scan`. Do not go looking for the server. Its
  absence is deliberate, not a fault to diagnose.
- On session start: read `_EJECT BUTTON/` instead of sweeping sensors. The
  README, the Biter Attack Ritual, and `RUN-002-Assistant-Report.md` are where a
  session picks up what is in progress.
- We are between runs — after the `RUN_002/BITER_ATTACK!!` tag and before the
  next `SAME_SHIP_DIFFERENT_DAY` tag. There is no world to play until that tag
  lands.
- Never read or edit files in `_THE VAST UNKNOWN/`. The fence outlives the
  engine: the old engine's files are still on disk, still off-limits, and the
  vault is now gitignored so nothing there re-enters the repo by accident.
- When a new engine is registered, replace this whole section with what it
  actually is. A section describing an engine that isn't connected is the exact
  failure `e7b7b1a` was written to end.
