"""
Phase 4 - Exercise 5 (Mini Project - Self-practice)
Mini QA Pipeline: embed -> retrieve -> generate.

Muc tieu:
- Ket hop 3 bai truoc thanh 1 pipeline hoan chinh
- Ingest tai lieu (danh sach chuoi hoac file .txt)
- Nhan cau hoi -> embed -> tim chunk lien quan -> goi LLM -> tra loi
- Danh gia co ban: do dai tra loi, top chunk duoc chon
- (Tuy chon) Them lich su hoi-dap (multi-turn)
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

# Import cac ham da lam o cac bai truoc
# Neu chua implement, file van chay voi mock noi bo
try:
    from exercise_1_llm_api_basics import chat_completion, extract_reply
except ImportError:
    def chat_completion(messages, temperature=0.3, max_tokens=512, **kw):
        user_content = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        return {
            "choices": [{"message": {"role": "assistant", "content": f"[MOCK] {user_content[:80]}"}}],
            "usage": {"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150},
        }

    def extract_reply(response):
        return response["choices"][0]["message"]["content"]

try:
    from exercise_3_text_embeddings import embed_texts, load_model, cosine_similarity
except ImportError:
    def load_model(name="all-MiniLM-L6-v2"):
        return SentenceTransformer(name)

    def embed_texts(texts, model):
        return model.encode(texts, convert_to_numpy=True)

    def cosine_similarity(a, b):
        norm = np.linalg.norm(a) * np.linalg.norm(b)
        return float(np.dot(a, b) / norm) if norm > 0 else 0.0

try:
    from exercise_4_token_context_management import build_context_within_limit, count_tokens
except ImportError:
    def build_context_within_limit(chunks, max_context_tokens=2000, **kw):
        return "\n\n---\n\n".join(chunks[:5])

    def count_tokens(text, model="gpt-4o-mini"):
        return len(text.split()) * 4 // 3  # uoc tinh don gian


# -----------------------------------------------------------------------
# Data model
# -----------------------------------------------------------------------
@dataclass
class QAResult:
    question: str
    answer: str
    top_chunks: list[tuple[float, str]]          # [(score, chunk_text)]
    input_tokens: int = 0
    output_tokens: int = 0


@dataclass
class QAPipeline:
    """
    Pipeline don gian:
      corpus (list[str])  ->  index (np.ndarray)  ->  model (SentenceTransformer)
    """
    corpus: list[str] = field(default_factory=list)
    index: np.ndarray | None = field(default=None, repr=False)
    model: SentenceTransformer | None = field(default=None, repr=False)
    model_name: str = "all-MiniLM-L6-v2"
    llm_model: str = "gpt-4o-mini"
    max_context_tokens: int = 1500
    top_k: int = 3

    # Lich su hoi-dap (multi-turn)
    history: list[dict] = field(default_factory=list)


# -----------------------------------------------------------------------
# Exercise 5.1 - Khoi tao va nap tai lieu
# -----------------------------------------------------------------------
def create_pipeline(
    model_name: str = "all-MiniLM-L6-v2",
    llm_model: str = "gpt-4o-mini",
    max_context_tokens: int = 1500,
    top_k: int = 3,
) -> QAPipeline:
    """
    Khoi tao QAPipeline moi voi SentenceTransformer da duoc load.

    TODO:
        1. Goi load_model(model_name) -> model
        2. Tao va return QAPipeline(model=model, model_name=model_name, ...)
    """
    # TODO: implement
    raise NotImplementedError("Implement create_pipeline")


def ingest_texts(pipeline: QAPipeline, texts: list[str]) -> None:
    """
    Nap danh sach van ban (da chunk san) vao pipeline.
    Tao embeddings va luu vao pipeline.index.

    TODO:
        1. pipeline.corpus = texts
        2. pipeline.index = embed_texts(texts, pipeline.model)
    """
    # TODO: implement
    raise NotImplementedError("Implement ingest_texts")


def ingest_file(pipeline: QAPipeline, path: Path, chunk_size: int = 150) -> int:
    """
    Doc file .txt va chunk theo so tu, roi goi ingest_texts.

    Returns:
        So luong chunk da nap

    TODO:
        1. Doc text tu path.read_text(encoding="utf-8")
        2. Chia theo tu: words = text.split()
        3. Tao chunks voi step = chunk_size (khong overlap cho don gian)
           hoac them overlap = chunk_size // 5 neu muon
        4. Goi ingest_texts(pipeline, chunks)
        5. Return len(chunks)
    """
    # TODO: implement
    raise NotImplementedError("Implement ingest_file")


# -----------------------------------------------------------------------
# Exercise 5.2 - Retrieval
# -----------------------------------------------------------------------
def retrieve(pipeline: QAPipeline, query: str) -> list[tuple[float, str]]:
    """
    Tim top_k chunk tuong dong voi query.

    Returns:
        list[(score, chunk_text)] sap xep giam dan

    TODO:
        1. Embed query: query_emb = embed_texts([query], pipeline.model)[0]
        2. Tinh cosine_similarity giua query_emb va moi hang trong pipeline.index
        3. Lay top_k chi so cao nhat
        4. Return [(score, pipeline.corpus[i]) for i in top_k_indices]
    Hint: np.argsort(scores)[::-1][:pipeline.top_k]
    """
    # TODO: implement
    raise NotImplementedError("Implement retrieve")


# -----------------------------------------------------------------------
# Exercise 5.3 - Generation
# -----------------------------------------------------------------------
def generate_answer(
    pipeline: QAPipeline,
    question: str,
    top_chunks: list[tuple[float, str]],
    use_history: bool = False,
) -> tuple[str, dict]:
    """
    Xay dung messages va goi LLM de tao cau tra loi.

    Returns:
        (answer_text, usage_dict)

    TODO:
        1. Lay chi phan chunk text (bo score): [text for _, text in top_chunks]
        2. Goi build_context_within_limit(chunk_texts, pipeline.max_context_tokens)
        3. Xay dung messages:
            - system: "Tra loi cau hoi chi dua vao tai lieu duoi day.
                       Neu khong co thong tin, noi 'Khong tim thay trong tai lieu.'"
            - (neu use_history == True): them pipeline.history vao giua
            - user: f"Tai lieu:\n{context}\n\nCau hoi: {question}"
        4. Goi chat_completion(messages, temperature=0.2, max_tokens=400)
        5. Return (extract_reply(response), response.get("usage", {}))
    """
    # TODO: implement
    raise NotImplementedError("Implement generate_answer")


# -----------------------------------------------------------------------
# Exercise 5.4 - Pipeline chinh
# -----------------------------------------------------------------------
def ask(pipeline: QAPipeline, question: str, use_history: bool = False) -> QAResult:
    """
    Chay toan bo pipeline: retrieve -> generate -> log history.

    TODO:
        1. Goi retrieve(pipeline, question) -> top_chunks
        2. Goi generate_answer(pipeline, question, top_chunks, use_history) -> (answer, usage)
        3. Neu use_history: them vao pipeline.history:
               {"role": "user", "content": question}
               {"role": "assistant", "content": answer}
        4. Return QAResult(question=question, answer=answer, top_chunks=top_chunks,
                           input_tokens=usage.get("prompt_tokens", 0),
                           output_tokens=usage.get("completion_tokens", 0))
    """
    # TODO: implement
    raise NotImplementedError("Implement ask")


# -----------------------------------------------------------------------
# Exercise 5.5 - Luu va hien thi ket qua
# -----------------------------------------------------------------------
def save_results(results: list[QAResult], output_path: Path) -> None:
    """
    Luu danh sach QAResult ra file JSON.

    TODO:
        1. Chuyen moi result thanh dict:
           {
               "question": ...,
               "answer": ...,
               "top_chunks": [{"score": s, "text": t} for s, t in result.top_chunks],
               "input_tokens": ...,
               "output_tokens": ...,
           }
        2. json.dump(records, ..., ensure_ascii=False, indent=2)
    """
    # TODO: implement
    raise NotImplementedError("Implement save_results")


def print_result(result: QAResult) -> None:
    """
    In QAResult dep ra stdout.

    TODO:
        In theo dinh dang:
        Q: <question>
        A: <answer>
        Top chunks:
          [score] chunk_text[:80]
        Tokens: input=X, output=Y
    """
    # TODO: implement
    raise NotImplementedError("Implement print_result")


# -----------------------------------------------------------------------
# Ham chay demo
# -----------------------------------------------------------------------
DEMO_KNOWLEDGE_BASE = [
    "RAG la viet tat cua Retrieval-Augmented Generation. Day la ky thuat ket hop tim kiem tai lieu voi kha nang sinh van ban cua LLM.",
    "Trong RAG, tai lieu nguon duoc chia thanh cac doan nho goi la chunk. Moi chunk duoc chuyen thanh vector embedding.",
    "Vector embedding la bieu dien so hoc cua van ban trong khong gian nhieu chieu. Cac van ban co noi dung tuong dong se co vector gan nhau.",
    "Khi nguoi dung gui cau hoi, cau hoi cung duoc embed thanh vector. He thong tim cac chunk co vector gan nhat voi query vector.",
    "Cac chunk lien quan nhat duoc truyen vao LLM cung voi cau hoi goc. LLM su dung thong tin nay de tra loi chinh xac hon.",
    "Cosine similarity la phuong phap pho bien de do muc do tuong dong giua cac vector embedding trong RAG.",
    "Vector database nhu Pinecone, Weaviate, Qdrant hay ChromaDB duoc dung de luu tru va tim kiem embeddings hieu qua.",
    "Chunking strategy quan trong trong RAG: chunk qua nho co the mat context, chunk qua lon co the gay nhieu thong tin khong lien quan.",
    "Sentence-transformers la thu vien Python cho phep tao embedding chat luong cao, chay hoan toan offline khong can API key.",
    "tiktoken la thu vien dem token cho cac mo hinh OpenAI, giup quan ly context window hieu qua va uoc tinh chi phi.",
    "Re-ranking la buoc tuy chon sau retrieval: dung mo hinh cross-encoder de sap xep lai cac chunk theo muc do phu hop thuc su.",
    "Lich su hoi-dap (conversation history) cho phep LLM hieu duoc nguong canh cau hoi trong cac cuoc tro chuyen nhieu luot.",
]

DEMO_QUESTIONS = [
    "RAG la gi?",
    "Embedding duoc dung nhu the nao trong RAG?",
    "Co the dung vector database nao voi RAG?",
    "Tai sao chunking strategy lai quan trong?",
]


def exercise_4_5():
    print("=" * 60)
    print("PHASE 4 - EXERCISE 5: MINI QA PIPELINE")
    print("=" * 60)

    # --- 5.1: Khoi tao pipeline ---
    print("\n[5.1] Khoi tao pipeline va nap tai lieu")
    try:
        pipeline = create_pipeline(
            model_name="all-MiniLM-L6-v2",
            llm_model="gpt-4o-mini",
            max_context_tokens=1000,
            top_k=3,
        )
        ingest_texts(pipeline, DEMO_KNOWLEDGE_BASE)
        print(f"  Da nap {len(pipeline.corpus)} chunks")
        print(f"  Index shape: {pipeline.index.shape}")
    except NotImplementedError as e:
        print(f"  [TODO] {e}")
        return

    # --- 5.2: Retrieval ---
    print("\n[5.2] Retrieval")
    try:
        test_q = "Cosine similarity la gi?"
        hits = retrieve(pipeline, test_q)
        print(f"  Query: '{test_q}'")
        for score, text in hits:
            print(f"  [{score:.4f}] {text[:70]}")
    except NotImplementedError as e:
        print(f"  [TODO] {e}")

    # --- 5.3 + 5.4: Full pipeline (ask) ---
    print("\n[5.3 + 5.4] Full QA pipeline")
    results: list[QAResult] = []
    for q in DEMO_QUESTIONS:
        try:
            result = ask(pipeline, q)
            results.append(result)
            try:
                print_result(result)
            except NotImplementedError:
                print(f"  Q: {q}")
                print(f"  A: {result.answer[:150]}")
            print()
        except NotImplementedError as e:
            print(f"  [TODO] {e}")
            break

    # --- Multi-turn ---
    print("\n[Multi-turn] Hoi tiep theo nguong canh")
    pipeline.history.clear()
    multi_turn_qs = [
        "Vector database la gi?",
        "No khac gi so voi database thuong?",  # phu thuoc cau truoc
    ]
    for q in multi_turn_qs:
        try:
            result = ask(pipeline, q, use_history=True)
            print(f"  Q: {q}")
            print(f"  A: {result.answer[:200]}")
            print()
        except NotImplementedError as e:
            print(f"  [TODO] {e}")
            break

    # --- 5.5: Luu ket qua ---
    if results:
        output_file = Path(__file__).parent / "qa_results.json"
        try:
            save_results(results, output_file)
            print(f"[5.5] Da luu {len(results)} ket qua vao: {output_file}")
        except NotImplementedError as e:
            print(f"  [TODO] save_results: {e}")


if __name__ == "__main__":
    exercise_4_5()
