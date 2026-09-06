# rag_evals — Production RAG & Grounded Agent API

Evaluation-driven RAG + tool-using agent backend with Langfuse observability,
Ragas benchmarking, and a pytest safety pyramid.

## Architecture
Client → FastAPI (`/query`, `/agent/query`, SSE `/api/v1/chat/stream`)
→ Guardrail node → Hybrid retrieval (ChromaDB: BM25 + dense + rerank)
→ CRAG confidence router → [web-search fallback] → Pydantic-validated tool
execution → Gemini 2.5 Flash → Langfuse v4 traces (tokens, routes, latency, cost)

## Benchmarks (Sprint B — Day 30)
| Metric | Result | Target | Status |
|---|---|---|---|
| Test suite | 19/19 passed | 100% | ✅ |
| Guardrail boundary (1 ≤ months ≤ 36) | Enforced | 100% | ✅ |
| Adversarial injection refusal | 100% blocked | ≥90% | ✅ |
| Per-request latency (X-Process-Time) | 0.005–0.12s | <0.5s | ✅ |
| Langfuse tracing | Live | — | ✅ |

## Quickstart
cp .env.example .env   # fill in your keys
pip install -r requirements.txt
uvicorn app.main:app --reload
pytest -q

## Evaluation Harness
- `evals/golden_dataset.jsonl` — 40 queries (12 factual, 8 multi-source,
  5 comparison, 8 unanswerable, 7 adversarial)
- `python evals/validate_dataset.py` — schema + distribution checks
- `python evals/run_baseline_eval.py` — Ragas benchmark vs live endpoints
