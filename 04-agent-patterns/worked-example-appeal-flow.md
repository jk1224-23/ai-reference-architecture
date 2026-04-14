# Worked Example: Appeal Initiation Flow

## User Request: "I want to appeal my claim decision"

This example traces a real request through the architecture, showing how policy, tools, and audit trail work together.

---

## Step 1: Intent Recognition

**User Input:**
```
"My claim was denied. I think the decision is wrong. I want to appeal."
```

**Orchestrator Analysis:**
```
intent: APPEAL_INITIATION
confidence: 0.94
subject_binding: claim:C-2024-001234
risk_tier: HIGH
```

**Why HIGH risk?**
- User is requesting a state-changing action (appeal creation)
- Touches sensitive data (claim decision)
- Creates official record
- Legal implications if approved incorrectly

---

## Step 2: Policy Decision (Before LLM Acts)

The orchestrator checks policy **before** the LLM generates a response.

**Policy Check:**
```yaml
intent: APPEAL_INITIATION
subject: member:M-789456
resource: claim:C-2024-001234

checks:
  ✓ User identity verified: true (OAuth + session binding)
  ✓ Subject binding valid: true (member owns this claim)
  ✓ Risk tier HIGH: true
  ✓ HITL required: true (because risk_tier == HIGH)
  ✓ Tool access check: case.create.v1 (allowlisted for this intent)
  
policy_decision: HITL_REQUIRED

routing:
  - Block LLM tool execution
  - Escalate to human queue
  - Wait for approval
```

**Key:** Policy gates access **before** LLM sees the request. No tool calls happen until HITL approves.

---

## Step 3: Observability Events (Logged Immediately)

```json
{
  "event_type": "intent_recognized",
  "timestamp": "2026-04-14T14:23:45.123Z",
  "trace_id": "tr-9f8d2e1c",
  "user_id": "member:M-789456",
  "claim_id": "claim:C-2024-001234",
  "intent": "APPEAL_INITIATION",
  "intent_confidence": 0.94,
  "risk_tier": "HIGH",
  "policy_decision": "HITL_REQUIRED",
  "orchestrator_version": "v2.1"
}
```

---

## Step 4: LLM Prepares Draft (With Constraints)

The LLM is instructed to prepare a draft appeal case, but **cannot** execute any tools.

**LLM Prompt (simplified):**
```
User wants to appeal their claim. 

Your job:
1. Summarize their concern in professional language
2. Identify which claim field they're appealing (decision? amount? coverage?)
3. Prepare a draft case summary for human review

IMPORTANT: Do NOT call any tools. A human will review and approve first.
```

**LLM Output (Draft):**
```
Appeal Case Draft:
- Claim ID: C-2024-001234
- Appeal Reason: Member disputes coverage determination
- Member Statement: "The denial was based on incorrect info. I was 
  covered under the plan at the time of service."
- Recommended Action: Create appeal case and notify member
```

---

## Step 5: Human Review & Approval

The support team sees:

**Context:**
```
Member: John Smith (M-789456)
Claim: Denied claim for emergency room visit
Amount: $4,500
Denial Reason: Out-of-network provider

Member's Appeal: "I was emergent. No in-network options available."
```

**LLM Draft:**
```
Proposed appeal case:
- Claim ID: C-2024-001234
- Reason: Coverage determination dispute
- Member Statement: [above]
```

**Policy Gate:**
```
🔴 REQUIRES HUMAN APPROVAL
Risk Tier: HIGH
Approval Type: HITL

Human must verify:
✓ Member identity confirmed
✓ Claim details accurate
✓ Appeal rationale reasonable
✓ No duplicate appeals pending
```

**Human Decision:**
Support agent reviews claim history, member record, and draft.
Clicks: **APPROVE**

**Approval Event:**
```json
{
  "event_type": "approval_decision",
  "timestamp": "2026-04-14T14:25:12.456Z",
  "trace_id": "tr-9f8d2e1c",
  "decision": "APPROVED",
  "approved_by": "support_agent:A-5432",
  "approval_type": "HITL",
  "claim_id": "claim:C-2024-001234",
  "reason": "Member entitled to emergency coverage exception"
}
```

---

## Step 6: Tool Execution (Now Allowed)

Once approved, the orchestrator routes to tool execution.

**Tool Call (Validated Before Execution):**
```json
{
  "tool": "case.create.v1",
  "call_id": "call-9f8d2e1c",
  
  "parameters": {
    "claim_id": "C-2024-001234",
    "case_type": "APPEAL",
    "priority": "NORMAL",
    "member_statement": "The denial was based on incorrect info...",
    "approver": "support_agent:A-5432",
    "approval_timestamp": "2026-04-14T14:25:12Z"
  },
  
  "validation": {
    "schema_version": "v1",
    "claim_id_valid": true,
    "case_type_allowlist": ["APPEAL"],
    "member_id_matches": true,
    "approval_token_valid": true
  }
}
```

**Execution Result:**
```json
{
  "status": "success",
  "case_id": "case:AP-2024-005678",
  "case_url": "https://system-of-record.internal/cases/AP-2024-005678",
  "member_notified": true,
  "next_step": "Appeal review team will contact within 5 business days"
}
```

---

## Step 7: Full Audit Trail (Immutable Record)

```json
[
  {
    "event": "intent_recognized",
    "time": "2026-04-14T14:23:45.123Z",
    "user": "member:M-789456",
    "action": "User requested appeal for claim C-2024-001234"
  },
  {
    "event": "policy_decision",
    "time": "2026-04-14T14:23:45.234Z",
    "decision": "HITL_REQUIRED",
    "reason": "risk_tier=HIGH"
  },
  {
    "event": "hitl_escalated",
    "time": "2026-04-14T14:23:45.345Z",
    "queue": "support_team",
    "priority": "NORMAL"
  },
  {
    "event": "approval_decision",
    "time": "2026-04-14T14:25:12.456Z",
    "approved_by": "support_agent:A-5432",
    "decision": "APPROVED"
  },
  {
    "event": "tool_called",
    "time": "2026-04-14T14:25:12.567Z",
    "tool": "case.create.v1",
    "case_id": "AP-2024-005678",
    "status": "success"
  },
  {
    "event": "member_notified",
    "time": "2026-04-14T14:25:13.678Z",
    "notification": "Appeal case created - AP-2024-005678"
  }
]
```

---

## What This Example Shows

### 1. **Policy Gates Tool Execution**
- Request comes in
- Policy checks BEFORE LLM acts
- HITL required → No tool call yet
- Human approves → Tool execution allowed

### 2. **LLM Doesn't Control Tools**
- LLM prepares draft (safe, constrained)
- LLM cannot execute tools
- Human validates before anything commits
- Tool execution is orchestrated, not by LLM

### 3. **Audit Trail Is Complete**
- Every step logged with timestamps
- User intent → Policy decision → Human approval → Tool execution
- Traceable for compliance
- Defensible in audit

### 4. **No Surprises**
- User knows appeal is being created
- Human verified it's correct
- System of record is updated
- Member is notified

---

## Alternative: Request Denied by Policy

If risk check **fails**, flow stops:

```json
{
  "event": "policy_decision",
  "time": "2026-04-14T14:23:45.234Z",
  "decision": "DENIED",
  "reason": "Duplicate appeal already pending",
  "user_message": "There is already an active appeal for this claim (case AP-2024-005123). Please wait for that review to complete."
}
```

**No HITL escalation. No tool execution. Policy stopped it.**

---

## Key Takeaway

This flow shows how **policy prevents problems** rather than relying on the LLM to make safe decisions.

- ✅ The LLM doesn't need to know policies (policy engine knows)
- ✅ The LLM can't bypass controls (orchestrator enforces)
- ✅ Humans have real control (approval gates matter)
- ✅ Everything is auditable (traces are complete)
