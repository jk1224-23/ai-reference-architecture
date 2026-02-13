# Scope and Architectural Principles

## Why this document exists
AI reference architectures often fail because they mix:
- implementation detail with design intent
- tooling decisions with architectural responsibility
- experimentation with production accountability

This document establishes the **scope, intent, and principles** that govern all subsequent architecture decisions in this repository.

It answers **WHY this architecture exists**, before describing any structure.

---

## Problem Being Addressed
Healthcare voice and chat assistants introduce a unique architectural challenge:

- They interact with **multiple systems of record**
- They operate under **PHI, compliance, and audit constraints**
- They support **real-time channels** (voice) and asynchronous channels (chat)
- They rely on **non-deterministic AI systems** inside deterministic enterprises

Traditional application architectures assume:
- deterministic logic
- explicit failures
- predictable outputs

AI systems violate all three assumptions.

This reference architecture exists to **contain that risk**.

---

## Architectural Scope

### Included in scope
This reference architecture covers:

- Voice and chat entry points
- AI orchestration and control layers
- Tool-based access to enterprise systems
- Retrieval-Augmented Generation (RAG) for enterprise knowledge
- Agent patterns with **explicitly bounded autonomy**
- Human escalation and handoff
- Auditability, compliance, and observability
- Evaluation of AI behavior in production

The architecture is expressed at:
- **C4 Context level**
- **C4 Container level**

---

### Explicitly out of scope
To preserve architectural clarity, the following are **intentionally excluded**:

- Model training or fine-tuning
- Framework or SDK selection
- Prompt engineering techniques
- Vector database implementation details
- UI/UX design
- Infrastructure-as-code or deployment pipelines

These are **implementation concerns**, not architectural responsibilities.

---

## Core Architectural Position
This architecture treats AI as:

> A **probabilistic decision-support capability** operating inside a deterministic enterprise system.

AI is not treated as:
- a source of truth
- a system of record
- an autonomous decision-maker in high-risk domains

---

## Architectural Principles (Non-Negotiable)

### 1. AI does not own truth
All authoritative data remains in systems of record.
AI must retrieve or query truth — never infer it.

---

### 2. Bounded autonomy by design
AI behavior is explicitly constrained by:
- role
- intent
- confidence thresholds
- policy enforcement

If a boundary is unclear, autonomy is reduced — not expanded.

---

### 3. Human-in-the-loop for risk
Any interaction involving:
- financial impact
- coverage denial
- appeals or grievances
- clinical interpretation

must support deterministic human escalation.

AI assists. Humans decide.

---

### 4. Auditability over intelligence
Every AI interaction must be:
- traceable
- explainable at a system level
- reviewable after the fact

An un-auditable AI decision is considered a system defect.

---

### 5. Platform, not feature
AI capabilities are centralized into a governed platform.
Individual applications do not embed or customize AI behavior independently.

This prevents:
- inconsistent policy enforcement
- duplicated risk
- uncontrolled cost growth

---

## Decision-Making Philosophy
All architectural decisions in this repository follow a single rule:

> **Prefer predictability, control, and accountability over sophistication.**

When tradeoffs exist:
- safety wins over convenience
- clarity wins over cleverness
- governance wins over speed

---

## Non-functional requirements (NFRs) — measurable targets (starter)

This reference architecture is designed for regulated-domain assistants where **safety, auditability, and reliability** are as important as usability. The targets below are starter values; teams should tune them based on channel (voice vs chat), risk profile, and downstream system constraints.

### Availability and resilience
- **Platform availability:** target **99.9%+** for the orchestration/control plane (excluding downstream tool/system outages).
- **Degraded mode availability:** when tools are down, the assistant must still provide **KB-only** support for low-risk intents (where allowed).
- **Graceful degradation:** tool failures should not cascade into total outage; enforce circuit breakers and fallbacks.

### Latency (user experience)
Latency targets should be defined per channel:
- **Chat response time (P95):** target **≤ 3–5 seconds** for low-risk, KB-only queries.
- **Tool-backed queries (P95):** target **≤ 8–12 seconds** where downstream systems permit.
- **Voice turn latency (P95):** target **≤ 1.5–2.5 seconds** for acknowledgement + progressive responses (even if tool completion takes longer).
- **Timeout behavior:** if tool execution exceeds threshold, respond with a safe fallback (HITL or “we can’t complete this right now”).

### Reliability (correctness + tool health)
- **Tool execution success rate (P95 rolling window):** target **≥ 99%** for critical read-only tools; define per-tool baselines.
- **Tool failure handling:** retries must use backoff and be capped; circuit breakers must trip under sustained failure.
- **Evidence-first rule:** the assistant must not assert systems-of-record truth without tool evidence (enforced outside the LLM).

### Safety and compliance (PHI/PII)
- **PHI/PII leakage:** target **0 confirmed leaks** in user-visible responses (SEV0).
- **Redaction coverage:** PHI/PII detection + redaction must run for all responses that may contain sensitive data.
- **High-risk intents:** must be blocked or HITL-gated by policy (appeals, disputes, member-data updates, financial actions).
- **Policy bypass:** target **0 bypass incidents** (tool calls without allowlist approval).

### Auditability and traceability
- **Trace completeness:** target **≥ 99%** of interactions produce an auditable trace including:
  - intent classification outcome
  - policy decisions (allow/deny + reason)
  - tool calls (metadata and permitted payload references)
  - escalation events and human approvals
- **Reproducibility:** policy decisions must be deterministic and explainable from logged inputs.

### Data retention and privacy (starter stance)
Retention must be explicitly defined and enforced:
- **Conversation content retention:** keep minimal content needed for support/evaluation, per policy (e.g., **30–90 days**), with secure access controls.
- **Audit logs:** retain longer (e.g., **1–7 years**) as required by compliance, but minimize sensitive payload storage.
- **Vector store content:** exclude PHI by default; allow only approved sources and enforce retrieval filters.

### Rate limits and cost control
- **Per-user rate limits:** enforce per-channel quotas to prevent abuse and protect downstream tools.
- **Max tool calls per turn:** cap tool calls and plan depth to prevent runaway loops.
- **Token/cost budgets:** define per-interaction and per-session ceilings; degrade to safer modes when budgets are exceeded.

### Quality targets (evaluation)
- Maintain a “golden set” of scenarios and require:
  - **no regressions** in critical flows (member safety/compliance)
  - monitored thresholds for accuracy/helpfulness on allowed intents
  - regular red-team testing for prompt injection and tool misuse

---

## How to read the rest of this repository
Each subsequent document will:
1. Identify a concrete problem
2. Describe the constraints that matter
3. State the architectural decision
4. Explain alternatives that were rejected
5. Acknowledge tradeoffs and implications

No section exists to explain *how* to build something.
Every section exists to explain **why a boundary or component exists**.

---

## Intended Use
This repository is intended to support:
- AI architecture discussions
- enterprise design reviews
- leadership alignment
- interview and portfolio demonstration

It is not intended to be used as implementation guidance.

---

## Disclaimer
All system names, flows, and interactions are **genericized**.
No proprietary systems, schemas, or configurations are disclosed.

This material represents architectural reasoning only.
