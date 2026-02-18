# skill-claim-update

## Overview
`skill_claim_update` is a transactional skill that allows controlled claim updates through approved write-capable tools under policy and HITL controls.

## Preconditions & Scope
- Request intent matches allowed claim-update intents.
- Caller and runtime identity pass policy checks.
- Write path is restricted to approved fields and approved environments.
- PHI boundary note: PHI may be processed in-system for authorized operations, but logs and traces must use redaction/minimization by default.
- Identity is established at session start (authenticated user / CSR context).
- Subject binding is required before any member/claim access:
  - Resolve `member_id` (and permitted dependents, if applicable) from the authenticated session/context or via explicit member lookup.
  - Validate the caller is authorized to act on the resolved `member_id`.
- If subject binding or authorization fails, the skill must stop and emit `subject_binding_failed` / `authz_denied`.

## Inputs
- Claim identifier and tenant/context identifier.
- Requested update fields (allowlisted only).
- Business rationale or action intent summary.
- Correlation context for audit and tracing.

## Outputs
- Structured execution outcome (success, denied, failed).
- Redacted summary of applied or rejected updates.
- Approval result metadata when HITL is required.
- Correlation reference for audit lookup.

## High-Level Steps
1. Subject Binding & Authorization
   - Resolve `member_id`/`claim_id` in scope for this request (from session context or explicit lookup).
   - Confirm the caller is authorized for the subject (member/claim) and requested operation.
   - If mismatch/unauthorized -> block execution and route to escalation/HITL per policy.
2. Resolve intent to `skill_claim_update` from approved skill allowlist.
3. Run policy checks for scope, role, data boundary, and allowed update fields.
4. Trigger HITL approval when required by risk and environment policy.
5. Execute approved write tool through contracted adapter.
6. Record outcome and emit observability/audit events.

## Allowed Tools
- Write-capable tools aligned to tool-contracts for claim updates.
- Read-back verification tools for post-execution confirmation.
- No direct free-form tool invocation outside the approved skill path.

## Approval & Controls
- HITL is required for production state-changing actions.
- Deny-by-default behavior applies if policy checks or approvals fail.
- Idempotency and replay protection are required for write execution.

## Observability Events
- intent_recognized
- skill_resolved
- policy_check_completed
- subject_binding_verified
- subject_binding_failed (or authz_denied)
- approval_requested / approval_decision
- tool_execution_started / tool_execution_completed
- safe_fallback_triggered

## Failure Modes & Safe Fallback
- Policy denied: no write execution; return constrained guidance.
- Approval denied/timeout: no write execution; route to manual follow-up.
- Tool failure/conflict: return deterministic failure and recommend retry/escalation path.
- Verification mismatch: mark as unresolved and escalate to reviewer.
