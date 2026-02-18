from pathlib import Path

import yaml

from app.subject_binding import verify_subject_binding

BASE_DIR = Path(__file__).resolve().parents[1]
POLICY_PATH = BASE_DIR / "config" / "policy_rules.yaml"
ALLOWLIST_PATH = BASE_DIR / "config" / "tool_allowlist.yaml"

_policy = None
_allowlist = None


def _load_yaml(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _ensure_loaded():
    global _policy, _allowlist
    if _policy is None:
        _policy = _load_yaml(POLICY_PATH)
    if _allowlist is None:
        _allowlist = _load_yaml(ALLOWLIST_PATH)


def _extract_allowed_tools(entry: dict) -> list[str]:
    return [t["name"] for t in entry.get("allowed_tools", []) if t.get("name")]


def _apply_tool_circuit_breakers(
    *,
    allowed_tools: list[str],
    kill_switch_state: dict,
    reasons: list[str],
    kill_switches_active: list[str],
) -> list[str]:
    breakers = kill_switch_state.get("tool_circuit_breakers") or {}
    if not breakers:
        return allowed_tools

    filtered: list[str] = []
    for tool_name in allowed_tools:
        if breakers.get(tool_name):
            reasons.append(f"TOOL_CIRCUIT_BREAKER_ACTIVE:{tool_name}")
            kill_switches_active.append(f"tool_circuit_breaker:{tool_name}")
            continue
        filtered.append(tool_name)
    return filtered


def decide_policy(
    intent: str,
    confidence: float,
    risk_tier: str,
    entities: dict,
    channel: str,
    user_role: str,
    user_id: str,
    kill_switch_state: dict,
) -> dict:
    _ensure_loaded()

    reasons: list[str] = []
    kill_switches_active: list[str] = []

    if kill_switch_state.get("kb_only_mode"):
        kill_switches_active.append("kb_only_mode")
        reasons.append("KILL_SWITCH_KB_ONLY")
        return {
            "decision": "DEGRADED_KB_ONLY",
            "allowedTools": [],
            "hitlRequired": False,
            "reasons": reasons,
            "killSwitchesActive": kill_switches_active,
        }

    allowlist_entry = (_allowlist.get("intents") or {}).get(intent)
    if not allowlist_entry:
        reasons.append("DENY_BY_DEFAULT_NO_MAPPING")
        return {
            "decision": "DENY",
            "allowedTools": [],
            "hitlRequired": False,
            "reasons": reasons,
            "killSwitchesActive": kill_switches_active,
        }

    subject_binding = verify_subject_binding(
        intent=intent,
        entities=entities or {},
        user_id=user_id,
        user_role=user_role,
    )
    if not subject_binding.get("verified", False):
        reasons.extend(
            [
                "SUBJECT_BINDING_REQUIRED",
                str(subject_binding.get("reason", "SUBJECT_BINDING_FAILED")),
            ]
        )
        return {
            "decision": "DENY",
            "allowedTools": [],
            "hitlRequired": False,
            "reasons": reasons,
            "killSwitchesActive": kill_switches_active,
            "subjectBinding": subject_binding,
        }

    if subject_binding.get("required"):
        reasons.append("SUBJECT_BINDING_VERIFIED")

    base_allowed_tools = _extract_allowed_tools(allowlist_entry)
    allowed_tools = _apply_tool_circuit_breakers(
        allowed_tools=base_allowed_tools,
        kill_switch_state=kill_switch_state,
        reasons=reasons,
        kill_switches_active=kill_switches_active,
    )
    if base_allowed_tools and not allowed_tools:
        reasons.append("NO_TOOLS_AVAILABLE_AFTER_CIRCUIT_BREAKER")
        return {
            "decision": "DENY",
            "allowedTools": [],
            "hitlRequired": False,
            "reasons": reasons,
            "killSwitchesActive": kill_switches_active,
            "subjectBinding": subject_binding,
        }

    if kill_switch_state.get("hitl_first_mode"):
        kill_switches_active.append("hitl_first_mode")
        reasons.extend(["KILL_SWITCH_HITL_FIRST", "ALLOWLIST_MATCH"])
        return {
            "decision": "ALLOW_HITL" if allowed_tools else "ALLOW",
            "allowedTools": allowed_tools,
            "hitlRequired": bool(allowed_tools),
            "reasons": reasons,
            "killSwitchesActive": kill_switches_active,
            "subjectBinding": subject_binding,
        }

    if channel == "voice" and risk_tier in _policy["channels"]["voice"]["confirmation_required_risk_tiers"]:
        reasons.extend(["VOICE_CONFIRMATION_REQUIRED", "ALLOWLIST_MATCH"])
        return {
            "decision": "ALLOW_WITH_CONFIRMATION",
            "allowedTools": allowed_tools,
            "hitlRequired": False,
            "reasons": reasons,
            "killSwitchesActive": kill_switches_active,
            "subjectBinding": subject_binding,
        }

    if risk_tier == "HIGH":
        reasons.extend(["HIGH_RISK_INTENT", "ALLOWLIST_MATCH"])
        return {
            "decision": "ALLOW_HITL",
            "allowedTools": allowed_tools,
            "hitlRequired": True,
            "reasons": reasons,
            "killSwitchesActive": kill_switches_active,
            "subjectBinding": subject_binding,
        }

    reasons.extend(["ALLOWLIST_MATCH", "ROLE_OK"])
    return {
        "decision": "ALLOW",
        "allowedTools": allowed_tools,
        "hitlRequired": False,
        "reasons": reasons,
        "killSwitchesActive": kill_switches_active,
        "subjectBinding": subject_binding,
    }
