import pytest
from pydantic import ValidationError
from app.agents.schemas import MaintenanceFeeInput
from app.agents.runner import run_agent

def test_maintenance_fee_input_boundary_valid():
    valid_payload = MaintenanceFeeInput(apartment_type="2 Bed", months=12)
    assert valid_payload.months == 12

def test_maintenance_fee_input_boundary_invalid():
    with pytest.raises(ValidationError):
        MaintenanceFeeInput(apartment_type="2 Bed", months=0)

    with pytest.raises(ValidationError):
        MaintenanceFeeInput(apartment_type="2 Bed", months=48)

def test_agent_eval_benchmark_suite():
    eval_cases = [
        {"query": "Fee for 1 Bed for 2 months", "expected_tool": "calculate_maintenance_fee", "substring": "16,000"},
        {"query": "Penthouse maintenance for 1 month", "expected_tool": "calculate_maintenance_fee", "substring": "30,000"},
        {"query": "What is the policy for visitors?", "expected_tool": None, "substring": "real estate assistant"},
    ]

    for case in eval_cases:
        res = run_agent(case["query"])
        assert res["tool_used"] == case["expected_tool"]
        assert case["substring"] in res["response"]