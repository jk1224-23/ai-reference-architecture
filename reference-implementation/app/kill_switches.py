from __future__ import annotations

import os


def _as_bool(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_tool_breakers(raw_value: str | None) -> dict:
    """
    Supports comma-separated tool names:
    AI_TOOL_CIRCUIT_BREAKERS=claims.read.v1,case.create.v1
    """
    if not raw_value:
        return {}
    tools = [t.strip() for t in raw_value.split(",") if t.strip()]
    return {tool_name: True for tool_name in tools}


def get_kill_switch_state() -> dict:
    return {
        "kb_only_mode": _as_bool(os.getenv("AI_KB_ONLY_MODE")),
        "hitl_first_mode": _as_bool(os.getenv("AI_HITL_FIRST_MODE")),
        "tool_circuit_breakers": _parse_tool_breakers(os.getenv("AI_TOOL_CIRCUIT_BREAKERS")),
    }
