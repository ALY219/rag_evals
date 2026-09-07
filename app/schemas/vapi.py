from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class VapiFunctionCall(BaseModel):
    name: str
    arguments: Dict[str, Any]

class VapiToolCall(BaseModel):
    id: str
    type: str = "function"
    function: VapiFunctionCall

class VapiMessagePayload(BaseModel):
    type: str = Field(..., description="Message type from Vapi, e.g., tool-calls")
    toolCalls: Optional[List[VapiToolCall]] = None
    call: Optional[Dict[str, Any]] = None

class VapiToolResult(BaseModel):
    toolCallId: str
    result: str

class VapiResponse(BaseModel):
    results: List[VapiToolResult]