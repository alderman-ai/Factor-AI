---
Run: "002"
---
# **CRASH!**

 We've landed on this strange planet. I wonder what awaits us in this **vast unknown**.... 

## the-vast-unknown (MCP)

- The world engine is the MCP server `the-vast-unknown` (registered in the
  repo-root `.mcp.json`, but with paths relative to `_THE SHIP` — the Ship is
  the assumed cwd for reaching the engine. A session started anywhere else in
  this repo will fail to connect, by design. Config changes need a session
  restart).
- On session start: call the engine's `scan` tool with `guy_handle: "the-guy"`.
  If it answers, report the sensor sweep and pick up the run in progress.
  If the tool is missing, say so plainly and stop — the server isn't
  connected. Don't hunt for workarounds.
- Never read or edit files in `_THE VAST UNKNOWN/` — the engine and its
  world content are off-limits to Ship sessions. Play the world through
  the engine's tools, not the file system.