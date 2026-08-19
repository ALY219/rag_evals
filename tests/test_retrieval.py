from app.rag.pipeline import query_rag_system

def test_retrieval_returns_metadata():
    result = query_rag_system("What is the maintenance fee for Ocean View Apartments?")
    assert "sources" in result