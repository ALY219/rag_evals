from typing import TypedDict, List, Optional, Dict

class AgentState(TypedDict):
    session_id: str
    user_message: str
    retrieved_documents: List[str]
    crag_decision: str
    web_results: List[str]
    final_answer: str
    sources: Dict[str, List[str]]
    tool_used: Optional[str]
    error: Optional[str]