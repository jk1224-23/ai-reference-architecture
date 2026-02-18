# 5-Slide Interview Deck Script (with speaker notes)

## Slide 1 — Title + stance
**Title:** AI Reference Architecture — Healthcare Voice & Chat Assistant  
**Bullets:**
- Regulated-domain assistant (voice + chat) built for **governance and auditability**
- **Not a system-of-record**: transactional truth comes from tools
- **Bounded autonomy**: model proposes, policy decides, tools execute
- **Safety-first**: HITL for high-risk intents, degrade modes for failures

**Speaker notes:**  
Set the frame: this is not a demo bot. It’s an enterprise reference architecture for regulated environments. The key stance is separation of concerns: LLM for language and reasoning, tools for authoritative system access, policy engine for deterministic enforcement, and audit-first observability.

## Slide 2 — C4 Context: who/what interacts
**Title:** C4 Context — Clear boundaries  
**Bullets:**
- Users: Members / Providers / Internal agents via Voice & Chat channels
- Knowledge sources: Policies, SOPs, FAQs (RAG with citations)
- Systems of Record: Claims, Eligibility, Auth, Case/CRM (tool-backed)
- Boundary rule: Assistant mediates; it doesn’t replace workflows or SoR truth

**Speaker notes:**  
Explain that context is about ownership boundaries. The assistant can explain policy content via RAG, but any member-specific or transactional data is retrieved from systems-of-record through controlled tools. This prevents hallucination-as-truth and makes compliance and audit possible.

## Slide 3 — C4 Container: the control plane
**Title:** C4 Container — Enforce outside the LLM  
**Bullets:**
- **Orchestrator:** routes requests, manages state, enforces kill switches
- **Policy/Guardrail Engine:** deny-by-default, RBAC, PHI rules, HITL triggers
- **Tool Registry/Executor:** strict schemas, scoped tokens, audit metadata
- **RAG Service:** approved sources + filters + citations
- **Audit/Observability:** traces, guardrail metrics, release gates

**Speaker notes:**  
This is the heart: controls must be deterministic and enforced outside the model. The model cannot directly call tools or decide its own authority. The tool contract standard ensures every tool has schemas, error taxonomy, idempotency, and audit fields. Observability includes not just latency but policy denials, escalation rates, and PHI redaction events.

## Slide 4 — Security & governance (what makes it enterprise-ready)
**Title:** Security & governance — stop the real failures  
**Bullets:**
- Threat model: prompt injection, tool misuse, data exfiltration, PHI leakage
- Identity separation: **user vs agent/session vs tool identity**
- Least privilege: scoped credentials per tool call, no “god token”
- OWASP Agentic Top 10 alignment (2026) + kill switches for runaway behavior

**Speaker notes:**  
Call out the real attack surface: prompt injection and tool misuse. Explain deny-by-default allowlists, strict schema validation, and scoped tokens. Mention memory policy: long-term memory off by default, session state is bounded and provenance-based. Tie back to OWASP agentic guidance to show alignment with industry security thinking.

## Slide 5 — Walkthrough + operating reality
**Title:** Walkthrough — Claim status done safely  
**Bullets:**
1) Intent classification → risk tier  
2) Policy gate decides allow/deny + HITL requirement  
3) Tool call (Claims Read) with scoped token → evidence returned  
4) Response assembly: evidence-first + optional RAG explanation + citations  
5) Audit trace recorded; release gates + incident playbooks protect production

**Speaker notes:**  
Walk through one flow end-to-end and highlight what is allowed vs not allowed. Mention degrade behavior: if tool fails, go KB-only for safe intents or enforce HITL-first. Close with operational maturity: release gates (pre-merge/pre-release/post-release), canary rollout, rollback triggers, and incident playbooks for PHI leak, policy bypass, and tool outages.
