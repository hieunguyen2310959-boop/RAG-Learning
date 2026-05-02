"""
Phase 5 - Exercise 2 (Self-practice)
Document Indexing: load chunks -> embed -> luu vao ChromaDB voi metadata.

Muc tieu:
- Lam quen voi quy trinh INGESTION (nap tai lieu vao vector DB)
- Doc chunk JSON tu Phase 3 (hoac tu du lieu mau)
- Embed tung chunk bang sentence-transformers (nhu Phase 4)
- Luu vao ChromaDB kem metadata day du
- Biet cach cap nhat (upsert) va xoa tai lieu khoi index
- Hieu khai niem "index" trong vector DB

Luu y quan trong:
- Phai dung CUNG MOT embedding model khi ingest va khi query
- Luu ten model vao metadata cua collection de khong nham
- Moi chunk can co ID duy nhat (vi du: "source__page__chunk_idx")
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path

import chromadb
import numpy as np
from sentence_transformers import SentenceTransformer


# -----------------------------------------------------------------------
# Data model cho 1 chunk (tuong tu Phase 3)
# -----------------------------------------------------------------------

@dataclass
class ChunkRecord:
    chunk_id: str          # ID duy nhat, vi du: "doc1__p2__c5"
    text: str              # Noi dung van ban
    source: str            # Ten file goc, vi du: "ai_handbook.pdf"
    page_number: int | None = None
    chunk_index: int = 0
    word_count: int = 0
    extra: dict = field(default_factory=dict)   # truong mo rong tuy y


# -----------------------------------------------------------------------
# Exercise 2.1 - Load chunks tu JSON (output cua Phase 3)
# -----------------------------------------------------------------------

def load_chunks_from_json(json_path: str | Path) -> list[ChunkRecord]:
    """
    Doc danh sach ChunkRecord tu file JSON da luu o Phase 3.

    Cau truc JSON mong doi (moi phan tu):
        {
            "chunk_id"   : "doc1__p0__c0",
            "text"       : "noi dung...",
            "source"     : "doc1.pdf",
            "page_number": 0,
            "chunk_index": 0,
            "word_count" : 42
        }

    TODO:
        1. Dung json.loads hoac json.load de doc file
        2. Voi moi dict, tao ChunkRecord(...)
        3. Tra ve list[ChunkRecord]

    Hint: dung Path(json_path).read_text(encoding="utf-8")
    """
    text = Path(json_path).read_text(encoding="utf-8")
    raw_items = json.loads(text)

    records: list[ChunkRecord] = []
    for item in raw_items:
        records.append(
            ChunkRecord(
                chunk_id=item["chunk_id"],
                text=item["text"],
                source=item["source"],
                page_number=item.get("page_number"),
                chunk_index=item.get("chunk_index", 0),
                word_count=item.get("word_count", 0),
                extra=item.get("extra", {}),
            )
        )

    return records


def load_chunks_from_list(raw_texts: list[str], source: str = "inline") -> list[ChunkRecord]:
    """
    Tao ChunkRecord tu danh sach chuoi (khong can doc tu file).
    Tien loi cho viec thu nghiem nhanh.

    TODO:
        records = []
        for i, text in enumerate(raw_texts):
            records.append(ChunkRecord(
                chunk_id    = f"{source}__c{i}",
                text        = text,
                source      = source,
                chunk_index = i,
                word_count  = len(text.split()),
            ))
        return records
    """
    # TODO: implement
    records = []
    for i, text in enumerate(raw_texts):
        records.append(ChunkRecord(
            chunk_id = f"{source}__c{i}",
            text = text,
            source = source,
            chunk_index = i,
            word_count= len(text.split()),
        ))
    return records


# -----------------------------------------------------------------------
# Exercise 2.2 - Embed cac chunks
# -----------------------------------------------------------------------

def embed_chunks(
    chunks: list[ChunkRecord],
    model: SentenceTransformer,
    batch_size: int = 32,
    show_progress: bool = True,
) -> np.ndarray:
    """
    Embed tung chunk va tra ve numpy array shape (N, embedding_dim).

    Args:
        chunks      : danh sach ChunkRecord can embed
        model       : SentenceTransformer da load
        batch_size  : so chunk xu ly moi lan (giam de tiet kiem RAM)
        show_progress: in tien do ra man hinh

    TODO:
        texts = [c.text for c in chunks]
        embeddings = model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True,
        )
        return embeddings

    Hint: model.encode co tham so show_progress_bar=True/False
    """
    # TODO: implement
    texts = [c.text for c in chunks]
    embeddings = model.encode(
        texts,
        batch_size = batch_size,
        show_progress_bar=show_progress,
        convert_to_numpy=True
    )
    return embeddings


# -----------------------------------------------------------------------
# Exercise 2.3 - Ingest vao ChromaDB
# -----------------------------------------------------------------------

def ingest_chunks(
    collection: chromadb.Collection,
    chunks: list[ChunkRecord],
    embeddings: np.ndarray,
    overwrite: bool = True,
) -> int:
    """
    Luu chunks + embeddings vao ChromaDB.

    Args:
        collection : ChromaDB collection
        chunks     : danh sach ChunkRecord
        embeddings : numpy array, hang i tuong ung voi chunks[i]
        overwrite  : True = dung upsert (cap nhat neu ton tai),
                     False = dung add (loi neu id trung)

    Returns:
        so luong chunks da ingest
    """
    ids        = [c.chunk_id for c in chunks]
    documents  = [c.text for c in chunks]
    metadatas  = [
            {
                "source"     : c.source,
                "page_number": c.page_number if c.page_number is not None else -1,
                "chunk_index": c.chunk_index,
                "word_count" : c.word_count,
            }
            for c in chunks
        ]
    emb_list = embeddings.tolist()

    if overwrite:
        collection.upsert(documents=documents, ids=ids, metadatas=metadatas, embeddings=emb_list)
    else:
        collection.add(documents=documents, ids=ids, metadatas=metadatas, embeddings=emb_list)

    return len(chunks)




# -----------------------------------------------------------------------
# Exercise 2.4 - Quan ly tai lieu trong index
# -----------------------------------------------------------------------

def delete_document_by_source(collection: chromadb.Collection, source: str) -> int:
    """
    Xoa TẤT CA chunks thuoc ve 1 tai lieu (theo metadata["source"]).

    Args:
        collection: ChromaDB collection
        source    : ten file goc, vi du "ai_handbook.pdf"

    Returns:
        so chunks da xoa

    TODO:
        # 1. Tim tat ca ids co metadata.source == source
        existing = collection.get(where={"source": source})
        ids_to_delete = existing["ids"]

        # 2. Neu co id, xoa
        if ids_to_delete:
            collection.delete(ids=ids_to_delete)

        return len(ids_to_delete)

    Hint: collection.get(where={...}) tra ve tat ca records khop filter.
    """
    # TODO: implement
    exist = collection.get(where={"source": source})
    to_delete_ids = exist["ids"]
    
    if to_delete_ids:
        collection.delete(ids=to_delete_ids)
    
    return len(to_delete_ids)



def get_index_stats(collection: chromadb.Collection) -> dict:
    """
    Lay thong tin tong quan cua collection.

    TODO:
        total = collection.count()
        # Lay tat ca metadatas de dem so tai lieu doc
        all_meta = collection.get()["metadatas"] or []
        sources = {m.get("source", "unknown") for m in all_meta}
        return {
            "total_chunks": total,
            "unique_sources": len(sources),
            "sources": sorted(sources),
        }
    """
    # TODO: implement
    total = collection.count()
    all_meta = collection.get()["metadatas"] or []
    sources = {m.get("source", "unknow") for m in all_meta}
    return {
            "total_chunks": total,
            "unique_sources": len(sources),
            "sources": sorted(sources),
        }


# -----------------------------------------------------------------------
# Du lieu mau de thu
# -----------------------------------------------------------------------

SAMPLE_CHUNKS = [
    "Artificial intelligence is a branch of computer science focused on creating systems that can perform tasks that typically require human intelligence.",
    "Machine learning is a subset of AI where systems learn from data to improve their performance without being explicitly programmed.",
    "Deep learning uses neural networks with many layers to automatically learn representations from raw data.",
    "Natural language processing (NLP) enables computers to understand, interpret, and generate human language.",
    "Transformers are a neural network architecture that uses attention mechanisms to process sequential data like text.",
    "BERT is a transformer-based model pre-trained on large text corpora for understanding language context.",
    "GPT models generate text by predicting the next token based on the context provided.",
    "Vector embeddings represent semantic meaning as numerical vectors in high-dimensional space.",
    "Cosine similarity measures the angle between two vectors and is used to compare embeddings.",
    "ChromaDB is an open-source vector database optimized for AI and machine learning applications.",
    "Retrieval-Augmented Generation (RAG) combines document retrieval with language model generation.",
    "In a RAG system, relevant documents are retrieved and passed to an LLM as context for answering questions.",
]

SAMPLE_SOURCES = ["ai_basics.txt"] * 4 + ["transformers.txt"] * 4 + ["rag_guide.txt"] * 4


def make_sample_chunks() -> list[ChunkRecord]:
    records = []
    for i, (text, source) in enumerate(zip(SAMPLE_CHUNKS, SAMPLE_SOURCES)):
        records.append(ChunkRecord(
            chunk_id    = f"{source}__c{i}",
            text        = text,
            source      = source,
            page_number = i // 3,
            chunk_index = i % 4,
            word_count  = len(text.split()),
        ))
    return records


# -----------------------------------------------------------------------
# Demo
# -----------------------------------------------------------------------

def demo_document_indexing():
    print("=" * 60)
    print("Phase 5 - Exercise 2: Document Indexing Demo")
    print("=" * 60)

    # 1. Load model
    MODEL_NAME = "all-MiniLM-L6-v2"
    print(f"\n[1] Dang tai embedding model '{MODEL_NAME}'...")
    t0 = time.time()
    model = SentenceTransformer(MODEL_NAME)
    print(f"    Tai xong trong {time.time() - t0:.1f}s")

    # 2. Chuan bi chunks
    chunks = make_sample_chunks()
    print(f"\n[2] Chuan bi {len(chunks)} chunks tu {len(set(c.source for c in chunks))} nguon.")

    # 3. Embed
    print("\n[3] Dang embed chunks...")
    t0 = time.time()
    embeddings = embed_chunks(chunks, model, show_progress=False)
    print(f"    Embed xong: shape={embeddings.shape}, thoi gian={time.time() - t0:.2f}s")

    # 4. Ingest vao ChromaDB
    client = chromadb.Client()
    collection = client.get_or_create_collection(
        "phase5-ex2",
        metadata={"hnsw:space": "cosine", "embedding_model": MODEL_NAME},
    )
    n = ingest_chunks(collection, chunks, embeddings)
    stats = get_index_stats(collection)
    print(f"\n[4] Da ingest {n} chunks.")
    print(f"    Stats: {stats}")

    # 5. Thu ingest lai (upsert - khong loi)
    n2 = ingest_chunks(collection, chunks[:3], embeddings[:3], overwrite=True)
    print(f"\n[5] Upsert 3 chunks (khong loi): tong van la {collection.count()}")

    # 6. Xoa tai lieu theo source
    deleted = delete_document_by_source(collection, "ai_basics.txt")
    print(f"\n[6] Xoa source 'ai_basics.txt': da xoa {deleted} chunks.")
    print(f"    Stats sau khi xoa: {get_index_stats(collection)}")

    # 7. Thu load tu list text (khong can JSON)
    inline_chunks = load_chunks_from_list(
        ["Hello world", "This is a test chunk"],
        source="inline_test",
    )
    print(f"\n[7] load_chunks_from_list: tao {len(inline_chunks)} chunks.")
    for c in inline_chunks:
        print(f"    {c.chunk_id}: '{c.text}'")

    print("\nDone! Document indexing hoan thanh.")


if __name__ == "__main__":
    demo_document_indexing()
