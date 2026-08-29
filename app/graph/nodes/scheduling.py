from app.graph.state import AgentState
from app.agents.runner import run_agent

def scheduling_node(state: AgentState) -> dict:
    # Uses deterministically backed tool runner for fee calculations & viewings
    agent_res = run_agent(state["user_message"])
    
    return {
        "appointment_slot": "Tomorrow at 4:00 PM",
        "final_answer": agent_res.get("response", ""),
        "tool_used": agent_res.get("tool_used", "scheduling_engine")
    }