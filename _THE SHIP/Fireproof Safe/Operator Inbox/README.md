# Operator Inbox

**Where the assistant puts documents the operator has to fill out.**

An intake form, a question set, a coordinates form waiting on a decision — the
assistant writes it here and stops. Nothing here is answered by the assistant.

The flow is one direction with two stops:

    assistant writes  ──▶  Operator Inbox/  ──▶  Archived Intake Forms/
                            (live, waiting)        (dealt with)

A form is live while it sits in this folder. Once it has been ruled on — however
it was ruled, including "no" — it moves down to `Archived Intake Forms/`.

Nothing is deleted. A form that was answered badly is the most useful kind of
record this project produces.

## Note on live forms at repo root

`Batch Request.md` is a live operator form and it currently sits at repo root,
not here, because a batch is worked from root during the session that runs it.
Its master template lives in `Root level templates/Batch Request/`, and the
finished copy archives into `Archived Intake Forms/`. This inbox holds the
forms that wait; root holds the one being worked.
