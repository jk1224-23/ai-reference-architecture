# Minimal Reference Implementation Plan (Control Plane MVP)

## Goal
Prove the **controls** (policy gating, allowlists, HITL binding, audit) with the smallest runnable system.

## Recommended structure
```

reference-implementation/
README.md
DEMO.md
runbook.md
config/
policy_rules.yaml
tool_allowlist.yaml
app/
main.py
orchestrator.py
intent_classifier.py
policy_engine.py
response_assembler.py
audit_logger.py
kill_switches.py
tools/
registry.py
executor.py
claims_read_tool.py
case_create_tool.py
tool_registry.json
eval/
golden_set.json
red_team.json
logs/
audit_event_schema.json
sample_audit_events.jsonl

````

## Core interfaces (contracts)

### 1) Intent classifier
**Input:** user_message, channel, user_role  
**Output:**
```json
{ "intent": "CLAIM_STATUS", "confidence": 0.84, "riskTier": "MEDIUM", "entities": {"claimId":"..."} }
````

Rules: low confidence or missing critical entity → clarification or escalate.

### 2) Policy engine (deterministic)

**Input:** intent, riskTier, userRole, channel, entities, killSwitchState
**Output:**

```json
{
  "decision": "ALLOW",
  "allowedTools": ["claims.read.v1"],
  "hitlRequired": false,
  "reasonCodes": ["ALLOWLIST_MATCH", "ROLE_OK"]
}
```

Hard rules:

* deny-by-default if no mapping
* HITL required if riskTier=HIGH or transactional tool
* voice channel requires confirmation step for medium/high risk

### 3) Tool registry + executor

**Tool metadata required:**

* name/version, type (READ_ONLY/TRANSACTIONAL), sensitivity, idempotency, schema
* timeouts, rate limits

**Execution rule:** executor validates schema + checks policy decision before calling tool.

Transactional tool **must** require:

* `approvalId` (or deny)

### 4) Future (post-MVP): RAG service

RAG is intentionally out-of-scope for the MVP control-plane. Add after the tool gating + audit path is locked.

## Key files

* `config/policy_rules.yaml` — deterministic policy rules + kill switches
* `config/tool_allowlist.yaml` — deny-by-default allowlist for tool usage
* `tools/tool_registry.json` — structured tool metadata (contract enforcement)
* `logs/audit_event_schema.json` — audit event schema
* `logs/sample_audit_events.jsonl` — sample audit events

