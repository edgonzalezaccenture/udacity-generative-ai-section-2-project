import math
import os
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from typing import Dict, List, Optional

# RAGAS imports
try:
    from ragas import SingleTurnSample
    from ragas.metrics import BleuScore, NonLLMContextPrecisionWithReference, ResponseRelevancy, Faithfulness, RougeScore
    from ragas import evaluate
    RAGAS_AVAILABLE = True
except ImportError:
    RAGAS_AVAILABLE = False

EVALUATOR_MODEL = "gpt-4o-mini"
EVALUATOR_EMBEDDING_MODEL = "text-embedding-3-small"

def _validate_inputs(question, answer, contexts) -> Optional[str]:
    """Return an error message for empty or malformed inputs, None if they are valid"""
    if not isinstance(question, str) or not question.strip():
        return "Question must be a non-empty string"
    if not isinstance(answer, str) or not answer.strip():
        return "Answer must be a non-empty string"
    if answer.startswith("Error generating response"):
        return "Answer is an error message, nothing to evaluate"
    if not isinstance(contexts, list) or not contexts:
        return "Contexts must be a non-empty list of strings (no documents were retrieved)"
    if not all(isinstance(c, str) and c.strip() for c in contexts):
        return "Every context must be a non-empty string"
    return None

def evaluate_response_quality(question: str, answer: str, contexts: List[str],
                              reference: Optional[str] = None,
                              reference_contexts: Optional[List[str]] = None) -> Dict[str, float]:
    """Evaluate response quality using RAGAS metrics

    Always computes response relevancy and faithfulness. When a reference answer is
    given it also computes BLEU and ROUGE, and with reference contexts it computes
    non-LLM context precision.
    """
    if not RAGAS_AVAILABLE:
        return {"error": "RAGAS not available"}

    validation_error = _validate_inputs(question, answer, contexts)
    if validation_error:
        return {"error": validation_error}

    try:
        base_url = os.getenv("OPENAI_BASE_URL") or None
        evaluator_llm = LangchainLLMWrapper(
            ChatOpenAI(model=EVALUATOR_MODEL, temperature=0, base_url=base_url)
        )
        evaluator_embeddings = LangchainEmbeddingsWrapper(
            OpenAIEmbeddings(model=EVALUATOR_EMBEDDING_MODEL, base_url=base_url)
        )
    except Exception as e:
        return {"error": f"Could not create evaluator models: {e}"}

    metrics = {
        "response_relevancy": ResponseRelevancy(llm=evaluator_llm, embeddings=evaluator_embeddings),
        "faithfulness": Faithfulness(llm=evaluator_llm),
    }
    failed = []
    # Optional metrics need extra packages (sacrebleu, rouge_score); skip them if missing
    optional_metrics = []
    if reference:
        optional_metrics += [("bleu_score", BleuScore), ("rouge_score", RougeScore)]
    if reference_contexts:
        optional_metrics.append(("context_precision", NonLLMContextPrecisionWithReference))
    for name, metric_class in optional_metrics:
        try:
            metrics[name] = metric_class()
        except ImportError:
            failed.append(f"{name} (missing dependency)")

    sample = SingleTurnSample(
        user_input=question,
        response=answer,
        retrieved_contexts=contexts,
        reference=reference,
        reference_contexts=reference_contexts
    )

    results = {}
    for name, metric in metrics.items():
        try:
            score = metric.single_turn_score(sample)
            if score is None or math.isnan(score):
                failed.append(name)
            else:
                results[name] = float(score)
        except Exception as e:
            failed.append(f"{name} ({type(e).__name__})")

    if not results:
        return {"error": f"All metrics failed: {', '.join(failed)}"}
    if failed:
        results["failed_metrics"] = ", ".join(failed)
    return results
