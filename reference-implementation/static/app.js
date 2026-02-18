const form = document.getElementById("chat-form");
const transcriptEl = document.getElementById("transcript");
const tabs = document.querySelectorAll(".tab");
const tabContents = {
  intent: document.getElementById("tab-intent"),
  skill: document.getElementById("tab-skill"),
  policy: document.getElementById("tab-policy"),
  tools: document.getElementById("tab-tools"),
  audit: document.getElementById("tab-audit"),
};

const chipCorrelation = document.getElementById("chip-correlation");
const chipSkill = document.getElementById("chip-skill");
const chipRisk = document.getElementById("chip-risk");
const chipDecision = document.getElementById("chip-decision");
const chipMode = document.getElementById("chip-mode");
const userRoleEl = document.getElementById("userRole");
const userIdEl = document.getElementById("userId");

function setChips(payload) {
  chipCorrelation.textContent = `Correlation: ${payload?.audit?.correlationId ?? "—"}`;
  chipSkill.textContent = `Skill: ${payload?.skill?.skillId ?? "—"}`;
  chipRisk.textContent = `Risk: ${payload?.intent?.riskTier ?? "—"}`;
  chipDecision.textContent = `Decision: ${payload?.policy?.decision ?? "—"}`;
  const mode = payload?.policy?.hitlRequired
    ? "HITL"
    : payload?.policy?.decision === "DEGRADED_KB_ONLY"
    ? "KB-only"
    : "Normal";
  chipMode.textContent = `Mode: ${mode}`;
}

function setTabs(payload) {
  tabContents.intent.textContent = JSON.stringify(payload.intent || {}, null, 2);
  tabContents.skill.textContent = JSON.stringify(payload.skill || {}, null, 2);
  tabContents.policy.textContent = JSON.stringify(payload.policy || {}, null, 2);
  tabContents.tools.textContent = JSON.stringify(payload.toolCalls || [], null, 2);
  tabContents.audit.textContent = JSON.stringify(payload.audit || {}, null, 2);
}

function addTranscriptEntry(role, text) {
  const div = document.createElement("div");
  div.className = "bubble " + (role === "user" ? "user" : "bot");
  div.textContent = text;
  transcriptEl.prepend(div);
}

async function sendMessage(event) {
  event.preventDefault();
  const message = document.getElementById("message").value.trim();
  if (!message) return;

  const channel = document.getElementById("channel").value;
  const userRole = userRoleEl.value;
  const userId = userIdEl.value;
  const approvalId = document.getElementById("approvalId").value.trim() || null;

  addTranscriptEntry("user", message);

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, channel, userRole, userId, approvalId }),
    });
    if (!res.ok) {
      throw new Error(`Server returned ${res.status}`);
    }
    const data = await res.json();
    addTranscriptEntry("bot", data.response?.message || "(no message)");
    setChips(data);
    setTabs(data);
  } catch (err) {
    addTranscriptEntry("bot", `Error: ${err.message}`);
  }
}

form.addEventListener("submit", sendMessage);

userIdEl.addEventListener("change", () => {
  userRoleEl.value = userIdEl.value === "demo-agent-1" ? "AGENT" : "MEMBER";
});

tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    tabs.forEach((t) => t.classList.remove("active"));
    tab.classList.add("active");
    const target = tab.dataset.tab;
    Object.entries(tabContents).forEach(([key, el]) => {
      if (key === target) {
        el.classList.remove("hidden");
      } else {
        el.classList.add("hidden");
      }
    });
  });
});
