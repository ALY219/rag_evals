from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from app.rag.pipeline import query_rag_system
from app.agents.runner import run_agent

app = FastAPI(title="RAG & Grounded Agent API", version="1.0.0")

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