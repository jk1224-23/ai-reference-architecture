import re

def classify_intent(message: str, channel: str) -> dict:
    m = message.lower()

    if "appeal" in m or "grievance" in m:
        claim_id = _extract_claim_id(m)
        return {"intent": "APPEAL_INITIATION", "confidence": 0.78, "riskTier": "HIGH", "entities": _entities(claim_id)}

    if "update my address" in m or "change my address" in m:
        return {"intent": "MEMBER_UPDATE", "confidence": 0.75, "riskTier": "HIGH", "entities": {}}

    if "coverage" in m or "eligible" in m or "eligibility" in m:
        return {"intent": "ELIGIBILITY_VERIFY", "confidence": 0.80, "riskTier": "MEDIUM", "entities": {}}

    if "claim" in m and ("status" in m or "check" in m):
        claim_id = _extract_claim_id(m)
        conf = 0.86 if claim_id else (0.65 if channel == "voice" else 0.72)
        return {"intent": "CLAIM_STATUS", "confidence": conf, "riskTier": "MEDIUM", "entities": _entities(claim_id)}

    if "policy" in m or "benefit" in m or "explain" in m:
        return {"intent": "POLICY_EXPLANATION", "confidence": 0.75, "riskTier": "LOW", "entities": {}}

    if "faq" in m or "how do i" in m:
        return {"intent": "FAQ_GENERAL", "confidence": 0.70, "riskTier": "LOW", "entities": {}}

    if "ignore" in m and ("polic" in m or "rules" in m) and ("dump" in m or "all claims" in m):
        return {"intent": "UNKNOWN_OR_BLOCKED", "confidence": 0.62, "riskTier": "HIGH", "entities": {}}

    return {"intent": "UNKNOWN_OR_BLOCKED", "confidence": 0.60, "riskTier": "HIGH", "entities": {}}


def _extract_claim_id(text: str) -> str | None:
    m = re.search(r"\bclaim\s+(\d{4,})\b", text)
    if m:
        return m.group(1)
    m = re.search(r"\b(\d{5,})\b", text)
    return m.group(1) if m else None


def _entities(claim_id: str | None) -> dict:
    return {"claimId": claim_id} if claim_id else {}
