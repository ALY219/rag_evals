from app.graph.basic_rag_graph import basic_rag_graph

def test_basic_rag_graph_execution():
    initial_state = {
        "session_id": "test_session_001",
        "user_message": "What are the maintenance fees?",
        "retrieved_documents": [],
        "crag_decision": "",
        "final_answer": "",
        "tool_used": None,
        "error": None,
    }

    output_state = basic_rag_graph.invoke(initial_state)

    assert output_state["crag_decision"] == "high"
    assert "ocean_view_apartments.pdf" in output_state["retrieved_documents"]
    assert "PKR 12,000" in output_state["final_answer"]