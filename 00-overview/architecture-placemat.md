# Architecture Placemat — Healthcare Voice & Chat AI Assistant

A one-page summary of the **core architecture**, **boundaries**, and **production controls** for a regulated-domain AI assistant.

---

## What this is
An enterprise reference architecture for a healthcare voice + chat assistant that:
- uses **RAG** for explanatory knowledge (policies, SOPs, FAQs)
- uses **allowlisted tools** for systems-of-record access (claims, eligibility, case mgmt)
- enforces **bounded autonomy** via policy gates and HITL
- is **audit-first** with traceability across intent → policy → tools → response

---

## System boundary (C4 Context summary)
**Actors**
- Member / Provider / Internal agent
- Contact center channels (voice/chat)
- Systems of record (claims, eligibility, auth, CRM/case)
- Knowledge sources (policies, SOPs, FAQs)

**Core idea**
The assistant is a **mediator**, not a source of truth:
- It can explain using KB/RAG
- It can retrieve transactional truth only via tools
- It cannot autonomously execute high-risk actions

See: `01-context/c4-context.md`

---

## Platform building blocks (C4 Container summary)
- **Channel Adapters:** voice/chat normalization, auth handoff
- **Conversation Orchestrator:** routing, state, escalation, kill switches
- **Policy & Guardrail Engine:** RBAC, PHI constraints, intent gates, thresholds
- **Agent Reasoning Layer:** proposes plans/actions within limits
- **Tool Registry & Execution:** deterministic allowlists, strict schemas, scoped tokens
- **RAG / Retrieval Service:** safe knowledge lookup + citations
- **Audit & Observability:** traces, metrics, evaluations, incident signals

See: `02-container/c4-container.md`

---

## Non-negotiable boundaries
- **Not a system-of-record:** transactional truth must come from tools
- **No unbounded autonomy:** the model proposes; policy decides; tools execute
- **RAG is not truth for transactions:** KB explains, tools verify
- **High-risk intents require HITL:** appeals, disputes, member updates, financial actions
- **Everything is traceable:** intent, policy decision, tool calls, escalation, final response

See: `03-data-strategy/rag-vs-systems-of-record.md` and `04-agent-patterns/bounded-autonomy.md`

---

## End-to-end walkthrough (example)
**Member asks:** “What is the status of claim X?”
1. Intent classified as **Claim Status (medium risk)**
2. Policy checks RBAC/PHI constraints; confirms tools allowed
3. Tool execution calls **Claims Read API** with scoped token
4. Response assembled with **evidence** + safe explanation (RAG for policy context if needed)
5. Audit trace recorded (intent, policy decision, tool metadata, response)

Escalate to HITL if:
- low confidence / ambiguity
- tool returns inconsistent results
- user disputes outcome or requests appeal initiation

See: `README-executive-summary.md`

---

## Production controls (what makes it enterprise-ready)
### Security
- Threat model + mitigations mapped to components
- Tool allowlists, strict schemas, least-privilege scoped tokens
- PHI/PII redaction pre/post, safe logging + retention policies
- OWASP Agentic Top 10 alignment

See: `06-security-compliance/security-and-compliance.md`

### Quality + Operations
- Release gates (pre-merge, pre-release, post-release)
- Guardrail metrics (golden signals + agent signals + safety signals)
- Canary rollout, rollback/degrade triggers
- Incident playbooks and kill switches (KB-only, HITL-first, tool circuit breakers)

See: `05-evaluation-observability/evaluation-and-observability.md` and `07-operating-model/operating-model-and-change.md`

---

## How to start reading
1. `README-executive-summary.md`
2. `01-context/c4-context.md`
3. `02-container/c4-container.md`
4. `04-agent-patterns/bounded-autonomy.md`
