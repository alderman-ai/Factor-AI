# V2 World Design

Working design surface for the world behind the MCP. Derived from a design
conversation, not a session log — the Ship's Computer entries cover what
happened, this covers what it should be.

**Status markers used throughout:**

- **Settled** — operator decided it.
- **Open** — named, undecided.
- **Unratified** — assistant proposal, not yet accepted or rejected.

Nothing in here is built. No code exists.

---

## 1. The three surfaces

Decision 1 from session 003 — *where the line sits between server state and
repo files* — was underspecified because it was framed as a division between
two things. There are three.

| Surface | Operator | Assistant |
|---|---|---|
| Repo | reads | reads |
| MCP world state | **blind** | authors |
| DoD of the research project | holds | reads (it's in the README) |

**Settled:** the third surface is the DoD, not a hidden win condition. The
DoD is not a peer of the other two — it's the plane both are judged against.
Repo and MCP are *state*; the DoD is *authority*.

The DoD, restated from the root README: mechanically take an idea down the
belt — into BoN tasks, operator picks the best interpretation, approved tasks
go to the Splitter which weighs them into a task, a full executable spec, or a
project decomposed into a batch of specs. Plus the clause that does the most
work and is easiest to skip: **applicable in a corporate setting instead of
one guy's PC.**

**Unratified — the repo/server line.** An artifact lives in the repo if the
pipeline's output depends on it being inspectable; it lives in server state if
inspecting it would let the operator route around the work.

- **Repo = the trace.** Traceable routing is both an improvement goal and a
  hard DoD requirement. A trace nobody can audit isn't a trace.
- **Server = the gate.** Conditions, weighing, checks. Hidden because a
  visible gate is a gameable gate.

**Open — the auditability tension.** *"Operator never reads the cartridge"*
sits badly with the corporate clause. No buyer accepts a pipeline whose
decision logic they may not audit. Probable resolution: hiding is scoped to
**content** (the specific weights, gates, layout) while **mechanism** stays
fully auditable in the repo. If the cartridge hides *how* the Splitter
decides rather than *what* it decided, the thing being smoke-tested isn't
shippable.

---

## 2. What actually accumulates

**Settled.** The resource that survives resets is data and new knowledge. The
world is disposable. If the world goes off course, reset and keep collecting.

**Settled, and the load-bearing claim:** taking a small amount of intent and
leveraging it into a directionally correct complex series of steps **is the
work**. World-building is not a preliminary to the pipeline — it is an
instance of it, running at the meta level, first and cheapest. Each
world-building failure is data that prevents the next one. Same shape as the
pipeline further down the belt.

**Consequence — the world doesn't need to be correct, it needs to be
instrumented.** An off-course world that fails silently yields nothing. An
off-course world that fails legibly is a complete run of the pipeline under
research.

**Consequence — priority inverts.** If the only thing surviving reset is data,
the extraction and refinement line is the project and the world is the test
fixture. Sessions 001–003 spent their design attention the other way round:
the world got the thinking, the pumpjack was built once and left at red tier.
Worth making that a decision rather than a drift.

**Unratified — the restart toll.** The repo says STOP STARTING OVER in caps
(README, rule-adjacent) and the operator has now granted unlimited permission
to restart. Both hold only if the boundary is mechanical: world disposable,
data layer and pipeline not. Absent a mechanism, "each failure is data" is a
justification available for every shiny object — a tendency named by the
operator about himself in the Captain's Log. Proposal: **a reset is legal only
after a filed entry naming what the world failed at.** Pay the toll, then
burn it, which also makes the reset itself produce the resource.

**Open — the heap problem.** The claim is that accumulated data prevents the
next failure. Currently that data is four free-form prose entries answering
three questions. Entry 3 and entry 40 are not comparable, so a trend is
invisible — you can see that failures happened, not whether the
intent→decomposition step is improving. That is the refinery-fractions
question from session 002, promoted from "blocks the next component" to
"blocks the research." Minimum viable fraction set proposed and unratified:
score every failure by *where in the pipeline it broke* — intent ambiguous,
interpretation wrong, weighing wrong, decomposition wrong, execution wrong.
Five buckets and a count is enough to see a curve.

---

## 3. Gates, and how progress is measured

**Settled.** With enough new knowledge and enough repeats of the beginning,
any test designed to gate progress becomes trivial.

**Consequence — triviality is the readout, not the failure.** Knowledge is not
measured directly. It is measured by **how long a gate holds before it stops
being an obstacle.** Time-to-trivial is the instrument. Same way you'd rank
yourself in the original game: not "do I understand a main bus" but "how fast
to blue."

**Consequence — gates get retired and replaced at a higher abstraction, never
made harder.** The early game doesn't get harder; the map opens further out.
Adding resistance to a gate you've outgrown is fake difficulty. The ladder is
already written in the README: task → spec → decomposed project → *the level
above that the operator said he'd probably stop before*. That last one is the
next gate, reachable only once the one below goes trivial.

**Open — the leak/learned ambiguity.** A gate goes trivial for two reasons
that are indistinguishable from the inside: it was learned, or it leaked
(a route around was found, or the assistant pre-empted it and built something
shaped to pass). Decay rate is a valid metric **only** if gate integrity is
verified independently. Otherwise erosion reads as progress, and it will feel
exactly like getting better. This is the cheating detector flagged in the
Captain's Log, now load-bearing on the measurement rather than only on honesty.

**Resolved — what consumes science.** Not reading. Science is consumed **at
gate-design time**, spent to build the next constraint, which retires the
previous one. Research in, next tier of buildings out. This makes the
assistant the consumer, so retrieval must serve gate design rather than
browsing.

---

## 4. The knowledge base

**Settled.** Science compiles into a knowledge base served over MCP.

**Correction on the reason.** Resets are not the threat — git already survives
resets, permanently and auditably, and a world reset is a repo operation that
never touches `The Lab/`. The real reason is **retrieval**: a flat directory
of prose is not queryable at gate-design time. `science.query(stage, tier)` is.

**Unratified — git is the store of record, MCP is the index.** Entries stay as
files in the repo: public, versioned, auditable, on the trace. The server
compiles and serves them. Server dies, rebuild the index; git dies, the
project is gone. Same crude/render split already made at the pumpjack, one
layer up — called the strongest design decision in the session 002 log. If the
compiled layer becomes authoritative rather than derived, building-in-public
and the corporate audit clause are both lost in one move.

**Unratified — two servers, not one.** The world and the knowledge base have
opposite lifecycles. Disposable and permanent behind one process means a world
reset can take the knowledge with it. Two servers; one of them never restarts.

**Note.** An MCP-served knowledge base is the first component in this design
that is genuinely N-operator shaped. A *local* knowledge base is one guy's PC.

---

## 5. Primitives: ores as input templates

**Settled.** Primitives are input templates for different things, each
represented by a minable ore.

**Open — the pairs.** Tentative:

| Ore | Template for | Class |
|---|---|---|
| Coal | Guy actions — carry an item to a new place, explore for new ore, deconstruct/move a miner | **Fuel** — consumed, produces nothing, enables everything |
| Copper | Writing / designing new skills | Artifact |
| Stone | Creating new frontmatter variables | Artifact |
| Iron | Building executable docs | Artifact |
| Oil | Ontology entries | **Refined**, not assembled |
| Uranium | Altering the ontology template (see §6) | Late-game |

**Coal is a different class from copper/stone/iron.** Those three are pipeline
artifacts at ascending abstraction. Coal is fuel — true to the original, but
it means there are two resource *types*, not one taxonomy. Forcing them into
one schema will make the schema lie.

**Oil is the only pairing that is derived rather than assigned.** From the
session 002 call: ore is discrete and gets **assembled** (combined); oil is
continuous and gets **refined** (separated). An ontology entry takes one
undifferentiated notion and separates it into named fractions, and those
fractions are frontmatter keys. That pair passes the inserter test on its own.
Copper→skills does not yet.

**Unratified — settle scarcity before mapping.** Copper→skills / stone→keys /
iron→docs is currently swappable; nothing breaks if you rotate them, which is
the inserter test failing. What makes it non-arbitrary is mine time, already
noted in the Captain's Log. **The ore assignment is a statement about what you
want to be expensive.** Cheap stone means frontmatter keys get invented freely;
slow iron means every executable doc must earn itself. Decide the scarcity
curve first and the pairs fall out; decide pairs first and the justifications
get retrofitted.

**Unratified — recipes, not ores.** One ore → one output is a vending machine.
An executable doc costing iron *and* copper — because a doc no skill can
execute is inert — produces a dependency graph. That graph is traceable
routing arriving as game structure rather than as a goal to be studied.

---

## 6. The prose economy

**Settled — prose is capped absolutely and the cap never relaxes.**

- Executable tasks: ~10 words of prose.
- Skills: a few words of prose.
- Unlimited frontmatter variables, bought with stone.

**Settled — what scales is machinery, not permission.** Expressiveness does
not come from being allowed to say more. It comes from building more
info-management docs that convert variables into intent. Structure is free;
prose is rationed. The only way to say more is to invent a key.

**Settled — how complex skills get built.** An ontology entry (oil), combined
with a frontmatter schema *defined by* that ontology entry, is how a more
complex skill is assembled. Ontology entry = type definition. Frontmatter =
instance. Skill = the two combined.

**Note.** At ~10 words, an executable doc is almost entirely frontmatter, so
stone is buying *operational* keys, not descriptive ones. Those probably
shouldn't cost the same.

**Note.** A skill that is a name plus frontmatter, with behaviour derivable
from declared keys, is not *written* — it's **configured** from an ontology.
That is the operator's spec-section library, one abstraction level down,
arriving from the opposite direction. Reasonable evidence the model is right.

**Unratified — do not gate stone behind oil.** If a key requires a governing
ontology entry first, stone is inert until mid-game and ontology precedes
data — which is templating before the data, the operator's own doctrine and
the exact failure this project keeps circling. Oil is mid-game in the original
for a reason. Let the early game accumulate ad-hoc keys and make a mess.
**Oil is the refactor**, and the refactor is where the ontology lesson
actually lives. Nobody designs an ontology first; they impose structure on a
mess, and the imposing is the skill.

**Open — is an ontology entry itself prose-capped?** This is the whole design
or the whole leak depending on the answer. If entries are exempt, they are the
escape hatch and everything fenced elsewhere drains through them — the essay
gets written there and called a definition. If capped, they must carry
semantics some other way, and the only visible route is **composition**:
entries reference other entries, meaning is built by combination rather than
description.

**Open — uranium as a cap raise.** "Prose capped absolutely" and "uranium
gives more prose per entry" point opposite directions. A purchasable cap raise
is how constraint systems die — not through abuse, but because once 40 words
is legal you use 40, and the composition pressure quietly stops. Two proposed
saves, both unratified:

1. **Shape.** Uranium should buy *structure*, not word count. In the original,
   uranium is the only chain that behaves differently in kind — enrichment
   returns more input than it consumed. The analogue is an ontology entry that
   operates on other ontology entries. Meta-schema, self-refining. A genuine
   capability jump rather than a bigger budget.
2. **Timing.** The raise must arrive *after* the failure it solves. Hitting a
   definition that genuinely cannot be expressed by composition would be the
   most valuable single data point this system can produce — a real limit found
   at the frontier. Early uranium routes around that discovery before it
   happens.

---

## 7. Mining, sessions, and caps

**Settled.**

- Miners only mine while a session is cwd'd to their directory.
- The guy's skills are local to him, so a guy session must also be running.
- Therefore multiple parallel sessions are required to play. 6–8 concurrent is
  comfortable and not a constraint.
- Mine rate is wall-clocked.
- Mine output is capped at 5–10.
- Early primitives are basic and limited.

**This makes clobber prevention a requirement to play rather than an exercise.**
Improvement goal #8 arrives as the core loop.

**Note — the cap converts idling into a pulse rather than removing it.** Open,
let them cap, drain, repeat. That's hand-mining into a full inventory and it's
fine. But the number that matters is **cap ÷ cost**, not cap. If a drained
chest of 10 stone buys 10 frontmatter keys, the constraint never bites.
Starvation is the mechanic; the cap only produces it if consumption outruns a
full chest.

**Note — caps on both ends is one coherent scarcity model.** Chest on input,
crate slots on output; congestion rather than decay, all the way through.
Cost: a fully backed-up system is a stall, and a stall is the most informative
event available, so it should be *visible* rather than something noticed by
feeling stuck.

**Open — do action templates occupy crate slots?** If not, cheap deconstruct
(§8) means the optimal play is constant churn — chase whatever the rarity curve
currently favours, move miners every session, pay nothing real. If they do
occupy slots, churn self-limits through congestion. They probably belong in the
same crates as everything else.

---

## 8. Expansion, deconstruction, and the real bottleneck

**Settled — the bottleneck is that making the resources for a new miner to
deploy on a patch is difficult.** This is the Factorio-true constraint:
finding ore has always been free, the drill is the cost.

**This dissolves the radar-abundance problem.** Discovery can be uncapped
because discovery is not capacity. A patch is inert until it can be afforded.

**Unratified — cost alone doesn't bind; competition does.** A miner must be
denominated in the same resources it competes with. Every stone spent on a
miner is a frontmatter key not created. If miners cost a separate expansion
currency, the tension evaporates and it becomes a tech tree rather than an
economy. The decision worth forcing is *invest in capacity or ship work*, which
exists only when both draw from one pool.

**Unratified — miners for radar-discovered types cost oil.** To mine a new kind
of thing you must first be able to say what kind of thing it is. Starting
miners are free (crash-landed with them), same as placing a burner drill by
hand. Side effect: you can *see* a patch you cannot yet define — the fog-of-war
property from session 003, arriving through the economy instead of through
skill visibility.

**Settled — deconstruct and move-miner are ordinary skills costing one action
template (coal), not build resources.** Nothing is lost, expansion decisions
are reversible, and early wrong calls don't compound. Correct for a system
whose premise is *make the mistake, capture the data*; expensive undo would
fight the loop.

**Note — the real cost of an action template is the declaration.** Paying coal
to move a miner means filling out a template: source, destination, what moved.
Every physical operation in the world therefore emits a filled artifact into
git. **Traceable routing stops being something to build and becomes the exhaust
of playing.** Improvement goal #2 as a byproduct.

---

## 9. Power

**Settled.**

- Power station and radar are buildings.
- Radar searches for new ore patches while the power station session is running.
- A unit of power has multiple consumers. An automated inserter costs 1; a
  radar costs ~10.
- Finding ore therefore means *not doing something else*.

**Power prices automation, which turns doctrine into economics.** Manual →
template → automate stops being a discipline to maintain and becomes a budget
that can't be beaten. You cannot afford to automate early. Every automated
inserter is 1 power not looking for ore.

**Power is the first global state in this design.** Everything else is
per-directory — a patch, a chest, a guy. Power is one pool drawn on by 6–8
concurrent sessions, making it the first thing that forces the server to
arbitrate contention between them. Until now parallel sessions coexist; with a
shared bus they *interact*. Clobber prevention as a real concurrency problem
with a correct answer.

**Open — brownout behaviour.** Hard refusal teaches nothing, it just blocks.
**Proportional degradation** — everything slows at once — is the loud-failure
answer and the most instructive mechanic in the original, precisely because you
feel it before you can name it and then have to diagnose it. Unratified but
recommended.

**Coal is the master dial.** It pays for movement, exploration, deconstruct,
and plausibly power generation. Every physical operation routes through one
resource. True to the original, but it means coal scarcity is the global clock
speed of the world: loose and nothing has weight, tight and the world seizes.
Of all the curtain levers, the one to tune most carefully and log most strictly.

### 9a. Power and token spend

**Settled — power denominated in real spend forces optimisation.** Named
consequences: routing cheap actions to Haiku-class models, writing succinct
descriptions, pushing meaning into frontmatter rather than prose, and learning
to use cached inputs.

**Rule 4 check — clear, with one tripwire.** The README bans *"token spend
subbed for power and needing to spend more tokens to make more power so that I
can spend more tokens."* What's banned is the **loop** — spend generating the
resource that permits spend. What's proposed is **denomination** — a fixed
budget drawn against at true cost. The tripwire is generation: the moment power
is produced by uptime or by spend, it's the treadmill. **Keep the power station
as a meter, not a generator.**

**Caching is the deep one.** Cached input runs around a tenth the price of
fresh. The economically optimal shape is a large, stable, cacheable context —
ontology, lexicon, templates — with a tiny variable payload on top. That is
exactly the architecture being designed: heavy declared structure, ten words of
prose. **The constraint and the bill point the same direction**, which is rare;
gamified constraints usually fight the underlying economics. The cache is why
this design is right rather than merely elegant.

**Settled — cost is not the binding constraint.** 20x Max subscription; spend
on this project is negligible against normal work.

**Settled — rate-limit brownout is off by at least an order of magnitude** at
current scale. It does not arrive until 10+ specs are running at once.

**Consequence — two power sources, one handoff.** Early game needs an
*artificial* power budget, set below what's affordable, held behind the curtain.
Late game gets *real* grid pressure for free: concurrent sessions drawing on one
shared pool with a hard ceiling and a fixed refill rate is structurally a power
grid, and its brownout is exactly the wanted failure — everything degrades at
once and the greedy consumer must be diagnosed. **The handoff happens at the
DoD**: real pressure arrives precisely when running the batches of specs this
project is built to produce.

**Why the early budget must be behind the curtain.** The optimisation pressure
(Haiku routing, terseness, caching) only fires if the budget bites. A
self-set budget gets raised the first time it pinches during real work, and it
won't feel like cheating — it'll feel like being reasonable.

---

## 10. Radar and world generation

**Settled — rarity is a curtain lever, held by the assistant, not the
operator.** This removes the cheat surface entirely.

**It also makes the world responsive rather than correct.** Aiming at the DoD
happens continuously in reaction to operator behaviour, instead of being
specified up front: spam keys without generalising and stone gets rarer; haven't
hit the composition wall yet and uranium doesn't appear.

**Open — X% per tick makes the world unlearnable.** If radar rolls dice each
tick, ore distribution isn't a fact — it's generated on demand. Nothing can be
mapped, no theory about the world can be falsified, and beliefs get built out of
variance. Three quiet sessions of no iron reads identically as "iron is rare
here" and "unlucky."

**Unratified — seed, not dice.** Generate the layout once from a seed at world
creation; radar *reveals* what is already there. Exploration then means
something, theories can be wrong, and the reset story gets clean: new seed,
genuinely new world, knowledge about how to play carried over intact. That makes
"data survives resets" mechanically true rather than aspirational.

**Unratified — lever asymmetry.** An adaptive difficulty knob in the assistant's
hands is a machine for quietly removing friction, and CLAUDE.md already names the
assistant as the single largest threat to loud failure. Tightening is safe — it's
the product. Loosening is the dangerous direction. Proposal: scarcity may be
increased freely; **any loosening is a logged, dated, committed event.**

---

## 11. Open decisions, consolidated

Ordered by what blocks the most downstream work.

1. **Is an ontology entry prose-capped?** (§6) Whole design or whole leak.
2. **The fractions.** (§2) What axis every failure is scored on. Still blocking,
   now blocking the research rather than a component.
3. **Scarcity curve before ore pairs.** (§5) The pairs fall out of it.
4. **Seed or per-tick dice.** (§10) Determines whether the world is learnable.
5. **Uranium: structure or word count, and when.** (§6)
6. **Brownout behaviour.** (§9) Refusal, proportional degradation, or priority.
7. **Do action templates occupy crate slots?** (§7) Otherwise churn is free.
8. **Gate integrity verification.** (§3) Without it, time-to-trivial measures
   erosion, not learning.
9. **Cartridge auditability scope.** (§1) Content hidden, mechanism public?
10. **One server or two.** (§4) Opposite lifecycles behind one process.

## 12. Carried forward, unresolved from session 003

**Per-directory skill locality is untested and this design rests on it.** The
guy-session mechanic requires skills to resolve per-directory. Live pickup
failed its only real test last session when the skill was in a parent
directory; the own-directory test has never been run. Recorded in
`The Lab/Global Inbox/2026-08-17_223326.md`.

**Obsidian Sync is a third writer.** It can dirty the git tree without passing
through the terminal, and the cheating detector cannot distinguish a pulled file
from a hand-edited one. Not yet in any spec.
