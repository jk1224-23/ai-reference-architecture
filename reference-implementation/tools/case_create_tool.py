import time

def case_create(intent: dict, correlation_id: str) -> dict:
    start = time.time()
    dur = int((time.time() - start) * 1000)
    return {
        "toolName": "case.create.v1",
        "toolVersion": "v1",
        "requestId": f"t-{correlation_id}-case",
        "durationMs": dur,
        "result": "FAILURE",
        "errorCode": "SHOULD_HAVE_BEEN_BLOCKED",
        "inputSummary": {},
        "outputSummary": {}
    }
