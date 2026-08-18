# RUN-002 — Autopsy

**What this is.** A post-mortem of run 002, written *after* the scuttle, after
`RUN_002/BITER_ATTACK!!`, and during the repair phase. It has hindsight the toll
did not: the tag is planted, the repair commits exist, and — decisively — the
fence around `_THE VAST UNKNOWN/` has been lifted for root-cwd sessions, so the
engine source is readable for the first time.

**This is deliberately a separate document from `RUN-002-Assistant-Report.md`.**
That report is the toll: filed before the reset, from outside the fence, by the
run that died. It is a record of what was knowable at that moment and it should
stay unedited. This document extends it and, in one place, **corrects** it. Where
the two disagree, this one has the code and the toll had a hypothesis.

Read the toll first. It is not restated here.

---

## Verdicts at a glance

| # | Finding | Verdict |
|---|---|---|
| 1 | Run 002 has no opening tag | **Confirmed as fact, broken as diagnosis.** Cosmetic at runtime; a permanently lost measurement; a symptom, not a cause. The `chart-course` rationale is factually wrong. |
| 2 | The Ship ran on the planet's Python | **Confirmed.** Still live in `enter-hyperspeed`. Worse than reported: the dependency runs one layer deeper than the interpreter path. |
| 3 | Cryobay hypothesis | **BROKEN.** Cryobay was never observed at all. It was hand-authored `Visible: Yes` on purpose, one commit before `spawn()` existed. |

---

## Finding 1 — the missing opening tag

### Confirmed as fact

```
$ git tag -l
RUN_001/PROJECT_START
RUN_001/BITER_ATTACK!!
RUN_002/BITER_ATTACK!!
```

`RUN_002/SAME_SHIP_DIFFERENT_DAY` does not exist. `git tag -l 'RUN_002/*'`
returns one tag where `Commit Ritual.md` lines 25-31 say two should stand.

Three of the seven rows in the navigation table (`Commit Ritual.md` lines
98-106) are unrunnable against run 002. Verified, exact output:

```
$ git log 'RUN_002/SAME_SHIP_DIFFERENT_DAY..RUN_002/BITER_ATTACK!!'
fatal: ambiguous argument 'RUN_002/SAME_SHIP_DIFFERENT_DAY..RUN_002/BITER_ATTACK!!':
unknown revision or path not in the working tree.
```

Same fatal for *"What run 2 built"* and *"What The Ship carried across."*
`git show RUN_002/BITER_ATTACK!!`, `git tag -l 'RUN_002/*'` and the `git runs`
alias all work — the alias is present in `.git/config` and resolves.

The candidate landing commit `7fb5681` is correct. Its parent is `2121230`,
which is exactly `RUN_001/BITER_ATTACK!!`:

```
$ git log -1 --format='%h parents=%p' 7fb5681
7fb5681 parents=2121230
$ git rev-list -n1 'RUN_001/BITER_ATTACK!!'
212123049052de782a68f48038d819bffb32eb23
```

**Zero commits separate the death of run 001 from the first commit of run 002.**

### Broken as diagnosis

`chart-course/SKILL.md` lines 47-50 assert:

> *"If the most recent run has no `BITER_ATTACK!!` tag, or no assistant report,
> stop. Charting a course out of a run that was never closed is exactly how run
> 002 launched."*

**Run 001 *was* closed.** `RUN_001/BITER_ATTACK!!` points at `2121230`, *"BITER
ATTACK: the planet is scuttled, the Ship carries on"* — a real scuttle, 16 files,
4093 deletions, tagged. The tag half of the gate was satisfied at the
run-001→002 boundary.

What was actually missing was the **toll**. `_THE SHIP/_EJECT BUTTON/` did not
exist until `9864b76` — *inside run 002*. Run 001 filed no assistant report
because the artifact that receives one had not been invented yet. Step 1 of the
ritual is younger than the boundary it is being retroactively applied to.

So: **the gate is right and its stated reason is wrong.** Applied at the
run-001→002 boundary the gate would still have fired — on the missing report,
not the missing tag. The sentence as written would send a future reader looking
for an untagged run 001 that does not exist. That is the same defect this repo
has already corrected twice in `CLAUDE.md` (`e7b7b1a`, `034a858`): a
true-sounding line that sends a session hunting a bug that isn't there.

### Cause, symptom, or cosmetic?

**Not a cause.** Nothing in the engine, the skills, or the scripts reads a tag.
Run 002 would have been built and would have died identically with the tag
planted. Every fault below is independent of it.

**A symptom.** `Commit Ritual.md` step 3, *"The landing"* (lines 75-80), pairs a
scaffolding commit with the `SAME_SHIP_DIFFERENT_DAY` tag. `7fb5681` is that
landing in substance — it builds the new world's machinery — and it was simply
never recognised as a step. The missing tag is the visible residue of the whole
ritual being skipped, not a thing forgotten on its own.

**Not cosmetic, though.** `Commit Ritual.md` lines 115-121 call
`git diff RUN_00N/BITER_ATTACK!! RUN_00M/SAME_SHIP_DIFFERENT_DAY` *"the
measurement this gives away for free"* and the run-over-run falsification test.
For run 002 that measurement can never be computed, because the left endpoint of
its span does not exist. The instrument's first datapoint is permanently absent.
`5675ee4` separately records that this instrument is also **mislabelled** — that
span is the repair phase, not what the Ship carried across.

A fix would have to address: whether a tag may be planted retroactively at
`7fb5681`, and rewriting the `chart-course` rationale to name the missing toll
rather than a missing tag.

---

## Finding 2 — the Ship ran on the planet's Python

### Confirmed, and still live

Introduced at `2e65027`, both skills:

```
### 2e65027 The loop gets its two terminal verbs
+    "_THE VAST UNKNOWN/.venv/Scripts/python.exe" ".../chart_course.py"
+    "_THE VAST UNKNOWN/.venv/Scripts/python.exe" ".../enter_hyperspeed.py"
### d2ecf9c chart-course becomes the between-runs driver
-    "_THE VAST UNKNOWN/.venv/Scripts/python.exe" ".../chart_course.py"
+    python ".../chart_course.py"
```

`chart-course` fixed at `d2ecf9c`. **`enter-hyperspeed/SKILL.md` line 10 still
carries the dead path.**

### What it would have broken, and when

It has not broken yet, and the reason is worth stating precisely: the scuttle
used `git rm --cached` (`205ec1b`), so `.venv/Scripts/python.exe` is *still on
disk*. Untracked, now gitignored (`034a858`), but present and runnable.

It breaks on the first of these:

- **A fresh clone.** Already true today. `205ec1b`'s own message accepts it:
  *"a fresh clone of this repo now contains no engine."* `_THE VAST UNKNOWN/` is
  gitignored, so the vault never arrives, and `/enter-hyperspeed` fails on a
  missing interpreter with no hint that the missing thing is a *world*.
- **Any real disposal of the planet.** The whole premise is that the vault can
  be deleted. The moment it is, stage 03 of the loop — a durable Ship verb —
  dies with it.

`d2ecf9c` justified leaving it: *"enter-hyperspeed still points at the venv and
is untouched; it writes into the vault, so its dependency is not the same bug."*
**That reasoning does not hold.** Writing an output *into* a directory is not the
same as requiring an *interpreter* from it. `chart_course.py` and
`enter_hyperspeed.py` both live under `_THE SHIP/`; both are durable Ship
tooling. Only the second cannot run without the planet.

### The layer nobody named

`enter-hyperspeed` cannot simply be switched to plain `python` the way
`chart-course` was.

`enter_hyperspeed.py` line 16 is `import yaml`. Not stdlib. `chart_course.py`
imports only `argparse, re, shutil, sys, pathlib` — which is exactly why
`d2ecf9c`'s fix was safe there.

And the dependency is declared in the wrong manifest:

`_THE VAST UNKNOWN/pyproject.toml` line 10 declares `"pyyaml>=6"`.
`grep -n yaml "_THE VAST UNKNOWN/server.py"` returns **nothing** — the engine
never imports yaml. The engine's package manifest carries a dependency that
exists solely to satisfy a script on the Ship. (Corroborating: in
`.venv/Lib/site-packages/`, `_yaml` is timestamped `15:10` against `14:18` for
everything installed at venv creation — pyyaml was added later, when
`enter_hyperspeed.py` needed it.)

So the inversion is two-deep. The Ship borrowed the planet's interpreter, and
the planet's manifest was edited to carry the Ship's dependency. Removing the
interpreter path alone leaves a script that fails on `import yaml` under system
python.

A fix would have to address: where a durable Ship script declares its own
dependencies, given the Ship currently has no manifest of its own.

---

## Finding 3 — Cryobay. Hypothesis **BROKEN**.

The toll hypothesised (`RUN-002-Assistant-Report.md` lines 43-51) that Cryobay
was *observed* before `cd4342c` taught `observe` to write through, leaving a
flag without a file. Coherent theory, wrong on every clause. Cryobay was never
observed, and the flag never came from the journal.

### The evidence

**1. Cryobay was born visible.** `_THE VAST UNKNOWN/cartridge.json`, verbatim,
current on disk and unchanged since `e30694c`:

```json
{
  "run": 2,
  "objects": [
    { "Name": "The Guy",    "Visible": "No",  "First Appearance": "Run-002", "Version": 1 },
    { "Name": "Cryobay.md", "Visible": "Yes", "First Appearance": "Run-002", "Version": 1 }
  ]
}
```

`git show e30694c:"_THE VAST UNKNOWN/cartridge.json"` — the commit that first
introduces Cryobay — already has `"Visible": "Yes"`. It has never held any other
value.

**2. It was deliberate.** `e30694c`'s own commit message says so outright:

> *"cartridge.json now holds Run 002's world — **one visible thing, one hidden**.
> scan became a sensor sweep."*

One thing was made visible at authoring time so `scan` would have something to
report. That was the intent. Nothing about it was accidental.

**3. The journal never mentions it.** `_THE VAST UNKNOWN/Crash Sites/Run 002 State.json`
in full — the entire durable state of run 002:

```json
[
  {
    "event": "discovered",
    "Name": "The Guy",
    "guy_handle": "the-guy",
    "seq": 1,
    "at": "2026-08-18T16:16:29+02:00"
  }
]
```

One event. `The Guy`. There is no Cryobay event and there never was.

**4. No code path could ever have materialised it.** `server.py`:

```python
146	    hidden = [o for o in WORLD["objects"] if o["Visible"] == "No"]
...
152	    target = hidden[0]
153	    dest = spawn(target)
```

`spawn()` is called from exactly one place — line 153, inside `observe()`. And
`observe()` only ever selects from `hidden`, i.e. objects with `Visible == "No"`
(line 146). **An object authored `Visible: "Yes"` is unreachable by the only
function that writes to disk.** Not "was not spawned" — *cannot be*, by
construction, in every version of the engine that ever had a `spawn()`.

**5. The timeline runs the other way.** `e30694c` authored the visible flag.
`cd4342c` — the write-through commit the toll pointed at — came *after* and
introduced `spawn()` for the first time. `git diff 7fb5681 cd4342c` on
`server.py` shows `spawn`, `observe`, `record`, `replay` and `VAULT_SPAWN_ROOT`
all arriving in that single commit. So Cryobay does predate write-through — but
not because it was observed early. Because it was **written into the world
already flagged, one commit before the machinery that materialises things
existed at all.**

### Correction to the toll

`RUN-002-Assistant-Report.md` lines 34-36 state:

> *"Two sources of truth, already drifted. `Run 002 State.json` carries the
> Visible flag."*

**It does not.** The journal is an append-only event list and carries no flags.
`replay()` (lines 79-89) reads events and can only ever *set* `Visible = "Yes"`;
it never stores one. The Visible flag lives in `cartridge.json` and nowhere else.
The toll named the wrong file as the liar.

The "two sources of truth" framing survives the correction, but the pair is
different: it is **`cartridge.json` versus the filesystem**, and they were never
in sync — not "drifted," never joined. Drift implies they agreed once.

### What the actual defect is

The engine has an unstated invariant — *`Visible: Yes` implies the thing exists
in the vault* — which `scan()` (line 132) reports as though it were guaranteed,
which `observe()` is the only thing that ever establishes, and which **nothing
enforces at load**.

- `schema.json` validates *shape*, not world-to-disk consistency. `Visible` is
  `{"enum": ["Yes", "No"]}` — a hand-authored cartridge may declare anything
  visible with no obligation to produce it.
- `load_world()` (lines 37-59) checks schema conformance and stops. It never
  looks at the filesystem.
- `replay()` refuses on a journal event naming a thing not in the cartridge
  (lines 84-88) — a real consistency check, in the one direction that could not
  have produced this bug.

The engine has precisely one integrity check and it points the wrong way.

The toll's closing judgement holds, and is stronger than it knew: *"the engine
looks healthy while lying."* This was not legacy state from before a fix. It was
the world as authored, faithfully served, on every scan from `e30694c` onward.

A fix would have to address: a load-time reconciliation of every `Visible: Yes`
against the vault, refusing boot on mismatch the way an invalid cartridge does.

---

## Beyond the three — what nobody had named

### N1. The pipeline's middle is missing. This is Cryobay's root cause.

The loop's stage 03 does not feed the engine. Nothing connects them.

- `enter_hyperspeed.py` line 115 writes `Crash Sites/New World {run:03d}.json`.
- `server.py` line 25 reads `sys.argv[1]` if given, **else `HERE / "cartridge.json"`**.
- `.mcp.json` at `b460417` — the only version that ever registered the engine —
  passed `args: ["../_THE VAST UNKNOWN/server.py"]`. **No `argv[1]`.** The engine
  always read `cartridge.json`.

And the two files are not even the same shape. `New World 002.json` holds
`difficulty`, `length`, `world_objective`, `learning_objective`, `source`,
`extracted_at`. `schema.json` requires `["run", "objects"]` with
`"additionalProperties": false`. Feeding one to the other is a guaranteed
`BOOT REFUSED`.

`2c3dde2` states the gap plainly and it was never closed:

> *"this JSON is what the **cartridge generator** will build it from."*

`grep -rln "cartridge" --include=*.py .` returns exactly one file: `server.py`,
which only reads. **The cartridge generator was never written.** So
`cartridge.json` was hand-authored — which is how a human decided, by hand, in
prose, that one thing would start visible, with no script and no schema in any
position to ask what that flag obligated.

This is the most consequential finding in the run, and it makes Finding 3 a
*category* rather than an incident: `/enter-hyperspeed` reported success
(`2c3dde2`, *"validated clean and landed as the engine's first crash site"*)
while producing an artifact the engine cannot consume. The loop's terminal stage
03 emitted into a void and printed `hyperspeed:` while doing it.

A fix would have to address: either the generator that turns coordinates into a
cartridge, or an explicit statement that hand-authoring the cartridge is the
design — in which case Finding 3's reconciliation check is not optional.

### N2. A hardcoded constant silently overruled an operator ruling.

`e30694c`'s message records a decision:

> *"His win condition is falsifiable per their Q5 ruling: the folder `The Guy/`
> git-moved from `_THE SHIP/` to root."*

`server.py` line 26, written one commit later at `cd4342c`:

```python
VAULT_SPAWN_ROOT = HERE.parent / "_THE SHIP"
```

`spawn()` therefore put The Guy back at `_THE SHIP/The Guy/`, which is where the
toll found it and where `git ls-files` still shows `_THE SHIP/The Guy/.gitkeep`.
The operator's ruling was recorded in a commit message; the code that had to
honour it hardcoded the opposite; nothing compared them.

The toll listed *"spawn destination is unspecified"* as open design. It was not
unspecified — it was **specified and then contradicted**. That reclassifies it
from an undecided to a defect.

(Caveat: the ruling's own git-move leaves no trace in `e30694c`'s diff, which is
consistent with moving an empty untracked directory — git records nothing.
`git log --all --diff-filter=ADR -- "*The Guy*"` returns only `e30694c` and
`6be6fa0`. The ruling exists only in prose.)

### N3. `Version` and `First Appearance` are decoration.

Both are `required` in `schema.json`. Neither appears anywhere in `server.py`
outside the cartridge dict that passes through `scan()`:

```
$ grep -n 'Version\|First Appearance' "_THE VAST UNKNOWN/server.py"
(no matches)
```

Nothing increments a Version. Nothing derives a First Appearance from `run`, or
checks that `"Run-002"` agrees with `"run": 2`. The toll's sensor table reporting
*"Cryobay.md (v1)"* was quoting hand-typed cartridge text, not engine state.

This sits in direct tension with `server.py`'s own docstring, lines 11-12:
*"Derivable values are computed on read, never stored."* `First Appearance` is
derivable from the journal. `Version` is derivable from an edit count. Both are
stored, both are hand-set, neither is ever computed. Two of the four fields in
the thing-schema are inert.

**Undecided, not broken.** No behaviour depends on them being right. But they
are exactly the kind of field that looks authoritative in a report — and did, in
this one.

### N4. The engine was only reachable from the side forbidden to touch it.

`b460417` moved `.mcp.json` to `../`-relative paths, making `_THE SHIP/` the
mandatory cwd — a deliberate call, well argued in that commit. The consequence:
from repo root, `../_THE VAST UNKNOWN/server.py` resolves to
`C:\Users\alder\Desktop\_THE VAST UNKNOWN\server.py`, outside the repo. **Root —
the only working directory with no fences — could not boot the engine.** The
only cwd that could was `_THE SHIP/`, which both `CLAUDE.md` files forbid from
reading the engine.

That is precisely the shape of the problem this session was created to unblock,
and it was baked in at `b460417`. Not a bug in itself; a structural corner that
made engine work impossible from either side at once.

### N5. The rituals describe a repo that does not exist — knowingly.

`Commit Ritual.md` line 147: **"No run has been scuttled yet."** Two have.
Line 91's invariant — *"a scuttle commit must delete nothing under `_THE SHIP/`"*
— was false when written, because `The Guy` lived under `_THE SHIP/` and was
meant to die with the run.

This is **already fully self-reported** by `5675ee4`, which lands the text
labelled `KNOWN STALE` and enumerates all four defects, and by `d2ecf9c` and
`034a858`. Committing it broken-and-labelled over silently-patched is defensible
and I am not relitigating it. Noted only because a reader of the ritual alone
gets no warning: the label lives in the commit message, not in the document.
Line 147 reads as current state.

**Correction to my own first pass:** the SHA in that table, `24efdd4`, is
*correct*. `git rev-list -n1 RUN_001/PROJECT_START` → `24efdd4…`. (`git tag -l
--format='%(objectname:short)'` reports `a0eee1f`, which is the annotated *tag
object*, not the commit it points at. Easy trap; recorded so the next reader
doesn't fall into it.)

### N6. Run 002's only flight recorded null provenance.

`enter_hyperspeed.py` lines 110-111 capture `Version` and `Version Date` from
the form. `Crash Sites/New World 002.json` records both as `null`, because
`Atlas of Worlds/New World 002.md` frontmatter (lines 1-7) has no such keys —
they were added to the master template afterwards (`New World Coordinates.md`
lines 7-8: `Version: 2`, `Version Date: 2026-08-18`).

So the template-versioning field the pipeline exists to capture was null on the
only occasion it has ever run. Harmless now; it means run 002 cannot be traced
to the template it was flown against.

### N7. `observe`'s "nearest contact" is a fiction.

`server.py` line 143 documents *"Investigate the nearest unknown contact."*
Line 152 is `target = hidden[0]` — cartridge array order. There is no position
field in `schema.json` and no notion of distance anywhere in the engine. The
toll's *"observe cannot be targeted"* is right; the reason is not that aiming is
withheld but that **there is no space to aim in.** Spatial vocabulary in the
docstring implies a model the data has no field for.

Same class as the phantom `probe` the toll self-reported: a capability implied
by register rather than by inventory — here, in the engine's own docstring.

---

## What I checked and found fine

- **Skill duplication.** `d2ecf9c` flagged the Instrument Panel's copies as a
  drift risk. `diff` on both pairs: **identical, byte for byte.** No drift ever
  occurred. (The copies are being deleted in the operator's live restructure as
  this is written — staged `D` on both. The risk is being closed, not realised.)
- **`git runs` alias.** Present and correct in `.git/config`, resolves cleanly.
  `Commit Ritual.md` lines 125-137 are accurate.
- **Cartridge/schema co-evolution.** At `e30694c` the cartridge had no `run` key
  — but neither did the schema require one. `cd4342c` added it to both in the
  same commit. There is no window where the engine would have refused its own
  cartridge.
- **The scuttle's purity.** `205ec1b` touches exactly five paths, all under
  `_THE VAST UNKNOWN/`, all deletions. The invariant held for that commit; only
  the *general* form of the invariant is false.
- **`chart_course.py` refusals vs `File Move Ritual.md`.** All five documented
  preconditions (ritual lines 53-59) map one-to-one onto the script's `refuse()`
  calls (lines 35-64). Doc and code agree. `d2ecf9c` claimed this; it is true.
- **`chart_course.py` run numbering.** Derives from `max(atlas ∪ panel) + 1`
  (lines 42-48), so the by-hand archival at `f05dd76` still yields 003. Verified
  by reading, not by executing. `f05dd76`'s reasoning holds.
- **Current preconditions for the next chart.** Master template exists with an
  empty `Run:` slot (line 2); Instrument Panel exists; `Atlas of Worlds/` exists
  and holds `New World 002.md`; the Panel holds zero live forms.
  `chart_course.py` would not refuse today.

---

## Live and in flight — flagged, not judged

`git status` currently shows `D "_THE SHIP/The Guy/.gitkeep"` — deleted in the
working tree, uncommitted. `File Move Ritual.md` lines 73-75 list
`_THE SHIP/The Guy/` as **Undecided**, and line 71 states *"nothing may move it
silently."*

The Ship's `CLAUDE.md` has also been rewritten during this session and now
asserts *"Everything under `_THE SHIP/` is 100% durable… A run creates nothing
in this folder"* — which, if it lands, resolves that undecided row and makes The
Guy's removal correct rather than silent, and makes the `Commit Ritual.md`
invariant true and hook-enforceable for the first time.

Recorded as observed state, not as a fault. The ritual and the working tree
currently disagree, and the operator is mid-decision.

---

## What I could not determine

- **Whether Cryobay was ever meant to materialise.** `e30694c` says one thing
  was made visible so `scan` had something to report. Whether the operator
  understood that as "a file the operator will find in the vault" or as "a
  display fixture" is not recoverable from the repo. The *mechanism* is settled
  beyond doubt; the *intent behind the flag* is a question only the operator can
  answer — and the answer decides whether N1's fix is a generator or a boot
  check.
- **What `Cryobay.md` was supposed to contain.** No draft, no template, no
  registry page. `_THE SHIP/Hitchhiker's Guide/Schema/` holds `The Guy.md` and
  nothing for Cryobay. It has no content anywhere in git history.
- **Whether the engine actually served a stale scan more than once.** I did not
  run the server — forbidden, and correctly so. The code proves what any scan
  *must* have returned; it cannot tell me how many times it was asked.
- **Whether `python` resolves to a pyyaml-bearing interpreter on this machine.**
  `d2ecf9c` reports system python 3.14.4 and `.venv/pyvenv.cfg` confirms
  `C:\Python314`. Whether pyyaml is installed there is untested — I did not run
  python, and `pip` was off-limits. This is the one open question that decides
  how much work Finding 2's fix actually is.
- **Run 001's internals.** Out of scope and unexamined except at the boundary.

---

## Fence report

`_THE VAST UNKNOWN/` was **read** by this session, under the root-cwd exemption
in root `CLAUDE.md` ("Root has no fences", lines 12-24). Files opened:

| File | What it bought |
|---|---|
| `server.py` (all 165 lines) | Settled Finding 3 outright. Lines 146/152/153 prove `spawn()` is unreachable for a `Visible: Yes` object. Lines 79-89 disprove the toll's "the state file carries the flag." Line 26 exposed N2. Lines 143/152 exposed N7. The absence of `Version`/`First Appearance` exposed N3. |
| `cartridge.json` | The smoking gun. `Cryobay.md` has `"Visible": "Yes"` and always did. |
| `schema.json` (+ its versions at `7fb5681`, `e30694c`) | Showed the schema validates shape only, never world-to-disk consistency — the reason nothing caught this. Confirmed cartridge/schema co-evolution was clean. |
| `pyproject.toml` | Exposed the second layer of Finding 2: `pyyaml>=6` declared by the engine for a Ship script. |
| `Crash Sites/Run 002 State.json` | One event, `The Guy`. No Cryobay, ever. |
| `Crash Sites/New World 002.json` | Exposed N1 — its shape cannot satisfy `schema.json`, so stage 03's output was never engine input. |
| `.venv/pyvenv.cfg`, `.venv/Scripts/` listing | Confirmed the dead interpreter still exists on disk (why Finding 2 has not bitten yet) and dated pyyaml's late install. |

Nothing under `_THE VAST UNKNOWN/` was written, edited, moved, or executed. The
server was not started. No `pip`. No writing git command was run anywhere.

**What the access was worth.** The toll wrote *"the desync was fully diagnosable
from outside the fence. Holding it cost nothing."* That was true of the
*symptom* and false of the *diagnosis*. From outside, the best available theory
was a plausible, coherent, and entirely wrong story about a stale flag surviving
a fix. Twenty lines of `server.py` and six lines of `cartridge.json` replaced it
with a proof — and turned an incident into a class: **the engine cannot check
that the world it describes is a world it can produce, and the pipeline that was
supposed to build that world was never connected to it.**

Holding the fence cost one wrong hypothesis — filed as the run's headline
finding, and carved into the tag message on `RUN_002/BITER_ATTACK!!`.
