"""THE VAST UNKNOWN — content-blind MCP engine skeleton.

The engine loads a cartridge it knows nothing about, validates it against
schema.json, and serves it. An invalid cartridge means the engine refuses
to boot — loudly, naming the precondition that failed and the state it
actually observed. Graceful degradation is failure-hiding with good manners.
"""

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from mcp.server import MCPServer

HERE = Path(__file__).resolve().parent
SCHEMA_PATH = HERE / "schema.json"
CARTRIDGE_PATH = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE / "cartridge.json"


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

mcp = MCPServer("THE VAST UNKNOWN")


@mcp.tool()
def scan(guy_handle: str) -> dict:
    """Report what the engine is serving. Placeholder verb — real verbs are undesigned.

    guy_handle is the acting guy's identity: a parameter on every call, never a
    process global (2026-07-28 spec — build it as a global and it dies when hosted).
    Accepted and echoed; unused until identity is designed.
    """
    return {
        "guy_handle": guy_handle,
        "object_count": len(WORLD["objects"]),
        "objects": WORLD["objects"],
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
