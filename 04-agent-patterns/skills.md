# Agent Skills

## Definition
Agent Skill = bounded, versioned capability wrapper governing tool usage, data scope, approval, and observability.

## Why Skills Exist
- Prevent free-form tool invocation from unconstrained prompts.
- Enforce bounded autonomy through allowlisted capabilities.
- Centralize policy enforcement for approvals, data boundaries, and telemetry.

## Skill Categories
1. Read-only Skills (Flow A)
2. Transactional Skills (Flow B)

| Skill | Category | Allowed Tool Types | Human Approval? | Observability Events |
|---|---|---|---|---|
| `skill_kb_grounded_answer` | Read-only Skills (Flow A) | Knowledge search, document retrieval | No | intent_recognized, skill_resolved, retrieval_completed, response_emitted |
| `skill_provider_lookup` | Read-only Skills (Flow A) | Directory lookup, metadata query | No | intent_recognized, skill_resolved, tool_called, response_emitted |
| `skill_incident_context` | Read-only Skills (Flow A) | Ticket read, runbook search, health summary read | No | intent_recognized, skill_resolved, tool_called, citation_attached |
| `skill_claim_update` | Transactional Skills (Flow B) | Record update, status transition, note append | Yes | intent_recognized, skill_resolved, approval_requested, tool_called, outcome_recorded |
| `skill_change_request_submit` | Transactional Skills (Flow B) | Change draft/create/submit | Yes | intent_recognized, skill_resolved, approval_requested, tool_called, outcome_recorded |
| `skill_incident_assignment` | Transactional Skills (Flow B) | Assignment update, priority update | Conditional by risk policy | intent_recognized, skill_resolved, approval_decision, tool_called, outcome_recorded |

## Skill Lifecycle
- **Draft:** skill definition exists but is not executable in production paths.
- **Approved:** skill is allowlisted with explicit controls and observability requirements.
- **Deprecated:** skill remains traceable for audit but is removed from active invocation paths.
