# Questions for the operator

2026-08-18 — end of the session that built the engine skeleton, gave the loop
its terminal verbs, and launched Run 002 into the Crash Sites.

Grouped by what they block, hardest blockers first. Answer inside the fences —
an empty fence is a legal answer, it means "deferred," and deferred is honest.

## A. Blocking the Run 002 world (The Guy needs a world to escape)

**1. Where does hidden world content live so you can't read it?**
The repo is readable by you, so the fog has to be enforced somewhere specific.
Options with different costs: a gitignored file (invisible to the future cheat
detector — tension with .gitignore-as-ontology), committed-but-pledged (fog by
discipline), generated fresh at server boot from a committed seed (you can read
the seed but not the world), or something you'd rather invent. This is Debris
decision 01, sharpened by a real run now waiting on it.

```
Well, can't the object spawn into the vault at the time of the discovery? Can't you have a discovery trigger in the MCP server, and once observed you create the file in the vault?
```

**2. What fields must a thing in The Guy's world have?**
Debris decision 02 — now the single last blocker before cartridge generation.
The engine's placeholder schema is `{objects: [{id}]}`. Even three or four
fields unblock the run; the enumeration is yours.

```
This is part of the world building. I don't know yet. Let's start with 
Name: <Name Of File or Folder>
Visible: (Yes | No ) -- revealed to operator or note
First Appearance: <Run-NNN>
Version: <1>
```

**3. How free is generation?**
Your redline dropped object budgets, verb budgets, and surprise license from
the coordinates schema. For an Easy/Quick run: roughly how many things may I
invent, may the world add new tools at all, and what must be disclosed to you
up front versus legitimately hidden?

```
Right now we are just testing the mechanics, we can fine tine stuff like that once we have a working concept of what this looks like
```

**4. What is the generation step, mechanically?**
A skill I run in the terminal (a third verb in the loop), code behind the MCP
server, or a one-off for this run? The Debris provenance mechanic — verbatim
prompt attached in git at generation time — rides on this choice, and whether
`UserPromptSubmit` exposes prompt text is still unverified.

```
I don't know what you mean
```

**5. What does "The Guy gets out of the ship" mean, observably?**
The win condition should be falsifiable like a rollout: what does the terminal
show at the moment he is out?

```
The Guy/ is git moved from /_THE SHIP/ to /  
```

## B. Blocking the fences

**6. Is the fence repo-wide or world-only?**
Debris decision 05, unchanged and still blocking every hook matcher. Repo-wide
means you never hand-edit anything again, including notes; world-only is
reasonable but keeps Obsidian a free-typing zone.

```
Too early for this decision
```

**7. Hook build order.**
PostToolUse auto-commit, PreToolUse fast feedback, pre-commit backstop — none
exist yet. Build them now, or let Run 002 run fenceless to prove the loop by
hand first?

```
Run fenceless for now
```

**8. The Obsidian Sync third-writer problem.**
Unsolved since Debris Protocol, and now live: Instrument Panel forms are inside
the vault, so a phone edit arrives looking exactly like a hand-edit. Excluded
folder? Sync off during runs? Accept and whitelist sync artifacts? This must be
answered before any cheat detector exists, or it will accuse you falsely.

```
If I'm at the Desktop it's always a hand edit. I will try to limit it to /Distress Beacon/ and C:\Users\alder\Desktop\Factor-AI\_THE SHIP\Hitchhiker's Guide\Instruction Manual
```

**9. What does processing emit?**
Debris decision 04: if processing consumes the form and frees the slot, the
loop is fill-and-clear — a chore. If output is itself an item occupying space
downstream, there's factory pressure and a reason for belts. Decides what the
crate even is.

```
A crate, if it makes it into production, is a folder, with only one type of file allowed (it's acceptance criteria must be paired with it's name on a new document -- I don't know where or what this would be yet. And each crate has a max supply, also on that document. So a preuse write tool in that crate must first check the inventory sheet, look up its max limit and approved cargo, and either confirm or deny write.)
```

**10. Crate size, and is there a scrap verb?**
Starting slot count sets difficulty; if processing is the only way to free a
slot, an unfillable form is a dead slot forever.

```
only processing
```

**11. Does the prose budget grow?**
Doubles per tier (expressiveness is earned) or never grows (you only ever get
more keys). Debris called the second more brutal and more interesting; still
your call.

```
don't know yet
```

## C. Schema and registry housekeeping

**12. Where does a World Objective get defined?**
Your own TODO from the schema body: "saved somewhere so that just the variable
alone conveys the entire meaning." The Guy is currently defined inline in the
002 form — which the next chart-course will archive into the Atlas.

```
C:\Users\alder\Desktop\Factor-AI\_THE SHIP\Hitchhiker's Guide\Schema here for now
```

**13. What does `Version` mean on a spawned instance?**
chart-course copies the master verbatim, so instances now carry `Version: 2` —
which reads as "spawned from template v2." Intended? Keep the key name, or
rename on instances to avoid ambiguity with a future per-instance version?

```
intended, the master for this template will version over time
```

**14. Define the other four Lengths.**
Only Quick has a definition. Short / Normal / Long / Epic — and in what unit?
(Rollouts, presumably, per your own hours-vs-rollouts ruling.)

```
Don't know yet, let's see what quick looks like
```

**15. Easy difficulty, concretely for Run 002.**
"Purposeful friction … infrequently" — roughly what cadence and kind? One
staged friction event this run? Zero? Assistant's discretion?

```
just try something out, i have no idea what to expect
```

## D. Meta

**16. Did the engine survive your restart?**
Untested from my side: after restarting Claude Code you should have been
prompted to approve `.mcp.json`, and the `scan` tool should be callable. Was
it? If not, that's a bug I need to see.

```
i haven't started new session yet
```

**17. Science the skill-pickup contradiction?**
Live pickup from repo-root `.claude/skills/` worked twice this session — the
exact mechanism that failed in Session 003, with no explanation for the
difference. Capture now as a science entry, or wait for a third data point?

```
Probably because i either softened the fence or changed the output folder -- not sure why it failed before
```

**18. Where does this document live?**
It's in scratch until you name its home in the vault — and once answered, I'd
argue the filled copy deserves a commit: these are design decisions, and the
ledger should carry them.

```
C:\Users\alder\Desktop\Factor-AI\_THE SHIP\Fireproof Safe\Operator Inbox\Archived Intake Forms
```
