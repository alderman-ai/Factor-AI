# Instrument Panel

**The live cockpit.** What the ship is doing right now, and the durable tooling
that does it.

The Panel holds **exactly one live world form** — the world currently being
charted or flown. Every retired form is in `Atlas of Worlds/`, permanently. That
invariant is enforced by `Ignition Codes/chart_course.py`, which archives every
live form it finds before stamping the next one. Doing it by hand produces the
same directory listing and skips every refusal.

Right now there is no live form. We are between runs.

`INDEX.md` routes to what is here.
