import time

def claims_read(claim_id: str) -> dict:
    start = time.time()
    if not claim_id:
        return {
            "name": "claims.read.v1",
            "result": "FAILED",
            "error": {"code": "VALIDATION_ERROR", "message": "Missing claimId"},
        }

    status = "Processed"
    last_updated = "2026-02-10"
    dur = int((time.time() - start) * 1000)
    return {
        "status": status,
        "lastUpdated": last_updated,
        "durationMs": dur,
    }
