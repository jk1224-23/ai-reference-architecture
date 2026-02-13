from pathlib import Path
import yaml

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


def decide_policy(intent: str, confidence: float, risk_tier: str, entities: dict, channel: str,
                 user_role: str, kill_switch_state: dict) -> dict:
    _ensure_loaded()

    reasons = []
    kill_switches_active = []

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

    if kill_switch_state.get("hitl_first_mode"):
        kill_switches_active.append("hitl_first_mode")
        reasons.append("KILL_SWITCH_HITL_FIRST")
        allowed_tools = [t["name"] for t in allowlist_entry.get("allowed_tools", [])]
        return {
            "decision": "ALLOW_HITL" if allowed_tools else "ALLOW",
            "allowedTools": allowed_tools,
            "hitlRequired": bool(allowed_tools),
            "reasons": reasons + ["ALLOWLIST_MATCH"],
            "killSwitchesActive": kill_switches_active,
        }

    if channel == "voice" and risk_tier in (_policy["channels"]["voice"]["confirmation_required_risk_tiers"]):
        reasons.append("VOICE_CONFIRMATION_REQUIRED")
        allowed_tools = [t["name"] for t in allowlist_entry.get("allowed_tools", [])]
        return {
            "decision": "ALLOW_WITH_CONFIRMATION",
            "allowedTools": allowed_tools,
            "hitlRequired": False,
            "reasons": reasons + ["ALLOWLIST_MATCH"],
            "killSwitchesActive": kill_switches_active,
        }

    if risk_tier == "HIGH":
        reasons.append("HIGH_RISK_INTENT")
        allowed_tools = [t["name"] for t in allowlist_entry.get("allowed_tools", [])]
        return {
            "decision": "ALLOW_HITL",
            "allowedTools": allowed_tools,
            "hitlRequired": True,
            "reasons": reasons + ["ALLOWLIST_MATCH"],
            "killSwitchesActive": kill_switches_active,
        }

    reasons.append("ALLOWLIST_MATCH")
    reasons.append("ROLE_OK")
    allowed_tools = [t["name"] for t in allowlist_entry.get("allowed_tools", [])]
    return {
        "decision": "ALLOW",
        "allowedTools": allowed_tools,
        "hitlRequired": False,
        "reasons": reasons,
        "killSwitchesActive": kill_switches_active,
    }
