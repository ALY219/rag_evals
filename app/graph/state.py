from typing import TypedDict, List, Optional, Dict

class AgentState(TypedDict):
    session_id: str
    user_message: str
    retrieved_documents: List[str]
    crag_decision: str
    web_results: List[str]
    lead_info: Dict[str, Optional[str]]
    appointment_slot: Optional[str]
    final_answer: str
    sources: Dict[str, List[str]]
    tool_used: Optional[str]
    is_safe: bool
    error: Optional[str]