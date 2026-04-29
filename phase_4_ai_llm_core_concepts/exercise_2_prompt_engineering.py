"""
Phase 4 - Exercise 2 (Self-practice)
Prompt Engineering: system prompt, few-shot, CoT, structured output.

Muc tieu:
- Thiet ke system prompt ro rang
- Su dung few-shot examples trong messages
- Ap dung Chain-of-Thought (CoT) de cai thien suy luan
- Yeu cau LLM tra ve JSON co cau truc
"""

import json
import os
from dotenv import load_dotenv

load_dotenv()

# Import ham chat tu exercise 1 (hoac dung mock neu chua lam)
try:
    from exercise_1_llm_api_basics import chat_completion, extract_reply
except ImportError:
    def chat_completion(messages, temperature=0.7, max_tokens=256, **kw):
        user_text = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        return {
            "choices": [{"message": {"role": "assistant",
                                     "content": f"[MOCK] {user_text[:60]}"}}],
            "usage": {"total_tokens": 50},
        }

    def extract_reply(response: dict) -> str:
        return response["choices"][0]["message"]["content"]


# -----------------------------------------------------------------------
# Exercise 2.1 - System prompt ro rang
# -----------------------------------------------------------------------
def chat_with_system(system_prompt: str, user_message: str, **kwargs) -> str:
    """
    Gui request voi system prompt rieng biet.

    TODO:
        1. Xay dung list messages gom {"role": "system", ...} va {"role": "user", ...}
        2. Goi chat_completion
        3. Return extract_reply(response)
    """
    # TODO: implement
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_message},]
    response = chat_completion(messages, **kwargs)
    return extract_reply(response) 


# -----------------------------------------------------------------------
# Exercise 2.2 - Few-shot prompting
# -----------------------------------------------------------------------
def few_shot_sentiment(text: str) -> str:
    """
    Phan loai cam xuc (positive / negative / neutral) dung few-shot.

    TODO:
        Xay dung messages voi it nhat 3 cap vi du truoc khi hoi ve `text`:
        Vi du:
            user:  "San pham tuyet voi, giao hang nhanh!"
            assistant: "positive"
            user:  "Chat luong kem, that vong."
            assistant: "negative"
            user:  "Hang da nhan, binh thuong."
            assistant: "neutral"
        Sau do them user message la `text` can phan loai.
    Hint: them SYSTEM prompt: "Chi tra ve 1 tu: positive, negative, hoac neutral."
    """
    messages = [
        {"role": "system", "content": "Chi tra ve 1 tu: positive, negative, hoac neutral."},
        {"role": "user", "content": "San pham tuyet voi, giao hang nhanh!"},
        {"role": "assistant", "content": "positive"},
        {"role": "user", "content": "Chat luong kem, that vong."},
        {"role": "assistant", "content": "negative"},
        {"role": "user", "content": "Hang da nhan, binh thuong."},
        {"role": "assistant", "content": "neutral"},
        {"role": "user", "content": text},
    ]
    response = chat_completion(messages, temperature=0.0, max_tokens=10)
    return extract_reply(response).strip()


# -----------------------------------------------------------------------
# Exercise 2.3 - Chain-of-Thought (CoT)
# -----------------------------------------------------------------------
def cot_math_solver(problem: str) -> str:
    """
    Giai bai toan toan hoc bang cach yeu cau LLM suy luan tung buoc (CoT).

    TODO:
        1. Them vao system prompt: 'Hay suy nghi tung buoc truoc khi dua ra dap an cuoi cung.'
        2. Them vao user message: f'{problem}\n\nHay giai tung buoc.'
        3. Goi chat_completion voi max_tokens >= 400 de du cho cac buoc giai
        4. Return chuoi reply
    Hint: CoT hoat dong tot khi bao LLM 'think step by step'
    """
    messages = [
        {"role": "system", "content": "Hay suy nghi tung buoc truoc khi dua ra dap an cuoi cung."},
        {"role": "user", "content": f"{problem}\n\nHay giai tung buoc."},
    ]
    response = chat_completion(messages, temperature=0.2, max_tokens=400)
    return extract_reply(response)


# -----------------------------------------------------------------------
# Exercise 2.4 - Structured output (JSON)
# -----------------------------------------------------------------------
def extract_entities_as_json(text: str) -> dict:
    """
    Yeu cau LLM trich xuat thong tin tu doan van va tra ve JSON.

    Dinh dang JSON mong muon:
    {
        "persons": ["ten1", "ten2"],
        "organizations": ["to chuc1"],
        "locations": ["dia diem1"],
        "dates": ["ngay1"]
    }

    TODO:
        1. Xay dung system prompt: chi tra ve JSON thuan tuy, khong them markdown fence.
        2. User message: yeu cau trich xuat entities tu `text`
        3. Goi chat_completion voi temperature=0.0 (deterministic)
        4. Parse reply bang json.loads(...)
        5. Neu parse loi, thu cat bo ```json ... ``` roi parse lai
        6. Return dict (hoac dict rong neu that bai)
    Hint: temperature thap giup output on dinh hon.
    """
    system_prompt = (
        "Trich xuat thong tin tu doan van va tra ve JSON thuan tuy, khong them markdown fence.\n"
        "Dinh dang JSON:\n"
        '{"persons": [...], "organizations": [...], "locations": [...], "dates": [...]}'
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Trich xuat entities tu doan van sau:\n{text}"},
    ]
    response = chat_completion(messages, temperature=0.0, max_tokens=300)
    reply = extract_reply(response).strip()
    try:
        return json.loads(reply)
    except json.JSONDecodeError:
        # Thu cat bo markdown fence ```json ... ```
        clean = reply
        if clean.startswith("```"):
            clean = clean.split("\n", 1)[-1]
        if clean.endswith("```"):
            clean = clean.rsplit("```", 1)[0]
        try:
            return json.loads(clean.strip())
        except json.JSONDecodeError:
            return {}


# -----------------------------------------------------------------------
# Exercise 2.5 - Prompt template voi bien so
# -----------------------------------------------------------------------
def build_rag_prompt(question: str, context_chunks: list[str]) -> list[dict]:
    """
    Tao messages list cho RAG: noi context cac chunk roi hoi LLM.

    Args:
        question: cau hoi cua nguoi dung
        context_chunks: danh sach doan van lien quan lay tu retrieval

    Returns:
        messages list san sang de truyen vao chat_completion

    TODO:
        1. Noi cac chunk bang "\n\n---\n\n"
        2. System prompt:
            "Tra loi cau hoi dua tren nguon tai lieu duoc cung cap.
             Neu thong tin khong co trong tai lieu, hay noi 'Khong tim thay thong tin.'"
        3. User message:
            "Tai lieu:\n{context}\n\nCau hoi: {question}"
        4. Return messages list
    """
    context = "\n\n---\n\n".join(context_chunks)
    messages = [
        {
            "role": "system",
            "content": (
                "Tra loi cau hoi dua tren nguon tai lieu duoc cung cap.\n"
                "Neu thong tin khong co trong tai lieu, hay noi 'Khong tim thay thong tin.'"
            ),
        },
        {
            "role": "user",
            "content": f"Tai lieu:\n{context}\n\nCau hoi: {question}",
        },
    ]
    return messages


# -----------------------------------------------------------------------
# Ham chay demo
# -----------------------------------------------------------------------
def exercise_4_2():
    print("=" * 60)
    print("PHASE 4 - EXERCISE 2: PROMPT ENGINEERING")
    print("=" * 60)

    # --- 2.1: System prompt ---
    print("\n[2.1] System prompt")
    try:
        reply = chat_with_system(
            system_prompt="Ban la chuyen gia Python ngan gon. Chi tra loi bang gach dau dong.",
            user_message="Liet ke 3 thu vien Python pho bien cho xu ly van ban.",
            max_tokens=150,
        )
        print(f"  {reply}")
    except NotImplementedError as e:
        print(f"  [TODO] {e}")

    # --- 2.2: Few-shot sentiment ---
    print("\n[2.2] Few-shot sentiment")
    test_sentences = [
        "Dich vu cham soc khach hang rat tot!",
        "Toi da doi hang 3 tuan ma van chua nhan duoc.",
        "Don hang da giao, khong co van de gi.",
    ]
    for s in test_sentences:
        try:
            label = few_shot_sentiment(s)
            print(f"  '{s[:45]}' -> {label}")
        except NotImplementedError as e:
            print(f"  [TODO] {e}")
            break

    # --- 2.3: Chain-of-Thought ---
    print("\n[2.3] Chain-of-Thought math")
    problem = "Mot cua hang ban 3 loai san pham: A gia 50k, B gia 80k, C gia 120k. Khach mua 2A + 1B + 3C. Tong tien la bao nhieu?"
    try:
        solution = cot_math_solver(problem)
        print(f"  {solution[:300]}")
    except NotImplementedError as e:
        print(f"  [TODO] {e}")

    # --- 2.4: Structured JSON output ---
    print("\n[2.4] Extract entities as JSON")
    sample_text = (
        "Nguyen Van An, Giam doc cong ty ABC tai Ha Noi, "
        "da ky hop dong voi Microsoft vao ngay 15/03/2024."
    )
    try:
        entities = extract_entities_as_json(sample_text)
        print(f"  {json.dumps(entities, ensure_ascii=False, indent=2)}")
    except NotImplementedError as e:
        print(f"  [TODO] {e}")

    # --- 2.5: RAG prompt template ---
    print("\n[2.5] RAG prompt template")
    chunks = [
        "RAG la viet tat cua Retrieval-Augmented Generation.",
        "RAG ket hop retrieval (tim kiem tai lieu) voi generation (sinh van ban) cua LLM.",
    ]
    try:
        msgs = build_rag_prompt("RAG hoat dong nhu the nao?", chunks)
        print(f"  Messages count: {len(msgs)}")
        for m in msgs:
            print(f"  [{m['role']}]: {m['content'][:80]}")
        # Goi LLM voi prompt nay
        resp = chat_completion(msgs, temperature=0.2, max_tokens=200)
        print(f"  Reply: {extract_reply(resp)[:200]}")
    except NotImplementedError as e:
        print(f"  [TODO] {e}")


if __name__ == "__main__":
    exercise_4_2()
