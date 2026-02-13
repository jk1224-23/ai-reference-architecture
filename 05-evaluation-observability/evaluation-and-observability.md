# Article 7 — Evaluation & Observability  
## Measuring Trust in Production AI Systems

---

---

## Operational metrics (what you must measure)

### Golden signals (platform)
- Latency (p50/p95/p99) — end-to-end and per hop (LLM, tools, RAG)
- Error rate — by component and by intent
- Throughput — requests/min, tool calls/min, token usage
- Saturation — queue depth, worker utilization, rate-limit hits

### Agent signals (governance)
- Escalation rate — overall and by intent/risk tier
- Policy deny rate — which rules are blocking and why
- Human override rate — approvals, edits, rejections, overrides with justification
- Tool-plan success rate — % plans that execute without re-plan/retry

### Safety signals (compliance)
- PHI/PII redaction events — count and severity
- Blocked intents / disallowed tool attempts — jailbreak / policy bypass indicators
- Hallucination flags — unsupported claims detected by evaluation tests
- Data leakage indicators — responses containing restricted identifiers

### SLO suggestions (starter targets)
- **Read-only KB answers:** p95 < 3s, error rate < 1%
- **Tool-backed answers (read):** p95 < 8s, tool failure < 2%
- **Escalations:** human handoff created < 10s, trace completeness 100%


## Why this document exists
In traditional systems, failures are explicit:
- an API returns an error
- a service goes down
- a transaction fails

In AI systems, failures are often **silent**:
- answers are plausible but wrong
- policies are applied inconsistently
- costs drift without clear root cause
- users lose trust before metrics spike

This document defines **evaluation and observability as architectural requirements**, not post-launch optimizations.

---

## Problem being addressed
Healthcare AI assistants must operate continuously under:
- non-deterministic reasoning
- evolving data and policies
- changing user behavior
- strict regulatory oversight

Without explicit evaluation and observability:
- correctness cannot be measured
- regressions go undetected
- incidents cannot be reconstructed
- accountability becomes ambiguous

This architecture treats **lack of visibility as a system failure**.

---

## Core principle
> **If AI behavior cannot be measured, it cannot be trusted.**

Evaluation answers: *Is the system doing the right thing?*  
Observability answers: *Can we understand why it did what it did?*

Both are required.

---

## Evaluation vs Observability (architectural distinction)

### Evaluation
Evaluation measures **quality and correctness** of AI behavior.

It focuses on:
- accuracy relative to expectations
- consistency over time
- regression detection after change

Evaluation is **intentional and designed**.

---

### Observability
Observability provides **evidence and traceability** of AI behavior in production.

It focuses on:
- visibility into decisions
- reconstruction of events
- incident investigation
- compliance review

Observability is **continuous and comprehensive**.

---

## What must be evaluated (WHY-driven)

### 1. Intent classification accuracy
**Why**
All downstream behavior depends on correct intent detection.

**Risk if absent**
- wrong data source selected
- improper escalation
- policy violations

---

### 2. Data source correctness
**Why**
Trust depends on using the correct authority (RAG vs system of record).

**Risk if absent**
- hallucinated transactional data
- stale or misapplied policies

---

### 3. Policy enforcement consistency
**Why**
Policies define safety and compliance boundaries.

**Risk if absent**
- autonomy creep
- inconsistent user experiences
- audit failures

---

### 4. Escalation correctness (HITL)
**Why**
Missed escalations are high-impact failures.

**Risk if absent**
- AI overreach
- human accountability gaps

---

### 5. Response quality (bounded)
**Why**
Not all incorrect answers are equally harmful.

**Risk if absent**
- false confidence
- erosion of trust

---

## Evaluation mechanisms (architectural, not tooling)

### Golden interaction sets
A curated set of representative interactions used to:
- validate expected behavior
- detect regressions
- compare behavior before and after changes

Golden sets are versioned artifacts, not ad-hoc tests.

---

### Scenario-based evaluation
Scenarios capture:
- edge cases
- high-risk intents
- ambiguous inputs

They test **decision behavior**, not linguistic quality.

---

### Change-based evaluation
Any change to:
- prompts
- policies
- tools
- data sources

must trigger targeted re-evaluation.

Evaluation is tied to **change events**, not schedules.

---

## Observability requirements (WHY-driven)

### 1. End-to-end traceability
Every interaction must be traceable across:
- user input
- intent classification
- policy decisions
- tool calls
- responses
- escalations

Without traceability, audits are speculative.

---

### 2. Decision logging (not just text)
Logs must capture:
- what decision was made
- why it was allowed or blocked
- which policy applied
- which data source was used

Free-form text logs are insufficient.

---

### 3. Behavior metrics
Architecturally relevant signals include:
- escalation rate by intent
- RAG vs system-of-record usage ratio
- tool failure and retry rates
- average cost per interaction
- no-answer and fallback frequency

These metrics measure **system health**, not model quality.

---

### 4. Incident reconstruction
The system must support:
- replaying decision paths
- understanding alternative paths that were blocked
- identifying responsibility ownership

This is essential for compliance and learning.

---

## Architectural implications
- Evaluation artifacts are first-class assets
- Observability is designed, not added later
- Silent failures are treated as incidents
- Metrics influence architecture evolution
- AI behavior becomes reviewable and improvable

---

## Explicit non-goals
This architecture does **not**:
- rely on user complaints as primary signals
- treat model confidence as correctness
- evaluate AI only during development
- prioritize linguistic fluency over decision safety

---

## Transition to next concern
With evaluation and observability defined, the remaining architectural question is **operational ownership**.

The next article addresses:
- how AI systems are operated over time
- change management and rollout
- incident response and accountability

These concerns determine whether AI systems can scale sustainably.
