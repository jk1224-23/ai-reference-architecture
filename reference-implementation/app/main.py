from fastapi import FastAPI
from pydantic import BaseModel, Field
from app.orchestrator import handle_request

app = FastAPI(title="Reference Implementation (Control Plane MVP)")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    channel: str = Field("chat", pattern="^(chat|voice)$")
    userRole: str = "MEMBER"
    userId: str = "demo-user-1"  # for demo only; hash in audit
    sessionId: str = "demo-session-1"


@app.post("/chat")
def chat(req: ChatRequest):
    return handle_request(
        message=req.message,
        channel=req.channel,
        user_role=req.userRole,
        user_id=req.userId,
        session_id=req.sessionId,
    )
