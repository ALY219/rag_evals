from app.graph.routing import crag_routing_graph

def test_graph_internal_rag_path():
    state = {
        "session_id": "test_001",
        "user_message": "What are the maintenance fees?",
        "retrieved_documents": [],
        "crag_decision": "",
        "web_results": [],
        "final_answer": "",
        "sources": {},
        "tool_used": None,
        "error": None
    }
    result = crag_routing_graph.invoke(state)
    assert result["crag_decision"] == "high"
    assert len(result["sources"]["internal"]) > 0
    assert len(result["sources"]["external"]) == 0

def test_graph_web_search_fallback_path():
    state = {
        "session_id": "test_002",
        "user_message": "What are the current external market trends in DHA?",
        "retrieved_documents": [],
        "crag_decision": "",
        "web_results": [],
        "final_answer": "",
        "sources": {},
        "tool_used": None,
        "error": None
    }
    result = crag_routing_graph.invoke(state)
    assert result["crag_decision"] == "low"
    assert result["tool_used"] == "web_search_fallback"
    assert len(result["sources"]["external"]) > 0
    assert "External market report" in result["final_answer"]