# Reference Architecture Release Checklist

Use this checklist before publishing changes to the reference architecture (docs-only or future implementations).

---

## 1) Document quality checks
- [ ] All markdown renders cleanly in GitHub (no broken headings, no malformed lists).
- [ ] Mermaid diagrams render without errors.
- [ ] No encoding artifacts (`�`) or BOM-related issues.
- [ ] File names and links are consistent (paths match actual files).
- [ ] Terminology is consistent (SoR vs Systems of Record; HITL; bounded autonomy).

## 2) Navigation checks
- [ ] `README.md` provides an accurate reading order and links work.
- [ ] “Start here / Next read” blocks (where present) point to valid files.
- [ ] Executive summary references the correct articles/folders.

## 3) Architecture completeness checks
- [ ] Boundaries are explicit (what the platform owns vs doesn’t own).
- [ ] RAG vs tools decision stance is clear and includes examples.
- [ ] Bounded autonomy is operationally defined (intent → policy → tools → escalation).
- [ ] HITL criteria and handoff contract are present and complete.

## 4) Security & compliance checks
- [ ] Threat model section exists and maps threats → controls → enforcement points.
- [ ] OWASP Agentic Top 10 alignment section exists (and mapping table if used).
- [ ] Identity model is clear (user vs agent vs tool identities).
- [ ] Least privilege and token scoping principles are stated.
- [ ] Data retention and logging minimization rules are stated.

## 5) Evaluation & observability checks
- [ ] Metrics include golden signals + agent signals + safety signals.
- [ ] Release gates are defined (pre-merge / pre-release / post-release).
- [ ] Rollback/degrade triggers are explicit.
- [ ] Sampling/audit approach is defined (who reviews traces, how often).

## 6) Operating model checks
- [ ] RACI table exists and has single-accountable owner per activity.
- [ ] Change lifecycle/versioning rules exist for prompts, tools, policies, models.
- [ ] Incident playbooks exist (PHI leak, policy bypass, tool outage, injection spike).

## 7) Final “ship” steps
- [ ] Summarize changes in a short changelog entry (PR description or release note).
- [ ] Tag the release (optional): `vX.Y` for major documentation revisions.
- [ ] Verify that all changes remain consistent with non-goals and principles.

---
