# Glossary

Short definitions for key terms used across this reference architecture.

---

## Agent
A reasoning component that can propose actions and request tools within explicit limits. The agent is not a system-of-record and does not have uncontrolled execution authority.

## Agentic application
An application that uses an LLM to plan/coordinate multi-step work and optionally invoke tools or workflows, typically with policy enforcement and audit controls.

## Audit-first
A design stance where every critical decision and action (intent, policy outcomes, tool calls, escalations) is traceable and reviewable.

## Bounded autonomy
A pattern where the model can propose actions, but execution is constrained by architecture: policy gates, allowlisted tools, HITL requirements, and kill switches.

## Canary rollout
A release approach where a change is deployed to a small percentage of traffic first and expanded only if metrics remain healthy.

## Circuit breaker
A resiliency control that stops calling a failing dependency/tool to prevent cascading failures and runaway retries.

## Confidence threshold
A decision boundary used to trigger escalation or fallback when intent classification or entity resolution confidence is low.

## Degrade mode
A safer operating mode used during incidents or instability (e.g., KB-only, HITL-first, tool-disabled).

## Evaluation (offline)
Pre-release testing using curated scenarios (“golden sets”) and red-team suites to measure quality, safety, and regressions.

## Golden set
A curated set of representative conversations/scenarios used for regression testing and evaluation across releases.

## Guardrail
A control that restricts unsafe behavior (policy enforcement, tool allowlists, PHI redaction, rate limits, etc.). Guardrails must be enforced outside the LLM wherever possible.

## HITL (Human-in-the-Loop)
A control requiring human review and/or approval for high-risk intents or actions (e.g., appeals, disputes, member updates, financial actions).

## Intent classification
A deterministic step that maps a user request to an intent category used for routing, policy, allowlists, and escalation decisions.

## Least privilege
A security principle where identities and tokens are granted only the minimum permissions needed for a specific task.

## LLM
Large Language Model. Used for language understanding and generation, but not treated as a system-of-record or a deterministic policy engine.

## Observability
The ability to understand system behavior through traces, logs, and metrics (including safety and governance signals).

## Policy gate / Guardrail engine
A deterministic enforcement layer that decides whether actions/tools are allowed based on RBAC, PHI rules, intent, risk tier, rate limits, and governance policies.

## RAG (Retrieval-Augmented Generation)
A technique where relevant knowledge is retrieved from an approved corpus and provided to the model for grounded responses, typically with citations.

## Risk tiering
Classification of requests into risk levels (low/medium/high) used to control tool access and escalation requirements.

## SoR (System of Record)
The authoritative source for transactional truth (claims, eligibility, authorizations, member data, etc.). The assistant must not invent SoR truth.

## Tool
A controlled capability exposed to the assistant (API call, workflow action, database query) with strict schema, permissions, and audit logging.

## Tool allowlist
A deterministic mapping of intent categories to permitted tools (and required approvals). Deny-by-default.

## Trace
A structured record of an interaction including intent, policy decisions, tool calls, escalations, and final output.

## Vector store
A database optimized for similarity search used by RAG. In regulated domains, PHI must be excluded by default unless explicitly approved and controlled.

---
