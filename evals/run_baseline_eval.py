import json
import os
from pathlib import Path
import pandas as pd
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    context_precision,
    context_recall,
    faithfulness,
    answer_relevancy,
)

EVAL_FILE = Path("evals/golden_dataset.jsonl")
RESULTS_FILE = Path("evals/baseline_results.csv")

def load_dataset():
    records = []
    with open(EVAL_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data = json.loads(line)
                # Mocking baseline retriever/generator outputs for initial pipeline dry-run
                records.append({
                    "question": data["question"],
                    "ground_truth": data["ground_truth"],
                    "contexts": [data["ground_truth"]],  # Placeholder for retrieved chunks
                    "answer": data["ground_truth"]       # Placeholder for LLM generation
                })
    return Dataset.from_pandas(pd.DataFrame(records))

def run_evaluation():
    if not os.getenv("OPENAI_API_KEY"):
        print("[!] Warning: OPENAI_API_KEY environment variable is missing.")
        print("Please set it in PowerShell using: $env:OPENAI_API_KEY='your-key'")
        return

    print("[*] Loading dataset into Ragas format...")
    dataset = load_dataset()

    print("[*] Running Ragas metric evaluations (Precision, Recall, Faithfulness, Relevancy)...")
    results = evaluate(
        dataset=dataset,
        metrics=[
            context_precision,
            context_recall,
            faithfulness,
            answer_relevancy,
        ],
    )

    df_results = results.to_pandas()
    df_results.to_csv(RESULTS_FILE, index=False)
    print(f"[✓] Baseline evaluation complete! Results saved to: {RESULTS_FILE}")
    print("\n--- Summary Metrics ---")
    print(df_results[['context_precision', 'context_recall', 'faithfulness', 'answer_relevancy']].mean())

if __name__ == "__main__":
    run_evaluation()