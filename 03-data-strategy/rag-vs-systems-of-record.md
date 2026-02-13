# Article 3 â€” Data Strategy  
## RAG vs Systems of Record

---

## Decision table: RAG vs Tools (KB vs Systems of Record)

| Need | Use RAG / KB Retrieval | Use Tool (System-of-Record access) | Notes |
|---|---|---|---|
| Explain policies, benefits, procedures, FAQs | âœ… | âŒ | Cite sources; avoid fabricating transactional outcomes |
| Answer â€œwhat does this code mean?â€ (e.g., reason/denial code definitions) | âœ… | âœ… | Tool gets the *code*; RAG explains the *meaning* |
| Provide claim status / eligibility / coverage attributes | âŒ | âœ… | System-of-record is the source of truth |
| Create/update a case, appeal, authorization, request | âŒ | âœ… (guarded) | Requires approvals / HITL for high-risk intents |
| Troubleshoot â€œwhy did the system do X?â€ | âœ… | âœ… | Combine logs/tool outputs with KB explanations |


---

## Knowledge base (KB) governance and lifecycle

RAG is only as trustworthy as the knowledge sources behind it. In regulated domains, the KB must be treated as a governed asset with clear ownership, freshness expectations, and emergency removal controls.

### 1) Approved source types (examples)
KB content must come from approved systems, such as:
- official policy documents (PDFs, controlled wikis)
- standard operating procedures (SOPs)
- provider/member-facing FAQs
- internal runbooks and knowledge articles

**Non-approved by default**
- ad-hoc notes, personal docs, unreviewed content
- scraped web content without explicit approval

### 2) Data classification rules (what is allowed in KB)
- **PHI is excluded by default** from KB and vector stores.
- KB is intended for **explanatory knowledge**, not member-specific data.
- If any exception is required (rare), it must be explicitly approved with:
  - documented purpose
  - restricted audience
  - encryption and access controls
  - retention limits
  - retrieval filters that prevent broad exposure

### 3) Ownership and approvals
Define ownership explicitly:
- **Data Steward:** accountable for KB quality, source approvals, metadata standards
- **Security/Compliance:** approves classification rules and any PHI-related exceptions
- **Platform Owner:** responsible for ingestion pipeline, retrieval controls, and auditability

**Approval gate**
- No new KB source enters production RAG without a documented approval (PR/record).

### 4) Ingestion pipeline (controlled steps)
A standard pipeline should include:
1. Source acquisition (from approved repository)
2. Content normalization (format cleanup, removal of sensitive fields if present)
3. Chunking strategy (consistent chunk sizes, stable boundaries)
4. Metadata enrichment (source, version, owner, classification, effective dates)
5. Embedding generation
6. Index publish to vector store
7. Verification checks (spot sampling, retrieval tests, citation validation)

### 5) Freshness, re-indexing, and “staleness” control
Define minimum expectations:
- **Freshness SLA:** how quickly updates must be reflected (e.g., within X days/hours)
- **Re-index cadence:** scheduled refresh for key sources (weekly/monthly)
- **Stale content protection:** prefer content with effective/last-updated metadata
- **Deprecation handling:** expired policies must be removed or deprioritized automatically

### Freshness and deprecation rules (minimum)

To prevent stale or incorrect guidance from being “amplified” by RAG:

- **Every KB item must carry metadata:** `source`, `owner`, `effectiveDate`, `lastReviewedDate`, and (when applicable) `expiryDate`.
- **Expiry-aware retrieval:** content past `expiryDate` must be excluded (or heavily down-ranked) by retrieval filters.
- **Review cadence:** high-impact policy sources must be reviewed on a defined schedule (e.g., quarterly) and re-indexed after review.
- **Staleness warnings:** if a user asks about a topic where the newest content is older than a threshold, the assistant should:
  - indicate potential staleness, and/or
  - prefer escalation/HITL for high-risk interpretations.
- **Deprecation process:** deprecated/incorrect articles must be:
  1) removed from retrieval immediately (kill switch),
  2) tracked with an audit record (who/when/why),
  3) replaced with corrected content and re-indexed.
### 6) Retrieval controls (prevent unsafe grounding)
- Source allowlists (only approved sources retrievable for specific intents)
- Metadata filters (classification, effective date, version)
- Query safety filters (block prompts that request sensitive content)
- Citation requirement (responses cite KB sources where applicable)

### 7) Emergency response: KB “kill switch”
If content is found to be incorrect, sensitive, or unsafe:
- The platform must support immediate removal or disabling of:
  - a specific document
  - an entire source collection
  - retrieval for a specific intent category
- All removals must be auditable (who removed, when, why)

### 8) Definition of done (KB governance)
KB is “production-ready” only when:
- sources are approved and owned
- classification rules are defined and enforced
- ingestion steps and metadata are standardized
- freshness/re-index expectations are documented
- retrieval filters and citations are working
- emergency kill switch exists and is tested

See also:
- `02-container/c4-container.md` (Tool contract standard and execution controls)
- `06-security-compliance/security-and-compliance.md` (Threat model and OWASP alignment)

---`r`n`r`n---

## Knowledge base (KB) governance and lifecycle

RAG is only as trustworthy as the knowledge sources behind it. In regulated domains, the KB must be treated as a governed asset with clear ownership, freshness expectations, and emergency removal controls.

### 1) Approved source types (examples)
KB content must come from approved systems, such as:
- official policy documents (PDFs, controlled wikis)
- standard operating procedures (SOPs)
- provider/member-facing FAQs
- internal runbooks and knowledge articles

**Non-approved by default**
- ad-hoc notes, personal docs, unreviewed content
- scraped web content without explicit approval

### 2) Data classification rules (what is allowed in KB)
- **PHI is excluded by default** from KB and vector stores.
- KB is intended for **explanatory knowledge**, not member-specific data.
- If any exception is required (rare), it must be explicitly approved with:
  - documented purpose
  - restricted audience
  - encryption and access controls
  - retention limits
  - retrieval filters that prevent broad exposure

### 3) Ownership and approvals
Define ownership explicitly:
- **Data Steward:** accountable for KB quality, source approvals, metadata standards
- **Security/Compliance:** approves classification rules and any PHI-related exceptions
- **Platform Owner:** responsible for ingestion pipeline, retrieval controls, and auditability

**Approval gate**
- No new KB source enters production RAG without a documented approval (PR/record).

### 4) Ingestion pipeline (controlled steps)
A standard pipeline should include:
1. Source acquisition (from approved repository)
2. Content normalization (format cleanup, removal of sensitive fields if present)
3. Chunking strategy (consistent chunk sizes, stable boundaries)
4. Metadata enrichment (source, version, owner, classification, effective dates)
5. Embedding generation
6. Index publish to vector store
7. Verification checks (spot sampling, retrieval tests, citation validation)

### 5) Freshness, re-indexing, and “staleness” control
Define minimum expectations:
- **Freshness SLA:** how quickly updates must be reflected (e.g., within X days/hours)
- **Re-index cadence:** scheduled refresh for key sources (weekly/monthly)
- **Stale content protection:** prefer content with effective/last-updated metadata
- **Deprecation handling:** expired policies must be removed or deprioritized automatically

### Freshness and deprecation rules (minimum)

To prevent stale or incorrect guidance from being “amplified” by RAG:

- **Every KB item must carry metadata:** `source`, `owner`, `effectiveDate`, `lastReviewedDate`, and (when applicable) `expiryDate`.
- **Expiry-aware retrieval:** content past `expiryDate` must be excluded (or heavily down-ranked) by retrieval filters.
- **Review cadence:** high-impact policy sources must be reviewed on a defined schedule (e.g., quarterly) and re-indexed after review.
- **Staleness warnings:** if a user asks about a topic where the newest content is older than a threshold, the assistant should:
  - indicate potential staleness, and/or
  - prefer escalation/HITL for high-risk interpretations.
- **Deprecation process:** deprecated/incorrect articles must be:
  1) removed from retrieval immediately (kill switch),
  2) tracked with an audit record (who/when/why),
  3) replaced with corrected content and re-indexed.
### 6) Retrieval controls (prevent unsafe grounding)
- Source allowlists (only approved sources retrievable for specific intents)
- Metadata filters (classification, effective date, version)
- Query safety filters (block prompts that request sensitive content)
- Citation requirement (responses cite KB sources where applicable)

### 7) Emergency response: KB “kill switch”
If content is found to be incorrect, sensitive, or unsafe:
- The platform must support immediate removal or disabling of:
  - a specific document
  - an entire source collection
  - retrieval for a specific intent category
- All removals must be auditable (who removed, when, why)

### 8) Definition of done (KB governance)
KB is “production-ready” only when:
- sources are approved and owned
- classification rules are defined and enforced
- ingestion steps and metadata are standardized
- freshness/re-index expectations are documented
- retrieval filters and citations are working
- emergency kill switch exists and is tested

See also:
- `02-container/c4-container.md` (Tool contract standard and execution controls)
- `06-security-compliance/security-and-compliance.md` (Threat model and OWASP alignment)

---## Why this document exists
Most AI assistant failures in healthcare are incorrectly labeled as â€œhallucination problemsâ€.

In reality, they are **data trust problems**.

This document establishes **when the AI Assistant Platform may use knowledge retrieval (RAG)** and **when it must defer to enterprise systems of record**, and explains why confusing the two leads to production failures.

---

## Problem being addressed
Healthcare AI assistants must answer questions that appear similar but differ fundamentally in risk:

- â€œWhat does my plan generally cover?â€
- â€œWhat is my deductible today?â€
- â€œIs prior authorization required for this procedure?â€
- â€œWhy was this specific claim denied?â€

Treating all of these as â€œinformation retrievalâ€ problems causes:
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
> â€œWhat typically requires prior authorization under my plan?â€

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
> â€œWas prior authorization required for my MRI last week?â€

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
> â€œWhy was my claim denied?â€

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
- attempt to â€œtrain awayâ€ hallucinations
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




