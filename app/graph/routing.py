from langgraph.graph import StateGraph, START, END
from app.graph.state import AgentState
from app.rag.pipeline import query_rag_system
from app.graph.web_search import web_search_node

def retrieve_node(state: AgentState) -> dict:
    rag_res = query_rag_system(state["user_message"])
    docs = rag_res.get("sources", [])
    answer = rag_res.get("answer", "")
    return {
        "retrieved_documents": docs,
        "final_answer": answer,
        "sources": {"internal": docs, "external": []}
    }

def grade_node(state: AgentState) -> dict:
    docs = state.get("retrieved_documents", [])
    user_query = state.get("user_message", "").lower()
    
    # Route to web search if internal RAG yields no documents or explicitly asks for external trends
    if not docs or "market trend" in user_query or "external" in user_query:
        decision = "low"
    else:
        decision = "high"
        
    return {"crag_decision": decision}

def route_crag_decision(state: AgentState) -> str:
    if state.get("crag_decision") == "high":
        return "end"
    return "web_search"

# Graph Construction with Conditional Routing
builder = StateGraph(AgentState)

builder.add_node("retrieve", retrieve_node)
builder.add_node("grade", grade_node)
builder.add_node("web_search", web_search_node)

builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "grade")

# Add conditional branch based on CRAG quality score
builder.add_conditional_edges(
    "grade",
    route_crag_decision,
    {
        "end": END,
        "web_search": "web_search"
    }
)

builder.add_edge("web_search", END)

crag_routing_graph = builder.compile()