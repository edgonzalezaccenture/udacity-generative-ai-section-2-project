import os
import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from typing import Dict, List, Optional
from pathlib import Path

EMBEDDING_MODEL = "text-embedding-3-small"
MAX_CHARS_PER_DOCUMENT = 1500

def _get_embedding_function() -> OpenAIEmbeddingFunction:
    """Embedding function matching the one used by the embedding pipeline"""
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("CHROMA_OPENAI_API_KEY")
    return OpenAIEmbeddingFunction(
        api_key=api_key,
        model_name=EMBEDDING_MODEL,
        api_base=os.getenv("OPENAI_BASE_URL") or None
    )

def discover_chroma_backends() -> Dict[str, Dict[str, str]]:
    """Discover available ChromaDB backends in the project directory"""
    backends = {}
    current_dir = Path(".")

    # Look for ChromaDB directories
    chroma_dirs = [
        d for d in current_dir.iterdir()
        if d.is_dir() and d.name.lower().startswith("chroma")
    ]

    for chroma_dir in sorted(chroma_dirs):
        try:
            client = chromadb.PersistentClient(
                path=str(chroma_dir),
                settings=Settings(anonymized_telemetry=False)
            )
            collections = client.list_collections()

            for collection in collections:
                key = f"{chroma_dir.name}::{collection.name}"
                try:
                    count = collection.count()
                except Exception:
                    count = "unknown"
                backends[key] = {
                    "directory": str(chroma_dir),
                    "collection_name": collection.name,
                    "display_name": f"{collection.name} ({chroma_dir.name}, {count} chunks)",
                    "count": count
                }

        except Exception as e:
            # Keep inaccessible directories visible so the user knows why they can't be used
            error = str(e)
            backends[f"{chroma_dir.name}::error"] = {
                "directory": str(chroma_dir),
                "collection_name": "",
                "display_name": f"{chroma_dir.name} (error: {error[:50]}{'...' if len(error) > 50 else ''})",
                "count": 0
            }

    return backends

def initialize_rag_system(chroma_dir: str, collection_name: str):
    """Initialize the RAG system with specified backend (cached for performance)"""

    try:
        client = chromadb.PersistentClient(
            path=chroma_dir,
            settings=Settings(anonymized_telemetry=False)
        )
        collection = client.get_collection(
            name=collection_name,
            embedding_function=_get_embedding_function()
        )
        return collection, True, None
    except Exception as e:
        return None, False, str(e)

def _normalize_mission(mission_filter: Optional[str]) -> Optional[str]:
    """Convert UI values such as 'Apollo 11' into the stored metadata value 'apollo_11'"""
    if not mission_filter:
        return None
    mission = mission_filter.strip().lower().replace(" ", "_")
    if mission in ("all", "all_missions", "any", "none"):
        return None
    return mission

def retrieve_documents(collection, query: str, n_results: int = 3,
                      mission_filter: Optional[str] = None) -> Optional[Dict]:
    """Retrieve relevant documents from ChromaDB with optional filtering"""

    if not query or not query.strip():
        return None

    where_filter = None
    mission = _normalize_mission(mission_filter)
    if mission:
        where_filter = {"mission": mission}

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where_filter,
        include=["documents", "metadatas", "distances"]
    )

    # Results come sorted by distance; drop repeated chunks while keeping that order
    seen = set()
    documents, metadatas, distances, ids = [], [], [], []
    for doc_id, doc, metadata, distance in zip(results["ids"][0], results["documents"][0],
                                                results["metadatas"][0], results["distances"][0]):
        if doc in seen:
            continue
        seen.add(doc)
        ids.append(doc_id)
        documents.append(doc)
        metadatas.append(metadata)
        distances.append(distance)

    return {
        "ids": [ids],
        "documents": [documents],
        "metadatas": [metadatas],
        "distances": [distances]
    }

def format_context(documents: List[str], metadatas: List[Dict]) -> str:
    """Format retrieved documents into context"""
    if not documents:
        return ""

    context_parts = ["=== Retrieved NASA mission documents ==="]

    seen = set()
    for document, metadata in zip(documents, metadatas or [{}] * len(documents)):
        if document in seen:
            continue
        seen.add(document)
        i = len(seen)
        metadata = metadata or {}

        mission = metadata.get("mission", "unknown")
        mission = mission.replace("_", " ").title()
        source = metadata.get("source", "unknown source")
        category = metadata.get("document_category", "general")
        category = category.replace("_", " ").title()

        source_header = f"\n[Source {i}] Mission: {mission} | Document: {source} | Category: {category}"
        context_parts.append(source_header)

        if len(document) > MAX_CHARS_PER_DOCUMENT:
            document = document[:MAX_CHARS_PER_DOCUMENT] + "..."
        context_parts.append(document)
        context_parts.append("-" * 60)

    return "\n".join(context_parts)
