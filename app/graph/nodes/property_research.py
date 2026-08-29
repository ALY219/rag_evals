from app.graph.state import AgentState
from app.rag.pipeline import query_rag_system

def property_research_node(state: AgentState) -> dict:
    rag_res = query_rag_system(state["user_message"])
    docs = rag_res.get("sources", [])
    
    return {
        "retrieved_documents": docs,
        "final_answer": rag_res.get("answer", ""),
        "sources": {"internal": docs, "external": []},
        "tool_used": "property_research"
    }