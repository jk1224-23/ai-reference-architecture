# Article 8 — Security, Privacy & Compliance  
## PHI-First Architecture for Enterprise AI

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
