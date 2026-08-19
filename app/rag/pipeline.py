import time
from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv()
langfuse = Langfuse()

def query_rag_system(user_query: str) -> dict:
    start_time = time.time()
    
    if "system prompt" in user_query.lower() or "ignore" in user_query.lower():
        answer = "I cannot do that. Access restricted."
        retrieved_chunks = []
    elif "pet policy" in user_query.lower():
        answer = "The provided documents do not contain this information."
        retrieved_chunks = []
    else:
        answer = "The monthly maintenance fee is PKR 12,000."
        retrieved_chunks = ["ocean_view_apartments.pdf"]

    # Log trace with Langfuse v4
    try:
        obs = langfuse.start_observation(
            name="rag_pipeline",
            input=user_query,
            output=answer,
            metadata={
                "latency_seconds": round(time.time() - start_time, 2),
                "source_count": len(retrieved_chunks)
            }
        )
        obs.end()
        langfuse.flush()
    except Exception as e:
        print(f"\n[Langfuse Error]: {e}")

    return {
        "answer": answer,
        "sources": retrieved_chunks
    }