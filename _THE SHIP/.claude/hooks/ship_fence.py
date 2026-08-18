#!/usr/bin/env python3
"""
The Ship's fence. A PreToolUse hook, not a paragraph.

WHY THIS IS A SCRIPT AND NOT A SENTENCE IN CLAUDE.md
----------------------------------------------------
A session started at `_THE SHIP/` loads BOTH CLAUDE.md files -- root's and the
Ship's -- concatenated, root first. They do not override each other. The docs
are explicit that when two loaded instructions contradict, the model "may pick
one arbitrarily," and that CLAUDE.md is "context, not enforced configuration."

Root's CLAUDE.md says root has no fences. That sentence is now sitting in every
Ship session's context. Asking prose not to be believed is not a fence.

This is. It runs before the tool call and returns a deny the model cannot talk
its way past.

WHAT IT BLOCKS
--------------
Filesystem access from a Ship-cwd session to:

  1. `_THE VAST UNKNOWN/`  -- the engine. Ship may not read or write its files.
  2. `_THE SHIP/.claude/`  -- itself. The fenced party may not edit its own
                              fence. Root can; that is where fences are changed.

WHAT IT DELIBERATELY DOES NOT BLOCK
-----------------------------------
MCP tool calls. If an engine is registered, the Ship calling `scan` is not a
filesystem operation and never reaches this hook. That is the intended shape:
the Ship knows the world through the TOOL SURFACE and never through the source
behind it. The fence is about what the Ship is allowed to KNOW, and a path rule
was only ever a proxy for that.

WHY IT CHECKS cwd EVEN THOUGH IT ONLY LOADS AT THE SHIP
-------------------------------------------------------
Settings load from the working directory's `.claude/`, so a root session should
never see this file at all. The cwd check is belt-and-braces: if that
assumption is ever wrong, root stays unfenced anyway, which is the design.

Exit 0 with no output = no decision, normal permission flow. Exit 0 with a
deny = blocked. Never exits 2; a crash in the fence must not read as a block.
"""

import json
import os
import sys

SHIP_DIR_NAME = "_THE SHIP"
ENGINE_DIR_NAME = "_THE VAST UNKNOWN"

# Tool input keys that carry a filesystem path.
PATH_KEYS = ("file_path", "path", "notebook_path")


def norm(p):
    return os.path.normcase(os.path.normpath(os.path.abspath(p)))


def is_inside(child, parent):
    child, parent = norm(child), norm(parent)
    return child == parent or child.startswith(parent + os.sep)


def find_ship_root(cwd):
    """Walk up from cwd to the `_THE SHIP` directory. None if not under it."""
    cur = os.path.abspath(cwd)
    while True:
        if os.path.basename(cur) == SHIP_DIR_NAME:
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return None
        cur = parent


def deny(reason):
    json.dump({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }, sys.stdout)
    sys.exit(0)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)          # unreadable payload is not a block

    cwd = data.get("cwd") or os.getcwd()
    ship_root = find_ship_root(cwd)
    if ship_root is None:
        sys.exit(0)          # not a Ship session -- no fence applies

    repo_root = os.path.dirname(ship_root)
    engine = os.path.join(repo_root, ENGINE_DIR_NAME)
    fence_self = os.path.join(ship_root, ".claude")

    tool = data.get("tool_name", "")
    ti = data.get("tool_input") or {}

    # --- Bash: inspect the command text, not a path field ---------------
    if tool == "Bash":
        cmd = str(ti.get("command", ""))
        low = cmd.lower()
        if ENGINE_DIR_NAME.lower() in low or "vast unknown" in low:
            deny(
                "FENCE (Ship). This command names `%s`. The Ship may not reach "
                "the engine's files -- only its MCP tools, if one is "
                "registered. Engine work happens from the repo root, in a "
                "different session. Do not rewrite the command to get past "
                "this; report the block." % ENGINE_DIR_NAME
            )
        if ".claude" in low and ("ship_fence" in low or "settings.json" in low):
            deny(
                "FENCE (Ship, self-protection). This command targets the "
                "Ship's own hook configuration. The fenced party does not edit "
                "its own fence. Change it from the repo root."
            )
        sys.exit(0)

    # --- Everything else: check the path-bearing fields ------------------
    candidates = []
    for key in PATH_KEYS:
        v = ti.get(key)
        if isinstance(v, str) and v:
            candidates.append(v)

    # Glob/Grep can also smuggle the folder name through the pattern.
    pat = ti.get("pattern")
    if isinstance(pat, str) and ENGINE_DIR_NAME.lower() in pat.lower():
        deny(
            "FENCE (Ship). This pattern names `%s`. The Ship may not search "
            "the engine's files." % ENGINE_DIR_NAME
        )

    for c in candidates:
        target = c if os.path.isabs(c) else os.path.join(cwd, c)
        if is_inside(target, engine):
            deny(
                "FENCE (Ship). `%s` is inside `%s`. The Ship may not read or "
                "write the engine's files -- only call its MCP tools, if one "
                "is registered. Root CLAUDE.md's 'no fences' section applies "
                "to a session started at the repo root, not to this one. "
                "Report the block; do not route around it." % (c, ENGINE_DIR_NAME)
            )
        if is_inside(target, fence_self):
            deny(
                "FENCE (Ship, self-protection). `%s` is the Ship's own hook "
                "configuration. The fenced party does not edit its own fence. "
                "Change it from the repo root." % c
            )

    sys.exit(0)


if __name__ == "__main__":
    main()
