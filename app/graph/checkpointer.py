from langgraph.checkpoint.memory import MemorySaver

# In-memory checkpointer for multi-turn state retention
memory_checkpointer = MemorySaver()

def get_thread_config(session_id: str) -> dict:
    return {"configurable": {"thread_id": session_id}}