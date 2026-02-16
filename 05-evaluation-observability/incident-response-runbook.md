# AI Incident Response Runbook (LLM + Agents)

This runbook defines how to detect, triage, contain, and remediate incidents involving LLMs, agents, tools, and retrieval systems.

## Goals

- Minimize harm (sensitive data exposure, incorrect actions, unsafe outputs).
- Contain blast radius quickly with clear “kill switches”.
- Preserve evidence for root-cause analysis and compliance.
- Restore service safely with controlled rollback/canary.

---

## Incident Categories (Common)

1) **Sensitive Data Disclosure**
- PHI/PII appears in output, logs, traces, or downstream tool results.

2) **Prompt Injection / Jailbreak Spike**
- sudden rise in policy bypass attempts
- model following malicious instructions embedded in user content or retrieved docs

3) **Tool Misuse / Abuse**
- unexpected tool calls
- abnormal volume / cost spike
- “write” tools executed when not expected

4) **Hallucination with Business Impact**
- materially wrong guidance
- incorrect coverage/benefit interpretation
- incorrect claim/provider details

5) **Availability / Degradation**
- provider outage
- high latency
- timeouts cascading through tools/retrieval

---

## Severity Levels (Suggested)

- **SEV-1**: confirmed PHI leakage at scale, unauthorized actions, regulatory exposure
- **SEV-2**: limited PHI exposure, repeated unsafe outputs, major tool misuse, widespread outage
- **SEV-3**: localized errors, partial outage, isolated unsafe output
- **SEV-4**: near-miss, blocked attempts, minor degradations

---

## Immediate Containment (Kill Switches)

> Use the smallest lever that stops harm, then escalate if needed.

### Switch A — KB-Only Mode
- Disable tool calls
- Allow retrieval + templated responses only

Use when:
- tool misuse suspected
- cost spike
- injection suspected via tool actions

### Switch B — HITL-First Mode
- all “actions” require approval before execution
- customer-facing responses may still be drafted but require review

Use when:
- high-risk workflows
- write operations are possible
- uncertainty is high

### Switch C — Disable Specific Tools (Targeted)
- disable a single tool_id or tool category (e.g., all write tools)

Use when:
- only one tool is misbehaving or being abused

### Switch D — Disable Memory / Persistence
- prevent saving conversation summaries or user states

Use when:
- sensitive data retention risk
- memory contamination

### Switch E — Provider / Model Failover
- force routing to secondary provider/tier

Use when:
- outage, throttling, or systemic model failure

---

## Triage Checklist (First 15 Minutes)

1. Confirm incident type(s) and severity level
2. Identify time window and affected channels (chat, voice, internal, batch)
3. Activate appropriate kill switch(es)
4. Capture **correlation_ids** and a small set of representative examples
5. Determine blast radius:
   - impacted tenants/apps
   - impacted users
   - impacted tools
6. Notify incident channel + stakeholders per severity
7. Start evidence bundle collection (see below)

---

## Evidence Bundle (What to Collect)

Minimum artifacts:
- correlation_id list
- request/response metadata (timestamps, model_id, route tier)
- tool-call records (tool_id, params shape, response codes)
- retrieval records (doc ids, chunk ids, similarity scores if available)
- policy decisions (allow/deny reasons, safety classifier results)
- prompt versions / policy versions / tool contract versions
- deployment versions (agent/orchestrator build, config hashes)

**Rule**: Do not copy raw PHI into tickets. Store evidence in approved secure location.

---

## Playbooks (By Incident Type)

### A) Sensitive Data Disclosure (PHI/PII)

1. Contain
   - Disable memory/persistence (Switch D)
   - If outputs are leaking: KB-only or HITL-first
2. Stop logging leakage
   - ensure redaction/masking is applied before logs
   - reduce log level if necessary (per policy)
3. Identify source
   - model output alone vs retrieved docs vs tool results
4. Patch
   - tighten redaction
   - restrict retrieval scope
   - adjust tool outputs (mask fields)
5. Validate
   - run regression eval: “no PHI in outputs/logs”
6. Communicate
   - follow compliance notification process if required

### B) Prompt Injection / Jailbreak Spike

1. Contain
   - KB-only mode OR disable risky tools
   - tighten input filtering on retrieved docs (strip instructions)
2. Confirm vector
   - user prompt injection
   - document injection (retrieval)
   - tool response injection
3. Patch
   - strengthen tool allowlist + parameter validation
   - add instruction hierarchy enforcement
   - add output validation / safe rendering rules
4. Validate
   - run injection test suite
5. Monitor
   - track attempt rate; tune blocks to reduce false positives

### C) Tool Misuse / Abuse (Cost or Action Spike)

1. Contain
   - disable suspect tools (Switch C)
   - enforce tool-call budgets (max calls/turn)
   - if write actions: HITL-first immediately
2. Investigate
   - identify which tool_ids and consumers spiked
   - check auth scopes and token minting policies
3. Patch
   - least privilege scopes
   - per-tool rate limits
   - stronger parameter validation + schema strictness
4. Validate
   - replay a sample of abusive flows in sandbox

### D) Hallucination with Business Impact

1. Contain
   - switch to Tier 1 (more templated) or HITL-first for affected flows
2. Identify
   - missing retrieval grounding?
   - stale knowledge base?
   - ambiguous user question?
3. Patch
   - enforce retrieval-required for that intent
   - add “cite evidence” requirement
   - add output constraints (must include uncertainty / next steps)
4. Validate
   - scenario-based regression tests with known correct answers

### E) Availability / Latency Outage

1. Contain
   - model/provider failover (Switch E)
   - reduce context size and retrieval chunk count
2. Patch
   - tune timeouts + retries
   - add circuit breakers for tools
3. Validate
   - load test + chaos test (provider outage simulation)

---

## Recovery & Return to Normal

Return criteria:
- leakage stopped
- tool misuse stopped
- safety metrics back within threshold
- latency/availability within SLO
- regression eval suite passes

Rollback / forward-fix rules:
- if root cause is deployment/config → rollback
- if root cause is prompt/policy/tool contract → forward fix + canary

---

## Communications (Template)

- What happened:
- When it started / ended:
- Impacted systems/channels:
- Severity:
- Containment actions taken:
- Customer/user impact:
- Next update time:
- Owner + incident commander:

---

## Postmortem Checklist

- [ ] Root cause identified (technical + process)
- [ ] Contributing factors documented
- [ ] Corrective actions created (policy/tool/prompt/code)
- [ ] Regression tests added to prevent recurrence
- [ ] Monitoring alerts improved
- [ ] Documentation updated (routing/runbook/tool registry)
