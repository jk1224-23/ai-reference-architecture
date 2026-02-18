# Tool Registry and Enforcement

This document defines the **Tool Registry** as the authoritative control plane for agent tool usage and the **enforcement layer** that ensures tools are invoked safely, consistently, and auditable — **outside the LLM**.

## Why this exists

LLMs are probabilistic. Tool calls must be governed by deterministic controls:
- prevent unauthorized tools/actions
- validate inputs/outputs against contracts
- enforce least privilege and rate limits
- provide kill switches during incidents
- ensure auditability (who/what/when/why)

---

## Definitions

- **Tool**: A callable capability (API/function/workflow) available to an agent or application.
- **Tool Contract**: The specification for inputs/outputs, error model, idempotency, limits, and NFRs.
- **Tool Registry**: Catalog of approved tools + metadata + policy bindings.
- **Enforcement Layer**: Runtime gate that validates and authorizes tool calls before execution.
- **Tool Allowlist**: Set of tools enabled per environment / tenant / application / agent.
- **Write Tool**: Any tool that changes state (create/update/delete, side effects).

---

## Architecture Overview (Logical)

1) **Agent/Orchestrator** proposes a tool call (tool_id + args)
2) **Enforcement Layer** checks:
   - allowlist (is tool enabled here?)
   - authZ (is caller allowed to use it?)
   - schema validation (args valid?)
   - budgets (tool calls, rate limits, cost)
   - policy (risk rules, HITL, PHI constraints)
3) If allowed → execution occurs
4) Output is validated/sanitized and logged with correlation_id

> Key rule: **Only the enforcement layer actually executes tools.**

---

## Tool Registry: Required Fields

Each tool registered must include:

### Identity
- **tool_id**: stable id (e.g., `claims.search.v1`)
- **name**
- **owner** (team)
- **domain**
- **version**
- **status**: active | deprecated | disabled

### Contract Binding
- **contract_ref**: link/path to tool contract doc
- **input_schema_hash** / **output_schema_hash** (optional but recommended)
- **error_model**: standardized envelope

### Runtime Policy Metadata
- **risk_level**: low | medium | high
- **data_classification**: public | internal | confidential | PHI
- **side_effects**: none | read_only | write
- **allowed_environments**: dev | stage | prod
- **default_timeouts_ms**
- **retry_policy**: retryable codes + max retries
- **rate_limits**: steady + burst
- **requires_HITL**: true/false (default true for write tools)

### Audit/Observability
- **required_audit_events**: list
- **log_redaction_rules**: what must be masked
- **metrics_required**: calls, latency, failures, throttles

---

## Allowlisting Model

Allowlisting must be possible at multiple levels:

- **Environment** (dev/stage/prod)
- **Tenant** (if multi-tenant)
- **Application** (caller app)
- **Agent** (specific agent profile)
- **User role** (admin vs standard)

### Example allowlist policy (conceptual)
- Prod: only tools with `status=active` and `approved_for_prod=true`
- Customer-facing agents: read-only tools only unless HITL enabled
- Batch jobs: limited tool set + higher rate limits but strict budgets

---

## Enforcement Checks (Mandatory)

The enforcement layer must perform these checks on every tool call:

### 1) Tool Resolution
- tool_id exists in registry
- tool status is active
- tool version is allowed (no deprecated versions in prod)

### 2) Authentication & Authorization
- caller identity verified (workload identity / OAuth / mTLS)
- tool-specific scope/role checks (least privilege)
- deny-by-default if missing required scope

### 3) Schema Validation (Input)
- validate args strictly against tool contract schema
- reject unknown fields if strict mode
- validate sizes, ranges, patterns (e.g., IDs, dates)
- enforce default values only in enforcement layer (not in LLM prompt)

### 4) Policy Enforcement (Risk & Compliance)
- PHI/PII guardrails: block or require HITL based on classification
- write tools: require explicit approval gate
- tool chaining restrictions (e.g., no “read PHI → write external” without policy)

### 5) Budgets & Rate Limits
- per-request tool-call budget
- per-session tool-call budget
- per-tool rate limits (steady + burst)
- circuit breaker for repeated failures/timeouts

### 6) Idempotency & Replay Protection (Write Tools)
- require idempotency key for write operations
- reject duplicate requests within window or safely return prior result
- prevent “LLM retries” from causing double writes

### 7) Output Validation (Output + Safety)
- validate output shape against output schema
- sanitize tool outputs (strip instructions, scripts, untrusted markup)
- redaction/masking before logs and before returning to model (if required)

### 8) Audit Logging (Minimum)
- correlation_id propagated end-to-end
- tool_id, version, caller identity, decision (allow/deny), reason
- latency, response code, retry count
- no sensitive payloads in logs (store in approved secure store if needed)

---

## Human-in-the-Loop (HITL) Policy

### When HITL is required
- any write tool in prod (default)
- any tool classified as PHI/confidential with external impact
- any workflow with financial/regulatory impact
- any abnormal behavior (loop detection, spikes, unknown inputs)

### HITL approval payload should contain
- tool_id + intent summary (human-readable)
- redacted args preview (no PHI unless explicitly permitted)
- expected side effects
- rollback guidance (if applicable)

---

## Kill Switches (Operational Controls)

Kill switches must exist at:
- **global level** (all tools)
- **tool level** (single tool_id)
- **tool category** (all write tools)
- **tenant/app/agent level**

### Typical containment modes
- KB-only mode (no tools)
- disable write tools
- disable a specific tool used in an incident
- force HITL-first mode
- force provider/model failover (routing policy integration)

> These switches must be fast to apply (config-driven) and reversible.

---

## Standard Error Envelope (for Tool Calls)

All tools should return a consistent structure:

- `code` (stable)
- `message` (safe)
- `details` (structured, non-sensitive)
- `correlation_id`
- `retryable` (boolean)

Common codes:
- INVALID_ARGUMENT
- UNAUTHENTICATED
- PERMISSION_DENIED
- NOT_FOUND
- CONFLICT
- RATE_LIMITED
- UPSTREAM_TIMEOUT
- INTERNAL

---

## Contract Testing & Governance

### Contract Tests (Required)
- schema validation tests for inputs/outputs
- negative tests (reject invalid args)
- auth tests (scope required)
- timeout/retry behavior tests

### Versioning Rules (Recommended)
- **v1 → v2** for breaking input/output changes
- keep v1 active until consumers migrate
- deprecation requires:
  - notice period
  - migration guide
  - “deny in prod” date

---

## What “Good” Looks Like (Checklist)

- [ ] All tools have a registered tool_id + owner + contract_ref
- [ ] Allowlist exists per environment and per agent
- [ ] Enforcement layer validates inputs/outputs and blocks unknown fields
- [ ] Write tools require idempotency key + HITL approval in prod
- [ ] Budgets and rate limits are enforced with circuit breakers
- [ ] Kill switches exist (global/tool/category/agent/tenant)
- [ ] Audit logs include correlation_id and allow/deny reasons (no PHI)
- [ ] Contract tests run in CI for every tool change
