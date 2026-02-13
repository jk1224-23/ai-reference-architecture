import json
import sys
from pathlib import Path

from jsonschema import validate  # pip install jsonschema


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "tools" / "tool_registry.json"
SCHEMA = ROOT / "standards" / "schemas" / "tool-contract.schema.json"


def main() -> int:
    if not REGISTRY.exists():
        print(f"ERROR: Missing tool registry: {REGISTRY}")
        return 2
    if not SCHEMA.exists():
        print(f"ERROR: Missing schema: {SCHEMA}")
        return 2

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

    validate(instance=registry, schema=schema)

    tool_names = [t["name"] for t in registry.get("tools", [])]
    if len(tool_names) != len(set(tool_names)):
        dupes = sorted({n for n in tool_names if tool_names.count(n) > 1})
        print(f"ERROR: Duplicate tool names found: {dupes}")
        return 2

    print("OK: tool_registry.json matches the Tool Contract schema.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
