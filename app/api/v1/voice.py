import time
from fastapi import APIRouter, HTTPException, status, Response
from app.schemas.vapi import VapiMessagePayload, VapiResponse, VapiToolResult
from app.graph.multi_agent import multi_agent_graph
from app.graph.checkpointer import get_thread_config

router = APIRouter(prefix="/voice", tags=["Voice Assistant (Vapi)"])

@router.post("/vapi", response_model=VapiResponse)
async def vapi_webhook_endpoint(payload: VapiMessagePayload, response: Response):
    start_time = time.perf_counter()
    try:
        call_id = payload.call.get("id", "vapi_default_session") if payload.call else "vapi_default_session"
        
        # Enrich thread config with trace tags & metadata for Langfuse channel filtering
        config = get_thread_config(call_id)
        config["tags"] = ["channel:voice", f"call_id:{call_id}"]
        config["metadata"] = {
            "channel": "voice",
            "call_id": call_id,
            "event_type": payload.type
        }

        # 1. Handle live speech tool calls
        if payload.type == "tool-calls" and payload.toolCalls:
            results: list[VapiToolResult] = []
            for tool_call in payload.toolCalls:
                user_message = tool_call.function.arguments.get("query") or tool_call.function.arguments.get("message", "")

                input_state = {
                    "session_id": call_id,
                    "user_message": user_message,
                    "channel": "voice"
                }

                graph_result = await multi_agent_graph.ainvoke(input_state, config=config)
                raw_answer = graph_result.get("final_answer", "I could not retrieve that information right now.")
                
                # TTS string sanitization
                speech_output = raw_answer.replace("*", "").replace("#", "").strip()

                results.append(VapiToolResult(toolCallId=tool_call.id, result=speech_output))

            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            response.headers["X-Voice-Latency-MS"] = str(latency_ms)
            return VapiResponse(results=results)

        # 2. Handle assistant call connection setup
        elif payload.type == "assistant-request":
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            response.headers["X-Voice-Latency-MS"] = str(latency_ms)
            return VapiResponse(
                assistant={
                    "firstMessage": "Hello! I am your AI Real Estate Assistant. How can I help you find or evaluate a property today?"
                }
            )

        # 3. Handle end-of-call report logging
        elif payload.type == "end-of-call-report":
            return VapiResponse(status="call_logged")

        return VapiResponse(status="ignored_event")

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Voice execution failed: {str(e)}"
        )