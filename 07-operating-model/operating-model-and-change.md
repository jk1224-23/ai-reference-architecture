# Article 8 — Operating Model & Change Management  
## Running an AI System as a Governed Enterprise Capability

---

## Why this document exists
Most AI architectures fail **after** they are technically correct.

They fail because:
- ownership is unclear
- changes are made informally
- incidents are handled ad hoc
- responsibility drifts over time

In regulated environments, the question is not:
> “Can we build this AI system?”

It is:
> “Can we operate this AI system safely for years?”

This document defines the **operating model** required to sustain the AI Assistant Platform described in this reference architecture.

---

## Problem being addressed
AI systems differ fundamentally from traditional applications:

- behavior changes without code changes
- updates may affect reasoning, not execution
- failures may not trigger errors
- correctness is contextual and temporal

Without an explicit operating model:
- small changes cause large regressions
- accountability becomes ambiguous
- compliance posture erodes silently
- trust degrades gradually, then suddenly

This document treats **operations as an architectural concern**.

---

## Core operating principle
> **No AI behavior changes without ownership, visibility, and rollback.**

This principle governs all operational decisions.

---

## Ownership model and RACI (enterprise minimum)

An AI assistant platform fails in production when ownership is ambiguous. This section defines **who owns what** across prompts, tools, policies, evaluation, and incident response.

### Roles (used in the RACI)
- **Product Owner (PO):** defines business outcomes, approves user experience and “what the assistant is allowed to do”
- **Platform Owner (Platform):** owns orchestration, policy enforcement, tool registry, platform reliability
- **Security/Compliance (Sec/Comp):** owns PHI rules, retention requirements, audit expectations, risk sign-off
- **Data Steward (Data):** owns data classification, knowledge sources, vector store governance, access rules
- **Tool Owner (Tool):** owns each downstream tool/API contract, permissions, and reliability
- **SRE/Observability (SRE):** owns monitoring, incident response mechanics, on-call readiness, SLO reporting

### RACI table
| Activity | PO | Platform | Sec/Comp | Data | Tool | SRE |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Define intent catalog (what the assistant supports) | **A** | **R** | C | C | C | C |
| Add/modify prompts (prompt library changes) | A | **R** | C | C | C | I |
| Add/modify policy rules (guardrails, HITL gates) | C | **R** | **A** | C | C | I |
| Onboard a new tool/API into registry | I | **R** | C | C | **A/R** | C |
| Change tool permissions / scopes | I | C | **A** | C | **R** | I |
| Knowledge source onboarding (KB/docs) | I | C | C | **A/R** | I | I |
| Vector store configuration + retrieval filters | I | **R** | **A** | **R** | I | I |
| Offline evaluation dataset maintenance (golden sets) | C | **R** | C | **R** | C | I |
| Release gates definition (quality + safety) | C | **R** | **A** | C | C | **R** |
| Model upgrade / prompt major version release | A | **R** | **A** | C | C | **R** |
| Canary rollout + rollback decision | I | C | C | I | C | **A/R** |
| Incident response: PHI leak or policy bypass | I | **R** | **A** | C | C | **R** |
| Incident response: tool outage / degradation | I | C | I | I | **R** | **A/R** |
| Post-incident review + corrective actions | C | **R** | **A** | C | C | **R** |

Legend: **R** = Responsible, **A** = Accountable, **C** = Consulted, **I** = Informed

### Approval path (recommended default)
For any change that affects safety, compliance, or execution authority:
1. Change is proposed via PR (prompt/tool/policy/eval update)
2. Automated checks run (lint + evaluation gates + safety suite where applicable)
3. Required approvals are enforced (Platform + Sec/Comp + Tool Owner as needed)
4. Deploy via canary with monitored thresholds
5. Rollback/degrade automatically if guardrail triggers fire

### “Stop-the-line” authority
Any of the following parties can halt release or require rollback:
- **Security/Compliance** for PHI or policy violations
- **SRE** for SLO or stability breaches
- **Platform Owner** for tool misuse / governance failures

---

## Change lifecycle and versioning (prompts, tools, policies, models)

AI assistants change over time. Without disciplined change control, small edits can cause:
- behavior regressions
- policy bypasses
- compliance issues (PHI exposure)
- broken tools and silent failures

This architecture treats prompts, policies, tools, and models as **versioned enterprise assets**.

### What is versioned
- **Prompt templates and system instructions** (prompt library)
- **Policy rules** (intent allow/deny, HITL requirements, PHI controls)
- **Tool registry entries** (tool schemas, permissions, rate limits, fallbacks)
- **Model configuration** (provider, model name/version, safety settings, routing)
- **Evaluation assets** (golden conversation sets, red-team suites, scoring thresholds)

### Change categories (and how strict they are)
| Change type | Examples | Risk level | Required gates / approvals |
|---|---|---:|---|
| Cosmetic | wording, formatting, comments | Low | Platform review |
| Prompt behavior change | new instructions, tone rules, new response structure | Medium | Platform + evaluation regression gate |
| Policy change | HITL thresholds, allowlist mapping, PHI rules | High | Platform + **Security/Compliance** + safety suite |
| Tool change | new tool, schema change, new permissions/scope | High | Platform + Tool Owner + Security (if scope changes) |
| Model change | new model/provider, routing changes | High | Platform + SRE + Security + canary + rollback plan |
| Data source change | KB additions, retrieval filters, embedding pipeline updates | Medium/High | Data Steward + Platform + safety checks |

### Required pipeline gates (minimum)
**Pre-merge (PR level)**
- Tool schema validation (no breaking changes without version bump)
- Policy unit tests (deny-by-default not bypassed)
- Prompt regression tests on golden scenarios
- Static checks for prohibited patterns (e.g., “always call tool X”)

**Pre-release (promotion level)**
- Offline evaluation against golden set (quality targets met)
- Red-team suite (prompt injection / jailbreak / PHI leakage)
- Tool reliability tests (timeouts, partial failures, retries/backoff)
- Canary rollout plan defined (metrics + rollback thresholds)

**Post-release (runtime)**
- Guardrail dashboards monitored (deny rate, escalation rate, tool failure rate, redaction events)
- Drift detection (unexpected shifts in intent mix or response behavior)
- Automated rollback/degrade triggers enabled

### Compatibility rules (avoid breaking prod)
- **Tools:** schema changes must be backward compatible, or shipped as a new version (e.g., `claimsLookup:v2`).
- **Policies:** must remain deterministic; policy decisions must be reproducible and logged.
- **Prompts:** major prompt changes require a version bump and regression run.
- **Models:** treat as “runtime dependency” — always deploy with canary + rollback.

### Rollback and degrade strategy (default)
When safety or reliability degrades:
1. **Degrade to KB-only mode (RAG-only)** for safe explanatory responses.
2. **Force HITL-first** for transactional or ambiguous intents.
3. **Block known-abused intents** temporarily until patched.
4. Roll back prompt/model/tool version to last known-good.

### Change record requirements (audit-friendly)
For any high-risk change, capture:
- what changed (prompt/policy/tool/model version)
- who approved (roles)
- evaluation results (golden + safety)
- rollout method (canary % and duration)
- observed impact (metrics deltas)
- rollback plan and whether it was used

---

## Incident playbooks (enterprise minimum)

Agentic systems need **predefined playbooks** because failures can be fast, high-impact, and hard to debug without a repeatable process.

### Severity model (simple)
- **SEV0:** confirmed PHI leak, policy bypass, unauthorized tool execution, or active exploitation
- **SEV1:** strong indicators of leak/bypass risk, major outage, widespread wrong answers in critical flows
- **SEV2:** degraded tool reliability, evaluation regressions without confirmed compliance impact

### Global “kill switches” (must exist)
- **KB-only mode (RAG-only):** disable all transactional tools
- **HITL-first mode:** require human approval for all non-trivial intents
- **Intent blocklist:** temporarily block specific risky intents (appeals, updates, payments)
- **Tool circuit breakers:** disable a single tool causing cascading failure
- **Model/prompt rollback:** revert to last known-good versions

---

### Playbook 1 — Confirmed PHI/PII leak in user response (SEV0)
**Trigger**
- Confirmed PHI/PII exposure in an outbound response or export

**Immediate actions (first 15 minutes)**
1. Activate **KB-only mode** (disable transactional tools)
2. Enable **HITL-first mode** for member-specific flows
3. Stop/rollback the latest prompt/model/tool release (if recent change)
4. Preserve evidence: traces, prompts, tool calls, and policy decisions (secure audit store)

**Containment**
- Identify the leak source:
  - RAG retrieval (index contains sensitive content)
  - tool output exposure
  - logging/telemetry exposure
- Apply targeted blocks (intent/tool) until root cause is confirmed

**Recovery**
- Patch the control that failed (redaction rule, retrieval filter, allowlist policy)
- Run safety suite + PHI leak tests before re-enabling tools
- Re-enable gradually with canary and strict monitoring

**Post-incident**
- Compliance review + notification workflow (per org policy)
- Update evaluation sets with the exploit pattern
- Add guardrail alerting for recurrence (redaction spikes, retrieval anomalies)

---

### Playbook 2 — Policy bypass or unauthorized tool execution (SEV0)
**Trigger**
- Tool call executed without allowlist approval, or action taken outside intended scope

**Immediate actions**
1. Disable the affected tool(s) via **tool circuit breaker**
2. Roll back the change that introduced bypass (prompt/policy/tool version)
3. Rotate scoped credentials / tokens if any exposure suspected

**Investigation**
- Confirm which layer failed:
  - allowlist mapping bug
  - policy engine enforcement gap
  - tool executor accepted unvalidated params
  - identity scope too broad

**Recovery**
- Fix the enforcement gap (deny-by-default + deterministic allowlist)
- Add unit tests that reproduce the bypass attempt
- Re-release via canary with increased monitoring of allow/deny decisions

---

### Playbook 3 — Prompt injection / goal hijack spike (SEV1 → SEV0 if successful)
**Trigger**
- Surge in jailbreak attempts, policy denies, or suspicious tool requests

**Immediate actions**
1. Tighten policy thresholds (more aggressive deny + escalate)
2. Block known attack patterns (intent blocklist + input filters)
3. Force **HITL-first** for affected intent categories

**Recovery**
- Patch vulnerable instruction patterns (prompt hardening)
- Add new attack patterns to red-team suite and regression tests

---

### Playbook 4 — Tool outage or downstream degradation (SEV1/SEV2)
**Trigger**
- Tool timeouts, error rates, or latency breaches sustained

**Immediate actions**
1. Enable **degrade strategy**:
   - KB-only for explanatory flows
   - HITL-first for transactional intents
2. Trip tool circuit breaker and stop runaway retries

**Recovery**
- Restore tool health or switch to alternative tool endpoint
- Validate fallback messaging (“we can’t complete this action right now…”)
- Re-enable gradually with canary

---

### Playbook 5 — Cascading failures / runaway agent loops (SEV1)
**Trigger**
- Repeated tool calls, growing trace depth, exploding latency/cost, queue buildup

**Immediate actions**
1. Apply caps: max tool calls per turn, max plan depth, max tokens per session
2. Enable circuit breaker for repeated failure patterns
3. Shift to KB-only / HITL-first mode temporarily

**Recovery**
- Fix orchestration logic (timeouts, backoff, loop detection)
- Add regression tests for “runaway loop” scenarios

---

## Operating responsibilities (WHY-driven)

### AI Platform Ownership
**Why**
AI behavior must be managed centrally to prevent fragmentation and drift.

**Responsibilities**
- own the AI Assistant Platform
- manage model lifecycle and routing
- maintain shared capabilities (orchestration, policy, tools)
- coordinate cross-team changes

This role owns **how AI behaves**, not what business rules are.

---

### Domain System Ownership
**Why**
Systems of record retain authority over business logic and data.

**Responsibilities**
- define data access contracts
- validate tool behavior
- approve changes affecting transactional outcomes

AI does not reinterpret domain rules — it consumes them.

---

### Risk, Compliance, and Security Ownership
**Why**
AI introduces new failure and exposure modes that must be reviewed independently.

**Responsibilities**
- define policy constraints
- review audit artifacts
- participate in incident analysis
- approve high-risk changes

Compliance is a **continuous participant**, not a gate at the end.

---

### Operations / Support Ownership
**Why**
AI incidents require different response patterns than traditional outages.

**Responsibilities**
- monitor behavior metrics
- triage escalations and failures
- coordinate rollback or disablement
- interface with human agents during incidents

---

## Change management model

### Why change control is critical
AI systems change through:
- prompt updates
- policy updates
- tool changes
- data source changes
- model version changes

Each can alter behavior **without breaking the system**.

---

### Architectural decision
All changes are treated as **behavioral changes**, not configuration tweaks.

Each change must:
- declare expected behavior impact
- trigger targeted evaluation
- support rollback
- be attributable to an owner

---

## Safe change lifecycle

### 1. Proposal
Changes are proposed with:
- rationale
- affected intents or flows
- risk classification
- rollback strategy

---

### 2. Pre-change evaluation
Changes are evaluated against:
- golden interaction sets
- high-risk scenarios
- compliance constraints

Approval is conditional, not implicit.

---

### 3. Controlled rollout
Changes are introduced:
- incrementally
- with monitoring
- with escalation readiness

AI behavior is observed before it is trusted.

---

### 4. Post-change review
After rollout:
- metrics are reviewed
- deviations are analyzed
- corrective actions are documented

Learning is institutionalized.

---

## Incident management (WHY-driven)

### Why AI incidents are different
AI incidents may involve:
- incorrect but plausible responses
- missed escalations
- inappropriate autonomy
- data misuse without outages

---

### Architectural response
- Treat behavioral anomalies as incidents
- Preserve decision traces
- Identify decision ownership
- Apply rollback before root-cause perfection

Speed of containment matters more than precisio
