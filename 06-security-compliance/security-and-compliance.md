# Article 6 — Security, Privacy & Compliance  
## PHI-First Architecture for Enterprise AI

---

## Security model clarity (identity, least privilege, retention)

### Identity: user vs agent vs tool
- **User identity:** the human (member/CSR/employee) authenticated by the enterprise IdP.
- **Agent identity:** the orchestrator-controlled runtime identity used to call the LLM and coordinate steps (not a “user”).
- **Tool identity:** per-tool service identity used for system access; mapped to least-privilege scopes and audited.

**Rule:** Tool calls must be attributable to *both* the user context and the tool service identity.

### Least privilege: scoped tokens per tool call
- Issue **short-lived, scope-limited tokens** for each tool invocation.
- Scope is derived from: intent category + risk tier + policy outcome + user role.
- High-risk tool calls require **HITL approval** before a token is minted.

### Data retention: what is logged, how long, where
Log what you need for audit and incident response, but minimize PHI:
- Store **decision traces** (intent, confidence, risk, policy outcomes, tool IDs, timestamps).
- Store **tool call metadata** by default; store payloads only when permitted and necessary.
- Apply retention by data class (e.g., short retention for raw prompts, longer for audit events).

**Rule:** “Audit-first” does not mean “log everything forever.”

---

## Threat model (STRIDE-lite)

This threat model focuses on the most common failure modes for **agentic assistants in regulated domains**. The goal is to map each threat to **concrete architectural controls** and **where they are enforced** (outside the LLM wherever possible).

| Threat / attack pattern | Impact | Primary controls | Where enforced (component) | Evidence / telemetry |
|---|---|---|---|---|
| Prompt injection (user tries to override rules, force tool use, bypass policy) | Unauthorized actions, policy bypass, data leakage | Policy gate must be authoritative; intent classification; tool allowlists; deny-by-default for high-risk intents | Orchestrator + Policy/Guardrail Engine + Tool Registry | Policy deny logs, blocked-intent counters, jailbreak attempt signals, conversation trace |
| Tool manipulation (model tries “creative” tool parameters, chaining, or hidden requests) | Data exfiltration or unintended side effects | Strict tool schemas; input validation; parameter allowlists; scoped tokens; output filtering | Tool Execution Layer + Policy Engine | Tool call audit (input/output hashes), validation failures, abnormal parameter patterns |
| Data exfiltration via RAG (prompt asks for secrets/PHI “from docs”) | PHI/PII exposure, compliance breach | Data classification rules; RAG index must exclude PHI by default; retrieval filters; redaction on outputs | RAG Service + Policy Engine + Response Quality Gate | Retrieval logs, redaction events, PHI detection alerts, vector-store access audit |
| Data exfiltration via tools (model requests broad “dump” queries) | PHI/PII exposure, over-collection | Least-privilege tool scopes; row/field-level access; query guardrails; purpose limitation | Tool Execution Layer + Downstream APIs | Tool query size metrics, denied queries, abnormal “wide” query detection |
| Unauthorized tool access / privilege escalation (agent gains access to tools it shouldn’t) | Unauthorized transactions or data access | Deterministic allowlist mapping (intent → tools); RBAC; scoped credentials per tool call; no shared “god token” | Policy Engine + Tool Registry + IAM | Allowlist resolution logs, RBAC deny logs, token scope audit, privilege anomaly detection |
| Identity spoofing / session hijack (replay tokens, impersonation, wrong member context) | Wrong-user disclosure, fraudulent actions | Strong auth (OIDC); session binding; step-up auth for high-risk; context confirmation for member-specific actions | Channel Adapters + Orchestrator + IAM | Auth events, step-up triggers, mismatch detection, session anomaly alerts |
| Hallucination presented as transactional truth (“claim is approved” without SoR evidence) | Misleading decisions, member harm, compliance risk | “No SoR truth without tools” rule; evidence-first response assembly; citations and tool provenance; refusal when evidence missing | Orchestrator + Response Assembly + Quality Gate | Evidence completeness score, hallucination flags, “no-evidence response” blocks, QA sampling results |
| PHI leakage in responses (model includes sensitive data unintentionally) | Compliance breach | Pre/post redaction; PHI detectors; response templates that minimize exposure; safe summaries; logging redaction | Quality Gate + Policy Engine + Observability | PHI redaction counts, blocked responses, sampling audits, incident triggers |
| PHI leakage in logs/traces (telemetry captures raw PHI) | Compliance breach, retention violations | Log minimization; tokenization/hashing; separate secure audit store; retention policies; access controls | Observability Pipeline + Audit Store | Field-level redaction metrics, audit access logs, retention enforcement reports |
| Denial of service (token floods, tool burst storms, retries) | Outages, degraded service | Rate limiting; circuit breakers; queueing; retries with backoff; per-user/per-channel quotas | Channel Adapters + Orchestrator + Tool Execution | Rate-limit metrics, queue depth, tool timeout rates, circuit breaker events |
| Supply-chain / drift (model/provider change, prompt edits, tool version changes) | Behavior regressions, new failure modes | Change control; versioned prompts/tools; canary releases; rollback; evaluation gates before promotion | Operating Model + Evaluation + Tool Registry | Release gate results, drift detection, rollback events, change audit trail |

### Security validation checklist (minimum bar)
Use this checklist as the “definition of done” for security controls:

- Tool execution is **deny-by-default** and only allowed through a **deterministic allowlist** (intent → tools).
- All tool calls use **scoped credentials** (least privilege) with short-lived tokens where possible.
- Tool inputs are **schema-validated** and parameter-guarded (reject broad queries / unsafe params).
- High-risk intents (appeals, grievances, updates, financial actions) are **blocked or HITL-gated** by policy.
- Responses cannot assert systems-of-record truth **without tool evidence** (enforced outside the model).
- PHI/PII protection is enforced via **pre/post redaction** and **response quality gates**.
- Logs/traces do not persist raw PHI by default (redaction/minimization + controlled audit store).
- Rate limits, circuit breakers, and backoff exist for both LLM calls and downstream tools.
- Security telemetry is monitored (policy denies, jailbreak attempts, redaction spikes, tool anomalies).
- Changes to prompts, tools, and policies require review + release gates (evaluation + canary + rollback).

---


## Why this document exists
In healthcare environments, AI failures are not evaluated by sophistication or intent.
They are evaluated by **exposure**.

Security, privacy, and compliance are often treated as implementation concerns
(addressed through tooling, configurations, or vendor assurances).

This document establishes them as **architectural constraints** that shape:
- system boundaries
- data flows
- agent autonomy
- auditability
- operational ownership

In this reference architecture, **security is not a layer added later — it is a design premise**.

---

## Problem being addressed
Healthcare AI assistants operate under conditions where:
- sensitive data (PHI/PII) is routinely present
- access must be purpose-limited and role-aware
- regulatory review may occur long after interactions complete
- violations can occur silently, without obvious system failure

Traditional application security assumes:
- deterministic execution paths
- explicit data access patterns
- static permission models

AI systems violate all three.

This document defines how **architectural controls compensate for that mismatch**.

---

## Core architectural position
> **AI systems must be treated as untrusted intermediaries operating within trusted boundaries.**

This architecture assumes:
- models may produce unsafe outputs
- prompts may be manipulated
- reasoning paths may be non-obvious
- confidence is not correctness

Therefore, trust is enforced **outside** the AI model, not within it.

---

## Security objectives (WHY-driven)

### 1. Prevent unauthorized disclosure
AI must not reveal PHI or sensitive information beyond the authenticated user’s scope.

### 2. Enforce least privilege
AI must only access data and actions explicitly permitted for the user’s role and intent.

### 3. Preserve auditability
All AI interactions must be reconstructable for compliance and investigation.

### 4. Maintain accountability
Responsibility for decisions must be attributable to humans and systems, not models.

---

## PHI handling as an architectural concern

### Why PHI requires architectural treatment
PHI exposure can occur through:
- model responses
- logs and telemetry
- escalation artifacts
- cached context or memory

Relying on “careful prompts” or “trusted models” is insufficient.

---

### Architectural decisions for PHI protection

#### 1. Data minimization by design
**Decision**
- Only the minimum necessary data is retrieved for a given intent.
- Context is scoped per interaction.

**Why**
Reducing data exposure reduces blast radius.

---

#### 2. Role- and purpose-based access
**Decision**
- All data access is mediated through tools enforcing role and purpose.
- AI reasoning never bypasses access controls.

**Why**
PHI access is contextual, not global.

---

#### 3. Explicit redaction boundaries
**Decision**
- PHI redaction is applied before logging, analytics, or persistence.
- Redaction rules are policy-driven.

**Why**
Logs are a common but overlooked leakage vector.

---

## Policy enforcement architecture

### Why policy cannot live in prompts
Policies embedded in prompts:
- are not testable
- are not versioned independently
- cannot be audited reliably
- are easy to bypass

---

### Architectural decision
Policies are enforced by a **dedicated Policy & Guardrail Engine** that:
- evaluates intents and actions
- applies allow/deny rules
- enforces HITL requirements
- blocks disallowed behavior deterministically

AI reasoning proposes.
Policy decides.

---

## Identity, access, and consent

### Why identity is foundational
Without identity:
- permissions cannot be enforced
- PHI boundaries collapse
- audit trails lose meaning

---

### Architectural requirements
- Every interaction is associated with an authenticated identity or declared anonymity.
- Roles (member, provider, CSR) are explicit inputs to policy decisions.
- Consent status influences data access and retention.

Identity is **not optional context** — it is an architectural dependency.

---

## Auditability and compliance posture

### Why auditability is non-negotiable
Healthcare regulations require the ability to answer:
- who accessed what
- when
- for what purpose
- with what outcome

AI systems must support **post hoc reconstruction**, not just real-time monitoring.

---

### Audit architecture decisions
- All prompts, decisions, tool calls, and escalations are logged with correlation IDs.
- Logs capture decisions and rationales, not just raw text.
- Audit data is immutable and access-controlled.

An AI interaction without an audit trail is treated as a compliance incident.

---

## Handling prompt injection and misuse

### Why this matters architecturally
Prompt injection is not just a model weakness — it is an **interface vulnerability**.

---

### Architectural mitigations
- Strict separation between user input and system instructions
- Policy enforcement independent of model output
- Tool access gated by orchestration, not reasoning
- Escalation on suspicious or conflicting intents

The system assumes **inputs may be hostile**.

---

## Data retention and lifecycle

### Why retention must be explicit
AI systems tend to accumulate:
- conversation history
- inferred context
- derived artifacts

Without explicit retention rules, systems drift into non-compliance.

---

### Architectural decisions
- Retention periods are defined per data class.
- Derived AI artifacts follow the strictest applicable retention rule.
- Deletion is enforceable and auditable.

---

## Architectural implications
- Security controls exist outside the model boundary.
- AI autonomy is constrained by policy, not confidence.
- PHI exposure paths are minimized structurally.
- Compliance is verifiable, not assumed.
- Incidents are investigable after the fact.

These implications shape every other architectural layer.

---

## Explicit non-goals
This architecture does **not**:
- assume model-level safety is sufficient
- rely on vendor assurances for compliance
- allow AI to self-govern access
- trade auditability for performance
- treat security as a post-deployment concern

---

## Transition forward
With security, privacy, and compliance constraints defined, the reference architecture is now **complete at the design level**.

What remains is **how this architecture is operated over time**:
- how changes are introduced safely
- how incidents are handled
- how ownership is maintained

This operational model is informed by — and subordinate to — the constraints defined here.
