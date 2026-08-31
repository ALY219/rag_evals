from app.graph.multi_agent import multi_agent_graph
from app.graph.checkpointer import get_thread_config

def test_checkpoint_multi_turn_state_persistence():
    session_id = "user_session_99"
    config = get_thread_config(session_id)

    # Turn 1: User provides budget information
    state_turn1 = {
        "session_id": session_id,
        "user_message": "I want to buy an apartment with budget 30 million",
        "chat_history": [],
        "retrieved_documents": [],
        "crag_decision": "",
        "web_results": [],
        "lead_info": {},
        "appointment_slot": None,
        "final_answer": "",
        "sources": {},
        "tool_used": None,
        "is_safe": True,
        "error": None
    }
    
    res1 = multi_agent_graph.invoke(state_turn1, config=config)
    assert res1["lead_info"]["budget"] == "30 million"

    # Turn 2: Follow-up query under identical thread_id
    state_turn2 = {
        "user_message": "Calculate maintenance fee for 2 Bed for 2 months",
        "chat_history": []
    }
    
    res2 = multi_agent_graph.invoke(state_turn2, config=config)
    
    # Assert state from Turn 1 (budget) persisted into Turn 2 output state
    assert res2["lead_info"]["budget"] == "30 million"
    assert res2["tool_used"] == "calculate_maintenance_fee"