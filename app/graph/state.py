from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    session_id: str
    user_message: str
    retrieved_documents: List[str]
    crag_decision: str
    final_answer: str
    tool_used: Optional[str]
    error: Optional[str]