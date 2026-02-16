def assemble_response(message: str, intent: dict, policy: dict, tool_calls: list[dict], channel: str) -> dict:
    decision = policy["decision"]
    intent_name = intent["intent"]

    if decision == "DENY":
        return {
            "responseType": "REFUSAL",
            "responseSummary": "Refused unsafe or unmapped request; no tool executed.",
            "message": "I can’t help with that request. If you need support, I can connect you to a representative."
        }

    if decision == "DEGRADED_KB_ONLY":
        return {
            "responseType": "KB_ONLY",
            "responseSummary": "KB-only mode active; tools disabled.",
            "message": "Tools are temporarily unavailable. I can still help with general policy/FAQ questions, or connect you to support for account-specific requests."
        }

    if decision == "ALLOW_WITH_CONFIRMATION":
        return {
            "responseType": "ESCALATION",
            "responseSummary": "Voice confirmation required before tool execution.",
            "message": "I can help, but I need to confirm the claim number first. Please repeat the claim ID."
        }

    if decision == "ALLOW_HITL" and policy.get("hitlRequired", False):
        success = next((t for t in tool_calls if t.get("result") == "SUCCESS"), None)
        if success:
            case_id = (success.get("outputSummary") or {}).get("caseId", "pending")
            status = (success.get("outputSummary") or {}).get("status", "PENDING_REVIEW")
            return {
                "responseType": "TOOL_BACKED",
                "responseSummary": "Transactional action executed after approval.",
                "message": f"Appeal case {case_id} created. Status: {status}.",
            }
        approval_id = policy.get("approvalId", "approval-required")
        return {
            "responseType": "ESCALATION",
            "responseSummary": "High-risk intent; execution blocked pending human approval.",
            "hitl": {"approvalRequired": True, "approvalId": approval_id, "approvalStatus": "PENDING"},
            "message": "I can draft this request, but a representative must approve it before submission. Provide the approval ID to proceed."
        }

    # Tool-backed SoR response (MVP: claim status only)
    if intent_name == "CLAIM_STATUS" and policy["decision"] == "ALLOW":
        success = next((t for t in tool_calls if t.get("result") == "SUCCESS"), None)
        if not success:
            return {
                "responseType": "ESCALATION",
                "responseSummary": "Tool evidence missing; did not assert SoR truth.",
                "message": "I can’t verify that right now because the system evidence wasn’t available. Please try again or contact support."
            }

        status = (success.get("outputSummary") or {}).get("status", "Unknown")
        last_updated = (success.get("outputSummary") or {}).get("lastUpdated", "")
        claim_id = (intent.get("entities") or {}).get("claimId")

        return {
            "responseType": "TOOL_BACKED",
            "responseSummary": "Returned claim status using tool evidence.",
            "message": f"Claim {claim_id} status: {status}. Last updated: {last_updated}."
        }

    return {
        "responseType": "KB_ONLY",
        "responseSummary": "Defaulted to safe response path.",
        "message": "I can help with general questions, or connect you to support for account-specific requests."
    }
