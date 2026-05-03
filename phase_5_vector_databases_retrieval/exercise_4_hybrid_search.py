"""
Phase 5 - Exercise 4 (Self-practice)
Hybrid Search: ket hop semantic search + keyword search.

Muc tieu:
- Hieu han che cua pure semantic search
- Implement BM25 keyword search (khong can vector DB)
- Ket hop 2 phuong phap bang Reciprocal Rank Fusion (RRF)
- Biet khi nao dung hybrid vs pure semantic

Khi nao semantic search that bai?
- Query chua ten rieng, ma san pham, so phien ban: "loi GPT-4o 404"
- Query chua tu viet tat chuyen nganh: "RAG vs FLARE"
- Corpus qua nho, embedding khong du context de hieu

BM25 la gi?
- Thuat toan tim kiem dua tren tan suat xuat hien tu (TF-IDF nang cao)
- Nhanh, khong can GPU, hoat dong tot voi ten rieng & tu khoa chinh xac
- Nhuoc diem: khong hieu ngu nghia (synonym, paraphrase)

Reciprocal Rank Fusion (RRF):
- Ket hop rank tu nhieu nguon khac nhau
- Score(d) = sum(1 / (k + rank_i(d))) voi k thuong = 60
- Don gian, hieu qua, khong can huan luyen
"""

from __future__ import annotations

import math
from collections import defaultdict

import chromadb
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer


# -----------------------------------------------------------------------
# Exercise 4.1 - BM25 Keyword Search
# -----------------------------------------------------------------------

class BM25Index:
    """
    BM25 index don gian tren list van ban.
    Dung rank_bm25 library (pip install rank-bm25).
    """

    def __init__(self, documents: list[str], ids: list[str]):
        """
        Khoi tao index BM25.

        Args:
            documents: danh sach van ban goc
            ids      : danh sach ID tuong ung

        TODO:
            self.documents = documents
            self.ids       = ids
            tokenized_docs = [doc.lower().split() for doc in documents]
            self.bm25      = BM25Okapi(tokenized_docs)

        Hint: BM25Okapi nhan list[list[str]] (da tach tu).
        """
        self.documents = documents
        self.ids = ids
        # TODO: implement — tao self.bm25
        tokenized_docs = [doc.lower().split() for doc in documents]
        self.bm25 = BM250kapi(tokenized_docs)

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """
        Tim kiem bang tu khoa, tra ve top-k ket qua.

        Args:
            query : cau hoi / tu khoa
            top_k : so ket qua

        Returns:
            list[dict] voi key: id, document, bm25_score
            Sap xep theo bm25_score giam dan.

        TODO:
            tokenized_query = query.lower().split()
            scores = self.bm25.get_scores(tokenized_query)

            # Lay chi so top-k (argsort giam dan)
            top_indices = np.argsort(scores)[::-1][:top_k]

            results = []
            for idx in top_indices:
                results.append({
                    "id"        : self.ids[idx],
                    "document"  : self.documents[idx],
                    "bm25_score": float(scores[idx]),
                })
            return results

        Luu y: bm25_score co the la 0.0 neu khong co tu nao khop.
        """
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append({
                "id": self.ids[idx],
                "document": self.documents[idx],
                "bm25_score": float(scores[idx]),
            })
        return results
        


# -----------------------------------------------------------------------
# Exercise 4.2 - Semantic Search wrapper
# -----------------------------------------------------------------------

def semantic_search(
    collection: chromadb.Collection,
    query_embedding: list[float],
    top_k: int = 10,
) -> list[dict]:
    """
    Semantic search don gian tu ChromaDB.
    Wrapper nho de dung chung voi hybrid search.

    Returns:
        list[dict] voi key: id, document, metadata, score
        Sap xep theo score giam dan.

    TODO:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
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
                "score"   : round(1 - dist, 4),
            })
        return formatted
    """
    # TODO: implement
    results = list(dict)
    embed_query = collection.query([query_embedding], n_results= top_k)
    for id, doc,dist,  meta in zip(embed_query["ids"][0], embed_query["documents"][0], embed_query["distances"][0], embed_query["metadatas"][0]):
        results.append({
                "id"      : id,
                "document": doc,
                "metadata": meta,
                "score"   : round(1 - dist, 4),
        })
    return results

# -----------------------------------------------------------------------
# Exercise 4.3 - Reciprocal Rank Fusion (RRF)
# -----------------------------------------------------------------------

def reciprocal_rank_fusion(
    result_lists: list[list[dict]],
    k: int = 60,
    id_key: str = "id",
) -> list[dict]:
    """
    Ket hop nhieu danh sach ket qua bang RRF.

    Cong thuc: rrf_score(d) = sum_over_lists( 1 / (k + rank(d, list)) )
    - Rank bat dau tu 1 (phan tu dau tien co rank=1)
    - k=60 la gia tri chuan theo bai bao goc cua Cormack et al. (2009)

    Args:
        result_lists: list cac list ket qua (moi list tu 1 phuong phap)
        k           : hang so dam bao doc lap (thuong = 60)
        id_key      : ten truong dung lam ID

    Returns:
        list[dict] voi key: id, document, rrf_score, sources
        Sap xep theo rrf_score giam dan.

    TODO:
        scores: dict[str, float] = defaultdict(float)
        docs  : dict[str, str]   = {}

        for result_list in result_lists:
            for rank, item in enumerate(result_list, start=1):
                doc_id = item[id_key]
                scores[doc_id] += 1.0 / (k + rank)
                if doc_id not in docs:
                    docs[doc_id] = item.get("document", "")

        fused = [
            {"id": doc_id, "document": docs[doc_id], "rrf_score": round(score, 6)}
            for doc_id, score in scores.items()
        ]
        return sorted(fused, key=lambda x: x["rrf_score"], reverse=True)

    Vi du don gian:
        - doc_A xep hang 1 trong semantic, hang 3 trong BM25:
          rrf = 1/(60+1) + 1/(60+3) = 0.01639 + 0.01563 = 0.03202
        - doc_B chi xuat hien trong semantic o hang 2:
          rrf = 1/(60+2) = 0.01613
        => doc_A duoc chon (xuat hien o ca 2, du hang khong cao)
    """
    # TODO: implement
    scores: dict[str, float] = defaultdict(float)
    docs: dict[str, str] = {}

    for result_list in result_lists:
        for rank, item in enumerate(result_list, start=1):
            doc_id = item[id_key]
            scores[doc_id] += 1.0 / (k +rank)
            if doc_id not in docs:
                docs[doc_id] = item.get("document", "")
    fused = [
            {"id": doc_id, "document": docs[doc_id], "rrf_score": round(score, 6)}
            for doc_id, score in scores.items()
        ]
    return sorted(fused, key=lambda x: x["rrf_score"], reverse=True)                


# -----------------------------------------------------------------------
# Exercise 4.4 - Full Hybrid Search
# -----------------------------------------------------------------------

def hybrid_search(
    collection: chromadb.Collection,
    bm25_index: BM25Index,
    query: str,
    query_embedding: list[float],
    top_k: int = 5,
    semantic_candidates: int = 20,
    bm25_candidates: int = 20,
    rrf_k: int = 60,
) -> list[dict]:
    """
    Hybrid search = semantic + BM25 -> RRF -> top-k.

    Luong:
        1. Lay semantic_candidates ket qua tu ChromaDB
        2. Lay bm25_candidates ket qua tu BM25
        3. Ket hop bang RRF
        4. Tra ve top_k ket qua

    Args:
        collection        : ChromaDB collection
        bm25_index        : BM25Index da build
        query             : chuoi cau hoi goc
        query_embedding   : vector da embed
        top_k             : so ket qua cuoi cung
        semantic_candidates: lay bao nhieu ung vien tu semantic search
        bm25_candidates   : lay bao nhieu ung vien tu BM25

    TODO:
        sem_results = semantic_search(collection, query_embedding, top_k=semantic_candidates)
        bm25_results = bm25_index.search(query, top_k=bm25_candidates)

        fused = reciprocal_rank_fusion([sem_results, bm25_results])
        return fused[:top_k]

    Hint: nho them "source_methods" vao moi ket qua de biet no tu dau ra.
    """
    # TODO: implement
    sem_results = semantic_search(collection, query_embedding, top_k=semantic_candidates)
    bm25_results = bm25_index.search(query, top_k=bm25_candidates)

    fused = reciprocal_rank_fusion([sem_results, bm25_results])
    return fused[:top_k]

# -----------------------------------------------------------------------
# Exercise 4.5 - So sanh cac phuong phap
# -----------------------------------------------------------------------

def compare_search_methods(
    collection: chromadb.Collection,
    bm25_index: BM25Index,
    model: SentenceTransformer,
    query: str,
    top_k: int = 5,
) -> None:
    """
    In bang so sanh ket qua cua 3 phuong phap cho cung 1 query.

    TODO:
        query_emb = model.encode([query], convert_to_numpy=True)[0].tolist()

        sem  = semantic_search(collection, query_emb, top_k=top_k)
        bm25 = bm25_index.search(query, top_k=top_k)
        hyb  = hybrid_search(collection, bm25_index, query, query_emb, top_k=top_k)

        # In 3 cot ket qua de so sanh
        ...

    Phuong phap in dep co the la in tung phuong phap rieng theo dang:
        === Semantic ===
        [1] score=0.82 | ...
        [2] score=0.75 | ...
    """
    # TODO: implement
    query_emb = model.encode([query], convert_to_numpy=True)[0].tolist()

    sem  = semantic_search(collection, query_emb, top_k=top_k)
    bm25 = bm25_index.search(query, top_k=top_k)
    hyb  = hybrid_search(collection, bm25_index, query, query_emb, top_k=top_k)


# -----------------------------------------------------------------------
# Du lieu mau
# -----------------------------------------------------------------------

CORPUS = [
    # Semantic dang manh
    "Vector databases allow fast approximate nearest neighbor search on embeddings.",
    "Semantic search finds documents by meaning, not just exact keyword matches.",
    "Cosine similarity is the standard metric for comparing text embeddings.",
    "Transformers use attention to capture long-range dependencies in text.",
    "RAG improves LLM answers by grounding them in retrieved source documents.",
    # BM25 dang manh (ten rieng, so phien ban)
    "ChromaDB version 0.4 introduced persistent storage with SQLite backend.",
    "Qdrant v1.7 added support for multi-vector named vectors.",
    "OpenAI text-embedding-3-small was released in January 2024.",
    "LangChain version 0.1.0 became the stable API after months of 0.0.x releases.",
    "FAISS is Facebook AI Similarity Search, optimized for billion-scale vector search.",
    # Trung lap (ca 2 deu tot)
    "BM25 is a probabilistic keyword ranking function used in search engines.",
    "Hybrid search combines dense vector retrieval with sparse BM25 keyword search.",
    "Re-ranking with a cross-encoder model improves precision after initial retrieval.",
    "Metadata filters let you restrict vector search to a subset of your documents.",
    "The recall-precision tradeoff is fundamental to evaluating retrieval systems.",
]

CORPUS_METADATA = [{"source": f"doc_{i}.txt", "idx": i} for i in range(len(CORPUS))]


def build_demo_index(model: SentenceTransformer):
    """Tao ChromaDB collection va BM25Index tu CORPUS."""
    client = chromadb.Client()
    collection = client.get_or_create_collection(
        "phase5-ex4",
        metadata={"hnsw:space": "cosine"},
    )
    embeddings = model.encode(CORPUS, convert_to_numpy=True)
    collection.add(
        documents=CORPUS,
        ids=[f"doc_{i}" for i in range(len(CORPUS))],
        metadatas=CORPUS_METADATA,
        embeddings=embeddings.tolist(),
    )
    bm25 = BM25Index(CORPUS, ids=[f"doc_{i}" for i in range(len(CORPUS))])
    return collection, bm25


# -----------------------------------------------------------------------
# Demo
# -----------------------------------------------------------------------

def demo_hybrid_search():
    print("=" * 60)
    print("Phase 5 - Exercise 4: Hybrid Search Demo")
    print("=" * 60)

    MODEL_NAME = "all-MiniLM-L6-v2"
    print(f"\n[1] Load model '{MODEL_NAME}'...")
    model = SentenceTransformer(MODEL_NAME)
    collection, bm25 = build_demo_index(model)
    print(f"[2] Index san sang: {collection.count()} docs, BM25 tren {len(bm25.documents)} docs.")

    test_queries = [
        "how does semantic search work?",                     # semantic manh
        "ChromaDB version 0.4 SQLite",                       # BM25 manh (ten + version)
        "hybrid retrieval for RAG pipelines",                # ca hai
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: '{query}'")
        compare_search_methods(collection, bm25, model, query, top_k=3)

    print("\nDone! Hybrid search hoan thanh.")


if __name__ == "__main__":
    demo_hybrid_search()
