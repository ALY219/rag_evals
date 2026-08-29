from app.graph.state import AgentState

def guardrail_node(state: AgentState) -> dict:
    query = state.get("user_message", "").lower()
    unsafe_keywords = ["ignore previous", "system prompt", "delete database", "drop table"]
    
    is_safe = not any(kw in query for kw in unsafe_keywords)
    
    if not is_safe:
        return {
            "is_safe": False,
            "final_answer": "I cannot perform this operation due to security policies.",
            "tool_used": "guardrail_refusal"
        }
    return {"is_safe": True}
