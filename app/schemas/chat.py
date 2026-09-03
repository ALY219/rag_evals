from pydantic import BaseModel, Field
from typing import Optional, Dict, List

class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Unique thread session ID", json_schema_extra={"example": "session_101"})
    message: str = Field(..., description="User prompt or message", json_schema_extra={"example": "I want to buy an apartment with budget 25 million"})

class ChatResponse(BaseModel):
    session_id: str
    response: str
    tool_used: Optional[str] = None
    is_safe: bool
    sources: Dict[str, List[str]]
    lead_info: Dict[str, Optional[str]]
    appointment_slot: Optional[str] = None