# SLOs and Success Metrics

## Overview

This architecture is evaluated not by model accuracy or throughput, but by **safety, governance, and operational health**.

Success means: requests are governed, decisions are auditable, and the system stays in control.

---

## Business & Safety SLOs

### Policy Decision SLO
**Metric:** Time from request received to policy decision made  
**Target:** < 200ms (p99)  
**Why:** Users notice latency; policy should be fast  
**Alert:** If p99 > 250ms for 5 minutes

```
Policy decision latency measures how quickly we can gate or allow a request.
Slow policy = frustrated users.
Fast policy = good UX without sacrificing safety.
```

---

### Tool Execution Success Rate
**Metric:** % of policy-approved tool calls that execute successfully  
**Target:** > 99.5%  
**Why:** If approved tools fail, users lose trust  
**Alert:** If success rate < 99%

```
Approved tool calls should almost always work.
If they're failing, it's a systems-of-record availability issue.
```

---

### HITL Approval SLA
**Metric:** Time from escalation to human approval  
**Target:** < 2 minutes (p95)  
**Why:** HITL is a bottleneck; must be fast  
**Alert:** If queue depth > 50 or p95 latency > 3 minutes

```
HITL is a feature, not a bug. But if humans can't keep up,
escalations back up and users wait.
Monitoring queue depth prevents this.
```

---

## Safety & Governance SLOs

### False Negatives (Harmful Request Allowed)
**Metric:** % of high-risk requests that incorrectly pass policy  
**Target:** < 0.1% (goal: 0%)  
**How Measured:** Post-incident analysis + compliance audit  
**Alert:** Any false negative is investigated

```
A false negative is when we allowed something we shouldn't have.
This is the worst outcome. It gets caught in compliance reviews
and indicates policy rules are insufficient.
```

---

### Policy Bypass Attempts
**Metric:** Count of requests that violate policy rules  
**Target:** 0 (tracked and escalated when detected)  
**How Measured:** Policy engine logs all denials  
**Alert:** Any denial is counted; patterns indicate attack or misconfiguration

```
If the same user keeps triggering POLICY_DENIED, it could be:
1. They're misusing the system (educate)
2. Our policy is too strict (review)
3. They're trying to bypass controls (escalate to security)
```

---

### Audit Trail Completeness
**Metric:** % of requests with complete trace (intent → policy → decision → outcome)  
**Target:** 100%  
**Alert:** If any request has missing events

```
Incomplete audit trails are worse than no audit trail.
They break compliance and make incident investigation impossible.
100% is non-negotiable.
```

---

### PII/PHI Exposure Incidents
**Metric:** Count of unintended exposures of sensitive data  
**Target:** 0  
**How Measured:** Monitoring + customer reports + compliance audit  
**Alert:** Any incident immediately escalates to security

```
One exposure is too many in regulated domains.
This SLO is about prevention (data redaction, access controls)
and detection (monitoring).
```

---

### Compliance Audit Findings
**Metric:** Count of control deficiencies found in annual audit  
**Target:** 0 (or trend toward 0)  
**How Measured:** External audit + internal compliance reviews  
**Alert:** Failed audits require immediate remediation

```
If audit finds we're not doing what we claim to do,
the entire architecture is compromised.
Audit findings drive priority roadmap items.
```

---

## Operational SLOs

### System Availability
**Metric:** % uptime of orchestrator and policy engine  
**Target:** 99.9% (measured monthly)  
**Alert:** If availability < 99.5%

```
Policy decisions must be available. If policy engine is down,
the entire system fails safely (default: DENY all requests).
This is acceptable but should rarely happen.
```

---

### Observability Log Ingestion
**Metric:** % of events successfully written to audit log  
**Target:** 99%+  
**Alert:** If ingestion rate < 95%

```
If we can't log what happened, we can't audit or debug.
Logging must be more reliable than the main system.
```

---

### Incident Mean-Time-To-Detect (MTTD)
**Metric:** Time from incident start to detection  
**Target:** < 5 minutes  
**How Measured:** Alert latency + human review  
**Alert:** Any incident not detected within 5 minutes triggers post-mortem

```
With good observability, we should notice problems in minutes.
If we find out from customers (not alerts), we failed.
```

---

### Incident Mean-Time-To-Resolve (MTTR)
**Metric:** Time from incident detection to fix deployed  
**Target:** < 30 minutes (for critical issues)  
**Alert:** If any critical incident takes > 60 minutes

```
How fast can we fix a problem once we know about it?
This depends on runbook quality and team training.
```

---

## What We DON'T Measure

### ❌ Model Accuracy
We don't measure "how often the LLM is correct" because:
- Policy gates most dangerous outputs
- RAG is constrained to knowledge (not transactional data)
- Incorrect LLM outputs are caught by schema validation
- The architecture assumes the LLM can hallucinate

**Instead:** We measure policy effectiveness and tool execution success.

---

### ❌ Hallucination Rate
We don't measure this because:
- Hallucinations are inevitable
- Our architecture prevents their impact (not the hallucination itself)
- Measuring something we don't control is misleading
- Focus should be on: Does the system catch bad outputs?

**Instead:** We measure if bad outputs are blocked by schema validation.

---

### ❌ User Satisfaction
We don't optimize for satisfaction in the traditional sense because:
- Safety > speed
- Governance > convenience
- Audit trail > hidden magic
- Users in regulated domains expect process, not magic

**Instead:** We measure if users can complete their tasks safely.

---

### ❌ Token Efficiency
We don't optimize for tokens because:
- Cost is secondary to safety
- Policy + audit trail require structured logging
- Trying to be "cheap" often means cutting corners
- Enterprise budgets can absorb token costs

**Instead:** We optimize for observability and control.

---

## Monitoring & Alerting Strategy

### Tier 1: Critical (Immediate Alert)
```
- PII exposure detected
- Policy engine unavailable
- Audit trail ingestion failing
- False negative detected (harmful request allowed)
```

### Tier 2: High (Alert within 5 minutes)
```
- HITL queue backing up
- Policy decision latency > 250ms
- Tool execution success < 99%
- Compliance rule violation
```

### Tier 3: Medium (Daily review)
```
- Trend in policy denials (increasing)
- HITL SLA creeping up
- Observability ingestion < 99%
- Incident MTTD > 5 minutes
```

---

## Review Cadence

### Daily
- Incident alerts
- Queue depth monitoring
- Availability metrics

### Weekly
- Policy denial trends
- Tool execution errors
- HITL performance

### Monthly
- SLO attainment (all metrics)
- Audit trail completeness
- Operational health score

### Quarterly
- Security review (policy rules)
- Compliance gap analysis
- Architecture effectiveness

### Annually
- External compliance audit
- Threat model refresh
- Architecture review

---

## Example Dashboard Tiles

```
┌─────────────────────────────────────┐
│ Policy Decision Latency (p99)       │
│ Target: < 200ms                     │
│ Current: 145ms ✅                   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Tool Execution Success Rate         │
│ Target: > 99.5%                     │
│ Current: 99.7% ✅                   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ HITL Queue Depth (now)              │
│ Alert Threshold: > 50               │
│ Current: 12 ✅                      │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Audit Trail Completeness            │
│ Target: 100%                        │
│ Current: 100% ✅                    │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ PII Exposures (This Month)          │
│ Target: 0                           │
│ Current: 0 ✅                       │
└─────────────────────────────────────┘
```

---

## Key Insight

> **Measure what you care about: control, safety, and auditability. Not throughput or cleverness.**

This architecture is about **operational certainty**, not peak performance.
