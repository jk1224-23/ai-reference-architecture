# Model Routing and Fallbacks

This document defines how the platform selects models (routing), how it degrades gracefully under failure (fallback), and how it enforces cost/latency/safety guardrails.

## Goals

- Predictable model selection (no ad-hoc “whatever model is available”).
- Resilience to provider outages, throttling, and upstream failures.
- Cost control (token budgets, tool-call budgets, and hard limits).
- Safety-aware routing (risk tiering, PHI/PII handling, and approval gates).

## Non-Goals

- Training, fine-tuning, or model customization details.
- Vendor-specific implementation; this is policy + architecture intent.

---

## Core Principle

**Route by intent + risk + complexity**, then apply **guardrails + fallback**.

### Routing Inputs (Signals)

- **Intent / task type**: Q&A, summarization, extraction, drafting, reasoning, coding, classification.
- **Risk tier**: PHI/PII exposure, financial impact, compliance obligations, user-facing vs internal.
- **Complexity**: multi-step reasoning, ambiguity, long context, tool orchestration needs.
- **Latency budget**: channel expectations (chat vs batch).
- **Tooling needs**: must call tools vs no tools.
- **Cost budget**: per-request and per-session caps.

---

## Model Tiers (Reference)

> Adjust names to match your providers. “Tier” is a behavior class, not a vendor.

### Tier 0 — Deterministic (No LLM)
Use rules/templates when feasible:
- input validation
- routing classification
- redaction/masking
- simple formatting
- known lookups

**Why**: cheapest, fastest, most predictable.

### Tier 1 — Fast / Cost-Optimized
Use for:
- summarization of short text
- extraction with clear schemas
- FAQ-style answers with strong retrieval grounding
- rewriting (tone/format) with low ambiguity

### Tier 2 — Reasoning / Higher-Accuracy
Use for:
- multi-hop reasoning
- ambiguous requests requiring disambiguation
- complex synthesis grounded in retrieved sources
- tool planning (multi-tool sequences)
- debugging/analysis tasks

### Tier 3 — High-Risk / Controlled
Use for:
- actions that can change state (write operations)
- workflows touching PHI/PII with high blast radius
- anything requiring compliance approval gates

**Rule**: Tier 3 requires **HITL** (human-in-the-loop) or “approval before execute” for tool calls.

---

## Default Routing Policy (Simple Table)

| Scenario | Risk | Complexity | Default Tier | Notes |
|---|---:|---:|---|---|
| Internal Q&A with RAG | Low | Low | Tier 1 | Retrieval required; no tools by default |
| Customer-facing response | Medium | Medium | Tier 2 | Add safety checks + templates |
| Generate structured output (JSON schema) | Low/Med | Medium | Tier 1→2 | Escalate to Tier 2 if validation fails |
| Multi-tool workflow (read-only tools) | Medium | High | Tier 2 | Tool allowlist, strict schemas |
| Any write-action tool call | High | Medium/High | Tier 3 | Require approval gate |

---

## Guardrails (Hard Limits)

### Token Budgets
- **Max input tokens**: enforce by truncation strategy (see below)
- **Max output tokens**
- **Max total tokens per session**
- **Max retries**: per request and per tool call

### Tool Call Budgets
- **Max tool calls per turn** (e.g., 3)
- **Max tool calls per session** (e.g., 20)
- **Max parallel tools** (e.g., 2) to avoid burst / cascading failures

### Loop Detection
Stop conditions:
- repeated identical tool calls
- repeated validation failures with no progress
- repeated “retryable” errors beyond threshold

When triggered:
- switch to safer mode (Tier 1 or Tier 0)
- ask user for clarification OR queue for human review (depending on channel)

---

## Context Window Strategy

### Truncation Order (Preferred)
1. Keep system policy + tool contracts intact
2. Keep user’s latest request intact
3. Keep retrieved evidence snippets (bounded)
4. Keep conversation summary
5. Drop older chat turns

### Summarize When
- history becomes large
- retrieved documents exceed evidence budget
- multi-turn task continues beyond context limits

**Rule**: store only safe summaries (no PHI/PII) if persistence is enabled.

---

## Fallback Strategy (Resilience)

Fallback triggers:
- model/provider outage
- rate limiting / throttling
- timeout
- safety block false positive (when policy allows retry in safer mode)
- repeated output validation failures

### Fallback Ladder (Example)
1. Retry same tier (short backoff + jitter) if retryable
2. Switch provider / model within same tier
3. Degrade Tier 2 → Tier 1 (simpler response, reduced reasoning)
4. Degrade to Tier 0 (templates + retrieval-only snippets)
5. Escalate to HITL / ticket (if user-facing and high-risk)

### Degradation Behaviors
- Reduce max tokens
- Reduce number of retrieved chunks
- Disable non-essential tools
- Return partial results + next steps

---

## Output Validation Policy

All model outputs that drive downstream behavior must be validated:
- JSON schema validation for structured outputs
- allowlist fields; reject extras if strict
- type checking and bounds checking
- safe rendering rules (no executable injection into UI)

If validation fails:
1. One repair attempt (same tier)
2. If still fails: escalate tier OR degrade to deterministic template

---

## Deployment Controls (Operational)

- Route policy is **configuration**, not hard-coded.
- Route policy changes require:
  - review (platform + security)
  - evaluation gate (regression suite)
  - canary rollout + rollback switch

---

## What to Log (Minimum)

- correlation_id (propagated through all steps)
- route decision: tier, model_id, provider
- budgets: tokens used, tool calls used
- fallback events + reasons
- validation pass/fail counts
- safety blocks and reason codes (no sensitive content)

---

## Appendix: Quick Checklist

- [ ] Tier definitions documented and agreed
- [ ] Default routing table exists
- [ ] Hard budgets enforced (tokens, tools, retries)
- [ ] Fallback ladder implemented and tested
- [ ] Output validation in place for any structured outputs
- [ ] Logs include correlation_id and route decisions
