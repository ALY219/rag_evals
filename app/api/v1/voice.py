from fastapi import APIRouter, HTTPException, status
from app.schemas.vapi import VapiMessagePayload, VapiResponse, VapiToolResult
from app.graph.multi_agent import multi_agent_graph
from app.graph.checkpointer import get_thread_config

router = APIRouter(prefix="/voice", tags=["Voice Assistant (Vapi)"])

@router.post("/vapi", response_model=VapiResponse)
async def vapi_webhook_endpoint(payload: VapiMessagePayload):
    try:
        # Extract unique call ID from Vapi or fallback to default session
        call_id = payload.call.get("id", "vapi_session_default") if payload.call else "vapi_session_default"
        config = get_thread_config(call_id)

        results: list[VapiToolResult] = []

        if payload.type == "tool-calls" and payload.toolCalls:
            for tool_call in payload.toolCalls:
                # Extract user query passed from Vapi voice model
                user_message = tool_call.function.arguments.get("query") or tool_call.function.arguments.get("message", "")

                input_state = {
                    "session_id": call_id,
                    "user_message": user_message
                }

                # Invoke LangGraph multi-agent pipeline
                graph_result = await multi_agent_graph.ainvoke(input_state, config=config)
                raw_answer = graph_result.get("final_answer", "I am unable to process that request right now.")

                # Clean output text for text-to-speech synthesis
                speech_output = raw_answer.replace("*", "").replace("#", "").strip()

                results.append(
                    VapiToolResult(
                        toolCallId=tool_call.id,
                        result=speech_output
                    )
                )

        return VapiResponse(results=results)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Voice agent execution failed: {str(e)}"
        )