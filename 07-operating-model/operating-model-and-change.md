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
