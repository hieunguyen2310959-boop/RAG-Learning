"""
Phase 5 - Exercise 5 (Mini Project - Self-practice)
Mini Retrieval System: ket hop Phase 3 + Phase 4 + Phase 5 thanh 1 he thong hoan chinh.

Muc tieu:
- Xay dung RETRIEVAL HALF cua RAG (chua co LLM generation)
- Ingest pipeline: van ban -> clean -> chunk -> embed -> luu ChromaDB
- Query pipeline: cau hoi -> embed -> retrieve -> loc -> tra ve ket qua
- Xu ly cac edge case: khong co ket qua, do tuong dong qua thap
- Luu index xuong dia va tai lai (persistent)

Day la mini project quan trong nhat cua Phase 5.
Sau khi hoan thanh, ban co "retrieval engine" thuc su —
chi can them LLM o Phase 6 la co RAG day du.

Kien truc he thong:
    +-----------------+     +-----------------+     +------------------+
    |   INPUT DOCS    | --> |  INGEST PIPELINE| --> | ChromaDB + BM25  |
    | (.txt, .pdf,    |     | chunk+embed+meta|     |   persistent     |
    |  raw strings)   |     +-----------------+     +------------------+
    +-----------------+                                      |
                                                             v
    +-----------------+     +-----------------+     +------------------+
    |  FINAL ANSWER   | <-- | FORMAT + FILTER | <-- |   QUERY ENGINE   |
    | (top chunks     |     | threshold, meta |     | semantic+hybrid  |
    |  + metadata)    |     +-----------------+     +------------------+
    +-----------------+
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

import chromadb
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer


# -----------------------------------------------------------------------
# Data models
# -----------------------------------------------------------------------

@dataclass
class RetrievedChunk:
    """1 chunk duoc tra ve tu retrieval engine."""
    chunk_id       : str
    text           : str
    source         : str
    page_number    : int | None
    score          : float          # 0.0 - 1.0 (cao hon = lien quan hon)
    rank           : int            # vi tri trong danh sach ket qua (bat dau tu 1)
    retrieval_method: str = "semantic"  # "semantic", "bm25", "hybrid"


@dataclass
class RetrievalResult:
    """Ket qua tra ve cho 1 query."""
    query          : str
    chunks         : list[RetrievedChunk]
    retrieval_time_ms: float = 0.0
    total_indexed  : int = 0

    @property
    def found(self) -> bool:
        return len(self.chunks) > 0

    def pretty_print(self) -> None:
        print(f"\nQuery: '{self.query}'")
        print(f"Tim thay {len(self.chunks)} chunks ({self.retrieval_time_ms:.1f}ms)")
        if not self.found:
            print("  [Khong tim thay chunk nao phu hop]")
            return
        for r in self.chunks:
            print(f"  [{r.rank}] score={r.score:.3f} | source={r.source} p{r.page_number}")
            print(f"       {r.text[:100]}...")


# -----------------------------------------------------------------------
# Exercise 5.1 - Ingest pipeline
# -----------------------------------------------------------------------

class DocumentIngestor:
    """
    Xu ly va nap tai lieu vao vector index.
    Nhan dau vao la van ban thuan tui (str) hoac list chunks.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        chunk_size: int = 100,
        chunk_overlap: int = 20,
    ):
        """
        Khoi tao ingestor.

        TODO:
            self.model_name    = model_name
            self.chunk_size    = chunk_size
            self.chunk_overlap = chunk_overlap
            self.model         = SentenceTransformer(model_name)
        """
        # TODO: implement
        raise NotImplementedError("Implement DocumentIngestor.__init__")

    def chunk_text(self, text: str, source: str) -> list[dict]:
        """
        Chia van ban thanh cac chunk bang sliding window (theo so tu).

        Args:
            text  : noi dung van ban sach
            source: ten nguon, dung lam prefix cho chunk_id

        Returns:
            list[dict] moi dict co: chunk_id, text, source, chunk_index, word_count

        TODO:
            words = text.split()
            step  = max(1, self.chunk_size - self.chunk_overlap)
            chunks = []
            i = 0
            while i < len(words):
                chunk_words = words[i: i + self.chunk_size]
                chunk_text  = " ".join(chunk_words)
                chunk_idx   = len(chunks)
                chunks.append({
                    "chunk_id"   : f"{source}__c{chunk_idx}",
                    "text"       : chunk_text,
                    "source"     : source,
                    "chunk_index": chunk_idx,
                    "word_count" : len(chunk_words),
                    "page_number": -1,
                })
                i += step
            return chunks
        """
        # TODO: implement
        raise NotImplementedError("Implement chunk_text")

    def ingest(
        self,
        collection: chromadb.Collection,
        text: str,
        source: str,
        page_number: int | None = None,
        overwrite: bool = True,
    ) -> int:
        """
        Toan bo pipeline cho 1 doan van ban:
        chunk -> embed -> luu vao ChromaDB.

        Args:
            collection  : ChromaDB collection dich
            text        : noi dung van ban da clean
            source      : ten tai lieu goc
            page_number : so trang (neu co)
            overwrite   : dung upsert thay vi add

        Returns:
            so chunks da ingest

        TODO:
            # 1. Chunk
            chunks = self.chunk_text(text, source)
            if not chunks:
                return 0

            # 2. Set page_number neu duoc truyen vao
            if page_number is not None:
                for c in chunks:
                    c["page_number"] = page_number

            # 3. Embed
            texts      = [c["text"] for c in chunks]
            embeddings = self.model.encode(texts, convert_to_numpy=True)

            # 4. Luu vao ChromaDB
            ids        = [c["chunk_id"] for c in chunks]
            metadatas  = [
                {
                    "source"     : c["source"],
                    "page_number": c["page_number"] if c["page_number"] is not None else -1,
                    "chunk_index": c["chunk_index"],
                    "word_count" : c["word_count"],
                }
                for c in chunks
            ]
            if overwrite:
                collection.upsert(
                    documents=texts, ids=ids, metadatas=metadatas,
                    embeddings=embeddings.tolist()
                )
            else:
                collection.add(
                    documents=texts, ids=ids, metadatas=metadatas,
                    embeddings=embeddings.tolist()
                )
            return len(chunks)
        """
        # TODO: implement
        raise NotImplementedError("Implement DocumentIngestor.ingest")

    def ingest_many(
        self,
        collection: chromadb.Collection,
        documents: list[dict],
    ) -> int:
        """
        Ingest nhieu tai lieu cuoi.

        Args:
            documents: list[dict] moi dict co key: "text", "source", "page_number" (tuy chon)

        Returns:
            tong so chunks da ingest

        TODO:
            total = 0
            for doc in documents:
                n = self.ingest(
                    collection  = collection,
                    text        = doc["text"],
                    source      = doc["source"],
                    page_number = doc.get("page_number"),
                )
                total += n
            return total
        """
        # TODO: implement
        raise NotImplementedError("Implement DocumentIngestor.ingest_many")


# -----------------------------------------------------------------------
# Exercise 5.2 - Query engine
# -----------------------------------------------------------------------

class RetrievalEngine:
    """
    Tim kiem semantic (va hybrid tuy chon) tren ChromaDB collection.
    """

    def __init__(
        self,
        collection: chromadb.Collection,
        model: SentenceTransformer,
        default_top_k: int = 5,
        default_min_score: float = 0.35,
    ):
        """
        TODO:
            self.collection       = collection
            self.model            = model
            self.default_top_k    = default_top_k
            self.default_min_score = default_min_score

            # Build BM25 tu documents trong collection
            self._bm25: BM25Okapi | None = None
            self._bm25_ids: list[str]    = []
            self._bm25_docs: list[str]   = []
        """
        # TODO: implement
        raise NotImplementedError("Implement RetrievalEngine.__init__")

    def _build_bm25(self) -> None:
        """
        Lay tat ca documents tu ChromaDB va build BM25 index.
        Goi ham nay sau khi ingest xong.

        TODO:
            all_data         = self.collection.get()
            self._bm25_ids   = all_data["ids"]
            self._bm25_docs  = all_data["documents"]
            tokenized        = [d.lower().split() for d in self._bm25_docs]
            self._bm25       = BM25Okapi(tokenized)
        """
        # TODO: implement
        raise NotImplementedError("Implement _build_bm25")

    def _embed_query(self, query: str) -> list[float]:
        """Embed query thanh vector."""
        return self.model.encode([query], convert_to_numpy=True)[0].tolist()

    def search(
        self,
        query: str,
        top_k: int | None = None,
        min_score: float | None = None,
        source_filter: str | None = None,
        use_hybrid: bool = False,
    ) -> RetrievalResult:
        """
        Tim kiem va tra ve RetrievalResult.

        Args:
            query        : cau hoi cua nguoi dung
            top_k        : so ket qua, mac dinh = self.default_top_k
            min_score    : nguong loc, mac dinh = self.default_min_score
            source_filter: chi tim trong 1 nguon cu the
            use_hybrid   : True = ket hop BM25 va semantic

        Returns:
            RetrievalResult

        TODO:
            k     = top_k or self.default_top_k
            score = min_score if min_score is not None else self.default_min_score
            t0    = time.time()

            query_emb = self._embed_query(query)

            where = {"source": source_filter} if source_filter else None

            # Semantic search
            results = self.collection.query(
                query_embeddings=[query_emb],
                n_results=min(k * 4, self.collection.count()),
                where=where,
            )

            candidates = []
            for id_, doc, dist, meta in zip(
                results["ids"][0], results["documents"][0],
                results["distances"][0], results["metadatas"][0],
            ):
                candidates.append({
                    "id"      : id_,
                    "document": doc,
                    "metadata": meta,
                    "score"   : round(1 - dist, 4),
                })

            # Optional: RRF voi BM25
            if use_hybrid and self._bm25 is not None:
                bm25_scores = self._bm25.get_scores(query.lower().split())
                bm25_ranked = sorted(
                    zip(self._bm25_ids, self._bm25_docs, bm25_scores),
                    key=lambda x: x[2], reverse=True
                )[:k * 4]

                # RRF
                rrf: dict[str, float] = {}
                # Semantic rank
                for rank, c in enumerate(candidates, 1):
                    rrf[c["id"]] = rrf.get(c["id"], 0) + 1 / (60 + rank)
                # BM25 rank
                for rank, (id_, _, _) in enumerate(bm25_ranked, 1):
                    rrf[id_] = rrf.get(id_, 0) + 1 / (60 + rank)

                # Sap xep lai theo rrf score
                id_to_cand = {c["id"]: c for c in candidates}
                for id_, doc, _ in bm25_ranked:
                    if id_ not in id_to_cand:
                        meta_data = self.collection.get(ids=[id_])["metadatas"]
                        meta = meta_data[0] if meta_data else {}
                        id_to_cand[id_] = {"id": id_, "document": doc, "metadata": meta, "score": 0.0}

                candidates = sorted(id_to_cand.values(), key=lambda x: rrf.get(x["id"], 0), reverse=True)
                for c in candidates:
                    c["score"] = round(rrf.get(c["id"], 0), 6)

            # Loc theo nguong va lay top-k
            filtered = [c for c in candidates if c["score"] >= score][:k]

            elapsed_ms = (time.time() - t0) * 1000

            chunks = [
                RetrievedChunk(
                    chunk_id        = c["id"],
                    text            = c["document"],
                    source          = c["metadata"].get("source", "unknown"),
                    page_number     = c["metadata"].get("page_number"),
                    score           = c["score"],
                    rank            = i + 1,
                    retrieval_method= "hybrid" if use_hybrid else "semantic",
                )
                for i, c in enumerate(filtered)
            ]

            return RetrievalResult(
                query             = query,
                chunks            = chunks,
                retrieval_time_ms = round(elapsed_ms, 2),
                total_indexed     = self.collection.count(),
            )
        """
        # TODO: implement
        raise NotImplementedError("Implement RetrievalEngine.search")

    def rebuild_bm25(self) -> None:
        """Rebuild BM25 sau khi ingest them tai lieu."""
        self._build_bm25()


# -----------------------------------------------------------------------
# Exercise 5.3 - Xu ly edge cases
# -----------------------------------------------------------------------

def handle_no_results(result: RetrievalResult, fallback_message: str = "") -> str:
    """
    Xu ly truong hop khong tim thay ket qua.
    Tra ve thong bao phu hop de truyen cho LLM o Phase 6.

    TODO:
        if result.found:
            return ""   # khong can xu ly
        if fallback_message:
            return fallback_message
        return (
            f"Khong tim thay tai lieu nao lien quan den query: '{result.query}'. "
            "Vui long thu lai voi tu khoa khac hoac mo rong nguong tim kiem."
        )
    """
    # TODO: implement
    raise NotImplementedError("Implement handle_no_results")


def format_context_for_llm(result: RetrievalResult, max_chunks: int = 3) -> str:
    """
    Dinh dang ket qua retrieval thanh chuoi context de truyen vao LLM.
    Day la buoc cau noi giua Retrieval va Generation cua RAG.

    Returns:
        Chuoi text da format, vi du:
        [Source: ai_handbook.pdf | Page 3]
        Vector databases store embeddings...

        [Source: rag_guide.txt | Page 1]
        RAG pipelines retrieve...

    TODO:
        if not result.found:
            return handle_no_results(result)

        context_parts = []
        for chunk in result.chunks[:max_chunks]:
            page_str = f"Page {chunk.page_number}" if chunk.page_number and chunk.page_number >= 0 else "N/A"
            header   = f"[Source: {chunk.source} | {page_str} | Score: {chunk.score:.2f}]"
            context_parts.append(f"{header}\n{chunk.text}")

        return "\n\n".join(context_parts)
    """
    # TODO: implement
    raise NotImplementedError("Implement format_context_for_llm")


def save_retrieval_result(result: RetrievalResult, output_path: str | Path) -> None:
    """
    Luu ket qua retrieval ra file JSON de debug hoac phan tich.

    TODO:
        data = {
            "query"            : result.query,
            "found"            : result.found,
            "retrieval_time_ms": result.retrieval_time_ms,
            "total_indexed"    : result.total_indexed,
            "chunks": [
                {
                    "chunk_id"       : c.chunk_id,
                    "text"           : c.text,
                    "source"         : c.source,
                    "page_number"    : c.page_number,
                    "score"          : c.score,
                    "rank"           : c.rank,
                    "retrieval_method": c.retrieval_method,
                }
                for c in result.chunks
            ],
        }
        Path(output_path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    """
    # TODO: implement
    raise NotImplementedError("Implement save_retrieval_result")


# -----------------------------------------------------------------------
# Du lieu mau (su dung trong demo)
# -----------------------------------------------------------------------

SAMPLE_DOCUMENTS = [
    {
        "source": "ai_overview.txt",
        "text": """
Artificial intelligence (AI) is intelligence demonstrated by machines.
Modern AI includes machine learning, deep learning, and natural language processing.
Machine learning enables systems to learn from data without explicit programming.
Deep learning uses neural networks to automatically learn feature representations.
NLP allows computers to understand and generate human language.
Large language models like GPT are trained on vast amounts of text data.
These models can answer questions, write code, summarize documents and more.
        """.strip(),
    },
    {
        "source": "vector_databases.txt",
        "text": """
Vector databases are specialized storage systems for high-dimensional vectors.
They enable fast approximate nearest neighbor search using algorithms like HNSW.
ChromaDB is an open-source vector database designed for AI applications.
Qdrant is a production-ready vector database with advanced filtering capabilities.
Pinecone provides a fully managed cloud vector database service.
Each vector in the database typically represents a text chunk with semantic meaning.
Metadata can be stored alongside vectors to enable hybrid filtering.
The query process involves embedding the input and finding similar vectors.
        """.strip(),
    },
    {
        "source": "rag_system.txt",
        "text": """
Retrieval-Augmented Generation (RAG) is a technique that enhances LLM responses.
RAG works by first retrieving relevant documents, then passing them to an LLM.
The ingestion pipeline converts raw documents into searchable vector chunks.
The query pipeline embeds the question and retrieves the most relevant chunks.
Context is built from retrieved chunks and inserted into the LLM prompt.
This grounds the LLM response in actual source documents, reducing hallucination.
Evaluation of RAG includes both retrieval quality and answer quality metrics.
RAGAS is a popular library for automated RAG evaluation.
        """.strip(),
    },
    {
        "source": "python_ecosystem.txt",
        "text": """
Python is the dominant language for AI and machine learning development.
FastAPI enables building high-performance REST APIs with automatic documentation.
Pydantic provides data validation and settings management using Python type hints.
The sentence-transformers library makes it easy to generate text embeddings locally.
ChromaDB integrates natively with Python and requires no external server setup.
LangChain and LlamaIndex are popular frameworks for building RAG applications.
Managing dependencies with virtual environments prevents package conflicts.
        """.strip(),
    },
]


# -----------------------------------------------------------------------
# Demo: he thong retrieval hoan chinh
# -----------------------------------------------------------------------

def demo_mini_retrieval_system():
    print("=" * 65)
    print("Phase 5 - Exercise 5: Mini Retrieval System Demo")
    print("=" * 65)

    MODEL_NAME = "all-MiniLM-L6-v2"
    print(f"\n[1] Khoi tao he thong...")
    model    = SentenceTransformer(MODEL_NAME)
    client   = chromadb.Client()
    collection = client.get_or_create_collection(
        "phase5-ex5",
        metadata={"hnsw:space": "cosine", "embedding_model": MODEL_NAME},
    )
    ingestor = DocumentIngestor(MODEL_NAME, chunk_size=60, chunk_overlap=15)
    engine   = RetrievalEngine(collection, model, default_top_k=4, default_min_score=0.3)

    # Ingest
    print(f"\n[2] Ingest {len(SAMPLE_DOCUMENTS)} tai lieu...")
    t0 = time.time()
    total = ingestor.ingest_many(collection, SAMPLE_DOCUMENTS)
    print(f"    Da ingest {total} chunks trong {time.time()-t0:.2f}s")

    # Rebuild BM25 sau ingest
    engine.rebuild_bm25()

    # Cac query thu nghiem
    queries = [
        ("Semantic tot", "how do vector databases store and search embeddings?"),
        ("Keyword tot", "ChromaDB HNSW Qdrant Pinecone"),
        ("Hybrid tot",  "RAG pipeline retrieval augmented generation"),
        ("Edge case",   "quantum computing blockchain NFT"),  # Khong trong corpus
    ]

    for label, query in queries:
        print(f"\n{'='*65}")
        print(f"[{label}] Query: '{query}'")

        result = engine.search(query, top_k=3, use_hybrid=True)
        result.pretty_print()

        if not result.found:
            print("  =>", handle_no_results(result))
        else:
            context = format_context_for_llm(result, max_chunks=2)
            print("\n  --- Context cho LLM ---")
            print(context[:400] + "..." if len(context) > 400 else context)

    # Luu ket qua
    last_result = engine.search("what is RAG and how does it work?")
    save_retrieval_result(last_result, "retrieval_result_sample.json")
    print(f"\n[3] Da luu ket qua mau ra 'retrieval_result_sample.json'")

    print("\nDone! Mini retrieval system hoan thanh.")
    print("Tiep theo: Phase 6 se them LLM vao de co RAG day du!")


if __name__ == "__main__":
    demo_mini_retrieval_system()
