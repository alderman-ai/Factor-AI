---
name: obsidian-sync
description: Force a sync of the local vault through Obsidian Sync using the headless `ob` CLI on the operator's desktop machine. Hard-halts unless running in a local CLI Claude Code session on that machine — never in a cloud/web session. Triggers on - /obsidian-sync, "force a sync", "obsidian sync", "sync obsidian now".
---

# /obsidian-sync — force a headless vault sync (local machine only)

Runs a one-shot Obsidian Sync over the vault using `ob`, the headless Obsidian client
([`obsidian-headless`](https://github.com/obsidianmd/obsidian-headless), installed globally at
`C:\Users\alder\AppData\Roaming\npm\ob.ps1`). It pushes local vault changes up to Obsidian Sync
(and pulls remote ones down) without the desktop app ever opening.

Everything below runs through the **PowerShell** tool. `ob` is a `.ps1` script — it is not usable
from the Bash tool.

## 0 · HALT — environment guard (run first, always)

This skill only works in a **CLI Claude Code session running on the operator's local desktop**
(`DESKTOP-91IG6RH`, user `alder`, Windows). Cloud sessions (claude.ai/code, remote sandboxes,
`--cloud` launches) run in a Linux VM that has neither the `ob` install, the Obsidian login
session, nor the real vault — a sync attempt there is at best a no-op and at worst runs against a
stale uploaded copy of the vault.

There is no documented env var that flags "cloud session", so verify ground truth instead. Run:

```powershell
$local = ($env:OS -eq 'Windows_NT') -and
         ($env:COMPUTERNAME -eq 'DESKTOP-91IG6RH') -and
         (Test-Path 'C:\Users\alder\AppData\Roaming\npm\ob.ps1') -and
         (Test-Path 'C:\Users\alder\Desktop\Factor-AI\.obsidian')
Write-Output "local=$local"
```

- **`local=True`** → proceed.
- **Anything else — `False`, an error, or the PowerShell tool itself unavailable** (cloud sessions
  are Linux; no PowerShell is itself the tell) → **halt immediately.** Do not improvise a
  workaround, do not install `ob`, do not touch the vault. Tell the operator: this session is not
  running on their desktop, and /obsidian-sync must be run from a local CLI Claude Code session on
  DESKTOP-91IG6RH.

## 1 · Resolve the target vault

Default target is **this vault**: `C:\Users\alder\Desktop\Factor-AI`. If the operator names a
different vault or path, resolve it via `ob sync-list-local --json` (returns
`{vaults:[{id,path,host}]}`) and match the name against each `path`'s leaf folder. One match →
use it. Zero or several → stop and show the list rather than guessing.

Always pass `--path "<absolute path>"` explicitly — never rely on `ob`'s implicit cwd default —
and quote every path (the vault names contain spaces).

## 2 · Preflight

```powershell
ob sync-status --path "<target>" --json
```

Read the result, don't just check the exit:

- **JSON with `vaultId` / `vaultName`** → linked; proceed. Note `vaultName` for the summary.
- **Error or no configuration** → the vault has never been connected to Sync. **Stop.** Do not run
  `sync-setup` — it creates or claims a remote vault and needs the operator's end-to-end
  encryption password, which is theirs to type, not yours to handle. Report the situation and
  offer the exact `ob sync-setup` command for them to run themselves.

## 3 · Force the sync

```powershell
ob sync --path "<absolute vault path>"; Write-Output "exit=$LASTEXITCODE"
```

`ob` reports failure through the exit code — a non-zero exit with quiet output is a real failure,
not a no-op.

**If it fails on authentication** (not logged in, expired session, MFA), stop and tell the
operator to run login themselves in this session:

> Type: `! ob login`

`ob login` prompts interactively for email, password, and MFA. The PowerShell tool is
non-interactive with no stdin — you cannot answer those prompts. The `!` prefix runs it in the
operator's own terminal where they can. Never pass `--password` or `--mfa` on their behalf.

## 4 · Report

One or two plain sentences: name the vault, say whether anything moved, and where it went. If `ob`
printed a file count or a conflict, surface it. A silent clean exit means "already up to date" —
say that rather than implying work happened.

## Hard rules

- **The §0 guard is not skippable**, even if the operator's request is urgent. If it fails, the
  answer is "run this from the desktop", not a workaround.
- **Never `sync-setup`, `sync-config`, `sync-unlink`, `sync-create-remote`, or any `publish-*`
  command.** This skill syncs already-linked vaults only; anything that creates, reconfigures, or
  disconnects a remote is the operator's deliberate call — offer the command, don't run it.
- **Other vaults are named, never discovered.** The project fence still holds: don't scan the
  Desktop for vaults or read inside another vault — hand the path to `ob` and nothing more.
- **One sync per invocation, no retry loops.** Two failures → stop and report; failing syncs mean
  auth or network, and neither is fixed by hammering.
- **Sync is bidirectional.** It can pull remote edits down into the working tree, not just push
  local ones up. If `ob` reports conflicts or unexpected incoming changes, say so prominently.
- **`--continuous` only when explicitly asked**, launched with `run_in_background: true` (in the
  foreground it blocks until the tool times out and the sync dies with it), and tell the operator
  it stops when the session ends.
