import time


def case_create(subject: str, description: str, claim_id: str, approval_id: str) -> dict:
    """Mock transactional tool requiring approvalId."""
    start = time.time()

    if not approval_id:
        return {
            "result": "BLOCKED",
            "error": {"code": "HITL_APPROVAL_REQUIRED", "message": "approvalId required"},
        }

    case_id = f"CASE-{claim_id or 'unknown'}"
    dur = int((time.time() - start) * 1000)
    return {
        "caseId": case_id,
        "status": "PENDING_REVIEW",
        "durationMs": dur,
        "subject": subject,
        "description": description,
    }
