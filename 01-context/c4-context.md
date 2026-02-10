# Article 1 — C4 Context  
## Healthcare Voice + Chat Assistant

---

## Why this document exists
AI assistants in healthcare frequently fail **after deployment**, not during demos.

The failure is rarely caused by model quality.  
It is caused by **unclear system boundaries**:

- who the AI is allowed to interact with
- what data the AI may access
- where decision authority must stop
- when humans must intervene

This document establishes the **system context** for a healthcare voice and chat assistant, defining responsibility boundaries before any internal architecture is discussed.

---

## Problem being addressed
A healthcare AI assistant must operate in an environment that is:

- **multi-actor** (members, providers, internal agents)
- **multi-system** (claims, eligibility, authorization, CRM)
- **regulated** (PHI, audit, retention)
- **real-time** (voice latency constraints)
- **non-deterministic** (probabilistic AI behavior)

Traditional application context diagrams assume deterministic logic and explicit failures.  
AI systems violate both assumptions.

This context view exists to **contain AI behavior within safe enterprise boundaries**.

---

## Actors in the system

### Primary users
- **Member**  
  Seeks benefits, claims status, coverage explanations, and plan information.

- **Provider**  
  Requests eligibility verification, authorization requirements, and claim-related information.

- **Customer Service Representative (CSR)**  
  Uses AI assistance to summarize cases, navigate systems, and guide conversations.

---

### Supporting actors
- **Human Agent / Call Center**  
  Owns final decision authority for sensitive or high-risk interactions.

- **Compliance & Audit Functions**  
  Review AI interactions for regulatory adherence and risk management.

- **Enterprise Systems of Record**  
  Maintain authoritative business data.

---

## System under consideration: AI Assistant Platform
The **AI Assistant Platform** is the bounded system being designed.

Its responsibilities are to:
- orchestrate conversations across voice and chat channels
- interpret user intent within defined constraints
- mediate access to enterprise capabilities via governed tools
- determine when escalation to humans is required
- generate auditable interaction records

The platform is **explicitly not**:
- a system of record
- an autonomous decision-maker
- a replacement for enterprise workflows

---

## Enterprise systems of record (outside the boundary)
Examples include:
- Eligibility & Benefits systems
- Claims processing systems
- Authorization / Utilization Management systems
- Provider directory and master data
- Case management / CRM systems
- Policy and document repositories

**Architectural rule:**  
If a system of record exists, the assistant must retrieve or query information — never infer or fabricate it.

---

## Trust boundaries

### Boundary 1: User ↔ AI Assistant
This boundary governs:
- authentication and role identification
- consent and disclosure
- session isolation and continuity

The assistant must always know **who** it is speaking to and **under what authority**.

---

### Boundary 2: AI Assistant ↔ Enterprise Systems
This boundary enforces:
- tool-based access only (no direct data access)
- role-based permissions per capability
- rate limits, retries, and failure isolation
- complete audit trails for every interaction

The assistant never bypasses enterprise controls.

---

### Boundary 3: AI Assistant ↔ Human Agent
This boundary defines:
- confidence thresholds
- sensitive intent categories
- escalation criteria
- structured handoff requirements

When risk increases, **autonomy decreases**.

---

## C4 Context Diagram

```mermaid
flowchart LR
    Member["Member"] -->|Chat / Voice| Channels
    Provider["Provider"] -->|Chat / Voice| Channels
    CSR["CSR"] -->|Agent Desktop| Channels

    Channels -->|Authenticated Requests| AIPlatform["AI Assistant Platform"]

    AIPlatform -->|Escalation| HumanAgent["Human Agent"]

    AIPlatform -->|Governed Tool Calls| CoreAdmin["Core Admin Systems"]
    AIPlatform -->|Read-only Queries| ProviderDir["Provider Directory"]
    AIPlatform -->|Case Creation| CaseMgmt["Case Management"]
    AIPlatform -->|Policy Lookup (RAG)| KnowledgeStore["Policy & Knowledge Store"]

    AIPlatform -->|Audit Events| Audit["Audit / Compliance"]

---

## Architectural implications

The C4 Context defined above enforces the following architectural implications:

- The AI Assistant Platform **cannot directly access enterprise systems** and must always operate through governed interfaces.
- AI does not own or persist authoritative business data.
- All AI-initiated actions must be attributable to an authenticated user role.
- Human escalation is a **first-class architectural path**, not an exception.
- Compliance and audit functions must be able to reconstruct AI interactions after the fact.

These implications constrain all subsequent architectural and implementation decisions.

---

## Explicit non-goals

This context explicitly does **not** support the following:

- Automated coverage determinations or benefit approvals
- Autonomous financial decisions affecting members or providers
- Clinical interpretation or medical advice
- Replacement of human agents in high-risk interactions
- Model training or fine-tuning activities

Excluding these goals is intentional and necessary to maintain safety, compliance, and accountability.

---

## Decision ownership and accountability

| Decision area | Ownership |
|--------------|-----------|
| AI behavior policy and boundaries | Architecture / AI Governance |
| Model selection and lifecycle | AI Platform Team |
| Enterprise business rules | System-of-record owners |
| Escalation thresholds | Operations / Contact Center |
| Compliance and audit review | Risk & Compliance |

Clear ownership is required to prevent ambiguity during incidents or regulatory review.

---

## Transition to container-level design

With system boundaries and responsibilities established, the next step is to examine
the **internal structure of the AI Assistant Platform**.

The following article introduces the **C4 Container view**, explaining:
- why each internal container exists
- what risk it mitigates
- what it is intentionally not responsible for

All container-level decisions inherit the constraints defined in this context.

