# skill-claim-update

## Overview
`skill_claim_update` is a transactional skill that allows controlled claim updates through approved write-capable tools under policy and HITL controls.

## Preconditions & Scope
- Request intent matches allowed claim-update intents.
- Caller and runtime identity pass policy checks.
- Write path is restricted to approved fields and approved environments.
- PHI boundary note: PHI may be processed in-system for authorized operations, but logs and traces must use redaction/minimization by default.

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
1. Resolve intent to `skill_claim_update` from approved skill allowlist.
2. Run policy checks for scope, role, data boundary, and allowed update fields.
3. Trigger HITL approval when required by risk and environment policy.
4. Execute approved write tool through contracted adapter.
5. Record outcome and emit observability/audit events.

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
- approval_requested / approval_decision
- tool_execution_started / tool_execution_completed
- safe_fallback_triggered

## Failure Modes & Safe Fallback
- Policy denied: no write execution; return constrained guidance.
- Approval denied/timeout: no write execution; route to manual follow-up.
- Tool failure/conflict: return deterministic failure and recommend retry/escalation path.
- Verification mismatch: mark as unresolved and escalate to reviewer.
