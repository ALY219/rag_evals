from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.rag.pipeline import query_rag_system

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
def handle_query(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=422, detail="Query cannot be empty.")
    
    response = query_rag_system(request.question)
    return response