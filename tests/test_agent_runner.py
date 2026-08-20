from app.agents.runner import run_agent

def test_agent_tool_routing():
    result = run_agent("What is the maintenance fee for a 3 Bed?")
    assert result["tool_used"] == "calculate_maintenance_fee"
    assert "18,000" in result["response"]

def test_agent_fallback_routing():
    result = run_agent("What time does the swimming pool close?")
    assert result["tool_used"] is None
    assert "real estate assistant" in result["response"]