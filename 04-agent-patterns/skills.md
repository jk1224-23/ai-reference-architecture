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

| Skill | Category | Allowed Tool Types | Human Approval? | Observability Events |
|---|---|---|---|---|
| knowledge_retrieval | Read-only (Flow A) | Retrieval/RAG connector, policy/KB lookup | No | skill_invoked, retrieval_started, retrieval_completed, citations_attached, skill_failed |
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
