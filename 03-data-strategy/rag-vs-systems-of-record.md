# Article 3 — Data Strategy  
## RAG vs Systems of Record

---

## Decision table: RAG vs Tools (KB vs Systems of Record)

| Need | Use RAG / KB Retrieval | Use Tool (System-of-Record access) | Notes |
|---|---|---|---|
| Explain policies, benefits, procedures, FAQs | ✅ | ❌ | Cite sources; avoid fabricating transactional outcomes |
| Answer “what does this code mean?” (e.g., reason/denial code definitions) | ✅ | ✅ | Tool gets the *code*; RAG explains the *meaning* |
| Provide claim status / eligibility / coverage attributes | ❌ | ✅ | System-of-record is the source of truth |
| Create/update a case, appeal, authorization, request | ❌ | ✅ (guarded) | Requires approvals / HITL for high-risk intents |
| Troubleshoot “why did the system do X?” | ✅ | ✅ | Combine logs/tool outputs with KB explanations |


## Why this document exists
Most AI assistant failures in healthcare are incorrectly labeled as “hallucination problems”.

In reality, they are **data trust problems**.

This document establishes **when the AI Assistant Platform may use knowledge retrieval (RAG)** and **when it must defer to enterprise systems of record**, and explains why confusing the two leads to production failures.

---

## Problem being addressed
Healthcare AI assistants must answer questions that appear similar but differ fundamentally in risk:

- “What does my plan generally cover?”
- “What is my deductible today?”
- “Is prior authorization required for this procedure?”
- “Why was this specific claim denied?”

Treating all of these as “information retrieval” problems causes:
- fabricated answers
- stale or incorrect responses
- compliance risk
- loss of trust

This document defines **data trust boundaries** that prevent those outcomes.

---

## Core architectural distinction

### Knowledge-based information
Information that is:
- descriptive
- policy-oriented
- generalizable
- not tied to a specific transaction
- not the source of financial or eligibility truth

Examples:
- benefit explanations
- coverage rules
- plan descriptions
- authorization guidelines
- procedural FAQs

---

### Transactional system-of-record data
Information that is:
- member- or provider-specific
- time-sensitive
- financially or operationally impactful
- legally auditable
- owned by an authoritative enterprise system

Examples:
- claim status
- deductible and out-of-pocket accumulators
- eligibility on a given date
- authorization decisions
- provider participation status

---

## Architectural rule (non-negotiable)
> **If a system of record exists, the AI Assistant must query it.  
> If no system of record exists, the AI Assistant may retrieve knowledge.**

This rule is enforced **architecturally**, not through prompt discipline.

---

## Why RAG exists in this architecture
Retrieval-Augmented Generation (RAG) exists to address a specific gap:

- Some information has no transactional owner
- Enterprise knowledge is fragmented across documents
- Policies change frequently and require version control
- Directly embedding knowledge in prompts is unmaintainable

RAG provides:
- controlled knowledge access
- traceability to source documents
- updateability without prompt rewrites

RAG is **not** a substitute for systems of record.

---

## Why RAG must be constrained
Using RAG for transactional questions introduces silent failure modes:

- outdated documents answering current-state questions
- policy text being misapplied to individual cases
- missing context such as effective dates or plan variants
- plausible but incorrect responses

These failures are difficult to detect and impossible to audit reliably.

Therefore, RAG usage is intentionally **restricted**.

---

## Data access patterns (WHY-driven)

### Pattern 1: Knowledge-first (RAG allowed)
Used when:
- the question is explanatory
- no transaction-specific answer is required
- incorrect answers do not directly cause financial harm

Example:
> “What typically requires prior authorization under my plan?”

Architectural reasoning:
- No single system of record owns the explanation
- The answer must be sourced and explainable
- Citations reduce ambiguity

---

### Pattern 2: System-of-record-first (RAG prohibited)
Used when:
- the question references a specific member, provider, or claim
- financial or eligibility outcomes are involved
- regulatory auditability is required

Example:
> “Was prior authorization required for my MRI last week?”

Architectural reasoning:
- The answer depends on historical state
- Only the authorization system is authoritative
- RAG responses would be speculative

---

### Pattern 3: Hybrid (bounded)
Used when:
- explanation is helpful
- transaction data determines the outcome

Example:
> “Why was my claim denied?”

Architectural reasoning:
- denial reason must come from claims system
- explanation of denial codes may come from knowledge
- the two must be explicitly separated

---

## Enforcing data trust architecturally
This architecture enforces data trust through:

- **Tool boundaries**  
  Transactional data is only accessible through governed tools.

- **Intent classification**  
  The orchestrator determines which data access pattern applies.

- **Policy enforcement**  
  RAG is blocked for intents classified as transactional.

- **Structured responses**  
  System-of-record outputs are never paraphrased as facts without attribution.

Trust is enforced by **structure**, not model behavior.

---

## Architectural implications
- Hallucinations are treated as **architecture defects**, not model defects.
- Knowledge and transactional data have distinct access paths.
- AI reasoning cannot decide which data source to trust independently.
- Data freshness and authority are explicit concerns.

---

## Explicit non-goals
This data strategy does **not**:
- attempt to “train away” hallucinations
- rely on prompt instructions to enforce trust
- allow knowledge documents to override transactional truth
- merge RAG and system queries into a single response path

---

## Transition to next layer
With data trust boundaries established, the next architectural concern is **autonomy**.

The following article introduces **agent patterns**, explaining:
- when AI may act
- how actions are constrained
- how humans remain in control

These patterns build directly on the data rules defined here.
