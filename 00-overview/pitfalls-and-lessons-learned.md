# Pitfalls & Lessons Learned

## What We Got Wrong (So You Don't)

---

## 1. Putting All Safety in Prompts

**❌ The Mistake:**
"We'll add system prompts that tell the LLM to be careful, follow policy, and never breach compliance."

**What Happened:**
- Prompts got jailbroken
- Users found creative ways to ask harmful questions
- Safety rules were bypassed with role-play and hypotheticals
- Policy enforcement was inconsistent (different models, different behavior)

**✅ What We Do Now:**
Safety is enforced **outside the LLM**, in a dedicated policy engine:
- Policy rules are checked before tool execution
- LLM output is validated against schema
- Allowlisting prevents unauthorized tool calls
- Jailbreaks don't matter because policy is external

**Why This Matters:**
Prompts are suggestions. Policy is enforcement.

---

## 2. Treating RAG as a Source of Truth

**❌ The Mistake:**
"RAG gives us up-to-date information. We can use it for claims status, eligibility, everything."

**What Happened:**
- Vector stores drifted from reality
- Claim amounts were outdated (cost money)
- Eligibility rules changed but RAG wasn't updated
- Customers got wrong information with "high confidence"
- Audit trail was incomplete (vector store is not auditable)

**✅ What We Do Now:**
- **RAG = Knowledge Only** (policies, FAQs, explanations)
- **Systems of Record = Truth** (claims, eligibility, authorization)
- Never use RAG for transactional data
- Hybrid answers are explicitly separated and marked

**Why This Matters:**
Vector stores are probabilistic. Databases are auditable. Use each for what it's designed for.

---

## 3. Making HITL Optional or Ad-Hoc

**❌ The Mistake:**
"We'll escalate to humans when something feels risky."

**What Happened:**
- Inconsistent escalation (same situation, sometimes escalated, sometimes not)
- High-risk actions executed without approval
- Liability when something went wrong
- Audit trail showed "no human approval" for sensitive operations

**✅ What We Do Now:**
- HITL is **required by policy** for HIGH-risk intents
- Policy decision is made upfront (not after LLM reasoning)
- No exceptions or "feels wrong" heuristics
- Audit log shows: HITL required → Human approved → Tool executed

**Why This Matters:**
Consistency is compliance. Audit trails are legal protection.

---

## 4. Skipping Observability Design

**❌ The Mistake:**
"We'll add monitoring later. For now, just log some debug info."

**What Happened:**
- Silent failures (tool calls that returned nothing)
- No trace of what the LLM requested vs. what actually executed
- Compliance audits found gaps in audit trails
- Incidents took hours to investigate because logs weren't structured
- "What happened?" became impossible to answer

**✅ What We Do Now:**
- Observability is designed upfront (not retrofitted)
- Traces capture: intent → policy decision → tool call → audit event
- Every decision point is logged with timestamps and metadata
- Audit trail is immutable and complete

**Why This Matters:**
Silent failures are worse than loud ones. You can't fix what you don't see.

---

## 5. No Tool Contract Enforcement

**❌ The Mistake:**
"The LLM knows what tools exist and what parameters they need."

**What Happened:**
- LLM called tools with wrong parameters (claim_id="all claims")
- Tools executed with invalid data
- Schema validation happened inside the tool (too late)
- One bad tool call bypassed all safety layers
- Audit trail showed garbage-in, garbage-out

**✅ What We Do Now:**
- Tool contracts are defined in JSON schema
- Tool calls are validated **before execution** (outside the LLM)
- Only allowlisted tools can be called
- Invalid calls are rejected with clear error messages
- Tool parameters are schema-validated

**Why This Matters:**
The LLM is creative but unreliable. Let the policy engine be the gatekeeper.

---

## 6. Assuming Audit Logs Are Enough

**❌ The Mistake:**
"We'll log everything and review logs if there's a problem."

**What Happened:**
- Logs were incomplete (missing context)
- Timestamps didn't align across services
- Audit trail had gaps
- Couldn't reconstruct decision-making during incident
- Compliance review found missing evidence

**✅ What We Do Now:**
- Observability events are structured (JSON with consistent schema)
- Traces link intent → policy → tool → outcome
- Every event includes: timestamp, actor, resource, decision, approval status
- Audit logs are immutable and queryable
- Incident response can reconstruct exact flow

**Why This Matters:**
Audit logs are legal evidence. They must be complete and defensible.

---

## 7. Not Planning for HITL Bottlenecks

**❌ The Mistake:**
"We'll add HITL gates for safety. Humans will approve quickly."

**What Happened:**
- HITL queue grew faster than humans could approve
- Users waited hours for responses
- Customers complained about system being "slower than before"
- SLA violations happened
- Some high-risk items were auto-approved to reduce queue (defeating the purpose)

**✅ What We Do Now:**
- Risk tiering means only HIGH-risk intents require HITL
- LOW-risk and MEDIUM-risk have faster paths (policy-only)
- HITL SLA is explicit (target: < 2 minutes)
- Monitoring alerts if queue depth exceeds threshold
- Escalation path exists for backed-up approvals

**Why This Matters:**
HITL is necessary but not free. Design for realistic human throughput.

---

## 8. Confusing Policy with Configuration

**❌ The Mistake:**
"Policy is just configuration. We can change it anytime without oversight."

**What Happened:**
- Policy changes happened without approval
- Risk tier for an intent was lowered (accidentally or intentionally)
- What was HIGH-risk suddenly didn't require HITL
- Compliance officer didn't notice
- Bad thing happened

**✅ What We Do Now:**
- Policy is versioned and change-controlled
- Policy changes require approval (not just deployment)
- All policy changes are audited
- Rollback is possible
- Breaking changes are tested before applying

**Why This Matters:**
Policy is not configuration. It's control.

---

## 9. RAG Hallucinations Are Not Your Problem

**❌ The Mistake (Common Misconception):**
"We need better models or better prompts to reduce RAG hallucinations."

**What Happened:**
- Focus on model quality, not architecture
- Spent time fine-tuning
- Hallucinations still happened
- Realized: This is the wrong problem to solve

**✅ What We Do Now:**
- **Architecture prevents hallucination impact** (not the hallucination itself)
- RAG answers are only used for knowledge (never transactional data)
- Hybrid answers are marked: "AI generated" vs. "from system of record"
- Citation tracking shows where information came from
- Users know which information is AI and which is authoritative

**Why This Matters:**
You can't eliminate hallucinations. You can eliminate their impact.

---

## 10. Underestimating Compliance Scope

**❌ The Mistake:**
"Compliance means HIPAA. We'll add some encryption and call it done."

**What Happened:**
- Compliance audit found gaps in audit trails
- Retention requirements weren't met
- Access controls were incomplete
- PII redaction wasn't consistent
- Had to redesign in a rush

**✅ What We Do Now:**
- Compliance is architectural, not bolted-on
- Audit trail design accounts for legal holds
- Data retention is built into observability
- PII/PHI redaction happens at write-time (not read-time)
- Access controls are enforced at policy layer

**Why This Matters:**
Compliance is not a feature. It's a requirement that shapes architecture.

---

## What We Still Get Wrong

This architecture is not perfect. We still:
- Struggle with HITL SLA during peak load
- Have to balance policy strictness vs. user experience
- Find edge cases in risk tiering
- Discover new threat vectors in production

The difference: We have a framework to handle when things go wrong.

---

## The Core Lesson

> **Architecture is about intentional constraints, not unlimited capability.**

We don't try to make AI do everything. We define what it **should** do, build controls to enforce it, and measure whether it's working.

Everything else follows.
