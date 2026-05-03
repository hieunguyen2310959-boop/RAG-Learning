"""
Phase 5 - Exercise 3 (Self-practice)
Retrieval Strategies: top-k, threshold filtering, va so sanh.

Muc tieu:
- Hieu va implement cac chien luoc retrieve khac nhau
- Top-k: lay K ket qua gan nhat
- Threshold filtering: chi tra ve ket qua co do tuong dong > nguong
- So sanh anh huong cua K va threshold den chat luong ket qua
- Hieu "why bad retrieval = bad RAG" — rac vao, rac ra

Khai niem can biet:
- Top-k: don gian, luon tra ve dung k ket qua (ke ca kem lien quan)
- Threshold: linh hoat hon, co the tra ve 0 ket qua neu khong co gi phu hop
- Precision vs Recall:
    * Precision: trong cac ket qua tra ve, bao nhieu % la dung?
    * Recall: trong tat ca ket qua dung, bao nhieu % duoc tim thay?
- Trong RAG: precision quan trong hon (rac vao LLM se gay hallucination)
"""

from __future__ import annotations

import chromadb
import numpy as np
from sentence_transformers import SentenceTransformer


# -----------------------------------------------------------------------
# Exercise 3.1 - Top-k retrieval
# -----------------------------------------------------------------------

def retrieve_top_k(
    collection: chromadb.Collection,
    query_embedding: list[float],
    k: int = 5,
) -> list[dict]:
    """
    Lay K chunks gan nhat voi query trong vector space.
    Day la chien luoc don gian nhat, luon tra ve dung k ket qua.

    Args:
        collection     : ChromaDB collection da index
        query_embedding: vector float cua cau hoi
        k              : so ket qua tra ve

    Returns:
        list[dict] voi cac key: id, document, metadata, distance, score
        Sap xep theo score GIAM DAN (tot nhat truoc).

    TODO:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
        )
        formatted = []
        for id_, doc, dist, meta in zip(
            results["ids"][0],
            results["documents"][0],
            results["distances"][0],
            results["metadatas"][0],
        ):
            formatted.append({
                "id"      : id_,
                "document": doc,
                "metadata": meta,
                "distance": round(dist, 4),
                "score"   : round(1 - dist, 4),   # voi cosine space
            })
        return formatted

    Luu y: ChromaDB da sap xep ket qua theo khoang cach (nho nhat truoc).
    """
    # TODO: implement
    result = collection.query(query_embeddings=[query_embedding], n_results=k)
    formatted = []
    for id_, doc,dist, meta in zip(result["ids"][0], result["documents"][0], result["distances"][0], result["metadatas"][0],):
        format.append({
            "id": id_,
            "document": doc,
            "metadata": meta,
            "distance": round(dist, 4),
            "score"   : round(1 - dist, 4),
        })
    return formatted


# -----------------------------------------------------------------------
# Exercise 3.2 - Threshold filtering
# -----------------------------------------------------------------------

def retrieve_with_threshold(
    collection: chromadb.Collection,
    query_embedding: list[float],
    min_score: float = 0.5,
    max_results: int = 10,
) -> list[dict]:
    """
    Lay cac chunks co do tuong dong >= min_score.
    Neu khong co chunk nao du nguong, tra ve list rong.

    Args:
        collection    : ChromaDB collection da index
        query_embedding: vector float cua cau hoi
        min_score     : nguong toi thieu (0.0 - 1.0), khuyen nghi 0.4-0.6
        max_results   : lay toi da bao nhieu ket qua truoc khi loc

    Returns:
        list[dict] chi chua cac ket qua co score >= min_score

    TODO:
        # 1. Lay nhieu ket qua truoc (max_results)
        candidates = retrieve_top_k(collection, query_embedding, k=max_results)

        # 2. Loc chi giu cac ket qua co score >= min_score
        filtered = [r for r in candidates if r["score"] >= min_score]

        return filtered

    Khi nao dung threshold?
    - RAG: neu khong co chunk nao phu hop, bao LLM "khong biet" con hon la
      truyen rac vao va de LLM bịa ra.
    - Nguong 0.4-0.6 la pho bien, tuy thuoc vao embedding model.
    """
    # TODO: implement
    candidates = retrieve_top_k(collection, query_embedding, k=max_results)
    filtered = [r for r in candidates if r["score"] >= min_score]
    return filtered


# -----------------------------------------------------------------------
# Exercise 3.3 - Metadata-filtered retrieval
# -----------------------------------------------------------------------

def retrieve_from_source(
    collection: chromadb.Collection,
    query_embedding: list[float],
    source: str,
    k: int = 5,
) -> list[dict]:
    """
    Chi tim trong cac chunks thuoc 1 tai lieu cu the.
    Hay dung khi nguoi dung hoi "trong file X, ..."

    Args:
        source: ten file goc, vi du "ai_handbook.pdf"

    TODO:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where={"source": source},
        )
        # Xu ly ket qua tuong tu retrieve_top_k
        ...

    Hint: ChromaDB cho phep ket hop filter metadata voi semantic search.
    """
    result = collection.query(query_embeddings= [query_embedding], n_results=k,where={"source": source}),
    format = [dict]
    for __id, doc, dist, meta in zip(result["ids"][0], result["documents"][0], result["distances"][0], result["metadatas"][0]):
        format.append(
            {
                "id": __id,
                "document": doc,
                "metadata": meta,
                "distance": round(dist, 4),
                "score"   : round(1 - dist, 4),
            }
        )
    return format

def retrieve_by_page_range(
    collection: chromadb.Collection,
    query_embedding: list[float],
    page_min: int,
    page_max: int,
    k: int = 5,
) -> list[dict]:
    """
    Chi tim trong cac chunks thuoc khoang trang cu the.

    TODO:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where={
                "$and": [
                    {"page_number": {"$gte": page_min}},
                    {"page_number": {"$lte": page_max}},
                ]
            },
        )
        # Xu ly ket qua...

    Hint: ChromaDB ho tro cac toan tu: $eq, $ne, $gt, $gte, $lt, $lte, $and, $or
    """
    # TODO: implement
    result = collection.query(
        query_embeddings=[query_embedding],
        n_results= k,
        where= {
            "$and": [
                {"page_number": {"$gte: page_min"}},
                {"page_number": {"$lte": page_max}},
            ]
        },
    )
    format = [dict]
    for __id, doc, dist, meta in zip(result["ids"][0], result["documents"][0], result["distances"][0], result["metadatas"][0]):
        format.append(
            {
                "id": __id,
                "document": doc,
                "metadata": meta,
                "distance": round(dist, 4),
                "score"   : round(1 - dist, 4),
            }
        )
    return format


# -----------------------------------------------------------------------
# Exercise 3.4 - Phan tich ket qua retrieval
# -----------------------------------------------------------------------

def analyze_retrieval_quality(results: list[dict]) -> dict:
    """
    Tinh cac chi so co ban ve tap ket qua retrieval.

    Returns:
        dict voi:
        - count        : so luong ket qua
        - avg_score    : diem trung binh
        - min_score    : diem thap nhat
        - max_score    : diem cao nhat
        - score_std    : do lech chuan cua diem (cao = cac ket qua rat khac nhau ve do phu hop)

    TODO:
        if not results:
            return {"count": 0, "avg_score": 0.0, "min_score": 0.0,
                    "max_score": 0.0, "score_std": 0.0}

        scores = [r["score"] for r in results]
        return {
            "count"    : len(scores),
            "avg_score": round(float(np.mean(scores)), 4),
            "min_score": round(float(np.min(scores)), 4),
            "max_score": round(float(np.max(scores)), 4),
            "score_std": round(float(np.std(scores)), 4),
        }
    """
    # TODO: implement
    if not results:
        return {"count": 0, "avg_score": 0.0, "min_score": 0.0,
                "max_score": 0.0, "score_std": 0.0}
    scores = [r["score"] for r in results]
    return {
            "count"    : len(scores),
            "avg_score": round(float(np.mean(scores)), 4),
            "min_score": round(float(np.min(scores)), 4),
            "max_score": round(float(np.max(scores)), 4),
            "score_std": round(float(np.std(scores)), 4),
        }


def compare_k_values(
    collection: chromadb.Collection,
    query_embedding: list[float],
    k_values: list[int] | None = None,
) -> None:
    """
    In bang so sanh ket qua voi cac gia tri k khac nhau.
    Giup ban hieu anh huong cua k den chat luong tap ket qua.

    TODO:
        k_values = k_values or [1, 3, 5, 10]
        print(f"\n{'k':>4}  {'avg_score':>10}  {'min_score':>10}  {'max_score':>10}")
        print("-" * 42)
        for k in k_values:
            results = retrieve_top_k(collection, query_embedding, k=k)
            stats   = analyze_retrieval_quality(results)
            print(f"{k:>4}  {stats['avg_score']:>10.3f}  {stats['min_score']:>10.3f}  {stats['max_score']:>10.3f}")

    Quan sat: khi k tang, avg_score giam vi cac ket qua xa hon duoc them vao.
    """
    # TODO: implement
    k_values = k_values or [1, 3, 5, 10]
    print(f"\n{'k':>4}  {'avg_score':>10}  {'min_score':>10}  {'max_score':>10}")
    print("-" * 42)
    for k in k_values:
            results = retrieve_top_k(collection, query_embedding, k=k)
            stats   = analyze_retrieval_quality(results)
            print(f"{k:>4}  {stats['avg_score']:>10.3f}  {stats['min_score']:>10.3f}  {stats['max_score']:>10.3f}")
        

def find_optimal_threshold(
    collection: chromadb.Collection,
    query_embedding: list[float],
    thresholds: list[float] | None = None,
) -> None:
    """
    In bang so ket qua con lai voi cac nguong khac nhau.
    Giup ban chon nguong phu hop cho ung dung cu the.

        thresholds = thresholds or [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
        print(f"\n{'threshold':>10}  {'results_kept':>14}")
        print("-" * 28)
        for t in thresholds:
            results = retrieve_with_threshold(collection, query_embedding, min_score=t)
            print(f"{t:>10.1f}  {len(results):>14}")
    """
    # TODO: implement
    thresholds = thresholds or [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    print(f"\n{'threshold':>10}  {'results_kept':>14}")
    print("-" * 28)
    for t in thresholds:
        results = retrieve_with_threshold(collection, query_embedding, min_score=t)
        print(f"{t:>10.1f}  {len(results):>14}")

# -----------------------------------------------------------------------
# Du lieu mau
# -----------------------------------------------------------------------

CORPUS = [
    # AI / ML
    "Machine learning algorithms learn patterns from training data to make predictions.",
    "Deep neural networks consist of multiple layers of interconnected nodes.",
    "Supervised learning uses labeled examples to train a model to classify or predict.",
    "Unsupervised learning finds hidden structure in data without labels.",
    "Reinforcement learning trains agents to maximize rewards through trial and error.",
    # Vector DB / RAG
    "ChromaDB stores embeddings alongside documents for fast similarity search.",
    "Pinecone is a fully managed cloud vector database with a generous free tier.",
    "RAG pipelines retrieve relevant documents before passing them to an LLM.",
    "Metadata filtering lets you narrow search results by attributes like date or author.",
    "Re-ranking uses a cross-encoder to reorder retrieval results for better accuracy.",
    # Python
    "Python is dynamically typed and known for readable, concise syntax.",
    "FastAPI is an async Python web framework built on Starlette and Pydantic.",
    "The pathlib module provides an object-oriented API for filesystem paths.",
    "List comprehensions are a compact way to create lists in Python.",
    "Virtual environments isolate Python package dependencies per project.",
]

CORPUS_METADATA = [
    {"source": "ml_intro.txt",    "topic": "ml",       "page_number": 0},
    {"source": "ml_intro.txt",    "topic": "ml",       "page_number": 0},
    {"source": "ml_intro.txt",    "topic": "ml",       "page_number": 1},
    {"source": "ml_intro.txt",    "topic": "ml",       "page_number": 1},
    {"source": "ml_intro.txt",    "topic": "ml",       "page_number": 2},
    {"source": "vectordb.txt",    "topic": "vector_db","page_number": 0},
    {"source": "vectordb.txt",    "topic": "vector_db","page_number": 0},
    {"source": "rag_guide.txt",   "topic": "rag",      "page_number": 0},
    {"source": "rag_guide.txt",   "topic": "rag",      "page_number": 1},
    {"source": "rag_guide.txt",   "topic": "rag",      "page_number": 1},
    {"source": "python_tips.txt", "topic": "python",   "page_number": 0},
    {"source": "python_tips.txt", "topic": "python",   "page_number": 0},
    {"source": "python_tips.txt", "topic": "python",   "page_number": 1},
    {"source": "python_tips.txt", "topic": "python",   "page_number": 1},
    {"source": "python_tips.txt", "topic": "python",   "page_number": 2},
]


def build_demo_collection(model: SentenceTransformer) -> chromadb.Collection:
    """Tao collection mau cho demo."""
    client = chromadb.Client()
    collection = client.get_or_create_collection(
        "phase5-ex3",
        metadata={"hnsw:space": "cosine"},
    )
    embeddings = model.encode(CORPUS, convert_to_numpy=True)
    collection.add(
        documents=CORPUS,
        ids=[f"doc_{i}" for i in range(len(CORPUS))],
        metadatas=CORPUS_METADATA,
        embeddings=embeddings.tolist(),
    )
    return collection


# -----------------------------------------------------------------------
# Demo
# -----------------------------------------------------------------------

def demo_retrieval_strategies():
    print("=" * 60)
    print("Phase 5 - Exercise 3: Retrieval Strategies Demo")
    print("=" * 60)

    MODEL_NAME = "all-MiniLM-L6-v2"
    print(f"\n[1] Load model '{MODEL_NAME}'...")
    model = SentenceTransformer(MODEL_NAME)

    collection = build_demo_collection(model)
    print(f"[2] Collection san sang: {collection.count()} documents.")

    QUERY = "how do vector databases work for semantic search?"
    query_emb = model.encode([QUERY], convert_to_numpy=True)[0].tolist()
    print(f"\nQuery: '{QUERY}'")

    # Top-k
    print("\n--- Top-k retrieval (k=3) ---")
    results = retrieve_top_k(collection, query_emb, k=3)
    for i, r in enumerate(results, 1):
        print(f"  [{i}] score={r['score']:.3f} | {r['document'][:65]}...")

    # Threshold
    print("\n--- Threshold retrieval (min_score=0.45) ---")
    results_thresh = retrieve_with_threshold(collection, query_emb, min_score=0.45)
    print(f"  Ket qua con lai: {len(results_thresh)}")
    for r in results_thresh:
        print(f"    score={r['score']:.3f} | {r['document'][:65]}...")

    # Source filter
    print("\n--- Filter theo source='vectordb.txt' ---")
    results_src = retrieve_from_source(collection, query_emb, source="vectordb.txt", k=3)
    for r in results_src:
        print(f"  score={r['score']:.3f} | {r['document'][:65]}...")

    # Phan tich
    print("\n--- So sanh cac gia tri k ---")
    compare_k_values(collection, query_emb)

    print("\n--- Tim nguong toi uu ---")
    find_optimal_threshold(collection, query_emb)

    print("\nDone! Retrieval strategies hoan thanh.")


if __name__ == "__main__":
    demo_retrieval_strategies()
