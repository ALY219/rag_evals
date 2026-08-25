from langgraph.graph import StateGraph, START, END
from app.graph.state import AgentState
from app.rag.pipeline import query_rag_system

def retrieve_node(state: AgentState) -> dict:
    rag_res = query_rag_system(state["user_message"])
    return {
        "retrieved_documents": rag_res.get("sources", []),
        "final_answer": rag_res.get("answer", "")
    }

def grade_node(state: AgentState) -> dict:
    docs = state.get("retrieved_documents", [])
    decision = "high" if docs else "low"
    return {"crag_decision": decision}

# Graph Construction
builder = StateGraph(AgentState)

builder.add_node("retrieve", retrieve_node)
builder.add_node("grade", grade_node)

builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "grade")
builder.add_edge("grade", END)

basic_rag_graph = builder.compile()