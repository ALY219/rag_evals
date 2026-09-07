import time
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError

from app.rag.pipeline import query_rag_system
from app.agents.runner import run_agent
from app.api.v1.chat import router as chat_router
from app.api.v1.stream import router as stream_router
from app.api.v1.voice import router as voice_router

app = FastAPI(
    title="Multi-Agent Real Estate RAG API",
    version="1.0.0",
    description="Enterprise Multi-Agent Graph backend powered by LangGraph & FastAPI",
)

# Middleware: Latency tracking
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    return response

# Global Exception Handler: Pydantic Validation Errors
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "Invalid payload format", "details": exc.errors()},
    )

# Include V1 Routers (REST, SSE Streaming & Voice)
app.include_router(chat_router, prefix="/api/v1")
app.include_router(stream_router, prefix="/api/v1")
app.include_router(voice_router, prefix="/api/v1")

# Schemas for Legacy / Direct Endpoints
class RAGQueryRequest(BaseModel):
    query: str

class RAGQueryResponse(BaseModel):
    answer: str
    sources: List[str]

class AgentQueryRequest(BaseModel):
    query: str

class AgentQueryResponse(BaseModel):
    response: str
    tool_used: Optional[str] = None

# System Diagnostics Endpoints
@app.get("/")
def read_root():
    return {"status": "online", "service": "Multi-Agent Real Estate RAG Engine"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "multi_agent_rag"}

# Direct RAG and Agent Endpoints
@app.post("/query", response_model=RAGQueryResponse)
def handle_rag_query(payload: RAGQueryRequest):
    try:
        result = query_rag_system(payload.query)
        return RAGQueryResponse(answer=result["answer"], sources=result["sources"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agent/query", response_model=AgentQueryResponse)
def handle_agent_query(payload: AgentQueryRequest):
    try:
        result = run_agent(payload.query)
        return AgentQueryResponse(
            response=result["response"],
            tool_used=result["tool_used"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))