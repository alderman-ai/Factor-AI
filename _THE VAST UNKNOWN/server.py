"""THE VAST UNKNOWN — content-blind MCP engine.

The engine loads a cartridge it knows nothing about, validates it against
schema.json, and serves it. An invalid cartridge means the engine refuses
to boot — loudly, naming the precondition that failed and the state it
actually observed. Graceful degradation is failure-hiding with good manners.

State is an append-only journal beside the run's crash site ("Run NNN
State.json"). Every mutating tool call writes through immediately — there
is no save ritual because saving is never an act. Current state = cartridge
replayed through the journal. Derivable values are computed on read, never
stored.
"""

import datetime
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from mcp.server import MCPServer

HERE = Path(__file__).resolve().parent
SCHEMA_PATH = HERE / "schema.json"
CARTRIDGE_PATH = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE / "cartridge.json"
VAULT_SPAWN_ROOT = HERE.parent / "_THE SHIP"


def refuse(precondition: str, observed: str) -> None:
    print(
        f"BOOT REFUSED\n  precondition: {precondition}\n  observed: {observed}",
        file=sys.stderr,
    )
    sys.exit(1)


def load_world() -> dict:
    if not SCHEMA_PATH.is_file():
        refuse("schema.json exists next to the engine", f"no file at {SCHEMA_PATH}")
    if not CARTRIDGE_PATH.is_file():
        refuse("a cartridge file exists", f"no file at {CARTRIDGE_PATH}")
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        refuse("schema.json parses as JSON", str(e))
    try:
        cartridge = json.loads(CARTRIDGE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        refuse(f"{CARTRIDGE_PATH.name} parses as JSON", str(e))
    errors = sorted(
        Draft202012Validator(schema).iter_errors(cartridge),
        key=lambda e: list(e.absolute_path),
    )
    if errors:
        observed = "; ".join(
            f"at /{'/'.join(map(str, e.absolute_path))}: {e.message}" for e in errors
        )
        refuse("cartridge conforms to schema.json", observed)
    return cartridge


WORLD = load_world()
RUN = WORLD["run"]
STATE_PATH = HERE / "Crash Sites" / f"Run {RUN:03d} State.json"


def load_journal() -> list:
    if not STATE_PATH.is_file():
        return []
    try:
        journal = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        refuse(f"{STATE_PATH.name} parses as JSON", str(e))
    if not isinstance(journal, list):
        refuse(f"{STATE_PATH.name} is an append-only event list", f"parsed as {type(journal).__name__}")
    return journal


def replay(journal: list) -> None:
    by_name = {o["Name"]: o for o in WORLD["objects"]}
    for i, ev in enumerate(journal):
        if ev.get("event") == "discovered":
            obj = by_name.get(ev.get("Name"))
            if obj is None:
                refuse(
                    "every journal event references a thing in the cartridge",
                    f"event {i} discovered {ev.get('Name')!r}, not in cartridge",
                )
            obj["Visible"] = "Yes"


JOURNAL = load_journal()
replay(JOURNAL)


def record(event: dict) -> None:
    event["seq"] = len(JOURNAL) + 1
    event["at"] = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    JOURNAL.append(event)
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(JOURNAL, indent=2) + "\n", encoding="utf-8")


def spawn(obj: dict) -> Path:
    """A discovered thing materialises in the vault. Name with an extension
    is a file; without one, a folder (seeded with .gitkeep so git can see it)."""
    dest = VAULT_SPAWN_ROOT / obj["Name"]
    if dest.exists():
        raise ValueError(
            f"REFUSED — precondition: spawn path is free; observed: {dest} already exists"
        )
    if Path(obj["Name"]).suffix:
        dest.touch()
    else:
        dest.mkdir(parents=True)
        (dest / ".gitkeep").touch()
    return dest


mcp = MCPServer("THE VAST UNKNOWN")


@mcp.tool()
def scan(guy_handle: str) -> dict:
    """Sensor sweep. Reports things the guy has discovered; hidden things show
    only as a contact count — the fog stays behind this process.

    guy_handle is the acting guy's identity: a parameter on every call, never a
    process global (2026-07-28 spec — build it as a global and it dies when hosted).
    Accepted and echoed; unused until identity is designed.
    """
    visible = [o for o in WORLD["objects"] if o["Visible"] == "Yes"]
    return {
        "guy_handle": guy_handle,
        "run": RUN,
        "visible": visible,
        "unknown_contacts": len(WORLD["objects"]) - len(visible),
    }


@mcp.tool()
def observe(guy_handle: str) -> dict:
    """Investigate the nearest unknown contact. Discovery is irreversible:
    the thing flips Visible, materialises in the vault, and the journal
    records the event — all in this one call, no save step."""
    hidden = [o for o in WORLD["objects"] if o["Visible"] == "No"]
    if not hidden:
        raise ValueError(
            "REFUSED — precondition: at least one unknown contact on sensors; "
            "observed: everything in this world is already discovered"
        )
    target = hidden[0]
    dest = spawn(target)
    target["Visible"] = "Yes"
    record({"event": "discovered", "Name": target["Name"], "guy_handle": guy_handle})
    return {
        "guy_handle": guy_handle,
        "discovered": target,
        "spawned": str(dest),
        "unknown_contacts": len(hidden) - 1,
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
