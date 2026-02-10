# Article 6 — Agent Pattern  
## Human-in-the-Loop (HITL) as an Architectural Control

---

## Why this document exists
In regulated environments, AI failures are not judged by intent — they are judged by **impact**.

Human-in-the-Loop (HITL) is often discussed as a user-experience feature or an operational fallback.  
In reality, HITL is an **architectural control mechanism** that defines:

- where AI authority ends
- where human accountability begins
- how risk is transferred safely

This document defines HITL as a **first-class architectural pattern**, not an exception path.

---

## Problem being addressed
Healthcare AI assistants operate in domains where:

- decisions affect finances, access to care, or compliance posture
- incorrect answers may be plausible but wrong
- AI confidence is not a reliable signal of correctness
- regulatory review may occur long after an interaction completes

Without explicit HITL boundaries, systems drift toward:
- silent overreach
- ambiguous accountability
- post-incident blame shifting
- erosion of user trust

This pattern ensures **deterministic human authority** where risk cannot be automated away.

---

## What HITL means in this architecture
In this reference architecture, HITL means:

> A **deterministic escalation mechanism** where AI assistance pauses and responsibility is transferred to a human actor under defined conditions.

HITL is **not**:
- a last-resort error handler
- a UX choice
- a sign of low AI confidence
- an optional operational process

It is a **designed boundary of autonomy**.

---

## When HITL is mandatory
HITL is enforced when interactions involve:

- financial impact to members or providers
- coverage determinations or denials
- appeals or grievances
- ambiguous eligibility or authorization scenarios
- regulatory or compliance-sensitive topics
- conflicting or incomplete system-of-record data

These conditions are **policy-driven**, not model-driven.

---

## Why confidence-based HITL is insufficient
Many systems rely on AI confidence scores to trigger escalation.

This approach fails because:
- models can be confidently wrong
- confidence is not calibrated to business risk
- low-risk queries may have low confidence
- high-risk queries may appear straightforward

Therefore, HITL decisions are based on:
- intent classification
- action type
- data sensitivity
- regulat
