# MVP: hardcoded toggles.
# Later: read from config/env/feature flags.

def get_kill_switch_state() -> dict:
    return {
        "kb_only_mode": False,
        "hitl_first_mode": False,
        "tool_circuit_breakers": {}  # e.g., {"claims.read.v1": True}
    }
