# Architecture Decisions (ADR-lite)

This document captures the key architectural decisions for the Healthcare Voice & Chat AI Assistant reference architecture. Each decision includes the **rationale** and the **trade-offs**.

> This is “ADR-lite”: fewer formalities, but clear decisions and traceable reasoning.

---

## AD-01 — The assistant is not a system-of-record
**Decision**  
The assistant must not become a transactional source of truth. Transactional statements must be backed by **systems-of-record tools**.

**Rationale**  
RAG content can be outdated or incomplete; model outputs are probabilistic. Regulated domains require authoritative data for claim/eligibility status and actions.

**Trade-offs**  
- More tool integration effort
- Higher latency for tool-backed flows

---

## AD-02 — Tool access is deny-by-default and allowlisted per intent
**Decision**  
All tool execution is blocked unless explicitly allowlisted by **intent category** and approved by policy.

**Rationale**  
Prevents privilege creep and tool misuse. Keeps execution authority outside the model.

**Trade-offs**  
- Slower onboarding of new tools/intents
- Requires governance for allowlist ownership

---

## AD-03 — Bounded autonomy is enforced outside the LLM
**Decision**  
The model can propose actions, but **policy gates and orchestration** enforce scope, data, and execution boundaries.

**Rationale**  
Trusting the model to “self-restrict” is not a control. Enforcement must be deterministic and auditable.

**Trade-offs**  
- More platform logic (policy engine, orchestration, tool registry)
- Requires careful design of escalation paths

---

## AD-04 — RAG is used for explanatory knowledge, not transactional truth
**Decision**  
RAG is used for policies, SOPs, FAQs, and explanations. Transactional state must come from tools.

**Rationale**  
Improves trust and auditability. Prevents “policy text” being mistaken for member-specific truth.

**Trade-offs**  
- Requires curated knowledge sources and retrieval governance
- Adds retrieval + citation complexity

---

## AD-05 — High-risk intents require HITL or explicit approvals
**Decision**  
Appeals, grievances, member-data updates, and financial/coverage-impacting actions require HITL approval gates.

**Rationale**  
Reduces harm from incorrect automation. Aligns with regulated expectations for accountability.

**Trade-offs**  
- Lower automation rate for high-risk work
- More operational effort to staff approvals

---

## AD-06 — Identity separation: user identity ≠ agent identity ≠ tool identity
**Decision**  
The architecture treats identities as separate layers:
- end user identity (who is asking)
- assistant/session identity (who is acting in the platform)
- tool identity (what downstream permissions are used)

**Rationale**  
Limits blast radius and supports least privilege. Prevents “one token does everything.”

**Trade-offs**  
- More IAM configuration complexity
- Requires disciplined token lifecycle management

---

## AD-07 — Least privilege with scoped, short-lived tool credentials
**Decision**  
Tool calls use scoped tokens/claims bound to:
- intent category
- user role
- tool permissions
- time limits (short-lived where possible)

**Rationale**  
Reduces data exposure and prevents wide-query exfiltration.

**Trade-offs**  
- Token minting/rotation overhead
- Requires strong IAM integration patterns

---

## AD-08 — Audit-first observability is mandatory
**Decision**  
Every interaction produces an auditable trace capturing:
- intent classification + confidence
- policy decision outcomes (allow/deny + reasons)
- tool calls (metadata and permitted payload references)
- escalation events and human approvals
- final response output (or reference)

**Rationale**  
Healthcare requires traceability for governance, incidents, and dispute resolution.

**Trade-offs**  
- Cost and complexity of logging + retention
- Requires careful PHI minimization in telemetry

---

## AD-09 — Release gates and canary rollout are required for changes
**Decision**  
Prompts, tools, policies, and models are versioned assets that must pass:
- pre-merge checks
- pre-release evaluation + safety suites
- canary rollout with rollback triggers

**Rationale**  
Agentic changes can cause regressions quickly; gates prevent unsafe promotions.

**Trade-offs**  
- Slower release cadence
- Requires evaluation infrastructure and test sets

---

## AD-10 — Degrade modes and kill switches are first-class
**Decision**  
The platform must support safe degrade modes:
- KB-only (RAG-only)
- HITL-first
- tool circuit breakers
- intent blocklist
- model/prompt rollback

**Rationale**  
Enables safe operation under attack, tool outages, or drift.

**Trade-offs**  
- More orchestration complexity
- Requires clear operational runbooks

---

## AD-11 — Data retention is explicit, minimal, and enforced
**Decision**  
Retention and storage locations are explicitly defined for:
- conversation content
- audit logs
- evaluation samples
- vector store contents

PHI is minimized and protected; vector stores exclude PHI by default.

**Rationale**  
Reduces compliance risk and aligns storage to purpose limitation.

**Trade-offs**  
- Requires disciplined data governance
- Can limit debugging if over-minimized

---

## AD-12 — Alignment to OWASP Agentic Top 10 (2026) is used as a baseline
**Decision**  
Threat modeling and controls align to OWASP Agentic Top 10 risk themes, maintained as a living reference.

**Rationale**  
Anchors security posture to an emerging industry baseline and supports review-board conversations.

**Trade-offs**  
- Must track updates as OWASP guidance evolves
- Requires periodic review to maintain mapping relevance

---
