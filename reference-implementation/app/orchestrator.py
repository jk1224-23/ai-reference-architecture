from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.intent_classifier import classify_intent
from app.policy_engine import decide_policy
from tools.executor import execute_tools
from app.response_assembler import assemble_response
from app.audit_logger import write_audit_event
from app.kill_switches import get_kill_switch_state


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def handle_request(
    message: str,
    channel: str,
    user_role: str,
    user_id: str,
    session_id: str,
    approval_id: str | None = None,
):
    correlation_id = f"c-{uuid.uuid4().hex[:8]}"
    request_id = f"r-{uuid.uuid4().hex[:8]}"
    timestamp = utc_now_iso()

    kill_switch_state = get_kill_switch_state()

    # 1) intent classification
    intent_result = classify_intent(message=message, channel=channel)

    # 2) deterministic policy decision
    policy_result = decide_policy(
        intent=intent_result["intent"],
        confidence=float(intent_result["confidence"]),
        risk_tier=intent_result["riskTier"],
        entities=intent_result.get("entities", {}),
        channel=channel,
        user_role=user_role,
        user_id=user_id,
        kill_switch_state=kill_switch_state,
    )

    if policy_result.get("hitlRequired"):
        policy_result["approvalId"] = approval_id or f"apr-{request_id}"
        if approval_id:
            policy_result.setdefault("reasons", []).append("HITL_APPROVAL_PROVIDED")

    # 3) prepare tool requests (only for allowed tools)
    tool_requests = []
    entities = intent_result.get("entities", {}) or {}
    claim_id = entities.get("claimId")
    for tool_name in policy_result.get("allowedTools", []):
        if tool_name == "claims.read.v1":
            tool_requests.append({"name": tool_name, "input": {"claimId": claim_id}})
        elif tool_name == "case.create.v1":
            tool_requests.append(
                {
                    "name": tool_name,
                    "input": {
                        "subject": "Appeal request",
                        "description": message,
                        "claimId": claim_id,
                    },
                }
            )

    # 4) tool execution (only if allowed)
    tool_calls = execute_tools(
        policy=policy_result,
        intent=intent_result,
        tool_requests=tool_requests,
        approval_id=approval_id,
        kill_switch_state=kill_switch_state,
    )

    # 5) response assembly (evidence-first)
    response = assemble_response(
        message=message,
        intent=intent_result,
        policy=policy_result,
        tool_calls=tool_calls,
        channel=channel,
    )

    # 6) audit event
    audit_event = {
        "correlationId": correlation_id,
        "requestId": request_id,
        "timestamp": timestamp,
        "channel": channel,
        "actor": {
            "userRole": user_role,
            "userIdHash": _hash_user(user_id),
            "sessionId": session_id,
        },
        "intent": {
            "name": intent_result["intent"],
            "confidence": float(intent_result["confidence"]),
            "riskTier": intent_result["riskTier"],
            "entities": intent_result.get("entities", {}),
        },
        "policy": {
            "decision": policy_result["decision"],
            "reasons": policy_result.get("reasons", []),
            "allowedTools": policy_result.get("allowedTools", []),
            "hitlRequired": bool(policy_result.get("hitlRequired", False)),
            "approvalId": policy_result.get("approvalId"),
            "killSwitchesActive": policy_result.get("killSwitchesActive", []),
        },
        "toolCalls": tool_calls,
        "outcome": {
            "responseType": response["responseType"],
            "responseSummary": response.get("responseSummary", ""),
            "citations": response.get("citations", []),
            "killSwitchesActive": policy_result.get("killSwitchesActive", []),
        },
    }

    subject_binding = policy_result.get("subjectBinding")
    if subject_binding:
        audit_event["subjectBinding"] = subject_binding

    if "hitl" in response:
        audit_event["hitl"] = response["hitl"]

    write_audit_event(audit_event)

    return {
        "correlationId": correlation_id,
        "intent": audit_event["intent"],
        "policy": audit_event["policy"],
        "toolCalls": tool_calls,
        "response": {
            "message": response["message"],
            "responseType": response["responseType"],
            "responseSummary": response.get("responseSummary", ""),
        },
        "audit": {
            "correlationId": correlation_id,
            "requestId": request_id,
            "timestamp": timestamp,
        },
    }


def _hash_user(user_id: str) -> str:
    import hashlib

    return "uHash-" + hashlib.sha256(user_id.encode("utf-8")).hexdigest()[:8]
