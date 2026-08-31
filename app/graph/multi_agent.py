from langgraph.graph import StateGraph, START, END
from app.graph.state import AgentState
from app.graph.checkpointer import memory_checkpointer
from app.graph.nodes.guardrail import guardrail_node
from app.graph.nodes.property_research import property_research_node
from app.graph.nodes.lead_qualification import lead_qualification_node
from app.graph.nodes.scheduling import scheduling_node

def route_intent(state: AgentState) -> str:
    if not state.get("is_safe", True):
        return "end"
        
    query = state.get("user_message", "").lower()
    
    if any(k in query for k in ["fee", "maintenance", "book", "appointment", "schedule"]):
        return "scheduling"
    elif any(k in query for k in ["budget", "buy", "rent", "contact"]):
        return "lead_qualification"
    else:
        return "property_research"

builder = StateGraph(AgentState)

builder.add_node("guardrail", guardrail_node)
builder.add_node("property_research", property_research_node)
builder.add_node("lead_qualification", lead_qualification_node)
builder.add_node("scheduling", scheduling_node)

builder.add_edge(START, "guardrail")

builder.add_conditional_edges(
    "guardrail",
    route_intent,
    {
        "end": END,
        "scheduling": "scheduling",
        "lead_qualification": "lead_qualification",
        "property_research": "property_research"
    }
)

builder.add_edge("scheduling", END)
builder.add_edge("lead_qualification", END)
builder.add_edge("property_research", END)

# Compile multi-agent graph with persistent memory checkpointer
multi_agent_graph = builder.compile(checkpointer=memory_checkpointer)