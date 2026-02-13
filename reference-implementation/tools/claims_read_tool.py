import time

def claims_read(intent: dict, correlation_id: str) -> dict:
    start = time.time()
    claim_id = (intent.get("entities") or {}).get("claimId")
    if not claim_id:
        return {
            "toolName": "claims.read.v1",
            "toolVersion": "v1",
            "requestId": f"t-{correlation_id}-claims",
            "durationMs": 0,
            "result": "FAILURE",
            "errorCode": "VALIDATION_ERROR",
            "inputSummary": {},
            "outputSummary": {}
        }

    status = "Processed"
    last_updated = "2026-02-10"

    dur = int((time.time() - start) * 1000)
    return {
        "toolName": "claims.read.v1",
        "toolVersion": "v1",
        "requestId": f"t-{correlation_id}-claims",
        "durationMs": dur,
        "result": "SUCCESS",
        "errorCode": "",
        "inputSummary": {"claimId": claim_id},
        "outputSummary": {"status": status, "lastUpdated": last_updated}
    }
