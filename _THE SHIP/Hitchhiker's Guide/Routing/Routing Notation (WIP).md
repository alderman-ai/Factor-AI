# Routing Notation — WORK IN PROGRESS

**Nothing here is enforced yet.** No script reads this file. It is the
operator's design notes for how a resource proves where it came from, written
down so the decisions stop living in chat scrollback.

When a verb enforces any of this, that verb belongs in
`Schema/ADRENALINE Rules.md` and this file becomes its explanation, not its
source. Until then: draft.

Scoped to Demo 001. Nothing below is a durable contract.

---

## The problem

A piece of ore arrives at the Ship. It claims it came from the ore patch. The
Definition of Done says five pieces of ore must arrive **from the patch** — so
"it's ore and it's here" is not enough. Something has to make the claim
falsifiable.

The requirement the operator set: **the check is one string that must equal an
expected string.** Not a prose log to read, not a tree to walk, not a
frontmatter to interpret. String equality, or it doesn't count.

---

## Two records, on purpose

A resource carries its route twice.

| | What it is | Who reads it |
|---|---|---|
| `R-NNN-*` fields | The verbose record. One numbered group per hop. | Humans |
| `R-Check` | The same journey squished into one comparable string. | The audit |

Neither is decoration. `R-Check` is derivable from the fields, so **a
disagreement between them is evidence of tampering rather than a formatting
quirk** — the same reason the ADRENALINE run log records both a breadcrumb and
a full log.

### Who writes them

Movers append as they go. The audit re-renders `R-Check` from the `R-NNN`
fields and requires the two to agree **before** comparing to expected.

```
movers append      -> R-Check on the resource
audit re-renders   -> from the R-NNN fields
   1. do the two agree?        catches a forged string or forged fields
   2. does it match expected?  catches an illegal route
both must pass
```

Appending as it travels — rather than composing the string on arrival — is
what lets a resource that **never arrives** still carry its partial route. Ore
that dies in a belt says where it stopped.

### The movers must not know the encoding

If four movers each append, the grammar lives in four skills and drifts within
a day. One shared script owns the encoding; a mover hands it the hop as fields
and never writes the string by hand. Same split as everywhere else in this
build: components supply values, the script owns the grammar.

It is also the only way the audit's re-render is guaranteed to agree with what
the movers wrote — both call the same encoder.

---

## The grammar

```
o-<ORIGIN>-<hop>-<hop>-...-e
```

A hop:

```
r<n> t<CODE> [v<CODE>] [w<CODE>] [b<CODE>]
```

| Key | Means | Example |
|---|---|---|
| `o` | origin sentinel, followed by where it was created | `o-OP1` |
| `r<n>` | hop number, sequential from 1 | `r3` |
| `t` | **to** — where the hop ended | `tC1` |
| `v` | **via** — the mover artifact that carried it | `vI1` |
| `w` | **with** — the kind of action | `wHA` |
| `b` | **by** — the actor who performed it | `bGUY` |
| `e` | end sentinel — the journey completed | `-e` |

**Keys are lowercase. Codes are UPPERCASE.** That is what makes a segment
self-delimiting with no separator inside it. It is not cosmetic: with
lowercase codes, `r1tb2vi2` is genuinely ambiguous, because `b` is both a key
and the first letter of a belt code. Uppercase codes remove the ambiguity
completely.

Segments are joined by `-`.

### Worked example

The reference ore, `Demo Ship/DEMO-001-ORE (correct pathing).md`:

```
o-OP1-r1tB1BvI2-r2tB1A-r3tC1vI1-r4tSHIPwHAbGUY-e
```

| Segment | Reads as |
|---|---|
| `o-OP1` | created at Ore Patch-001 |
| `r1tB1BvI2` | hop 1, to Belt-001 end B, via Inserter-002 |
| `r2tB1A` | hop 2, to Belt-001 end A — no mover, see **Belts** below |
| `r3tC1vI1` | hop 3, to Crate-001, via Inserter-001 |
| `r4tSHIPwHAbGUY` | hop 4, to the Ship, with a Human Action, by @The Guy |
| `-e` | arrived |

---

## Codes

Mostly derived, so there is almost no registry to keep in sync.

**Derivation:** drop the roman-numeral capacity suffix, take the word initials
of the name, uppercase, then the number without leading zeros, then the end
letter if the component has ends.

| Component | Code | |
|---|---|---|
| `Ore Patch-001-iii` | `OP1` | initials + number |
| `Belt-001-a-i` | `B1A` | + end letter |
| `Belt-001-b-i` | `B1B` | |
| `Crate-001-v` | `C1` | |
| `Inserter-001` | `I1` | |
| `Inserter-002` | `I2` | |

**Declared** — these have no number, so derivation has nothing to work with:

| Component | Code |
|---|---|
| `Demo Ship` | `SHIP` |
| `@The Guy` | `GUY` |
| `Human Action` | `HA` |

### The cost of deriving

**Renaming a folder silently invalidates every signature that mentions it.**
An explicit registry would survive renames; derivation does not. Accepted for
Demo 001 because the registry would be longer than the demo — but it is a real
debt, and belt and ore-patch names have already moved once today.

---

## Belts are one container with two ends

A belt moves resources **up and down** the tree, so it exists at two directory
levels at once. It is one belt, present at each end:

```
DEMO_001_Ore-Power/
├── Belt-001-a-i            top end,  1 slot
└── @Mining Station/
    └── Belt-001-b-i        deep end, 1 slot
```

This is why hop 2 in the example has **no `v`**. Nothing carried the ore
between the ends — the belt *is* the carrier, and the end letter changing from
`B` to `A` is the entire record of the traversal.

**Capacity is one slot per end.** That keeps the rule *"the roman numeral on a
folder is that folder's limit"* true with no exceptions, and it is the version
that can actually jam: a full end blocks the handoff, which is backpressure.

Numbering is global and starts from the top of the filetree, so `Belt-001` is
shallower than `Belt-002` regardless of what connects to what.

---

## The three mover classes

Each appears in the signature differently, and each is falsifiable a different
way. This is what makes the route *verified* rather than merely testified.

| Mover | In the signature | How the audit proves it |
|---|---|---|
| Inserter | `vI2` | `Inserter-002.md` exists in the lowest common parent of source and destination |
| Belt | end letter changes, no `v` | both ends carry the same belt number |
| Human | `wHAbGUY` | the ADRENALINE run log and the write probe |

Inserters and electric poles are **artifacts, not directories** — a file
sitting in the directory whose children it moves things between, enabling
horizontal movement there. Which is exactly why the claim `vI2` can be checked
against the filesystem instead of taken on faith.

### Power needs no field

Movement is gated on power, and an unpowered directory cannot move anything —
so an unpowered hop never happens and there is nothing to record. Absence is
the record. A `Powered:` field would only create somewhere to lie.

---

## The sequence numbers are load-bearing

`r1 r2 r3 r4` is the gap detector. Custody unaccounted for shows up as
`r1...r3...` with no `r2`, and no separate marker is needed.

Which means: **renumbering is forgery.** Nobody would guess that from looking
at the field names, so it is written down here.

---

## Reading the result

| `R-Check` | Means |
|---|---|
| ends `-e`, matches expected | counts toward the DoD |
| ends `-e`, does not match | arrived, but by an illegal path |
| no `-e` | never arrived — the last segment says how far it got |

The third row splits again by where the file physically sits: in a belt means
still in flight, in `CONSUMED/` means dead. **The string says how far, the
location says why it stopped.** The audit needs both.

`R-Check` is not an identity. Two pieces of ore that took the same path have
identical signatures, which is correct — the signature answers "was this route
legal", and `Session UUID` answers "which ore is this".

---

## Open

Genuinely undecided. Do not treat any of these as settled by omission.

| Question | Why it matters |
|---|---|
| Is `R-Check` ever **parsed**, or only ever **compared**? | If only compared, the grammar never has to be unambiguous. Uppercase codes make it unambiguous anyway, so this is now cheap either way — but it should be a decision, not an accident. |
| `R-Duration` — stamped by the script, or deleted? | It is derivable from `Origin Time` and `R-end`. An empty derivable field is somewhere for drift to live. Currently empty. |
| Does a **failed** hop get a segment? | Right now a failed hop appends nothing and the sequence gap is the record. That may be enough, or it may hide the difference between "never attempted" and "attempted and refused". |
| Where does the **expected literal** live? | Presumably `Schema/`, next to the rules that would compare against it. Not written yet. |
| Capacity enforcement | Roman numerals are machine-readable from folder names, so an over-full directory is checkable for free. No verb exists yet. |
| Tamper-evidence beyond agreement | Today a hand-typed but well-formed signature passes. A chained hash per hop would make that impossible. Not needed for Demo 001; noted as the cheap upgrade. |

---

## Naming

The filename of this document is the assistant's guess, not the operator's
decision. Rename it.
