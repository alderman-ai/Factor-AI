# Human Actions

**The actions available ON the Ship.** One document per action type.

Off-ship actions — the ones performed out in the world — are a different set
and live in `Ontology/Intake Primitives.md` under the Action tier, priced by
the resource each costs. The two verb lists are not a contradiction and neither
is stale: they are two scopes.

| Scope | Verbs | Where |
|---|---|---|
| **On ship** | `Move` · `Switch` · `Destroy` · `Pick up` | here |
| **Off ship** | `Move` · `Open` · `Close` · `Inspect` · `Hand-mine` · `Hand-craft` · `Move to` · `Search For` | `Ontology/Intake Primitives.md` |

Only `Move` appears in both, and that is fine — moving a thing is moving a
thing wherever you are.

## What an Action document is

```
---
Pathing: /file.md
Container: Self
---
- [ ] Move
- [ ] Switch
- [ ] Destroy
- [x] Pick up
```

**The two frontmatter values change. The ticked verb does not.**

That is the load-bearing rule of the whole format. `Pathing` and `Container`
are the parameters — what you are acting on, and in what scope. The checkbox is
**not a menu**. It is the document's identity: this file *is* a `Pick up`,
permanently, and a different verb means a different document.

Which makes the verb set a type system rather than a vocabulary. It also makes
the format checkable: a validator can assert that the ticked box never moves
between reads and that only the two frontmatter values differ.

The one-ticked-box grammar is the same one the batch request uses for operator
verdicts. That is deliberate — one shape, learned once.

## How Actions get performed

Nothing reaches directly into anything else. A participant emits an Action; a
processor executes it. See `Ontology/The Crate.md` for the exchange this was
built for.

The processor is invoked deliberately, not fired by a hook — the format is new,
and automating it before it has been exercised is the step the operator's own
rule warns about: *do it manually, then template, then automate.* This is the
template stage.
