from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.orchestrator import handle_request

ROOT = Path(__file__).resolve().parent
STATIC_DIR = ROOT / "static"

app = FastAPI(title="AI Reference Architecture Control Plane MVP", version="0.1.0")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    channel: str = Field("chat", pattern="^(chat|voice)$")
    userRole: str = "MEMBER"
    userId: str = "demo-user-1"
    sessionId: str = "demo-session-1"
    approvalId: str | None = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(req: ChatRequest):
    try:
        result = handle_request(
            message=req.message,
            channel=req.channel,
            user_role=req.userRole,
            user_id=req.userId,
            session_id=req.sessionId,
            approval_id=req.approvalId,
        )
        return result
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc


# Static assets
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index():
    index_path = STATIC_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="UI not built yet")
    return FileResponse(index_path)
