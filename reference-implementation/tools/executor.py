from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from tools.claims_read_tool import claims_read
from tools.case_create_tool import case_create
from tools.registry import load_tool_registry


@dataclass
class ToolExecutionError(Exception):
    code: str
    message: str


def execute_tools(
    *,
    policy: dict,
    intent: dict,
    tool_requests: list[dict] | None,
    approval_id: str | None = None,
) -> list[dict]:
    """
    Executes tool calls ONLY if policy allows it.

    MVP Option-A:
      - claims.read.v1 (READ_ONLY) : allowed for CLAIM_STATUS
      - case.create.v1 (TRANSACTIONAL) : allowed only with HITL + approvalId
    """
    tool_requests = tool_requests or []

    # If policy denies or is KB-only, do not execute anything.
    decision = policy.get("decision")
    if decision in ("DENY", "DEGRADED_KB_ONLY"):
        return []

    allowed = set(policy.get("allowedTools", []))
    if not allowed:
        return []

    registry = load_tool_registry()  # reads tools/tool_registry.json

    # MVP: only allow execution for tools present in registry (hard safety)
    registry_tools = {t["name"]: t for t in registry.get("tools", [])}

    results: list[dict] = []

    for req in tool_requests:
        tool_name = req.get("name")
        tool_input = req.get("input") or {}

        # Basic request validation
        if not tool_name:
            results.append(_tool_event_blocked(None, "VALIDATION_ERROR", "Missing tool name"))
            continue

        if tool_name not in allowed:
            results.append(_tool_event_blocked(tool_name, "AUTHZ_DENIED", "Tool not allowed by policy"))
            continue

        meta = registry_tools.get(tool_name)
        if not meta:
            results.append(_tool_event_blocked(tool_name, "VALIDATION_ERROR", "Tool not found in registry"))
            continue

        # Transactional tools require approvalId (HITL binding)
        if meta.get("type") == "TRANSACTIONAL":
            if not approval_id:
                results.append(
                    _tool_event_blocked(
                        tool_name,
                        "HITL_APPROVAL_REQUIRED",
                        "Transactional tool requires approvalId (HITL).",
                    )
                )
                continue
            # bind approvalId into tool input if not already included
            tool_input = dict(tool_input)
            tool_input.setdefault("approvalId", approval_id)

        # Execute
        try:
            output = _dispatch(tool_name, tool_input)
            results.append(
                {
                    "name": tool_name,
                    "result": "SUCCESS",
                    "outputSummary": output,
                }
            )
        except ToolExecutionError as e:
            results.append(_tool_event_failed(tool_name, e.code, e.message))
        except Exception as e:  # safe fallback
            results.append(_tool_event_failed(tool_name, "UNKNOWN", str(e)))

    return results


def _dispatch(tool_name: str, tool_input: dict[str, Any]) -> dict[str, Any]:
    """
    MVP Option-A dispatcher. Only two tools exist.
    """
    if tool_name == "claims.read.v1":
        _require(tool_input, ["claimId"])
        return claims_read(claim_id=tool_input["claimId"])

    if tool_name == "case.create.v1":
        _require(tool_input, ["subject", "description", "claimId", "approvalId"])
        return case_create(
            subject=tool_input["subject"],
            description=tool_input["description"],
            claim_id=tool_input["claimId"],
            approval_id=tool_input["approvalId"],
        )

    raise ToolExecutionError("VALIDATION_ERROR", f"Unknown tool: {tool_name}")


def _require(payload: dict[str, Any], keys: list[str]) -> None:
    missing = [k for k in keys if not payload.get(k)]
    if missing:
        raise ToolExecutionError("VALIDATION_ERROR", f"Missing required inputs: {', '.join(missing)}")


def _tool_event_blocked(tool_name: str | None, code: str, message: str) -> dict:
    return {
        "name": tool_name or "UNKNOWN",
        "result": "BLOCKED",
        "error": {"code": code, "message": message},
    }


def _tool_event_failed(tool_name: str, code: str, message: str) -> dict:
    return {
        "name": tool_name,
        "result": "FAILED",
        "error": {"code": code, "message": message},
    }
