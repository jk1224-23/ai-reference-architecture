# AI Evaluation & Reliability Strategy

## Purpose

Define how the AI Assistant is evaluated, monitored, and improved across development and production environments.

This applies to:
- Flow A (RAG – read-only)
- Flow B (Agent + Skills + HITL – transactional)

---

# 1. Evaluation Layers

## 1.1 Offline Evaluation (Pre-Deployment)

### A. Golden Dataset Testing
- Curated domain-specific test prompts
- Expected outputs / expected tool usage
- Regression comparison across model versions

Metrics:
- Response correctness %
- Grounded answer rate (RAG citation coverage)
- Tool selection accuracy %
- Hallucination rate %

---

### A.1 Golden Set Categories
- Happy path prompts
- Ambiguous prompts (clarification required)
- Adversarial prompts (prompt injection / jailbreak attempts)
- Policy-sensitive prompts (PHI/PII boundaries)
- Tool edge cases (timeouts, invalid parameters)

---

### B. Skill Routing Accuracy
- Intent → Expected Skill mapping validation
- False-positive and false-negative routing analysis

Metrics:
- Skill resolution precision / recall
- Ambiguity rate (clarification required)

---

### C. Tool Invocation Validation
- Validate tool parameters
- Validate data scope restrictions
- Validate approval triggers

Metrics:
- Invalid tool call rate
- Policy violation rate

---

### D. Identity, Subject Binding & Authorization Tests
- Validate that member/claim access is correctly bound to the authenticated subject.
- Ensure the system blocks cross-member access attempts and emits the correct events.

Metrics:
- Unauthorized access block rate
- Subject binding success rate
- False allow rate (must be 0 for cross-member access)

---

# 2. Online Evaluation (Post-Deployment)

## 2.1 Operational Metrics

- Latency (p95, p99)
- Tool execution success rate
- HITL invocation rate
- Fallback frequency

---

## 2.2 Behavioral Quality Signals

- User satisfaction score
- Clarification rate
- Escalation rate
- Response regeneration rate

---

## 2.3 Risk Signals

- Hallucination detection flags
- Unsafe output detection
- Unauthorized tool call attempts
- Rejected policy enforcement events
- subject_binding_failed / authz_denied event rate

---

# 3. Regression & Release Controls

- Model upgrade requires offline regression comparison
- Skill change requires golden-set revalidation
- Tool contract updates require compatibility check
- Rollout strategy: staged deployment (dev → test → prod)

---

## 3.1 Release Gates & Thresholds

- No regression > X% on golden-set score versus current baseline.
- Invalid tool call rate must remain below Y%.
- RAG citation coverage must remain at or above Z% for grounded answers.

Target thresholds will be set per domain after baseline.

---

# 4. Observability Events

All skills must emit:

- skill_invoked
- skill_blocked
- tool_call_started
- tool_call_completed
- approval_requested
- approval_granted / denied
- skill_failed

These events enable traceability and auditability.

---

# 5. Failure Handling Strategy

- Retrieval failure → clarification or fallback response
- Tool failure → retry (limited) → escalation
- Low confidence routing → ask user to clarify
- High-risk uncertainty → enforce HITL

---

# Outcome

The system must demonstrate:

- Controlled autonomy
- Measurable reliability
- Auditability
- Regression safety
