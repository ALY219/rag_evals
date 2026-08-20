from app.agents.schemas import MaintenanceFeeInput, MaintenanceFeeOutput

RATES_PKR = {
    "1 bed": 8000,
    "2 bed": 12000,
    "3 bed": 18000,
    "penthouse": 30000,
}

def calculate_maintenance_fee(data: MaintenanceFeeInput) -> MaintenanceFeeOutput:
    unit = data.apartment_type.lower().strip()
    
    if unit not in RATES_PKR:
        return MaintenanceFeeOutput(
            total_fee_pkr=0,
            breakdown=f"Unknown apartment type: '{data.apartment_type}'. Available options: {list(RATES_PKR.keys())}",
            is_valid=False
        )
        
    monthly_rate = RATES_PKR[unit]
    total = monthly_rate * data.months
    
    return MaintenanceFeeOutput(
        total_fee_pkr=total,
        breakdown=f"{data.apartment_type} ({data.months} mo @ PKR {monthly_rate:,}/mo)",
        is_valid=True
    )