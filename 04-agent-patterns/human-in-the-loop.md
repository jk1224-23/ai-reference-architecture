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
- regulatory / policy rulesory review may occur long after an interaction completes

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
- regulatory / policy rulesory or compliance-sensitive topics
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
- regulatory / policy rules


---

## Why HITL is non-negotiable in regulated systems
In healthcare, “accuracy” is not the only goal. The architecture must also guarantee:
- **accountability** (who approved what, and why)
- **auditability** (reconstruct the exact decision path)
- **risk containment** (prevent irreversible or unauthorized actions)
- **member safety and trust** (avoid harm from confident-but-wrong outputs)

HITL is therefore treated as an **architectural control**, not a product feature.

---

## What triggers HITL (decision drivers)
Escalation should be driven by **architecture-enforced signals**, not by the model “feeling uncertain.”

Common drivers:
- **Intent category** (e.g., appeals, grievances, disputes)
- **Confidence / ambiguity** (low classifier confidence, conflicting entities)
- **Action type** (transactional vs read-only)
- **Data sensitivity** (PHI exposure, member-identifiable data)
- **Regulatory / policy rules** (explicit “human approval required” constraints)
- **Tool failure modes** (timeouts, inconsistent system responses)
- **Safety signals** (PII redaction failures, jailbreak attempts)

---

## HITL escalation matrix (example)
| Scenario | Risk | Default action |
|---|---:|---|
| Explain a policy article with citations | Low | Auto-respond (RAG only) |
| Provide claim status pulled from SoR tools | Medium | Auto-respond **if** policy allows and evidence is complete |
| Create/modify a case, appeal, authorization, coverage decision | High | **Human approval required** before tool execution |
| Dispute, grievance, coverage denial explanation that could be interpreted as guidance | High | Escalate to human (or supervised response) |
| PHI redaction failed or policy denied | High | Escalate immediately + block response |

---

## Handoff contract (what the human must see)
A handoff is only safe if the human reviewer sees the right context, consistently.

Minimum handoff payload:
- **User intent** (classified) + confidence
- **Risk tier** + *why* it was assigned
- **Proposed action** (what the agent wants to do)
- **Tool plan** (which tools, in what order)
- **Evidence bundle** (tool outputs, citations, retrieved KB snippets)
- **Policy decision trace** (allow/deny + reasons)
- **Draft response** (what the user would receive)
- **Required approval type** (review-only vs approve-execute)

---

## Human actions (allowed operations)
Humans should be able to:
- **Approve** the draft response (send as-is)
- **Edit** the response (with changes tracked)
- **Approve execution** of a guarded tool action
- **Reject** the agent plan (force re-plan or end flow)
- **Override policy** *only with elevated role* and mandatory justification

---

## Audit requirements (must be captured)
To be audit-ready, record:
- escalation trigger(s) and timestamps
- the full handoff payload hash (or stored payload where permitted)
- approver identity + role
- decision outcome (approve/edit/reject/override)
- override justification (if any)
- final response content (or reference) and tool execution results

---

## Example: “Transactional action requires approval”
1. User requests: “Open an appeal for claim X”
2. Intent classified as **Appeal** (high-risk)
3. Policy enforces **HITL required**
4. Agent produces plan + draft response + evidence
5. Human reviews and approves execution
6. Orchestrator executes tool call with scoped token
7. Confirmation is sent to user with audit reference

---

## Summary
HITL is the **control plane for risk**:
- It prevents hidden autonomy and irreversible errors
- It provides accountable decision-making in high-risk flows
- It turns agent behavior into a governed, auditable enterprise capability
