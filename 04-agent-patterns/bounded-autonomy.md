# Article 4 - Agent Patterns
## Bounded Autonomy in Enterprise AI

---

## Why this document exists
"Agent-based AI" is one of the most misunderstood concepts in enterprise systems.

In many implementations, agents are introduced as:
- autonomous actors
- long-running workflows
- systems that decide and act independently

In regulated environments such as healthcare, **unbounded autonomy is not innovation - it is risk**.

This document defines **bounded autonomy** as an architectural pattern that allows AI agents to assist, reason, and coordinate actions **without exceeding explicit decision authority**.

---

## Problem being addressed
Healthcare AI assistants are expected to:
- reason across multiple steps
- interact with several systems
- adapt to incomplete or ambiguous input

At the same time, they must:
- respect PHI boundaries
- avoid unauthorized actions
- remain auditable
- escalate correctly when risk increases

Without architectural constraints, agent systems tend to:
- accumulate hidden authority
- bypass policy enforcement
- create non-reproducible behavior
- fail silently

This article explains how **agent behavior is constrained by design**, not by intent.

---

## What an "agent" means in this architecture
In this reference architecture, an agent is defined as:

> A **reasoning component** that can propose actions, request tools, and coordinate multi-step flows **within explicitly defined limits**.

An agent is **not**:
- a system of record
- an autonomous decision-maker
- a replacement for business workflows
- a long-running background process with unchecked permissions

This definition intentionally narrows the scope of what "agent" means.

---

## The principle of bounded autonomy
Bounded autonomy is enforced through **four architectural boundaries**:

1. Scope boundaries
2. Action boundaries
3. Data boundaries
4. Escalation boundaries

Each boundary exists to control a specific failure mode.

---

## 1. Scope boundaries
**Why this boundary exists**
Without scope constraints, agents tend to generalize beyond their intended purpose.

**Architectural decision**
- Each agent operates only within a predefined intent domain.
- Cross-domain reasoning requires orchestration approval.

**Example**
A "claims assistance" agent may explain claim status but cannot initiate appeals.

---

## 2. Action boundaries
**Why this boundary exists**
Reasoning does not imply execution authority.

**Architectural decision**
- Agents may *request* actions.
- Only the orchestration + policy layers may *approve and execute* actions.

**Example**
An agent may request "create case", but cannot create one directly.

---

## 3. Data boundaries
**Why this boundary exists**
Agents must not infer or fabricate transactional truth.

**Architectural decision**
- Agents access transactional data only through approved tools.
- Knowledge retrieval (RAG) is restricted to explanatory contexts.

**Example**
An agent may retrieve a denial reason code, but explanations are sourced separately and cited.

---

## 4. Escalation boundaries
**Why this boundary exists**
AI confidence is not a reliable proxy for correctness or risk.

**Architectural decision**
- Confidence thresholds and intent classification determine escalation.
- Certain intents always require human involvement.

**Example**
Appeals, grievances, or coverage disputes escalate regardless of agent confidence.

---

## Agent execution flow (operational: where bounded autonomy is enforced)

> Autonomy is granted per intent and risk tier, enforced by policy gates and tool allowlists, with mandatory audit and human escalation paths.

```mermaid
flowchart LR
  U[User Request] --> IC[Intent Classification]
  IC --> C{Confidence >= threshold?}

  C -- No --> EH1[Escalate to Human\nAmbiguous / Low confidence] --> AL[Audit Log]

  C -- Yes --> RT[Risk Tiering\nLow / Medium / High]
  RT --> PC{Policy Check\nRBAC + PHI + Scope + Rate Limits}

  PC -- Deny --> EH2[Escalate to Human\nPolicy denied] --> AL
  PC -- Allow --> TA[Tool Allowlist Resolver\nintent -> approved tools]

  TA --> TT{Tool Type?}

  TT -- Read-only --> RAG[RAG / Search\n(KB, policies, SOPs)]
  TT -- Transactional --> GX{Guarded Execution?\nApproval required}

  GX -- No --> EH3[Escalate to Human\nTransactional requires approval] --> AL
  GX -- Yes --> EX[Execute Tool\nLeast privilege + scoped tokens]

  RAG --> RA[Response Assembly\nCitations + "source of truth" rules]
  EX --> RA

  RA --> QG{Quality Gate\nPII redaction + format checks}
  QG -- Fail --> EH4[Escalate to Human\nRedaction/quality fail] --> AL
  QG -- Pass --> OUT[Respond to User] --> AL

  AL --> MET[Metrics/Tracing\nlatency, overrides, deny-rate]
```

---

## What this design prevents (failure modes)

Bounded autonomy is not a philosophy - it is a **risk containment mechanism**. It prevents:

- **Privilege creep:** agents gaining new abilities through "just one more tool"
- **Invisible policy bypass:** LLMs calling systems-of-record without enforcement
- **Non-reproducible outcomes:** different results with no traceable decision path
- **Silent failures:** incorrect answers that never triggered escalation
- **Audit gaps:** inability to prove who/what authorized an action

---

## Implementation notes (practical enforcement points)

These constraints must be enforced **outside** the LLM:

- **Intent classification** is an upstream gate (do not rely on the model's self-reported intent)
- **Tool allowlists** must be deterministic and centrally managed (registry-driven)
- **Transactional tools** require explicit approvals (HITL, dual-control, or workflow-based)
- **PHI handling** must be validated by policy + redaction gates (pre/post checks)
- **Audit logging** must capture:
  - intent, confidence, risk tier
  - policy outcomes (allow/deny + reason)
  - tool calls (inputs/outputs where permitted)
  - escalation events and human overrides

---

## Summary

Bounded autonomy enables agents to reason and coordinate multi-step workflows **without granting them uncontrolled execution authority**.

In healthcare, this pattern is the difference between:

- **assistive automation** (safe, auditable, governed)
- **unbounded autonomy** (non-compliant, non-repeatable, high-risk)
