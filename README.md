# Factor-AI

**Building an AI harness the way you'd build a Factorio base — in public, mistakes included.**

After roughly a thousand hours building with Claude and a similar thousand hours in Factorio over the last decade, I noticed something: the game had quietly taught me how to think about systems. Throughput. Bottlenecks. Ratios. When to build ugly and when to tear it down. Buffers, backpressure, and the discipline of not optimising a process you haven't run yet.

This repo is what happens when I stop treating that as a coincidence and build an AI engineering harness on those principles deliberately.

---

## Start here

New to the repo? Read in this order:

1. **This file** — what the project is and where it's going.
2. **[`CLAUDE.md`](CLAUDE.md)** — the standing contract the assistant operates under. Coaching posture, refusal conditions, behaviours to avoid.
3. **[`The Lab/Ontology.md`](The%20Lab/Ontology.md)** and **[`The Lab/Lexicon.md`](The%20Lab/Lexicon.md)** — the vocabulary. Nothing else makes sense without it.
4. **[`Ore patches/Miner-001-Science/Science Ore Patch.md`](Ore%20patches/Miner-001-Science/Science%20Ore%20Patch.md)** — a real template, carrying its own fill contract in the body.
5. **[`The Ship/Ship's Computer Entries/`](The%20Ship/Ship's%20Computer%20Entries/)** — session logs, including what went wrong.
6. **`git log`** — see below. The commit messages are the primary narrative.

---

## Why Factorio

You don't need to have played it. Three ideas do all the work:

**Everything is a throughput problem.** A factory is judged on one number — science per minute. Beautiful infrastructure producing nothing is a failed factory. The same is true of a knowledge system: capture is not the point, retrieval is.

**Constraints beat instructions.** In Factorio you can't build a machine you don't have the materials for. It isn't a rule you agree to follow, it's a fact about the world. Most AI harnesses enforce their rules with prose in a prompt, which degrades exactly when you need it most. This project keeps asking: can this rule be made of resources instead of requests?

**You will tear it down, and that's fine.** Your first base is spaghetti. Its job isn't to be good, it's to fund the next one. Building it is how you learn what the requirements actually were.

The theme is a design constraint, not a costume. Where it sharpens a decision it stays; where it would only be decoration it gets dropped. Three times in the first session the design got *better* by deliberately departing from the game.

---

## The Rocket

Factorio gives you one win condition: launch a rocket. Without one, there is no "done," only "more" — which is exactly how the game eats weekends.

**This project's rocket:**

> A fully working pipeline from an idea, to a complex project charter, decomposed into specs, each one-shot with no human in the loop — and the result *actually* meeting the entire charter's Definition of Done.

Not "produces plausible output." Meets the DoD, verifiably, without someone stepping in to clarify what was meant.

### Tech tiers

Milestones on the way, each publishable on its own:

| Tier | Milestone | Status |
|---|---|---|
| 🔴 Red | One artifact through the full template contract, manually triggered | **In progress** |
| 🟢 Green | Mining automated, constraints enforced by the harness, throughput matched to demand |  |
| 🔵 Blue | One charter decomposes into N specs with bidirectional traceability |  |
| 🟣 Purple | One spec, one-shot, no HITL, verified against its DoD |  |
| 🚀 Rocket | End to end |  |

---

## What I'm trying to get better at

I came to this from marketing, not engineering. The theme exists to force me into the deterministic toolkit that comes more naturally to people with a traditional technical background:

- System architecture and design
- Traceable routing
- Loops
- YAML frontmatter as a real schema, not decoration
- Pre-tool hooks — especially enforcing creative constraints so the assistant *can't* cheat
- Granular subagent configuration
- Clobber prevention across parallel sessions on one machine and one repo — **without** separate worktrees, partly because every session must see the same state, and partly as a constraint worth learning to work around

The assistant in this repo is configured to coach rather than execute, and to refuse work that routes around those goals via the prose-shaped comfort zone I'd otherwise default to.

---

## How to follow along

**Engineer notes**, published every 1–3 days.

**The commit log is the real story.** Commits are written as narrative — what was decided, why, what was rejected, and what question it leaves open for next time. They're meant to be read, not just diffed:

```bash
git log --format="%h  %s%n%n%b"
```

**Failures are in there too.** Session logs record what the assistant got wrong, not just what got built. In the first session alone that included claiming a constraint was enforced when nothing enforced it, and over-engineering the fix once caught.

---

## Repo map

| Path | What it is |
|---|---|
| `The Ship/` | Where we crashed. A read-only hold — it provides, nothing writes back to it. Starting items, and the session logs. |
| `The Lab/` | The knowledge base. Ontology, lexicon, taxonomy. Deliberately *not* globally loaded — availability on request, not by default. |
| `Blueprint Book/` | Where workflows and reusable builds get designed. |
| `Ore patches/` | Templates and the machinery that mints copies of them. Nothing in this system outputs a free-form document; the only legal output is a filled-in copy of a template that already exists. |

---

## Current state

Red tier, in progress. The template system exists, five blanks are mined, and fifteen learnings are staged in the commit log waiting on two open design decisions before the first one can be processed.

Zero output so far. Which, if the Factorio framing is worth anything, is exactly the number that should be bothering me most.

---

*Built with [Claude Code](https://claude.com/claude-code). Not affiliated with Wube Software.*
