from fastapi import APIRouter, HTTPException, status
from app.schemas.chat import ChatRequest, ChatResponse
from app.graph.multi_agent import multi_agent_graph
from app.graph.checkpointer import get_thread_config

router = APIRouter(prefix="/chat", tags=["Multi-Agent Chat"])

@router.post("", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    try:
        config = get_thread_config(payload.session_id)
        
        # Pass only current request inputs so checkpointer preserves turn-over-turn state
        input_state = {
            "session_id": payload.session_id,
            "user_message": payload.message
        }
        
        # Async execution of multi-agent graph with thread checkpointing
        result = await multi_agent_graph.ainvoke(input_state, config=config)
        
        return ChatResponse(
            session_id=payload.session_id,
            response=result.get("final_answer", ""),
            tool_used=result.get("tool_used"),
            is_safe=result.get("is_safe", True),
            sources=result.get("sources", {"internal": [], "external": []}),
            lead_info=result.get("lead_info", {}),
            appointment_slot=result.get("appointment_slot")
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent graph execution failure: {str(e)}"
        )