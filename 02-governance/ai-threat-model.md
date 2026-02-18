# AI Threat Model

## Purpose

Identify and mitigate risks specific to AI agent systems with tool access and PHI-sensitive data.

---

# 1. Prompt Injection

Threat:
- User attempts to override instructions or force unauthorized tool usage.

Mitigations:
- Skill allowlist enforcement
- No direct tool invocation from prompts
- System-level policy filtering before execution
- Output validation layer

---

# 2. Tool Abuse

Threat:
- Agent invokes high-risk tool without proper approval.

Mitigations:
- Tools accessible only via approved Skills
- Skill-level approval metadata
- Audit logging for all tool calls
- Least-privilege tool contracts

---

# 3. Data Exfiltration

Threat:
- Sensitive PHI exposed through RAG or output.

Mitigations:
- Data scope restrictions per skill
- PHI tagging and filtering
- No cross-domain retrieval without domain-specific skill
- Output redaction policies

---

# 4. Hallucinated Tool Calls

Threat:
- Model fabricates non-existent tools or invalid parameters.

Mitigations:
- Tool registry validation
- Strict tool contract schema
- Parameter validation before execution

---

# 5. Model Output Risk

Threat:
- Toxic, unsafe, or misleading output.

Mitigations:
- Content safety filters
- Post-generation validation
- Confidence threshold routing

---

# 6. Approval Bypass

Threat:
- Transactional skill executed without required HITL.

Mitigations:
- Approval requirement defined at skill level
- Enforcement before tool execution
- Immutable audit trail

---

# 7. Model Drift / Regression

Threat:
- Model update changes behavior unexpectedly.

Mitigations:
- Offline regression testing
- Staged deployment
- Canary rollout

---

# 8. External System Failure

Threat:
- Downstream API failure causes inconsistent state.

Mitigations:
- Retry with backoff
- Idempotency keys
- Escalation on repeated failure

---

# 9. Authorization & Identity

Threat:
- Authorization mismatch causes wrong-subject data access.
- Token replay or expired token misuse bypasses expected controls.
- Privilege escalation through tool adapter path.

Mitigations:
- Subject and scope validation before every tool call.
- Strict token validation (expiry, audience, signature) and replay protections.
- Least-privilege role mapping and deny-by-default enforcement.

---

# 10. RAG Poisoning

Threat:
- Malicious or tampered documents are introduced into knowledge sources and influence outputs.

Mitigations:
- Allowlisted ingestion sources with provenance metadata.
- Content review and integrity checks before indexing/retrieval.

---

# Security Posture Summary

This architecture enforces:
- Bounded autonomy
- Least privilege
- Human oversight for high-risk operations
- Full audit traceability
