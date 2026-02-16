# Observability Spec (LLM + Agents)

This document standardizes what we log, measure, and trace for LLM and agent systems to ensure:
- debuggability (root cause analysis)
- safety monitoring
- cost control
- reliability/SLO tracking
- auditability (without leaking sensitive data)

## Principles

- **Correlation-first**: every request has a correlation_id propagated end-to-end.
- **No sensitive payloads in logs** by default (redaction/masking required).
- **Measure decisions**: routing decisions, tool allow/deny decisions, safety actions.
- **Separate data planes**:
  - operational logs/metrics (safe)
  - secure evidence store (restricted, time-bound) when absolutely required

---

## Identifiers (Required)

- **correlation_id**: generated at ingress, propagated through all calls
- **session_id**: stable per user session (if applicable)
- **request_id**: unique per request/turn
- **agent_id**: which agent profile
- **consumer_id**: which app/tenant
- **tool_call_id**: unique per tool invocation
- **policy_version** / **prompt_version** / **tool_contract_version**
- **model_id** / **provider_id** / **route_tier**

---

## Logging Spec (Minimum Fields)

### Ingress Log (per user request)
- timestamp
- correlation_id, session_id, request_id
- channel (chat/voice/internal/batch)
- agent_id, consumer_id, tenant (if applicable)
- route decision (tier, model_id, provider)
- safety classification outcome (labels only)
- budgets configured (token cap, tool cap)

**Do NOT log**
- raw user text containing PHI/PII
- secrets
- full retrieved documents

### Tool Call Log (per tool invocation)
- timestamp
- correlation_id, tool_call_id
- tool_id + version
- allow/deny decision + reason code
- latency_ms, retries, status_code
- args shape summary (schema keys only; redacted values)
- response size (bytes), response schema validation pass/fail

### Retrieval Log (per retrieval step)
- correlation_id
- knowledge source id(s)
- doc ids / chunk ids (opaque ids)
- topK + similarity scores (if used)
- total tokens returned from retrieval
- any filtering applied (PII filters, instruction stripping)

### Safety Event Log (when safety controls trigger)
- correlation_id
- event_type: block | redact | degrade | hitl_required | tool_disabled
- reason code (policy label)
- action taken (KB-only, HITL-first, etc.)

---

## Metrics (Required)

### Core reliability
- requests_total (by agent_id, tier, provider)
- request_latency_ms (p50/p95/p99)
- errors_total (by type: model/tool/retrieval)
- availability (derived)
- timeouts_total

### Tooling
- tool_calls_total (by tool_id)
- tool_denied_total (by tool_id + reason)
- tool_latency_ms
- throttles_total
- circuit_breaker_open_total

### Safety
- safety_blocks_total (by reason)
- prompt_injection_signals_total
- redactions_total
- hitl_required_total
- unsafe_output_detected_total (if you run validators)

### Quality (lightweight)
- retrieval_required_rate (for intents that should be grounded)
- citation_present_rate (if you require citations/evidence)
- schema_validation_fail_rate (structured outputs)

### Cost
- tokens_in_total / tokens_out_total
- cost_estimate_total (by tier/provider)
- tool_cost_total (if tools incur cost)
- budget_exceeded_total (token/tool)

---

## Tracing (Distributed)

### Span naming (recommended)
- `agent.turn`
- `agent.route_decision`
- `agent.retrieval`
- `agent.tool_call.<tool_id>`
- `agent.output_validation`
- `agent.safety_check`

### Trace attributes (minimum)
- correlation_id
- agent_id, consumer_id
- model_id/provider_id
- tool_id (for tool spans)
- policy_version/prompt_version

---

## Alerts (Suggested)

### SEV-1 style alerts
- PHI leakage indicator spike (if classifier/validator exists)
- write tool calls executed without HITL (should be zero)
- tool allow/deny anomaly (denies spike or unexpected allows)
- cost spike (tokens or tool costs)

### Reliability alerts
- provider outage / error rate spike
- p95 latency breach
- tool timeouts spike
- retrieval failures spike

### Safety posture alerts
- injection signal spike
- repeated jailbreak attempts from same tenant/app
- repeated loop detection triggers

---

## Dashboards (Minimum)

1) **Operations dashboard**
- traffic, latency, errors by tier/provider
- tool call health
- budgets/cost

2) **Safety dashboard**
- blocks, redactions, HITL
- injection signals
- tool denials by reason

3) **Quality dashboard**
- retrieval grounding rates
- schema validation failure rate
- top intents by failure mode

---

## Data Retention (Guidance)

- Operational logs: short retention (per policy)
- Traces: short retention; sampled in prod if needed
- Secure evidence store: restricted access, time-bound retention, incident-only usage

---

## Definition of Done (Checklist)

- [ ] correlation_id propagates through agent → retrieval → tools
- [ ] logs contain route decisions and allow/deny reasons (no PHI)
- [ ] metrics exist for reliability, safety, cost, and tools
- [ ] traces show key spans for debugging
- [ ] alerts exist for SEV-1 and SLO breaches
- [ ] dashboards exist for ops + safety + cost
