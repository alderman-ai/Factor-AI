# Root level templates

**Masters for the files that live at repo root.**

A root-level file like `Batch Request.md` gets filled in during use, so the copy
at root is disposable and the master is here. Each batch starts by cutting a
fresh copy from this folder.

## The shape

**One subfolder per template, never a single loose file.** The subfolder holds
every version of that template plus its changelog:

    Root level templates/
      Batch Request/
        Batch Request v1.md
        CHANGELOG.md

Versions accrete. An old version is never overwritten or deleted — the reason a
template changed is usually more interesting than the change.

## What this is not

`Hitchhiker's Guide/Schema/` holds the master forms that **scripts consume** —
`New World Coordinates.md` is stamped onto the Instrument Panel by
`chart_course.py`, and `enter_hyperspeed.py` validates the filled result against
a schema. Those are machine contracts. Break one and a script refuses.

These are documents a **human fills in by hand**. Nothing validates them.

`Hitchhiker's Guide/Templates/` is a third thing and is deliberately untouched
for now, per operator instruction.
