"""
Phase 4 - Exercise 3 (Self-practice)
Text Embeddings: tao vector, do tuong dong, nearest neighbor.

Muc tieu:
- Hieu embedding la gi va tai sao can thiet trong RAG
- Tao embeddings bang sentence-transformers (chay local, khong can API key)
- Tinh cosine similarity thu cong
- Tim van ban tuong dong nhat voi query
- So sanh ket qua cua 2 model embedding khac nhau
"""

from __future__ import annotations

import numpy as np
from sentence_transformers import SentenceTransformer


# -----------------------------------------------------------------------
# Model mac dinh (nhe, nhanh, tot cho tieng Anh)
# Co the doi sang "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
# de ho tro tieng Viet tot hon.
# -----------------------------------------------------------------------
DEFAULT_MODEL = "all-MiniLM-L6-v2"


# -----------------------------------------------------------------------
# Exercise 3.1 - Khoi tao model va tao embeddings
# -----------------------------------------------------------------------
def load_model(model_name: str = DEFAULT_MODEL) -> SentenceTransformer:
    """
    Tai model SentenceTransformer.

    TODO:
        return SentenceTransformer(model_name)
    Hint: lan dau chay se tu dong download model (~80 MB).
    """
    return SentenceTransformer(DEFAULT_MODEL)



def embed_texts(texts: list[str], model: SentenceTransformer) -> np.ndarray:
    """
    Tao embeddings cho danh sach van ban.

    Args:
        texts: danh sach chuoi can embed
        model: SentenceTransformer model da khoi tao

    Returns:
        numpy array shape (len(texts), embedding_dim)

    TODO:   
        return model.encode(texts, convert_to_numpy=True)
    """
    return model.encode(texts, convert_to_numpy=True)


# -----------------------------------------------------------------------
# Exercise 3.2 - Cosine similarity
# -----------------------------------------------------------------------
def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """
    Tinh cosine similarity giua 2 vector.

    Cong thuc: cos(a, b) = (a . b) / (||a|| * ||b||)

    TODO:
        1. Tinh dot product: np.dot(vec_a, vec_b)
        2. Tinh norm: np.linalg.norm(vec_a) * np.linalg.norm(vec_b)
        3. Tranh chia cho 0 bang cach kiem tra norm > 0
        4. Return float trong [-1, 1]
    """
    dot_product = np.dot(vec_a,vec_b)
    norm = np.linalg.norm(vec_a) * np.linalg.norm(vec_b)
    try: 
        cosin = dot_product / norm
    except Exception as e: 
        print("loi norm= 0")
    return  float(cosin)


def similarity_matrix(embeddings: np.ndarray) -> np.ndarray:
    """
    Tinh ma tran cosine similarity NxN cho tap embeddings.

    TODO:
        Goi cosine_similarity cho moi cap (i, j) bang vong lap,
        hoac dung cach vector hoa nhanh hon:
        Hint: normalized = embeddings / norm; matrix = normalized @ normalized.T
    """
    # Vectorized approach: normalize then compute matrix product
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    normalized = embeddings / norms
    matrix = normalized @ normalized.T
    return matrix
    
    

# -----------------------------------------------------------------------
# Exercise 3.3 - Nearest neighbor (thu cong)
# -----------------------------------------------------------------------
def find_most_similar(
    query: str,
    corpus: list[str],
    model: SentenceTransformer,
    top_k: int = 3,
) -> list[tuple[float, str]]:
    """
    Tim top_k van ban trong corpus giong query nhat.

    Returns:
        list[(score, text)] sap xep giam dan theo score

    TODO:
        1. Embed query va tat ca corpus texts
        2. Voi moi corpus embedding, tinh cosine_similarity voi query embedding
        3. Sap xep giam dan va lay top_k
        4. Return list[(score, text)]
    """
    query_emb = embed_texts([query], model)[0]      # shape (D,)
    corpus_embs = embed_texts(corpus, model)         # shape (N, D)

    result = []
    for i, c in enumerate(corpus_embs):
        score = cosine_similarity(query_emb, c)
        result.append((score, corpus[i]))

    result.sort(key=lambda x: x[0], reverse=True)
    return result[:top_k]



        



# -----------------------------------------------------------------------
# Exercise 3.4 - Semantic search tren tap chunk nho
# -----------------------------------------------------------------------
def build_index(corpus: list[str], model: SentenceTransformer) -> np.ndarray:
    """
    Pre-compute va luu embeddings cho toan bo corpus.

    TODO:
        return embed_texts(corpus, model)
    Hint: trong RAG that, buoc nay duoc luu vao vector DB.
          Day ta gia lap bang numpy array.
    """
    return embed_texts(corpus, model)
    


def search_index(
    query: str,
    corpus: list[str],
    index: np.ndarray,
    model: SentenceTransformer,
    top_k: int = 3,
) -> list[tuple[float, str]]:
    """
    Tim kiem nhanh khi da co index san.

    TODO:
        1. Embed query (chi 1 van ban)
        2. Tinh cosine similarity giua query_emb va tung hang trong index
        3. Lay top_k chi so cao nhat
        4. Return list[(score, corpus[i])]
    Hint: np.argsort(scores)[::-1][:top_k]
    """
    embed_query = embed_texts([query], model)[0]              # shape (D,)
    norm_index = np.linalg.norm(index, axis=1)                # shape (N,)
    norm_query = np.linalg.norm(embed_query)                  # scalar
    scores = index @ embed_query / (norm_index * norm_query)  # shape (N,)
    top_indices = np.argsort(scores)[::-1][:top_k]
    return [(float(scores[i]), corpus[i]) for i in top_indices]


# -----------------------------------------------------------------------
# Exercise 3.5 - So sanh 2 model embedding
# -----------------------------------------------------------------------
def compare_models(query: str, corpus: list[str], model_names: list[str]) -> dict[str, list[tuple[float, str]]]:
    """
    So sanh ket qua tim kiem cua nhieu model embedding.

    TODO:
        1. Voi moi model_name trong model_names:
            a. load_model(model_name)
            b. find_most_similar(query, corpus, model, top_k=3)
            c. Luu ket qua vao dict {model_name: results}
        2. Return dict
    Goi y model de thu:
        - "all-MiniLM-L6-v2"  (nhe, nhanh)
        - "paraphrase-multilingual-MiniLM-L12-v2"  (ho tro nhieu ngon ngu)
    """
    result = {}
    for model_name in model_names:
        model = load_model(model_name)
        result[model_name] = find_most_similar(query, corpus, model)
    return result


# -----------------------------------------------------------------------
# Ham chay demo
# -----------------------------------------------------------------------
SAMPLE_CORPUS = [
    "RAG la phuong phap ket hop tim kiem tai lieu voi sinh van ban.",
    "Vector database luu tru embeddings de tim kiem nhanh.",
    "Cosine similarity do goc giua hai vector trong khong gian nhieu chieu.",
    "Python la ngon ngu lap trinh pho bien trong linh vuc AI.",
    "Transformer la kien truc neural network nen tang cua cac LLM hien dai.",
    "Chunking chia tai lieu lon thanh cac doan nho hon de xu ly.",
    "OpenAI cung cap API cho GPT-4 va cac mo hinh ngon ngu lon khac.",
    "Sentence-transformers la thu vien Python de tao text embeddings.",
]


def exercise_4_3():
    print("=" * 60)
    print("PHASE 4 - EXERCISE 3: TEXT EMBEDDINGS")
    print("=" * 60)

    # --- 3.1: Tai model va tao embeddings ---
    print("\n[3.1] Tai model va tao embeddings")
    try:
        model = load_model(DEFAULT_MODEL)
        embs = embed_texts(SAMPLE_CORPUS[:3], model)
        print(f"  Model: {DEFAULT_MODEL}")
        print(f"  Embedding shape: {embs.shape}")
        print(f"  Embedding dim: {embs.shape[1]}")
    except NotImplementedError as e:
        print(f"  [TODO] {e}")
        return  # cac bai sau deu can model, dung lai neu chua implement

    # --- 3.2: Cosine similarity ---
    print("\n[3.2] Cosine similarity")
    try:
        all_embs = embed_texts(SAMPLE_CORPUS, model)
        sim_01 = cosine_similarity(all_embs[0], all_embs[1])
        sim_03 = cosine_similarity(all_embs[0], all_embs[3])
        print(f"  RAG vs Vector DB: {sim_01:.4f}")
        print(f"  RAG vs Python:    {sim_03:.4f}")
        print("  (Ky vong: RAG va Vector DB tuong dong hon RAG va Python)")
    except NotImplementedError as e:
        print(f"  [TODO] {e}")

    # --- 3.3: Nearest neighbor ---
    print("\n[3.3] Nearest neighbor")
    query = "Lam the nao de tim kiem tai lieu trong RAG?"
    try:
        results = find_most_similar(query, SAMPLE_CORPUS, model, top_k=3)
        print(f"  Query: '{query}'")
        for score, text in results:
            print(f"  [{score:.4f}] {text}")
    except NotImplementedError as e:
        print(f"  [TODO] {e}")

    # --- 3.4: Pre-built index ---
    print("\n[3.4] Search voi pre-built index")
    try:
        index = build_index(SAMPLE_CORPUS, model)
        print(f"  Index shape: {index.shape}")
        results2 = search_index(query, SAMPLE_CORPUS, index, model, top_k=3)
        for score, text in results2:
            print(f"  [{score:.4f}] {text}")
    except NotImplementedError as e:
        print(f"  [TODO] {e}")

    # --- 3.5: So sanh model (optional) ---
    print("\n[3.5] So sanh 2 model embedding (co the mat vai phut tai model)")
    models_to_compare = [
        "all-MiniLM-L6-v2",
        "paraphrase-multilingual-MiniLM-L12-v2",
    ]
    try:
        comparison = compare_models(query, SAMPLE_CORPUS, models_to_compare)
        for m_name, res in comparison.items():
            print(f"\n  -- {m_name} --")
            for score, text in res:
                print(f"    [{score:.4f}] {text[:60]}")
    except NotImplementedError as e:
        print(f"  [TODO] {e}")


if __name__ == "__main__":
    exercise_4_3()
