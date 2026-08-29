import re
from app.graph.state import AgentState

def lead_qualification_node(state: AgentState) -> dict:
    query = state.get("user_message", "")
    
    # Extract budget intent if mentioned
    budget_match = re.search(r'(\d+)\s*(million|pkr|k)', query.lower())
    budget = budget_match.group(0) if budget_match else "Unspecified"

    lead_data = {
        "intent": "buy/rent interest",
        "budget": budget,
        "status": "qualified"
    }
    
    return {
        "lead_info": lead_data,
        "final_answer": f"Lead profile noted with budget '{budget}'. How can our property manager assist you further?",
        "tool_used": "lead_qualification"
    }