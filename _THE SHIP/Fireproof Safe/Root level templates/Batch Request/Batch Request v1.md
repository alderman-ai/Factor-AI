
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

## This file is a cut, not the master

The master lives at
`_THE SHIP/Fireproof Safe/Root level templates/Batch Request/`, one subfolder
holding every version and a changelog. **Each batch starts by cutting a fresh
copy of the current version to the repo root.** The copy at root is disposable
and gets filled in; the master never is.

A finished batch is a Ship artifact. It archives to
`_THE SHIP/Fireproof Safe/Operator Inbox/Archived Intake Forms/` — retired
regardless of outcome, deferred slots and all. It is not overwritten by the
next batch.

---

# `R1`

`<operator_request>`
```

```
`</operator_request>`

## `P1`

`<assistant_proposal>`
```

```
`</assistant_proposal>`

### `A1`

`<operator_approval>`
- [ ] APPROVED: Execute
- [ ] APPROVED (Subagent): Delegate to a `(empty=default)` Model
- [ ] ADJUST: Adjust accordingly to instructions in fence below, but execute
- [ ] RETRY: Propose a new plan based on the in instructions in fence below (regenerate proposal)
- [ ] DEFER: We will deal with this later

```

```
`</operator_approval>`

---

# `R2`

`<operator_request>`
```

```
`</operator_request>`

## `P2`

`<assistant_proposal>`
```

```
`</assistant_proposal>`

### `A2`

`<operator_approval>`
- [ ] APPROVED: Execute
- [ ] APPROVED (Subagent): Delegate to a `(empty=default)` Model
- [ ] ADJUST: Adjust accordingly to instructions in fence below, but execute
- [ ] RETRY: Propose a new plan based on the in instructions in fence below (regenerate proposal)
- [ ] DEFER: We will deal with this later

```

```
`</operator_approval>`

---

# `R3`

`<operator_request>`
```

```
`</operator_request>`

## `P3`

`<assistant_proposal>`
```

```
`</assistant_proposal>`

### `A3`

`<operator_approval>`
- [ ] APPROVED: Execute
- [ ] APPROVED (Subagent): Delegate to a `(empty=default)` Model
- [ ] ADJUST: Adjust accordingly to instructions in fence below, but execute
- [ ] RETRY: Propose a new plan based on the in instructions in fence below (regenerate proposal)
- [ ] DEFER: We will deal with this later

```

```
`</operator_approval>`

---

# `R4`

`<operator_request>`
```

```
`</operator_request>`

## `P4`

`<assistant_proposal>`
```

```
`</assistant_proposal>`

### `A4`

`<operator_approval>`
- [ ] APPROVED: Execute
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

```
`</operator_request>`

## `P5`

`<assistant_proposal>`
```

```
`</assistant_proposal>`

### `A5`

`<operator_approval>`
- [ ] APPROVED: Execute
- [ ] APPROVED (Subagent): Delegate to a `(empty=default)` Model
- [ ] ADJUST: Adjust accordingly to instructions in fence below, but execute
- [ ] RETRY: Propose a new plan based on the in instructions in fence below (regenerate proposal)
- [ ] DEFER: We will deal with this later

```

```
`</operator_approval>`

---

# `R6`

`<operator_request>`
```

```
`</operator_request>`

## `P6`

`<assistant_proposal>`
```

```
`</assistant_proposal>`

### `A6`

`<operator_approval>`
- [ ] APPROVED: Execute
- [ ] APPROVED (Subagent): Delegate to a `(empty=default)` Model
- [ ] ADJUST: Adjust accordingly to instructions in fence below, but execute
- [ ] RETRY: Propose a new plan based on the in instructions in fence below (regenerate proposal)
- [ ] DEFER: We will deal with this later

```

```
`</operator_approval>`

---

# `R7`

`<operator_request>`
```

```
`</operator_request>`

## `P7`

`<assistant_proposal>`
```

```
`</assistant_proposal>`

### `A7`

`<operator_approval>`
- [ ] APPROVED: Execute
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

```
`</operator_request>`

## `P8`

`<assistant_proposal>`
```

```
`</assistant_proposal>`

### `A8`

`<operator_approval>`
- [ ] APPROVED: Execute
- [ ] APPROVED (Subagent): Delegate to a `(empty=default)` Model
- [ ] ADJUST: Adjust accordingly to instructions in fence below, but execute
- [ ] RETRY: Propose a new plan based on the in instructions in fence below (regenerate proposal)
- [ ] DEFER: We will deal with this later

```

```
`</operator_approval>`

---

# `R9`

`<operator_request>`
```

```
`</operator_request>`

## `P9`

`<assistant_proposal>`
```

```
`</assistant_proposal>`

### `A9`

`<operator_approval>`
- [ ] APPROVED: Execute
- [ ] APPROVED (Subagent): Delegate to a `(empty=default)` Model
- [ ] ADJUST: Adjust accordingly to instructions in fence below, but execute
- [ ] RETRY: Propose a new plan based on the in instructions in fence below (regenerate proposal)
- [ ] DEFER: We will deal with this later

```

```
`</operator_approval>`

---

# `R10`

`<operator_request>`
```

```
`</operator_request>`

## `P10`

`<assistant_proposal>`
```

```
`</assistant_proposal>`

### `A10`

`<operator_approval>`
- [ ] APPROVED: Execute
- [ ] APPROVED (Subagent): Delegate to a `(empty=default)` Model
- [ ] ADJUST: Adjust accordingly to instructions in fence below, but execute
- [ ] RETRY: Propose a new plan based on the in instructions in fence below (regenerate proposal)
- [ ] DEFER: We will deal with this later

```

```
`</operator_approval>`
