import json
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from app.schemas.chat import ChatRequest
from app.graph.multi_agent import multi_agent_graph
from app.graph.checkpointer import get_thread_config

router = APIRouter(prefix="/chat", tags=["Multi-Agent Streaming"])

async def event_generator(payload: ChatRequest):
    config = get_thread_config(payload.session_id)
    input_state = {
        "session_id": payload.session_id,
        "user_message": payload.message
    }
    
    try:
        # Stream events from LangGraph multi-agent graph
        async for event in multi_agent_graph.astream_events(input_state, config=config, version="v2"):
            kind = event.get("event")
            
            # Stream node transition metadata
            if kind == "on_chain_start" and event.get("name") in ["guardrail", "property_research", "lead_qualification", "scheduling"]:
                data = json.dumps({"type": "node_start", "node": event["name"]})
                yield f"data: {data}\n\n"
            
            # Stream finalized state update when the chain completes
            elif kind == "on_chain_end" and event.get("name") == "LangGraph":
                output = event.get("data", {}).get("output", {})
                data = json.dumps({
                    "type": "final_result",
                    "session_id": payload.session_id,
                    "response": output.get("final_answer", ""),
                    "tool_used": output.get("tool_used"),
                    "is_safe": output.get("is_safe", True),
                    "lead_info": output.get("lead_info", {}),
                    "appointment_slot": output.get("appointment_slot")
                })
                yield f"data: {data}\n\n"
                
    except Exception as e:
        error_data = json.dumps({"type": "error", "message": str(e)})
        yield f"data: {error_data}\n\n"

@router.post("/stream")
async def chat_stream_endpoint(payload: ChatRequest):
    return StreamingResponse(
        event_generator(payload),
        media_type="text/event-stream"
    )