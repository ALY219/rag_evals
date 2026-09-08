from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class VapiFunctionCall(BaseModel):
    name: str
    arguments: Dict[str, Any]

class VapiToolCall(BaseModel):
    id: str
    type: str = "function"
    function: VapiFunctionCall

class VapiArtifact(BaseModel):
    transcript: Optional[str] = None
    summary: Optional[str] = None
    recordingUrl: Optional[str] = None

class VapiMessagePayload(BaseModel):
    type: str = Field(..., description="Vapi event type: 'tool-calls', 'assistant-request', or 'end-of-call-report'")
    toolCalls: Optional[List[VapiToolCall]] = None
    call: Optional[Dict[str, Any]] = None
    artifact: Optional[VapiArtifact] = None

class VapiToolResult(BaseModel):
    toolCallId: str
    result: str

class VapiResponse(BaseModel):
    results: Optional[List[VapiToolResult]] = None
    assistant: Optional[Dict[str, Any]] = None
    status: Optional[str] = None