# Agent Skills

## Definition
Agent Skill = bounded, versioned capability wrapper governing tool usage, data scope, approval, and observability.

## Why Skills Exist
- Prevent free-form tool invocation from unconstrained prompts.
- Enforce bounded autonomy through allowlisted capabilities.
- Centralize policy enforcement for approvals, data boundaries, and telemetry.

## Skill Metadata for Tiered Execution
- Each Skill declares: risk_tier, default_model, requires_hitl, max_tokens, top_k.
- Intent detection selects the Skill; the Skill determines the tier.
- A deterministic Model Router applies tier-based policy (model selection, caps, degraded-mode actions).
- The LLM does not choose tools or models directly; execution is gated by Skill policy.

## Skill Categories
1. Read-only Skills (Flow A)
2. Transactional Skills (Flow B)

Canonical naming convention: `skill.<name>.v<N>` (dot notation, versioned). All skill definitions and configs must use this form.

| Skill | Category | Allowed Tool Types | Human Approval? | Observability Events |
|---|---|---|---|---|
| `skill.kb_grounded_answer.v1` | Read-only (Flow A) | Knowledge search, document retrieval | No | intent_recognized, skill_resolved, retrieval_completed, citation_attached, response_emitted |
| `skill.claim_status_lookup.v1` | Read-only (Flow A) | Claim record read | No | intent_recognized, skill_resolved, tool_called, response_emitted |
| `skill.provider_lookup.v1` | Read-only (Flow A) | Directory lookup, metadata query | No | intent_recognized, skill_resolved, tool_called, response_emitted |
| `skill.incident_context.v1` | Read-only (Flow A) | Ticket read, runbook search, health summary read | No | intent_recognized, skill_resolved, tool_called, citation_attached |
| `skill.claim_update.v1` | Transactional (Flow B) | Record update, status transition, note append | Yes | intent_recognized, skill_resolved, approval_requested, tool_called, outcome_recorded |
| `skill.change_request_submit.v1` | Transactional (Flow B) | Change draft/create/submit | Yes | intent_recognized, skill_resolved, approval_requested, tool_called, outcome_recorded |
| `skill.incident_assignment.v1` | Transactional (Flow B) | Assignment update, priority update | Conditional by risk policy | intent_recognized, skill_resolved, approval_decision, tool_called, outcome_recorded |

Skill definitions: see `skill-examples/` for full contracts per skill.

## Skill Lifecycle
- **Draft:** skill definition exists but is not executable in production paths.
- **Approved:** skill is allowlisted with explicit controls and observability requirements.
- **Deprecated:** skill remains traceable for audit but is removed from active invocation paths.
