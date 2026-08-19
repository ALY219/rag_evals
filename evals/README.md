# Real Estate RAG Golden Evaluation Dataset

## Dataset Architecture
This directory contains the 40-question golden benchmark dataset used to measure context precision, context recall, faithfulness, and answer relevancy.

### Category Distribution
- **factual (12)**: Direct single-source lookup questions.
- **multi_source (8)**: Multi-document synthesis and cross-reference reasoning.
- **comparison (5)**: Pricing, amenity, and specification comparisons.
- **unanswerable (8)**: Out-of-scope domain questions testing system refusal.
- **adversarial (7)**: Prompt injection and tool-jailbreak attempts.

## Schema Standard (`golden_dataset.jsonl`)
```json
{
  "question": "string",
  "ground_truth": "string",
  "category": "factual | multi_source | comparison | unanswerable | adversarial",
  "expected_source": "string | null",
  "should_answer": boolean
}