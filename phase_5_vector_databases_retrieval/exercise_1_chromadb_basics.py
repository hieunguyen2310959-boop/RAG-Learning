"""
Phase 5 - Exercise 1 (Self-practice)
ChromaDB Basics: lam quen voi vector database dau tien.

Muc tieu:
- Hieu vector database la gi va tai sao can no trong RAG
- Khoi tao ChromaDB (local, khong can server)
- Tao collection, them documents, query ket qua
- Hieu metadata filtering va cach dung
- Biet su khac biet giua embed_by_chromadb va tu truyen embedding

Khai niem can biet truoc khi lam:
- Embedding: vector so dai dien cho y nghia cua van ban (da lam o Phase 4)
- ANN (Approximate Nearest Neighbor): tim vector gan nhat, NHANH hon exact search
- Collection: tuong tu "bang" trong SQL, luu cac document + embedding cua chung
- Metadata: thong tin phu kem theo moi document (source, page, date, ...)
"""

from __future__ import annotations

import chromadb
from chromadb.config import Settings


# -----------------------------------------------------------------------
# Exercise 1.1 - Khoi tao ChromaDB client
# -----------------------------------------------------------------------

def create_in_memory_client() -> chromadb.Client:
    """
    Tao ChromaDB client chay IN-MEMORY (du lieu mat khi tat chuong trinh).
    Dung cho viec hoc va thu nghiem nhanh.

    TODO:
        return chromadb.Client()

    Hint: chromadb.Client() la ephemeral (tam thoi).
    """
    # TODO: implement
    return chromadb.Client()



def create_persistent_client(path: str = "./chroma_db") -> chromadb.PersistentClient:
    """
    Tao ChromaDB client LUU DIA (du lieu giu lai giua cac lan chay).
    Dung cho du an thuc te.

    Args:
        path: thu muc luu du lieu ChromaDB

    TODO:
        return chromadb.PersistentClient(path=path)

    Hint: khi chay lan 2, neu collection da ton tai thi load lai.
    """
    # TODO: implement
    return chromadb.PersistentClient(path)



# -----------------------------------------------------------------------
# Exercise 1.2 - Tao va quan ly Collection
# -----------------------------------------------------------------------

def get_or_create_collection(
    client: chromadb.Client,
    name: str,
    metadata: dict | None = None,
) -> chromadb.Collection:
    """
    Lay collection neu da ton tai, neu chua thi tao moi.
    Khong bao gio loi khi collection da co.

    Args:
        client: ChromaDB client
        name  : ten collection (khuyen nghi: chu thuong, dau gach ngang)
        metadata: mo ta collection, vi du {"hnsw:space": "cosine"}

    TODO:
        return client.get_or_create_collection(
            name=name,
            metadata=metadata or {"hnsw:space": "cosine"},
        )

    Hint: "hnsw:space": "cosine" yeu cau ChromaDB dung cosine similarity (phu hop RAG).
          Mac dinh la "l2" (Euclidean distance).
    """
    return client.get_or_create_collection(
        name=name,
        metadata=metadata or {"hnsw:space": "cosine"},
    )
    


def list_collections(client: chromadb.Client) -> list[str]:
    """
    Liet ke ten tat ca collections trong client.

    TODO:
        return [col.name for col in client.list_collections()]
    """
    # TODO: implement
    return [col.name for col in client.list_collections()]


def delete_collection(client: chromadb.Client, name: str) -> None:
    """
    Xoa collection theo ten. Khong bao gio raise neu collection khong ton tai.

    TODO:
        try:
            client.delete_collection(name)
        except Exception:
            pass
    """
    # TODO: implement
    try: 
        client.delete_collection(name)
    except Exception:
        pass


# -----------------------------------------------------------------------
# Exercise 1.3 - Them documents vao Collection
# -----------------------------------------------------------------------

def add_documents(
    collection: chromadb.Collection,
    documents: list[str],
    ids: list[str],
    metadatas: list[dict] | None = None,
    embeddings: list[list[float]] | None = None,
) -> None:
    """
    Them documents vao collection.

    Co 2 che do:
    A) Truyen embeddings=None: ChromaDB tu tinh embedding (can cai dat embedding function)
    B) Truyen embeddings=[...]: dung embedding ban da tinh san (KHUYEN NGHI cho RAG)

    Args:
        collection : ChromaDB collection
        documents  : danh sach van ban (text goc)
        ids        : danh sach ID duy nhat cho moi document (phai unique)
        metadatas  : danh sach dict metadata tuong ung moi document
        embeddings : (tuy chon) list cac vector float da tinh truoc

    TODO:
        collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    Hint: ids PHAI unique, neu them id trung se loi.
    """
    # TODO: implement
    try:
        collection.add(documents=documents, ids=ids, metadatas=metadatas, embeddings=embeddings)
    except Exception: 
        raise print(Exception)
    


def upsert_documents(
    collection: chromadb.Collection,
    documents: list[str],
    ids: list[str],
    metadatas: list[dict] | None = None,
    embeddings: list[list[float]] | None = None,
) -> None:
    """
    Them hoac CAP NHAT document (neu id da ton tai thi ghi de).
    An toan hon add_documents khi chay pipeline nhieu lan.

    TODO:
        collection.upsert(
            documents=documents,
            ids=ids,
            metadatas=metadatas,
            embeddings=embeddings,
        )
    """
    # TODO: implement
    collection.upsert(documents=documents, ids=ids,metadatas=metadatas, embeddings=embeddings)



# -----------------------------------------------------------------------
# Exercise 1.4 - Query collection
# -----------------------------------------------------------------------

def query_by_text(
    collection: chromadb.Collection,
    query_texts: list[str],
    n_results: int = 3,
    where: dict | None = None,
) -> dict:
    """
    Tim kiem semantic bang van ban (ChromaDB tu embed query).
    Chi dung duoc neu collection dung default embedding function.

    Args:
        query_texts: danh sach cac cau hoi/query
        n_results  : so ket qua tra ve (top-k)
        where      : filter metadata, vi du {"source": "doc1.pdf"}


        return collection.query(
            query_texts=query_texts,
            n_results=n_results,
            where=where,
        )

    Ket qua tra ve co dang:
        {
          "ids": [[id1, id2, ...]],
          "documents": [[text1, text2, ...]],
          "distances": [[dist1, dist2, ...]],   # nho hon = gan hon
          "metadatas": [[meta1, meta2, ...]],
        }
    """
    # TODO: implement
    return collection.query(
            query_texts=query_texts,
            n_results=n_results,
            where=where,
        )


def query_by_embedding(
    collection: chromadb.Collection,
    query_embedding: list[float],
    n_results: int = 3,
    where: dict | None = None,
) -> dict:
    """
    Tim kiem semantic bang VECTOR da tinh san.
    Day la cach dung trong RAG thuc te (ban tu chon embedding model).

    Args:
        query_embedding: vector float da embed tu query
        n_results      : so ket qua tra ve
        where          : filter metadata

    TODO:
        return collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where,
        )

    Luong thuc te:
        query (str) -> embed_model.encode() -> vector -> query_by_embedding() -> ket qua
    """
    # TODO: implement
    return collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where,
        )


def get_document_by_id(collection: chromadb.Collection, doc_id: str) -> dict | None:
    """
    Lay 1 document theo id chinh xac.

    TODO:
        result = collection.get(ids=[doc_id])
        if result["ids"]:
            return {
                "id": result["ids"][0],
                "document": result["documents"][0],
                "metadata": result["metadatas"][0],
            }
        return None
    """
    # TODO: implement
    result = collection.get(ids=[doc_id])
    if result["ids"]:
        return {
                "id": result["ids"][0],
                "document": result["documents"][0],
                "metadata": result["metadatas"][0],
            }
    return None



def delete_document(collection: chromadb.Collection, doc_id: str) -> None:
    """
    Xoa 1 document khoi collection theo id.

    TODO:
        collection.delete(ids=[doc_id])
    """
    # TODO: implement
    collection.delete(ids=[doc_id])


# -----------------------------------------------------------------------
# Exercise 1.5 - Hieu ket qua tra ve
# -----------------------------------------------------------------------

def format_query_results(results: dict, top_k: int = 3) -> list[dict]:
    """
    Chuyen ket qua ChromaDB sang dang doc de hon.

    ChromaDB tra ve "distances" (KHOANG CACH), khong phai "scores" (do tuong dong).
    - Voi "cosine" space: distance = 1 - cosine_similarity (nho hon = tot hon)
    - Voi "l2" space: distance = L2 norm (nho hon = tot hon)

    Args:
        results: ket qua tu query_by_text hoac query_by_embedding
        top_k  : so ket qua can lay (mac dinh lay het)

    Returns:
        list[dict] voi cac key: id, document, metadata, distance, similarity_score

    TODO:
        ids       = results["ids"][0][:top_k]
        docs      = results["documents"][0][:top_k]
        dists     = results["distances"][0][:top_k]
        metas     = results["metadatas"][0][:top_k]

        formatted = []
        for id_, doc, dist, meta in zip(ids, docs, dists, metas):
            formatted.append({
                "id"              : id_,
                "document"        : doc,
                "metadata"        : meta,
                "distance"        : round(dist, 4),
                "similarity_score": round(1 - dist, 4),   # chi dung voi cosine space
            })
        return formatted
    """
    ids       = results["ids"][0][:top_k]
    docs      = results["documents"][0][:top_k]
    dists     = results["distances"][0][:top_k]
    metas     = results["metadatas"][0][:top_k]

    formatted = []
    for id_, doc, dist, meta in zip(ids, docs, dists, metas):
        formatted.append({
            "id"              : id_,
            "document"        : doc,
            "metadata"        : meta,
            "distance"        : round(dist, 4),
            "similarity_score": round(1 - dist, 4),   # chi dung voi cosine space
        })
    return formatted
    


# -----------------------------------------------------------------------
# Demo: chay de kiem tra
# -----------------------------------------------------------------------

SAMPLE_DOCS = [
    "ChromaDB is an open-source vector database designed for AI applications.",
    "Vector databases store embeddings and enable semantic similarity search.",
    "RAG stands for Retrieval-Augmented Generation, combining search with LLMs.",
    "Python is a versatile programming language popular in data science.",
    "FastAPI is a modern Python web framework for building REST APIs quickly.",
    "Embeddings convert text into numerical vectors that capture semantic meaning.",
    "Cosine similarity measures the angle between two vectors in high-dimensional space.",
    "LLMs like GPT-4 can generate human-quality text given a prompt.",
]

SAMPLE_METADATAS = [
    {"source": "chromadb_docs", "topic": "vector_db"},
    {"source": "ml_wiki",       "topic": "vector_db"},
    {"source": "rag_guide",     "topic": "rag"},
    {"source": "python_docs",   "topic": "programming"},
    {"source": "fastapi_docs",  "topic": "backend"},
    {"source": "ml_wiki",       "topic": "embeddings"},
    {"source": "math_notes",    "topic": "embeddings"},
    {"source": "openai_docs",   "topic": "llm"},
]


def demo_chromadb_basics():
    print("=" * 60)
    print("Phase 5 - Exercise 1: ChromaDB Basics Demo")
    print("=" * 60)

    # 1. Tao client in-memory
    client = create_in_memory_client()
    print(f"\n[1] Client tao thanh công: {type(client).__name__}")

    # 2. Tao collection
    collection = get_or_create_collection(client, "phase5-demo")
    print(f"[2] Collection '{collection.name}' san sang.")

    # 3. Them documents (ChromaDB tu embed)
    ids = [f"doc_{i}" for i in range(len(SAMPLE_DOCS))]
    add_documents(
        collection=collection,
        documents=SAMPLE_DOCS,
        ids=ids,
        metadatas=SAMPLE_METADATAS,
    )
    print(f"[3] Da them {collection.count()} documents.")

    # 4. Query
    query = "how do vector databases work for AI search?"
    print(f"\n[4] Query: '{query}'")
    results = query_by_text(collection, [query], n_results=3)
    formatted = format_query_results(results)

    for i, r in enumerate(formatted, 1):
        print(f"  [{i}] score={r['similarity_score']:.3f} | {r['document'][:60]}...")
        print(f"       metadata: {r['metadata']}")

    # 5. Query voi metadata filter
    print("\n[5] Query voi filter: chi tim trong topic='vector_db'")
    results_filtered = query_by_text(
        collection,
        [query],
        n_results=2,
        where={"topic": "vector_db"},
    )
    formatted_filtered = format_query_results(results_filtered)
    for i, r in enumerate(formatted_filtered, 1):
        print(f"  [{i}] score={r['similarity_score']:.3f} | {r['document'][:60]}...")

    # 6. Get by ID
    doc = get_document_by_id(collection, "doc_0")
    print(f"\n[6] Get by ID 'doc_0': {doc['document'][:50]}...")

    # 7. Xoa
    delete_document(collection, "doc_0")
    print(f"[7] Sau khi xoa doc_0: tong = {collection.count()} documents.")

    print("\nDone! ChromaDB basics hoan thanh.")


if __name__ == "__main__":
    demo_chromadb_basics()
