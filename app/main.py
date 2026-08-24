import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from typing import Optional, List

from app.rag.pipeline import query_rag_system
from app.agents.runner import run_agent

app = FastAPI(title="RAG & Grounded Agent API", version="1.0.0")

# Middleware: Latency tracking
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    return response

# Exception Handler: Validation Errors
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "Invalid payload format", "details": exc.errors()},
    )

# Request / Response Schemas
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

# Routes
@app.get("/")
def read_root():
    return {"status": "online", "service": "RAG & Tool-Using Agent Engine"}

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