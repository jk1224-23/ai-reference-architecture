from tools.registry import get_tool
from tools.claims_read_tool import claims_read
from tools.case_create_tool import case_create

TOOL_IMPLS = {
    "claims.read.v1": claims_read,
    "case.create.v1": case_create,
}

def execute_tools_if_allowed(policy: dict, intent: dict, user_role: str, channel: str, correlation_id: str) -> list[dict]:
    decision = policy["decision"]
    allowed_tools = policy.get("allowedTools", [])

    if decision in ("DENY", "DEGRADED_KB_ONLY"):
        return []

    if decision == "ALLOW_WITH_CONFIRMATION":
        return [{
            "toolName": "(none)",
            "toolVersion": "",
            "requestId": "",
            "durationMs": 0,
            "result": "BLOCKED",
            "errorCode": "CONFIRMATION_REQUIRED",
            "inputSummary": {},
            "outputSummary": {}
        }]

    tool_calls = []
    for tool_name in allowed_tools:
        meta = get_tool(tool_name)
        if not meta:
            tool_calls.append({
                "toolName": tool_name,
                "toolVersion": "",
                "requestId": "",
                "durationMs": 0,
                "result": "FAILURE",
                "errorCode": "TOOL_NOT_REGISTERED",
                "inputSummary": {},
                "outputSummary": {}
            })
            continue

        impl = TOOL_IMPLS.get(tool_name)
        if not impl:
            tool_calls.append({
                "toolName": tool_name,
                "toolVersion": "v1",
                "requestId": "",
                "durationMs": 0,
                "result": "FAILURE",
                "errorCode": "TOOL_NOT_IMPLEMENTED",
                "inputSummary": {},
                "outputSummary": {}
            })
            continue

        if meta.get("type") == "TRANSACTIONAL" and policy.get("hitlRequired", False):
            tool_calls.append({
                "toolName": tool_name,
                "toolVersion": "v1",
                "requestId": "",
                "durationMs": 0,
                "result": "BLOCKED",
                "errorCode": "APPROVAL_REQUIRED",
                "inputSummary": intent.get("entities", {}),
                "outputSummary": {}
            })
            continue

        result = impl(intent=intent, correlation_id=correlation_id)
        tool_calls.append(result)

    return tool_calls
