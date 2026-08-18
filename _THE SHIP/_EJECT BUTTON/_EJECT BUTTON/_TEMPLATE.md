---
# ROLLOUT SPEC — the handoff form across the engine/cartridge line.
# You fill this. It causes content you never read. v0 — redline freely.

rollout: 1                    # int, unique, sequential — the ledger counts rollouts, not hours
stage_name: ""                # string — the stage's visible name; your words
predecessor: null             # int or null — which rollout this builds on; items carry their own history

# --- what the stage is FOR ---
target_blind_spot: ""         # string — which operator improvement goal this stage attacks
objective: ""                 # string — observable win condition; falsifiable, like a rollout
failure_teaches: ""           # string — what a failed attempt should expose

# --- budgets the generator must respect ---
object_budget: 0              # int — max hidden things the assistant may generate
verb_budget: 0                # int — max new tools the stage may introduce
prose_budget_per_value: 4     # int — word cap on prose values inside generated content

# --- boundary rules ---
unlock_condition: ""          # string — what opens this stage; expressed as refusal, not absence
hard_constraints: []          # list of strings — rules the hidden content must obey; checked, not hoped
surprise_license: ""          # string — what the assistant may hide vs. must disclose up front
---

# Rollout intake

Fill the frontmatter above. Values only — the keys and comments are the
declared slots; touching anything else is the thing the cheat detector will
eventually exist for.

This form is meta-infrastructure: no prose budget applies here (operator
ruling, 2026-08-18). The budgets you *declare* above bind the generated
world content, not this document.

When filled, the extraction skill (not yet built — pending redline of this
template) validates every field and emits the JSON spec the engine's
cartridge generator consumes. You never see what it generates. That is the
point.
