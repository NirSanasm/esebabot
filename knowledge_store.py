"""
ChromaDB Knowledge Store — embeds the KNOWLEDGE_BASE using Gemini embeddings
and provides semantic search for the AI chat pipeline.
"""

import chromadb
from google import genai
import os
import time
from typing import Optional


CHROMA_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")
COLLECTION_NAME = "eseba_knowledge"
EMBED_MODEL = "gemini-embedding-001"

# Module-level state
_client: Optional[chromadb.PersistentClient] = None
_collection: Optional[chromadb.Collection] = None
_genai_client: Optional[genai.Client] = None


def _get_genai_client() -> genai.Client:
    """Lazy-init the Gemini client."""
    global _genai_client
    if _genai_client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not set in environment")
        _genai_client = genai.Client(api_key=api_key)
    return _genai_client


def _embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a batch of texts using Gemini embedding model."""
    client = _get_genai_client()
    all_embeddings = []
    # Process in batches of 20 to avoid rate limits
    batch_size = 20
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        result = client.models.embed_content(
            model=EMBED_MODEL,
            contents=batch,
        )
        all_embeddings.extend([e.values for e in result.embeddings])
        if i + batch_size < len(texts):
            time.sleep(0.5)  # Brief pause between batches
    return all_embeddings


def initialize(knowledge_base: list[dict]) -> None:
    """
    Initialize the ChromaDB collection from the KNOWLEDGE_BASE.
    Skips re-ingestion if the collection already has the right count.
    """
    global _client, _collection

    _client = chromadb.PersistentClient(path=CHROMA_DIR)

    # Check if collection already populated
    try:
        _collection = _client.get_collection(name=COLLECTION_NAME)
        if _collection.count() == len(knowledge_base):
            print(f"✅ ChromaDB collection '{COLLECTION_NAME}' already has {_collection.count()} docs. Skipping ingestion.")
            return
        else:
            print(f"🔄 Collection count mismatch ({_collection.count()} vs {len(knowledge_base)}). Re-creating...")
            _client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass  # Collection doesn't exist yet

    print(f"📦 Creating ChromaDB collection and embedding {len(knowledge_base)} entries...")
    _collection = _client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    # Prepare documents for embedding
    ids = []
    documents = []
    metadatas = []

    for item in knowledge_base:
        doc_text = f"Service: {item['service']}. Category: {item['category']}. Question: {item['question']}. Answer: {item['answer']}"
        ids.append(item["id"])
        documents.append(doc_text)
        metadatas.append({
            "service": item["service"],
            "category": item["category"],
            "question": item["question"],
            "answer": item["answer"],
        })

    # Embed all documents
    embeddings = _embed_texts(documents)

    # Upsert into ChromaDB
    _collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )
    print(f"✅ Successfully embedded and stored {len(ids)} knowledge base entries in ChromaDB.")


def query(text: str, n_results: int = 5) -> list[dict]:
    """
    Search the knowledge base for entries most similar to the query text.
    Returns a list of dicts with keys: id, service, category, question, answer, score.
    """
    if _collection is None:
        raise RuntimeError("Knowledge store not initialized. Call initialize() first.")

    # Embed the query
    query_embedding = _embed_texts([text])[0]

    results = _collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["metadatas", "distances"],
    )

    matches = []
    if results and results["ids"] and results["ids"][0]:
        for i, doc_id in enumerate(results["ids"][0]):
            meta = results["metadatas"][0][i]
            distance = results["distances"][0][i]
            # ChromaDB cosine distance: 0 = identical, 2 = opposite
            similarity = 1 - (distance / 2)
            matches.append({
                "id": doc_id,
                "service": meta.get("service", ""),
                "category": meta.get("category", ""),
                "question": meta.get("question", ""),
                "answer": meta.get("answer", ""),
                "score": round(similarity, 4),
            })

    return matches
