#!/usr/bin/env python3
"""
Batch evaluation of the NASA RAG system with RAGAS

Loads the questions in evaluation_dataset.txt, runs each one through the full
pipeline (retrieval -> LLM -> RAGAS) and prints per-question scores plus an
aggregate (mean, std, min, max) for every metric.
"""

import argparse
import os
from pathlib import Path
from typing import Dict, List

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

import llm_client
import rag_client
import ragas_evaluator

FIELDS = {"category", "mission", "question", "expected"}

def load_evaluation_dataset(path: str) -> List[Dict[str, str]]:
    """Parse the block-based evaluation_dataset.txt format"""
    entries = []
    current: Dict[str, str] = {}

    lines = Path(path).read_text(encoding="utf-8").splitlines() + [""]
    for line_number, line in enumerate(lines, start=1):
        line = line.strip()
        if line.startswith("#"):
            continue
        if not line:
            if current:
                if "question" not in current:
                    raise ValueError(f"{path}: entry ending at line {line_number} has no Question")
                entries.append(current)
                current = {}
            continue
        if ":" not in line:
            raise ValueError(f"{path}:{line_number}: expected 'Field: value', got {line!r}")
        field, value = line.split(":", 1)
        field = field.strip().lower()
        if field not in FIELDS:
            raise ValueError(f"{path}:{line_number}: unknown field {field!r}")
        current[field] = value.strip()

    return entries

def main():
    parser = argparse.ArgumentParser(description="Batch RAGAS evaluation of the NASA RAG system")
    parser.add_argument("--dataset", default="evaluation_dataset.txt", help="Evaluation dataset file")
    parser.add_argument("--chroma-dir", default="./chroma_db_openai", help="ChromaDB persist directory")
    parser.add_argument("--collection-name", default="nasa_space_missions_text", help="Collection name")
    parser.add_argument("--n-results", type=int, default=3, help="Number of documents to retrieve (top-k)")
    parser.add_argument("--model", default=llm_client.DEFAULT_MODEL, help="OpenAI chat model")
    parser.add_argument("--use-mission-filter", action="store_true",
                        help="Restrict retrieval to the mission given for each question")
    parser.add_argument("--limit", type=int, help="Only evaluate the first N questions")
    parser.add_argument("--output", default="evaluation_results.csv", help="CSV file for per-question results")
    args = parser.parse_args()

    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        parser.error("OPENAI_API_KEY is not set (environment or .env)")

    entries = load_evaluation_dataset(args.dataset)
    if args.limit:
        entries = entries[:args.limit]
    print(f"Loaded {len(entries)} questions from {args.dataset}")

    collection, success, error = rag_client.initialize_rag_system(args.chroma_dir, args.collection_name)
    if not success:
        raise SystemExit(f"Could not open ChromaDB collection: {error}")

    rows = []
    for i, entry in enumerate(entries, start=1):
        question = entry["question"]
        print(f"\n[{i}/{len(entries)}] ({entry.get('category', '-')}) {question}")

        mission_filter = entry.get("mission") if args.use_mission_filter else None
        results = rag_client.retrieve_documents(collection, question, args.n_results, mission_filter)
        documents = results["documents"][0] if results else []
        metadatas = results["metadatas"][0] if results else []
        context = rag_client.format_context(documents, metadatas)

        try:
            answer = llm_client.generate_response(openai_key, question, context, [], args.model)
        except Exception as e:
            answer = f"Error generating response: {e}"

        scores = ragas_evaluator.evaluate_response_quality(
            question, answer, documents, reference=entry.get("expected")
        )
        print(f"    Answer: {answer[:200]}{'...' if len(answer) > 200 else ''}")
        print(f"    Sources: {sorted({m.get('mission', '?') for m in metadatas})}")
        print(f"    Scores: {scores}")

        rows.append({
            "category": entry.get("category"),
            "mission": entry.get("mission"),
            "question": question,
            "answer": answer,
            "retrieved_missions": ", ".join(m.get("mission", "?") for m in metadatas),
            **{k: v for k, v in scores.items()}
        })

    df = pd.DataFrame(rows)
    df.to_csv(args.output, index=False)

    metric_columns = [c for c in df.columns
                      if c not in {"category", "mission", "question", "answer", "retrieved_missions",
                                   "error", "failed_metrics"}]

    print("\n" + "=" * 80)
    print("PER-QUESTION RESULTS")
    print("=" * 80)
    summary_columns = ["category", "mission"] + metric_columns
    if "error" in df.columns:
        summary_columns.append("error")
    with pd.option_context("display.max_columns", None, "display.width", 200, "display.precision", 3):
        print(df[summary_columns].to_string())

    print("\n" + "=" * 80)
    print("AGGREGATE (per metric)")
    print("=" * 80)
    if metric_columns:
        aggregate = df[metric_columns].agg(["mean", "std", "min", "max", "count"]).T
        with pd.option_context("display.precision", 3):
            print(aggregate.to_string())
    else:
        print("No metrics were computed.")

    print(f"\nPer-question results saved to {args.output}")

if __name__ == "__main__":
    main()
