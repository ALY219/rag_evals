from pydantic import BaseModel, Field

class MaintenanceFeeInput(BaseModel):
    apartment_type: str = Field(..., description="Type of unit, e.g., '2 Bed', '3 Bed', 'Penthouse'")
    months: int = Field(default=1, description="Number of months to compute fees for")

class MaintenanceFeeOutput(BaseModel):
    total_fee_pkr: int
    breakdown: str
    is_valid: bool