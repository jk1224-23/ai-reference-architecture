# AI Reference Architecture — Healthcare Voice & Chat Assistant

This repository provides a **practical, enterprise-ready reference architecture** for building a regulated-domain AI assistant (voice + chat) with **governed agent behavior**, **tool-based system access**, **RAG for explanatory knowledge**, and **audit-first observability**.

## Who this is for
- Enterprise architects and platform engineers
- Security/compliance stakeholders
- Product teams building customer support / internal assistant experiences in regulated environments (e.g., healthcare)

## How to read this repo (recommended order)
1. **Executive summary:** `README-executive-summary.md`
2. **Scope & principles:** `00-overview/scope-and-principles.md`
3. **C4 Context:** `01-context/c4-context.md`
4. **C4 Container:** `02-container/c4-container.md`
5. **Data strategy (RAG vs Systems of Record):** `03-data-strategy/rag-vs-systems-of-record.md`
6. **Agent patterns:**  
   - `04-agent-patterns/bounded-autonomy.md`  
   - `04-agent-patterns/planner-executor.md`  
   - `04-agent-patterns/human-in-the-loop.md`
7. **Evaluation & observability:** `05-evaluation-observability/evaluation-and-observability.md`
8. **Security & compliance:** `06-security-compliance/security-and-compliance.md`
9. **Operating model & change:** `07-operating-model/operating-model-and-change.md`

## Repository structure
- `00-overview/` — scope, non-goals, principles
- `01-context/` — C4 Context diagram and boundaries
- `02-container/` — C4 Container diagram and platform building blocks
- `03-data-strategy/` — RAG vs Systems of Record stance and governance
- `04-agent-patterns/` — bounded autonomy, planner–executor, HITL controls
- `05-evaluation-observability/` — quality, monitoring, tracing, evaluation
- `06-security-compliance/` — PHI controls, RBAC, auditing, retention, threat model
- `07-operating-model/` — rollout, enablement, change management, ownership

## Design stance (in one paragraph)
The assistant is **not** a system-of-record and does **not** “do things by itself.” It proposes actions, but **policy gates and allowlisted tools** control execution; **RAG is used for explanatory knowledge**; and **human escalation** is mandatory for high-risk intents. Every decision is **traceable and auditable**.
