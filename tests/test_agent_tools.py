from app.agents.schemas import MaintenanceFeeInput
from app.agents.tools import calculate_maintenance_fee

def test_calculate_fee_success():
    payload = MaintenanceFeeInput(apartment_type="2 Bed", months=3)
    result = calculate_maintenance_fee(payload)
    
    assert result.is_valid is True
    assert result.total_fee_pkr == 36000

def test_calculate_fee_invalid_unit():
    payload = MaintenanceFeeInput(apartment_type="Villa", months=1)
    result = calculate_maintenance_fee(payload)
    
    assert result.is_valid is False
    assert result.total_fee_pkr == 0