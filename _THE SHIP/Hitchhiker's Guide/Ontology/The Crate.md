# The Crate

**Nothing passes directly between the Ship and the Guy. Everything passes
through a crate.**

Operator ruling, batch request R3. This replaces the whole "how do we mark
run-created files for deletion" problem — there is nothing to mark, because
nothing a run creates lands inside `_THE SHIP/` any more.

---

## The rule it replaces

Before this, the Ship mixed durable and disposable in one folder. `The Guy/`
spawned at `_THE SHIP/The Guy/` and died with the run, which is why
`Commit Ritual.md`'s invariant — *"a scuttle commit must delete nothing under
`_THE SHIP/`"* — was false and could never be enforced by a hook.

Four provenance-marking schemes were proposed to work around it (frontmatter
key, per-run manifest, quarantine folder, sidecar marker). The operator killed
all four:

> "This is unnecessarily complicated. We will have a rule that nothing spawns
> in the ship."

**Everything under `_THE SHIP/` is durable. Full stop.** The invariant is now
true by construction, and a hook that enforces it is a hook that can never fire
a false positive.

---

## What exists at server launch

Two objects, at **repo root**, and both must be **visible**:

| Object | What it is |
|---|---|
| `/The Guy/` | The Guy. Spawned by the engine, run-lifetime, dies at the boundary. |
| `/C-THE SHIP-10` | The crate the Ship and the Guy trade through. |

### Reading the crate name

    C - THE SHIP - 10
    │      │        └── capacity: how many things it can hold
    │      └─────────── whose side of the exchange it serves
    └────────────────── C = Crate

Capacity is in the name because capacity is the constraint. A crate is a
bottleneck you can read off a directory listing without opening anything.

---

## The exchange

There is no Ship→Guy operation and no Guy→Ship operation. There are only
crate operations, and they are separate events:

    Ship  ──put──▶  C-THE SHIP-10  ──take──▶  Guy
    Guy   ──put──▶  C-THE SHIP-10  ──take──▶  Ship

The Ship adds an item to the crate. Later, the Guy removes it. Neither ever
reaches into the other. The crate is the only shared surface, and it is at root
— outside both.

**Why this shape:** a direct handoff is one atomic event with no state in
between and nothing to inspect. A crate makes the transfer two events with an
observable state between them, and gives the exchange a capacity limit that can
fill up. That is the difference between a chore and a factory.

---

## Consequences

- **`_THE SHIP/The Guy/` is retired.** It exists on disk as an empty directory
  staged for deletion. The Guy's home is root, not the Ship.
- **The file-move ritual has nothing to sweep out of the Ship.** Its Ship-side
  job is now archival only.
- **Anything the operator drops into the Ship mid-run survives**, automatically,
  because no deletion rule points at the Ship at all. That was the requirement
  that made the manifest scheme attractive; the spawn rule satisfies it for free.

---

## Open — not decided by this ruling

Named so nobody assumes an answer:

| Question | Status |
|---|---|
| Is a crate a directory, or a file with a list inside? | Undecided. `/C-THE SHIP-10` has no extension, which reads like a directory. |
| What happens when a crate is full? Refuse the put, or block? | Undecided. |
| Does the Guy have his own crate, or is one crate bidirectional? | The name suggests it belongs to the Ship's side. Undecided. |
| Who enforces capacity — the engine, a hook, or nothing yet? | Undecided. |
| Does the crate survive a run boundary, or die with the world? | Undecided. It sits at root, which is durable, but it is created at server launch, which is per-run. |

None of these block the spawn rule. All of them block building the crate.
