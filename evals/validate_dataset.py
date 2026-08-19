import json
from collections import Counter
from pathlib import Path

EVAL_FILE = Path("evals/golden_dataset.jsonl")


def validate_dataset():
    if not EVAL_FILE.exists():
        print(f"[!] File {EVAL_FILE} not found.")
        return

    categories = Counter()
    total = 0
    required_keys = {
        "question",
        "ground_truth",
        "category",
        "expected_source",
        "should_answer",
    }

    with open(EVAL_FILE, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue
            data = json.loads(line)

            # Enforce Schema Completeness
            missing = required_keys - set(data.keys())
            if missing:
                print(f"[!] Line {line_num} missing keys: {missing}")

            categories[data["category"]] += 1
            total += 1

    print("\n--- Golden Dataset Category Distribution ---")
    for cat, count in categories.items():
        print(f" - {cat}: {count}")
    print(f"\nTotal Questions: {total} / 40 Target")


if __name__ == "__main__":
    validate_dataset()