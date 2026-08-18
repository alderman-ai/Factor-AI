# The Crate

A **crate** is a capacity-limited container that things are put into and taken
out of. It is a general component, not a one-off: **many sources can fill one
crate, and many consumers can drain it.**

    C - THE SHIP - 10
    │      │        └── capacity: how many things it can hold
    │      └─────────── whose side of the exchange it serves
    └────────────────── C = Crate

Capacity is in the name because capacity is the constraint. A bottleneck should
be readable off a directory listing without opening anything.

**A crate is a directory.** Items in it are files. "Full" is a count. That
matches the Action verbs — `Move` and `Pick up` are things you do to files, not
to rows in a manifest.

---

## The rule this replaced

Before this, the Ship mixed durable and disposable in one folder. `The Guy/`
spawned at `_THE SHIP/The Guy/` and died with the run, which is why
`Commit Ritual.md`'s invariant — *"a scuttle commit must delete nothing under
`_THE SHIP/`"* — was false and could never be enforced by a hook.

Four provenance-marking schemes were proposed to work around it. The operator
killed all four:

> "This is unnecessarily complicated. We will have a rule that nothing spawns
> in the ship."

**Everything under `_THE SHIP/` is durable. Full stop.** The invariant is now
true by construction, and a hook enforcing it can never fire a false positive.

### Spawn is not the same as file

Nothing *spawns* in the Ship. Things can still be *filed* into it — and filing
is exactly what makes something durable. Moving an item out of a crate and into
the Ship is the act that saves it.

---

## `C-THE SHIP-10` is a test rig, not the destination

Stated plainly so nobody two months from now mistakes scaffolding for ontology:

> "There honestly probably won't be a ship crate after testing. Both guy and
> ship are directories so they can insert the item directly into each other."

The Ship↔Guy crate exists to **prove the exchange works** while it is still
observable. Once it has, the two directories hand off to each other and this
particular crate goes away. The *component* stays; this *instance* does not.

At server launch, two things exist at repo root and both are visible:

| Object | What it is |
|---|---|
| `/The Guy/` | Run-lifetime. Dies at the boundary. |
| `/C-THE SHIP-10` | The provisional crate the Ship and Guy trade through. |

**Why a crate at all, if the end state is direct handoff:** a direct handoff is
one atomic event with no state in between and nothing to inspect. A crate makes
the transfer two events with an observable state between them, and gives it a
limit that can fill up. During testing that is the entire point — you can see
the exchange half-done.

---

## Nothing reaches into anything — Actions mediate

The Ship does not open the crate. It emits an **Action document**, and something
processes it. See `Human Actions/`.

    Ship ── emits Action ──▶ processor ──▶ crate ──▶ processor ──▶ Guy

An Action carries two changeable frontmatter values, `Pathing` and `Container`,
and exactly one ticked verb. **The verb is the document's identity and does not
change** — an Action *is* a `Move`, permanently. It is not a menu.

The executor is a root-invoked processor, deliberately run rather than fired by
a hook. Root can reach the crate, `/The Guy/`, and the Ship, so no participant
needs elevated access to any other.

---

## At a run boundary

**The crate dies with the run, and its contents die with it.**

Anything still sitting in the crate when the biters arrive is destroyed. That is
the pressure: an item left in the crate is an item you failed to move in time,
and the reset staying expensive is the reason the reset exists.

**But the Ship is 100% durable.** Anything moved out of the crate and into
`_THE SHIP/` before the boundary survives — permanently, along with everything
else in there. Survival is available to anything; it just costs the work of
moving it.

This is also why SatNav remains the only *accumulator*. The crate is a buffer
with a deadline, not a second knowledge base.

---

## Open — not decided

| Question | Status |
|---|---|
| What happens when a crate is full? Refuse the put, or block? | Undecided. Capacity would be enforced by something that counts before allowing a put, same shape as the Ship's fence hook. |
| Does the Guy get his own crate while testing, or is `C-THE SHIP-10` bidirectional? | Undecided. The name reads one-directional. Moot once direct handoff lands. |
| What deletes `/The Guy/` and the crate at the boundary? | Undecided. Done by hand this transition. |

None of these block the spawn rule. All of them block building the crate.
