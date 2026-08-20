import time
from dotenv import load_dotenv
from langfuse import Langfuse
from app.agents.schemas import MaintenanceFeeInput
from app.agents.tools import calculate_maintenance_fee

load_dotenv()
langfuse = Langfuse()

def run_agent(user_query: str) -> dict:
    start_time = time.time()
    query_lower = user_query.lower()
    
    # Tool Selection & Execution
    if any(k in query_lower for k in ["fee", "maintenance", "cost"]):
        unit = "2 Bed"
        if "1 bed" in query_lower:
            unit = "1 Bed"
        elif "3 bed" in query_lower:
            unit = "3 Bed"
        elif "penthouse" in query_lower:
            unit = "Penthouse"
        elif "villa" in query_lower:
            unit = "Villa"

        tool_input = MaintenanceFeeInput(apartment_type=unit, months=1)
        tool_output = calculate_maintenance_fee(tool_input)
        
        response_text = (
            f"Total fee for {tool_input.apartment_type}: PKR {tool_output.total_fee_pkr:,}"
            if tool_output.is_valid
            else tool_output.breakdown
        )
        tool_used = "calculate_maintenance_fee"
    else:
        response_text = "I am a real estate assistant. Ask me about maintenance fees or property specifications."
        tool_used = None

    # Telemetry
    try:
        obs = langfuse.start_observation(
            name="agent_execution",
            input=user_query,
            output=response_text,
            metadata={
                "tool_used": tool_used,
                "latency_seconds": round(time.time() - start_time, 2)
            }
        )
        obs.end()
        langfuse.flush()
    except Exception as e:
        print(f"[Langfuse Warning]: {e}")

    return {
        "response": response_text,
        "tool_used": tool_used
    }