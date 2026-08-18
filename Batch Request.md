
# Instructions

A batch of fixes handed from operator to assistant in one pass, so approval
happens once over a whole list instead of once per message.

Three blocks per slot, and each has exactly one author:

| Block | Fence tag | Written by | What it is |
|---|---|---|---|
| `R<N>` | `<operator_request>` | Operator | The request. What is wrong, or what should change. |
| `P<N>` | `<assistant_proposal>` | Assistant | The proposed plan for that request. Never the work itself. |
| `A<N>` | `<operator_approval>` | Operator | The verdict. One checkbox, plus notes in the fence. |

Each tag opens the block and closes it with a slash: `</assistant_proposal>`.
The tags are how a block is found. Do not rename one in a live batch.

## The cycle

**Pass 1 — operator fills the `R` fences.**
Fill as many of the ten slots as this batch needs. Leave `P` and `A` alone.

**Pass 2 — assistant proposes. EXECUTES NOTHING.**
- Delete every slot whose `R` fence is empty.
- Write a plan into every remaining `P` fence.
- Read, search, and inspect as much as needed to propose well. Change no file.
  Run no command that writes. This pass produces a proposal and nothing else.

**Pass 3 — operator rules on each slot.**
Tick exactly one box per slot. `ADJUST` and `RETRY` require notes in the fence
below the boxes; `APPROVED`, `APPROVED (Subagent)`, and `DEFER` do not.

**Pass 4 — assistant acts, in this order:**
1. **Every `RETRY` first.** Regenerate those `P` blocks against the operator's
   notes. A regenerated proposal is still only a proposal — it goes back for
   approval, it does not execute in this pass.
2. **Then `APPROVED` and `ADJUST`.** Execute them.
3. **Then `DEFER`.** Do nothing. Leave the slot intact for a later pass.

Report per slot what actually happened. A slot that was attempted and failed is
reported as failed, with the real output.

## The two approve boxes

`APPROVED: Execute` runs the slot in the main session, with the whole
conversation as context.

`APPROVED (Subagent)` runs it in a spawned subagent instead. Write a model name
between the backticks — `opus`, `sonnet`, `haiku` — or leave the placeholder
untouched to accept the default.

Choosing subagent has consequences the assistant must respect:

- **The subagent does not inherit this conversation.** The main session must
  hand it everything it needs — paths, constraints, the fences — inside its
  prompt. If the slot cannot be made self-contained, say so rather than
  dispatching a subagent that will guess.
- **The main session reports the result.** It does not paste the subagent's
  transcript. It says what the subagent did, what changed, and what failed.
- **Fences bind the subagent too.** They are stated in its prompt explicitly,
  never assumed to carry over.

Use it for slots that are wide and read-heavy — sweeps, audits, autopsies —
where the file-by-file output would otherwise flood the main session.

## What a `P` block owes the operator

- **The files it will touch, by path.** Not "the ship's config" — the path.
- **Every assumption it had to make**, called out plainly. If the request did
  not specify a name, a location, or a format, the proposal says which one it
  picked and that it picked it. Approval is the operator's chance to catch a
  guess before it becomes a file, and that only works if guesses are visible.
- **Any dependency on another slot.** If R3 has to land before R7 makes sense,
  P7 says so. The assistant does not silently reorder the batch.
- **Anything it cannot do, and why.** A slot that is blocked says so in the
  proposal rather than failing quietly in Pass 4.

## Fences hold during a batch

Batching creates pressure to make things pass. It does not license it. If
executing a slot trips a hook, a validation refusal, or a guard, stop that slot
and show the operator the exact failure. Do not route around it, retry it
quietly, or pre-edit anything so it will not fire. The other slots continue; the
blocked one reports.

A slot whose request is itself a request to weaken a fence is a proposal
question, not an execution question. Surface it in `P` and let the operator rule
on it.

---

# `R1`

`<operator_request>`
```
(Opus subagent for this) We need a big sweep of all the routing.  we need the system to become more legible. README = what this subfolder is for, INDEX is a routing directory listing contents. INDEX's accrete as new content is added. READMES don't. For example, Ship's Computer Entries don't need to acreet, so readme is fine. Identify list of offenders, missing, wrong type, empty, indexes not fully cateloging contents you don't need to propose a plan on this UNLESS YOU LOOK AT A SUBFOLDER AND DONT KNOW WHAT IT DOES -- that's the only thing I would need from you. Just a list of those
```
`</operator_request>`

## `P1`
`<assistant_proposal>`
```
Opus subagent ran read-only, fence held (`_THE VAST UNKNOWN/` listed, never
opened). 37 directories. No plan proposed, per your instruction.

Headline number before the list: **0 folders have both a README and an INDEX.**
12 routing files exist across 37 folders. 4 are blank, 5 are the wrong type or
stale. **3 do their job.**

Here is the only thing you asked for — the folders it could not figure out.
Seven, each with the question that would unblock it.

1. `_THE SHIP/Fireproof Safe/`
   README is 1 byte. Five children with nothing in common: a lexicon, design
   essays, 20 .ico files, an inbox, an empty templates folder. `SatNav/README`
   already claims the "survives every reset" role, and `_THE SHIP/INDEX.md`
   does not list Fireproof Safe at all.
   Q: what property puts something HERE instead of `SatNav/Knowledge Base/` or
   `Hitchhiker's Guide/`? Survives a reset, operator-authored, or unfiled?

2. `_THE SHIP/Fireproof Safe/Ancient Artifacts/`
   Holds `Lexicon.md`, `Science Ore Patch.md`, `pumpjack.py`. The name says
   graveyard; the root README points readers here for `Lexicon.md` as live
   canon. Also `pumpjack.py` exists here AND at `Instrument Panel/Ignition
   Codes/pumpjack.py`.
   Q: archive of retired things, or the canon store? And which pumpjack is live?

3. `_THE SHIP/Fireproof Safe/Operator Inbox/`
   Zero files. One subfolder, `Archived Intake Forms/`. An inbox containing
   only an archive.
   Q: where does a LIVE unanswered form sit before archiving? `Batch Request.md`
   is a live operator form and it sits at the repo root, not here.

4. `_THE SHIP/Fireproof Safe/Operator Inbox/Archived Intake Forms/`
   Contains exactly one file: `Open Questions.md`. Something named "Open" inside
   something named "Archived".
   Q: does a form land here when ANSWERED, or when retired regardless of outcome?

5. `_THE SHIP/Fireproof Safe/Root level templates/`
   Empty. Its only mention anywhere is R8 of this very file.
   Q: "root level" = templates for repo-root files, or the top-level store of all
   templates? Reading two collides with `Hitchhiker's Guide/Templates/` and
   `Hitchhiker's Guide/Schema/`.

6. `_THE SHIP/Hitchhiker's Guide/Templates/`
   You renamed this twice DURING the survey — `Untitled/` to `YAML Front
   headers/` to `Templates/`. Contains only an INDEX describing subfolders that
   do not exist. Those two names mean different things: a frontmatter block is
   not a whole document.
   Q: what is a "template" here, and what separates it from `Schema/` (which
   holds `New World Coordinates.md`, itself a template) and from #5 above?

7. `_THE SHIP/Hitchhiker's Guide/Instruction Manual/`
   Boundary case, included so you can kill it in one line. README says "canon
   about game design, future build directions, lexicon, goals". All three of
   those live elsewhere: lexicon in Ancient Artifacts, build direction in
   `Game Improvement/`, rules in `Ontology/`. Folder is empty.
   Q: what would file here that would not go to `Ontology/` or `Game
   Improvement/`?

--- HELD AS THE EXECUTION WORKLIST (not asking you to read it now) ---

The offender inventory came back complete and I am holding it. Rough shape:
14 folders MISSING both files, 4 EMPTY routing files, 3 WRONG TYPE, 2 STALE.
Notable ones you may want to know about before ruling:

  - `_THE SHIP/INDEX.md` omits Fireproof Safe, Hitchhiker's Guide, Instrument
    Panel, and SatNav — four of its six children.
  - Root `README.md` points at `Lexicon.md` in the wrong folder and at a
    `Template Schema/` that does not exist under any name.
  - `Distress Beacon/README.md` cuts off mid-sentence: "For now, "
  - `SatNav/README.md` calls the intake folder "inbox"; on disk it is
    `Incoming Transmissions/`.
  - `Instrument Panel/INDEX.md` is a purpose statement routing to nothing —
    i.e. a README wearing an INDEX's name.

One routing decision the sweep surfaced that is NOT mine to make:
`Instrument Panel/chart-course.md` and `enter-hyperspeed.md` are byte-identical
copies of the two `.claude/skills/*/SKILL.md` files. See P5c — same decision,
ruled once.
```
`</assistant_proposal>`

### `A1`

`<operator_approval>`
- [ ] APPROVED: Execute
- [ ] APPROVED (Subagent): Delegate to a `(empty=default)` Model
- [x] ADJUST: Adjust accordingly to instructions in fence below, but execute
- [ ] RETRY: Propose a new plan based on the in instructions in fence below (regenerate proposal)
- [ ] DEFER: We will deal with this later

```
1.  
   This is the Operators Misc collection of things that are not for the assistant.

2. `_
   Q: archive of retired things, or the canon store? And which pumpjack is live?
   
   Things that I want to preserve as inspiration for future runs

2. `_
   
   A place, for now, to output input docs meant for me to fill out

2. `_

after 3. they go here to 4.

4. `_
   
   Batch request will be the first of this file type

5. `_
   
   Templates will be a big part of this system and im still getting my head around how and where to create them. here for now, each a subfolder, not single file, will contain previous versions and changelogs

6. `_
   
   Leave this one alone for now.
```
`</operator_approval>`

---

# `R2`

`<operator_request>`
```
The whole mid RUN ritual is incomplete. We need a new skill to end the RUN and the MCP server it's connected to. We need to decide which parts of the the-vast-unknown is saved when a run ends. We need to decide what a ship does when it boots without a running server. We need to decide if the mid run ritual happens at cwd root or cwd the ship. All task should have an 'owner' and all of the skills associated with those tasks whould be saved at the local level of that cwd
```
`</operator_request>`

## `P2`
`<assistant_proposal>`
```
R2 AND R3 ARE THE SAME SKILL. R2 asks for "a new skill to end the RUN and the
MCP server it's connected to." R3 specifies that skill in detail. I am not
building two. I propose R2 carries the four DECISIONS and the ownership rule,
and R3 carries the SKILL and the autopsy. If you disagree, RETRY this slot and
say which one owns the skill.

So P2 = four decisions only. Each needs a ruling from you. I recommend, I do
not decide.

--- DECISION 1: what of `the-vast-unknown` survives a run's end ---

This decision already has a home. `File Move Ritual.md` has an *Undecided*
table with two rows that are exactly this question:

  `_THE VAST UNKNOWN/Crash Sites/New World NNN.json`  — archive, delete, or leave?
  `_THE VAST UNKNOWN/` itself — does a new engine replace in place, or land beside?

Proposal: do NOT write a new document. Fill those two rows. A second document
covering the same artifacts is how the two chart-course copies happened.

My recommendation for row 1: the crash-site JSON is the engine's copy of a form
whose master is already archived forever in `Atlas of Worlds/`. It is derived,
not source. Let it die with the world. Recommendation for row 2: a new engine
lands in place, because the old one is already gitignored and untracked — but
this one I hold weakly and it may depend on what the next engine is.

--- DECISION 2: what the Ship does booting with no server ---

Right now `_THE SHIP/CLAUDE.md` hardcodes the answer in prose: a section titled
"the-vast-unknown (MCP) — UNPLUGGED" describing the current absence. That prose
must be hand-rewritten every time an engine connects or dies, and its own last
line admits the failure mode: "A section describing an engine that isn't
connected is the exact failure e7b7b1a was written to end." It is presently
correct and will silently rot the moment an engine lands.

Proposal: replace the prose with two defined boot states the Ship checks rather
than asserts.

  ENGINE PRESENT  — `.mcp.json` has a server AND its tool answers.
                    Report the sweep, pick up the run.
  ENGINE ABSENT   — `.mcp.json` is empty, or the tool is missing.
                    Say so plainly, read `_EJECT BUTTON/`, stop.
                    Do not hunt for it. Absence is a state, not a fault.

The distinction that matters: *registered but not answering* is a real fault and
must report loudly. *Not registered* is between-runs and is normal. Today the
Ship cannot tell those apart, which is exactly how run 002 opened — commit
b460417, "First contact fails: the engine was never started, not broken."

--- DECISION 3: does the mid-run ritual run at root cwd or Ship cwd ---

This is R6's whole question. I am not answering it twice. See P6. Rule on it
there and I will apply the answer here.

--- DECISION 4: task owners, skills stored at the owner's cwd ---

Current state: all five skills live at `./.claude/skills/` — repo root, no
exceptions. There is no `_THE SHIP/.claude/` at all. So the rule you are asking
for is currently violated by everything.

Proposal: every task gets a named owner, and its skill lives under that owner's
`.claude/skills/`. Owner is decided by what the task's *authority* is over, not
where its files happen to sit.

  ROOT owns    — git, tags, the ledger, .mcp.json, anything public-facing
  SHIP owns    — run rituals, the Instrument Panel, the forms, the reports
  ENGINE owns  — the world; unreachable from either, by fence

Consequence you must accept before approving: **a session at repo root will not
see Ship-owned skills, and a Ship session will not see root-owned ones.** That
is the mechanism, not a side effect — it makes cwd load-bearing instead of
advisory, which is the point. But it means `/chart-course` typed in the wrong
directory silently does not exist rather than erroring. See P6 for the three
ways to handle that; I recommend a loud stub.

Applying this rule to today's five skills is mechanical once you rule on R6, so
I have not pre-assigned them here.

--- WHAT I WILL NOT DO IN THIS SLOT ---

"End the MCP server" — I cannot specify the server-side half. `server.py`,
`cartridge.json` and `schema.json` are behind the fence and I have not read
them, deliberately. What a shutdown must do to engine internals has to come
from a session with the engine as cwd. I will specify only the Ship's side:
deregister from `.mcp.json`, confirm the tool no longer answers, record it.
```
`</assistant_proposal>`

### `A2`

`<operator_approval>`
- [ ] APPROVED: Execute
- [ ] APPROVED (Subagent): Delegate to a `(empty=default)` Model
- [x] ADJUST: Adjust accordingly to instructions in fence below, but execute
- [ ] RETRY: Propose a new plan based on the in instructions in fence below (regenerate proposal)
- [ ] DEFER: We will deal with this later

```
the fence is not meant for you! 1st, make it clear somewhere only for cwd root that you don't have any fences. It's your main purpose to not have the fences the child folders have, so complete the entire request please
```
`</operator_approval>`

---

# `R3`

`<operator_request>`
```
(OPus subagent) RUN 002 was broken. Do an atopsy. Then clarify the ritual
new skill ends the run from ship cwd -- produces assistant report (see eject button contents). Also ends all appropriate parts of the MCP server. The run is finished, resets the ship to it's pre-run condition (i'm deleting the guy myself this time) and triggers the biters attack commit with the assistant report being summarized in the toll commit. HOWEVER the new ship different day doesn't start yet. There's a clean up period that will be summarized as part of the new day commit. Before new day, chart course is called, which also triggers the move files ritual, cleaning up everything (this is where the removal of the guy or anything ADDED BY THE RUN -- if i stray add a file, i dont want it deleted. Basically I want anything added to the ship, or world beyond the ship to get a special indicator that it's a target for deletion at this part of the ritual)
then git ritual begins. T
```
`</operator_request>`

## `P3`
`<assistant_proposal>`
```
Two deliverables: the autopsy, and the marker mechanism. The marker is the hard
part and it is the only thing here I need you to rule on before I build.

--- PART A: the autopsy (Opus subagent, as you asked) ---

Scope: what actually went wrong across run 002, not just the Cryobay desync
already filed in RUN-002-Assistant-Report.md. Source material is the commit
range `RUN_001/BITER_ATTACK!!..RUN_002/BITER_ATTACK!!` plus the ship-side files.
The fence holds — `_THE VAST UNKNOWN/` filenames only, no file inside opened.
The existing report proved the desync was fully diagnosable from outside, so
this costs nothing.

Two findings I already have and will hand it as starting points, not
conclusions:

  1. Run 002 has NO opening tag. `RUN_001/BITER_ATTACK!!` (2121230) and
     `RUN_002/BITER_ATTACK!!` (205ec1b) both exist. `RUN_002/SAME_SHIP_
     DIFFERENT_DAY` was never planted. Every range query in Commit Ritual.md's
     navigation table is unrunnable against run 002. The candidate landing
     commit is 7fb5681. Your new chart-course already names this as the cause:
     "Charting a course out of a run that was never closed is exactly how run
     002 launched." The autopsy should confirm or break that.

  2. The Ship ran on the planet's Python. Both loop skills invoked
     `_THE VAST UNKNOWN/.venv/Scripts/python.exe` — durable tooling depending
     on the disposable world. You have already fixed this in chart-course
     (plain `python` now); enter-hyperspeed still carries the dead path, in
     both of its two copies.

Output: `_THE SHIP/_EJECT BUTTON/RUN-002-Autopsy.md`. Filename is a guess —
correct it if you want it elsewhere or named differently. It is deliberately
NOT the same file as RUN-002-Assistant-Report.md: that one is the toll, filed
before the scuttle by the run that died. An autopsy is written after, with
hindsight the run did not have. Merging them would rewrite history.

--- PART B: the marker mechanism (THE DECISION) ---

Your requirement, restated so you can check I have it: at the file-move stage,
everything the RUN created gets deleted; anything YOU created stays, even if
you added it randomly mid-run. So deletion must key off provenance, not path.

File Move Ritual.md already names why no path rule can work: "the Ship
currently mixes durable and disposable in one folder, so no path-based rule can
tell them apart."

Four ways to mark provenance:

  (i)   FRONTMATTER KEY — `disposable: RUN-002` in each file's header.
        Dies on anything without frontmatter. `The Guy/` is a FOLDER. Rejected.

  (ii)  MANIFEST — one ledger per run, e.g.
        `_THE SHIP/_EJECT BUTTON/RUN-NNN-Manifest.md`. Whatever creates a thing
        appends its path. At file-move, the ritual deletes exactly what is on
        the manifest and nothing else.

  (iii) QUARANTINE FOLDER — everything a run creates lands under one disposable
        directory. Cleanest rule, but it requires the spawn destination to be
        decided first, and that is open engine work (item 3 of the run-002
        report: "Spawn destination is unspecified"). Cannot be built today.

  (iv)  SIDECAR MARKER — a `.disposable` file dropped inside each run-created
        folder. Works for folders, but litters, and a file the run creates
        loose in an existing directory has nowhere to put its sidecar.

RECOMMENDATION: (ii), the manifest — for one reason above the others. **It
fails safe in exactly the direction you asked for.** Anything not on the
manifest is never touched, so your stray file survives by DEFAULT rather than
by being correctly classified. (i), (iii) and (iv) all fail the other way: an
unmarked run artifact is invisible and silently accumulates, or worse, a rule
gets broadened to catch it and starts eating your strays.

The manifest also carries which run made each thing, which none of the others
do, and it is auditable — you can read it before the deletion happens.

Its real cost, stated plainly: the manifest is only as true as the things
writing to it. A run artifact created by something that does not register gets
orphaned — it survives the cleanup and lives forever. That is the failure mode
you are buying, and it is the safe one, but it is not nothing. Mitigation is a
reconciliation check at file-move time that reports anything under the Ship
newer than the run's opening tag and NOT on the manifest, so orphans surface
instead of hiding. It reports; it never auto-deletes.

--- PART C: the phase order, as I read it back to you ---

Confirm this is right; a lot depends on it. Note this splits run-end from
run-start with a repair gap in between, which is the thing run 002 never had.

   1  END SKILL, from Ship cwd     assistant report; deregister the engine;
                                   reset Ship to pre-run condition
   2  TOLL COMMIT                  report summarized into the message
   3  BITER_ATTACK!! tag           the run is now dead
   4  >>> REPAIR PERIOD <<<        open-ended. No tag. Fixes land here.
                                   This is step 3 of your chart-course table,
                                   currently marked "not yet defined".
   5  /chart-course                triggers File Move Ritual: deletes what the
                                   manifest lists, stamps the blank form
   6  YOU fill the form            Obsidian, alone
   7  NEW DAY COMMIT               summarizes repair + cleanup
   8  SAME_SHIP_DIFFERENT_DAY tag  the next run is now alive

You said you are deleting The Guy yourself this time — already done, it is
staged as deleted right now. So step 5 has no live case to exercise on this
transition. I would rather that than invent one.

Skill name and location: not proposed. Naming is yours. It needs a name and,
per P2 decision 4, a home — presumably `_THE SHIP/.claude/skills/<name>/`,
which does not exist yet.
```
`</assistant_proposal>`

### `A3`

`<operator_approval>`
- [ ] APPROVED: Execute
- [ ] APPROVED (Subagent): Delegate to a `(empty=default)` Model
- [x] ADJUST: Adjust accordingly to instructions in fence below, but execute
- [ ] RETRY: Propose a new plan based on the in instructions in fence below (regenerate proposal)
- [ ] DEFER: We will deal with this later

```
Execute everything not dealing with ship-deletion subject as planned. Decision: everything in ship is 100% durable and nothing temporary will spawn there.

This is unescessarily complicated. We will have a full that nothing spawns in the ship. At launch of server, two things must be included AND visible at root. /The Guy/ and /C-THE SHIP-10  <- C = crate ; 10 = Crate capacity (number of things it can hold). Any interactions between guy and ship happen actually between guy and crate / ship and crate (ship add item to crate, then guy removes item from crate)
```
`</operator_approval>`

---

# `R4`

`<operator_request>`
```
Add a subagent button to this template for if I want you to solve this main session or if I want you to spawn a subagent. see a4
```
`</operator_request>`

## `P4`
`<assistant_proposal>`
```
EXECUTED. You had already ticked A4 before handing me the file, so I treated
that as approval rather than waiting a pass.

What changed, in this file only:
  - `APPROVED (Subagent)` added to all eight approval blocks, in the position
    and wording you demonstrated in A4.
  - Instructions gained a section, "The two approve boxes", covering what
    picking subagent commits me to: the subagent inherits none of this
    conversation so the slot must be self-contained or I say so instead of
    dispatching a guesser; I report what it did rather than pasting its
    transcript; and fences get restated in its prompt rather than assumed.

Nothing outside this file was touched.
```
`</assistant_proposal>`

### `A4`

`<operator_approval>`
- [x] APPROVED: Execute
- [ ] APPROVED (Subagent): Delegate to a `(empty=default)` Model
- [ ] ADJUST: Adjust accordingly to instructions in fence below, but execute
- [ ] RETRY: Propose a new plan based on the in instructions in fence below (regenerate proposal)
- [ ] DEFER: We will deal with this later

```

```
`</operator_approval>`

---

# `R5`

`<operator_request>`
```
Let's do a DRY sweep. There's stuff repeated everywhere. Operator improvement goals. I think a lot of root claude.md should be moved to separate files as a lazy loaded reading list.
```
`</operator_request>`

## `P5`
`<assistant_proposal>`
```
--- CONFIRMED DUPLICATION (verified, not suspected) ---

1. `_THE SHIP/Instrument Panel/chart-course.md` is BYTE-IDENTICAL to
   `.claude/skills/chart-course/SKILL.md`. Same for `enter-hyperspeed.md` and
   its SKILL.md. Two copies, hand-synced, and the drift has already started:
   chart-course got updated in both, enter-hyperspeed still names the dead
   `_THE VAST UNKNOWN/.venv/` interpreter in both. That venv is inside the
   scuttled, gitignored planet.

2. `pumpjack.py` exists twice: `Fireproof Safe/Ancient Artifacts/pumpjack.py`
   and `Instrument Panel/Ignition Codes/pumpjack.py`. Which is live is one of
   the seven questions in P1.

3. "Operator improvement goals" appears in root `CLAUDE.md` and again in
   `README.md` (line 44).

--- ROOT CLAUDE.md: 120 LINES, MOST OF IT NOT NEEDED EVERY TURN ---

Split by one test: does this change what I do THIS TURN, or is it background I
should fetch when relevant?

  STAYS (auto-loaded, every session):
    How the assistant should behave  — governs every turn
    Assistant behaviors to avoid     — governs every turn
    Friction is the product          — the fence rule
    Commit narrative rule            — governs every commit
    Architecture overview            — 3 lines, needed for orientation

  MOVES (on-demand, fetched when relevant):
    The purpose of this project
    Key long-term output
    Directional goal
    Operator improvement goals
    Key gameplay loop
    Ontology of this section + TL;DR
    Building in public / publishing format

That is roughly 120 lines down to ~40. Your own global preference is "on-demand
beats auto-loaded... bias conservative on auto-injection," so this is the
direction you already set.

--- WHAT I NEED FROM YOU ---

  a) WHERE the moved sections live. Candidate:
     `_THE SHIP/Hitchhiker's Guide/Ontology/`, which exists and is plausibly
     for exactly this — but note P1 question 7 flags that Ontology, Instruction
     Manual, and Game Improvement have overlapping unstated scopes, so this
     answer may depend on ruling that first. I am NOT choosing.

  b) WHAT REPLACES THEM in CLAUDE.md. A reading list only works if the pointer
     says enough that I know when to follow it. Proposal: a table of one line
     per file — path plus the trigger condition ("read before proposing a new
     loop stage"), not a summary. A summary is just the duplication again.

  c) WHICH COPY WINS for chart-course / enter-hyperspeed. `.claude/skills/`
     is the one Claude Code actually loads, so the Instrument Panel copies are
     the redundant pair. But `Instrument Panel/INDEX.md` says the folder holds
     "the Ship's starting locally deployed skills and durable scripts between
     runs," which reads like it is meant to be the home. These cannot both be
     true. This is a routing decision, it overlaps R1 and R6, and it is yours.

  d) THE README OVERLAP. README.md is public-facing and CLAUDE.md is
     instructional. Should the README keep its own copy of the improvement
     goals for readers, or point at the extracted file? Duplication is
     sometimes correct for a public README — I will not decide it for you.
```
`</assistant_proposal>`

### `A5`

`<operator_approval>`
- [ ] APPROVED: Execute
- [ ] APPROVED (Subagent): Delegate to a `(empty=default)` Model
- [x] ADJUST: Adjust accordingly to instructions in fence below, but execute
- [ ] RETRY: Propose a new plan based on the in instructions in fence below (regenerate proposal)
- [ ] DEFER: We will deal with this later

```
--- WHAT I NEED FROM YOU ---

  a) WHERE the moved sections live. Candidate:
     `_THE SHIP/Hitchhiker's Guide/Instruction Manual/Purpose of Factor-AI/

  b) WHAT REPLACES THEM in CLAUDE.md. A standard retrieval/routing optimized description of each once you actually add the files there, then write desc
  
  c) WHICH COPY WINS for chart-course / enter-hyperspeed. So, I basically want to be able to see at a glance which skills are available local at each cwd. So replace the Instrument Panel skills with Instrument Panel/Ship Capabilities.md which lists all deployed local skills with a clear desciption of what they do.
     
     

  d) THE README OVERLAP. README.md is public-facing and CLAUDE.md is
     instructional. Should the README keep its own copy of the improvement
     goals for readers, or point at the extracted file? Duplication is
     sometimes correct for a public README — I will not decide it for you.
     
     Duplication ok here
```
`</operator_approval>`

---

# `R6`

`<operator_request>`
```
We need to decide the role of cwd here and cwd at the ship
```
`</operator_request>`

## `P6`

`<assistant_proposal>`
```
SECOND PROPOSAL. Nothing in R6 executed. Your notes changed three things and
opened one question I am answering directly.

--- WHAT YOUR NOTES SETTLED ---

  1. THE SHIP GETS EXACTLY ONE GIT OPERATION. You caught the flaw in my
     version yourself: a report that is written and then handed to root does
     not SNAPSHOT anything. By the time root commits, the File Move Ritual has
     already run and the state the report describes is gone. So the end-run
     skill commits — minimally — before it moves anything.

  2. ROOT REACHES THE ENGINE. Done, executed under R2. Root `CLAUDE.md` now
     opens with a section stating that root is the working directory with no
     fences and that reading the engine from there is sanctioned, not cheating.
     The Ship's `CLAUDE.md` states that the exemption belongs to the directory
     and does not travel to a session that merely read about it.

  3. STUB, WITH AN EXPIRY. Option (b), as you ruled. Your caveat — "once we
     have more components I don't want all of them to have ALL the stubs" — is
     the important half, so I am proposing the retirement trigger now rather
     than discovering the noise later. See the last section.

--- THE REVISED ORDER, AS YOU DICTATED IT ---

Read this back and check it. This is the version I would build to.

   1  /end-run, from Ship cwd    Produces the assistant report. Deregisters
                                 the engine. Reports what root needs to reset
                                 the world.
   2  MINIMAL COMMIT             By the skill, from the Ship. Terse message.
                                 THE ONLY COMMIT THE SHIP EVER MAKES.
                                 Its whole job is to freeze the pre-cleanup
                                 state so the report has something to point at.
   3  FILE MOVE RITUAL           Same skill run. Archives the live form.
   4  STAMP THE BLANK FORM       Same skill run. New World NNN.md onto the
                                 Instrument Panel.
   5  YOU FILL THE FORM          Obsidian, alone.
   6  FORM + ANALYSIS TO ME      Repair period. We clean up between runs
                                 together — exactly what we are doing now.
   7  COMMIT RITUAL              Root. The toll commit, BITER_ATTACK!!, the
                                 new-day commit, SAME_SHIP_DIFFERENT_DAY.
   8  LAUNCH THE SERVER          <-- your open question. Answered below.

Note what this collapses: my previous version had chart-course as a separate
step 5 driving the file move. In yours, steps 2-4 are one skill run. That means
`/chart-course` either becomes the back half of `/end-run` or it disappears.
I have not touched either skill. Rule on it and I will.

One consequence to accept before approving step 2: **the Ship committing at all
breaks the clean "root owns git" line.** I think it is worth it, because the
alternative is a report that describes a state no commit holds — but it means
the invariant is no longer "the Ship never touches git." It is now "the Ship
makes exactly one commit, from exactly one skill, and never tags or pushes."
That is enforceable by a hook; the softer version is not.

--- YOUR OPEN QUESTION: WHERE DOES THE SERVER LAUNCH ---

"here's the problem, launching the server ... where? under root? under ship?"

The reason it feels unanswerable is that the question has two halves that have
been travelling as one. Split them and both halves are easy.

  WHERE THE ENGINE'S FILES ARE EDITED    -> root. Only root. Already ruled.
  WHERE THE ENGINE'S TOOLS ARE CALLED    -> the Ship. That is what play IS.

Claude Code reads `.mcp.json` from the working directory the session started
in. So the answer is mechanical: **`.mcp.json` gets registered in BOTH places**,
and the fence stops being about the engine and starts being about the surface.

  THE FENCE, RESTATED:
  The Ship may call the engine's TOOLS. The Ship may never read the engine's
  FILES. Root may read and write the engine's files. Root is not where play
  happens.

This is a better fence than the one we have, for a reason worth stating: the
current fence forbids the Ship from reading `server.py`, which is a rule about
a filesystem path, so it survives only as long as nobody types the path. The
proposed fence is about what the Ship is ALLOWED TO KNOW — the world through
the tool surface and nothing behind it — which is the actual creative
constraint. The path rule was always a proxy for it.

It also fixes something already written. The Ship's boot check I built under R2
has an ENGINE FAULTED state defined as "registered but the tool does not
answer." That state is unreachable if the Ship can never call a tool. Under
this proposal it is reachable, and the check is real rather than decorative.

  WHAT I NEED FROM YOU: yes or no on dual registration. If no, the Ship cannot
  call `scan` and the boot check loses a state — tell me and I will cut it.

I have NOT touched `.mcp.json`. It is `{"mcpServers": {}}` and stays that way
until an engine exists to register.

--- THE STUB, AND WHEN TO KILL IT ---

Per your ruling. A Ship-owned skill gets a same-named stub at root whose entire
body is the redirect — no instructions, or it becomes the duplication R5 exists
to kill.

    /end-run at root  ->  "This is Ship-owned. cd to _THE SHIP and retry."

Your caveat is the real design constraint: stubs are O(skills x components).
Two components and four skills is fine. Four components is not. So the trigger,
proposed concretely so it is not a judgement call later:

  **When a third working directory appears, the stubs are replaced by one
  skill that reports which cwd owns what.** Not N stubs of one line each — one
  capability page, which we now have the pattern for: `Ship Capabilities.md`
  already exists and already tells a reader where each skill loads from.

Until then, stubs. They are the only option that fails loudly, and a silently
missing command in a project whose stated rule is that friction must be visible
is the wrong failure.

--- WHAT IS STILL BLOCKED BEHIND THIS SLOT ---

Stated so you can see the cost of another RETRY:

  - P2 decision 3 (which cwd runs the mid-run ritual) — waiting on step 2 above.
  - P2 decision 4 (skills stored at their owner's cwd) — waiting on the stub
    rule being live, which needs the skills to actually move.
  - The end-run skill itself — unbuilt. It has no name yet. You called it
    "the end run skill (I forget name)"; it has never had one. Name it and it
    gets built.
  - `_THE SHIP/.claude/` does not exist. Nothing moves until this slot lands.
```
`</assistant_proposal>`

### `A6`

`<operator_approval>`
- [ ] APPROVED: Execute
- [ ] APPROVED (Subagent): Delegate to a `(empty=default)` Model
- [ ] ADJUST: Adjust accordingly to instructions in fence below, but execute
- [x] RETRY: Propose a new plan based on the in instructions in fence below (regenerate proposal)
- [ ] DEFER: We will deal with this later

```
---  RULE ---

/// fine, the end run skill gives a full report that gives Root everything it needs to reset the world. So the order now is /endrunskill, report generated AND also calls (or combines with)  ... but that doesn't work because it doesn't snapshot the state before the file move ritual. Ok, this is the only commit allowed by ship, only through the end run skill (I forget name), it does a quick, minimal comment commit THEN runs the file move ritual and generates form for new RUN. Once form is filled out by me then that + analysis goes to you -- together we clean up anything between runs like now, then all the commit ritual, then ... here's the problem, launching the server ... where? under root? under ship?

  ENGINE owns the world. Unreachable **TO ANYONE BUT ROOT** this is not hacking into a bank. This is not cheating on my SATs. I need some way to access this server because it doesn't work yet
  
  B, add a stub ... for now. Once we have more components I don't want all of them to have ALL the stubs 
```
`</operator_approval>`

---

# `R7`

`<operator_request>`
```
fix this template to change the tags between the middle sections to `<assistant_proposal>` -- see p7
```
`</operator_request>`

## `P7`
`<assistant_proposal>`
```
Agreed, and it was my error — I carried `<assistant_request>` over from your
draft rather than flagging it, then flagged it only after writing the file.

NOT EXECUTED. A7 is unticked and this slot changes the template itself. I am
not stepping over the gate on a slot just because the answer looks obvious;
that is the exact behaviour the gate exists to prevent.

On approval: all eight P blocks get `<assistant_proposal>` / `</assistant_
proposal>`, and the block table in Instructions is updated to match.

ONE CORRECTION TO YOUR DEMONSTRATION. You edited this block to:

    `<assistant_proposal>`      <- opening
    `<assistant_proposal>`      <- closing, missing the slash

Both tags are openers. Every other block in this file closes with `</...>`.
I have left your version untouched above and below this text so you can see it
as you wrote it. I propose the closing tag becomes `</assistant_proposal>`. Say
the word and it goes in; say otherwise and I will match whatever you specify
rather than assume.
```
`</assistant_proposal>`

### `A7`

`<operator_approval>`
- [x] APPROVED: Execute
- [ ] APPROVED (Subagent): Delegate to a `(empty=default)` Model
- [ ] ADJUST: Adjust accordingly to instructions in fence below, but execute
- [ ] RETRY: Propose a new plan based on the in instructions in fence below (regenerate proposal)
- [ ] DEFER: We will deal with this later

```

```
`</operator_approval>`

---

# `R8`

`<operator_request>`
```
Recreate a blank template for this at  C:\Users\alder\Desktop\Factor-AI\_THE SHIP\Fireproof Safe\Root level templates -- after you fix R7 and R4
```
`</operator_request>`

## `P8`
`<assistant_proposal>`
```
BLOCKED ON A7. Your own instruction is "after you fix R7 and R4." R4 is done.
R7 is unticked, so a blank cut today would ship with the wrong tags and need
recutting. Tick A7 and this becomes mechanical.

Destination exists and is empty:
  `_THE SHIP/Fireproof Safe/Root level templates/`

WHAT I NEED: THE FILENAME. Naming is yours, and the folder is empty so there is
no convention to follow. `Batch Request.md` matches the live file at root; if
you want the templates folder to mark its contents as templates the name should
say so. I am not picking.

Also note the survey could not determine what this folder is FOR — it is
question 5 in P1. "Root level templates" reads two ways, and one of them
collides with `Hitchhiker's Guide/Templates/`. You may want to answer that
before I put the first file in it and set the convention by accident.

The blank will carry:
  - the full Instructions section, current as of approval
  - ten empty slots, R1 through R10
  - both approve boxes per slot, per R4
  - `<assistant_proposal>` tags, per R7

One thing this makes real: a template at `Fireproof Safe/Root level templates/`
and a live copy at root is the same two-copies pattern as the chart-course
duplication in R5 — one is the master, one is in use, and they drift. The
difference is that here the drift is intended, because a live batch gets filled
in. Worth stating in the template itself: the Fireproof Safe copy is the
master, the root copy is disposable and gets replaced from the master each
batch. That also answers the question I left open when I first built this file
— what happens to a finished batch. Proposal: a finished batch is a Ship
artifact and should be archived rather than overwritten, but WHERE is yours to
say, and I have not assumed a location.
```
`</assistant_proposal>`

### `A8`

`<operator_approval>`
- [x] APPROVED: Execute
- [ ] APPROVED (Subagent): Delegate to a `(empty=default)` Model
- [ ] ADJUST: Adjust accordingly to instructions in fence below, but execute
- [ ] RETRY: Propose a new plan based on the in instructions in fence below (regenerate proposal)
- [ ] DEFER: We will deal with this later

```

```
`</operator_approval>`
