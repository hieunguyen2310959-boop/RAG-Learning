"""
Phase 4 - Exercise 4 (Self-practice)
Token Counting & Context Window Management.

Muc tieu:
- Dem token chinh xac bang tiktoken (cho OpenAI models)
- Uoc tinh chi phi API (cost estimation)
- Cat chunk phu hop voi token limit
- Build context string khong vuot qua gioi han token
- Hieu context window cua cac model pho bien
"""

from __future__ import annotations

import tiktoken


# -----------------------------------------------------------------------
# Thong tin context window va gia tien cua cac model pho bien (2024)
# -----------------------------------------------------------------------
MODEL_INFO: dict[str, dict] = {
    "gpt-4o-mini": {
        "context_window": 128_000,
        "input_price_per_1k": 0.00015,   # USD per 1000 input tokens
        "output_price_per_1k": 0.00060,  # USD per 1000 output tokens
        "encoding": "o200k_base",
    },
    "gpt-4o": {
        "context_window": 128_000,
        "input_price_per_1k": 0.0025,
        "output_price_per_1k": 0.01,
        "encoding": "o200k_base",
    },
    "gpt-3.5-turbo": {
        "context_window": 16_385,
        "input_price_per_1k": 0.0005,
        "output_price_per_1k": 0.0015,
        "encoding": "cl100k_base",
    },
    "gemini-1.5-flash": {
        "context_window": 1_000_000,
        "input_price_per_1k": 0.000075,
        "output_price_per_1k": 0.0003,
        "encoding": "cl100k_base",  # xap xi; Gemini dung tokenizer rieng
    },
}


# -----------------------------------------------------------------------
# Exercise 4.1 - Dem token
# -----------------------------------------------------------------------
def count_tokens(text: str, model: str = "gpt-4o-mini") -> int:
    """
    Dem so luong token cua mot chuoi van ban.

    TODO:
        1. Lay ten encoding tu MODEL_INFO[model]["encoding"],
           hoac dung "cl100k_base" lam fallback
        2. enc = tiktoken.get_encoding(encoding_name)
        3. return len(enc.encode(text))
    Hint: tiktoken.get_encoding("cl100k_base") luon hoat dong.
    """
    # TODO: implement
    raise NotImplementedError("Implement count_tokens")


def count_messages_tokens(messages: list[dict], model: str = "gpt-4o-mini") -> int:
    """
    Dem tong so token cua mot danh sach messages (chat format).

    Moi message them overhead: ~4 token / message (theo OpenAI cookbook).

    TODO:
        1. Dem token trong moi message["content"] bang count_tokens
        2. Cong 4 token overhead cho moi message
        3. Cong 3 token overhead cho ca cuoc tro chuyen (reply priming)
        4. Return tong
    Hint: tham khao https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
    """
    # TODO: implement
    raise NotImplementedError("Implement count_messages_tokens")


# -----------------------------------------------------------------------
# Exercise 4.2 - Uoc tinh chi phi
# -----------------------------------------------------------------------
def estimate_cost(
    input_tokens: int,
    output_tokens: int,
    model: str = "gpt-4o-mini",
) -> dict:
    """
    Uoc tinh chi phi cho mot request.

    Returns:
        {
            "model": str,
            "input_tokens": int,
            "output_tokens": int,
            "input_cost_usd": float,
            "output_cost_usd": float,
            "total_cost_usd": float,
        }

    TODO:
        1. Lay gia tu MODEL_INFO (neu model khong co, dung gpt-4o-mini lam fallback)
        2. Tinh input_cost = input_tokens / 1000 * input_price_per_1k
        3. Tinh output_cost tuong tu
        4. Return dict
    """
    # TODO: implement
    raise NotImplementedError("Implement estimate_cost")


# -----------------------------------------------------------------------
# Exercise 4.3 - Cat chunk theo token limit
# -----------------------------------------------------------------------
def truncate_to_token_limit(text: str, max_tokens: int, model: str = "gpt-4o-mini") -> str:
    """
    Cat chuoi text de khong vuot qua max_tokens.

    TODO:
        1. encode text thanh list[int] token ids
           Hint: enc.encode(text)
        2. Neu len(tokens) <= max_tokens: return text goc
        3. Neu qua dai: cat tokens[:max_tokens] roi decode lai
           Hint: enc.decode(tokens[:max_tokens])
    """
    # TODO: implement
    raise NotImplementedError("Implement truncate_to_token_limit")


# -----------------------------------------------------------------------
# Exercise 4.4 - Build context tu nhieu chunks
# -----------------------------------------------------------------------
def build_context_within_limit(
    chunks: list[str],
    max_context_tokens: int,
    model: str = "gpt-4o-mini",
    separator: str = "\n\n---\n\n",
) -> str:
    """
    Noi cac chunks lai theo thu tu uu tien (index nho = quan trong hon),
    dung khi tong token chua vuot qua max_context_tokens.

    TODO:
        1. Lap qua cac chunks theo thu tu
        2. Thu them tung chunk vao context (noi bang separator)
        3. Kiem tra count_tokens(context) <= max_context_tokens
        4. Neu van con cho: them chunk; neu vuot qua: dung lai
        5. Return context string cuoi cung
    Hint: tinh toan truoc: token cua separator khoang 4-6 tokens.
    """
    # TODO: implement
    raise NotImplementedError("Implement build_context_within_limit")


# -----------------------------------------------------------------------
# Exercise 4.5 - Phan tich request truoc khi gui
# -----------------------------------------------------------------------
def analyze_request(
    messages: list[dict],
    expected_output_tokens: int = 300,
    model: str = "gpt-4o-mini",
) -> dict:
    """
    Phan tich request truoc khi gui API: token count, chi phi, % context da dung.

    Returns:
        {
            "model": str,
            "context_window": int,
            "input_tokens": int,
            "expected_output_tokens": int,
            "total_expected_tokens": int,
            "context_usage_pct": float,     # % context window da dung
            "fits_in_context": bool,
            "estimated_cost": dict,
        }

    TODO:
        1. Dem token cua messages bang count_messages_tokens
        2. Tinh tong = input_tokens + expected_output_tokens
        3. Lay context_window tu MODEL_INFO
        4. Tinh context_usage_pct = total / context_window * 100
        5. fits_in_context = total <= context_window
        6. Goi estimate_cost
        7. Return dict
    """
    # TODO: implement
    raise NotImplementedError("Implement analyze_request")


# -----------------------------------------------------------------------
# Ham chay demo
# -----------------------------------------------------------------------
SAMPLE_CHUNKS = [
    "RAG la viet tat cua Retrieval-Augmented Generation, mot ky thuat ket hop tim kiem tai lieu voi mo hinh ngon ngu lon.",
    "Trong RAG, tai lieu duoc chia thanh cac chunk nho, sau do duoc embed va luu vao vector database.",
    "Khi co query, he thong se embed query, tim cac chunk tuong dong, va truyen vao LLM de tao ra cau tra loi.",
    "Vector database la thanh phan quan trong trong RAG, no luu tru embeddings va cho phep tim kiem nhanh.",
    "Cac LLM pho bien su dung trong RAG bao gom GPT-4, Claude, Gemini va cac mo hinh open-source nhu Llama.",
    "Chunking strategy anh huong lon den chat luong cua RAG: chunk qua nho mat context, chunk qua lon gay noise.",
    "Cosine similarity la cach pho bien nhat de do muc do tuong dong giua cac embeddings trong RAG.",
    "Re-ranking la buoc tuy chon sau retrieval de chon ra cac chunk thuc su lien quan nhat.",
]


def exercise_4_4():
    print("=" * 60)
    print("PHASE 4 - EXERCISE 4: TOKEN & CONTEXT MANAGEMENT")
    print("=" * 60)

    # --- 4.1: Dem token ---
    print("\n[4.1] Dem token")
    sample_text = "RAG ket hop tim kiem tai lieu voi sinh van ban cua LLM."
    try:
        n = count_tokens(sample_text)
        print(f"  Text: '{sample_text}'")
        print(f"  Token count: {n}")
    except NotImplementedError as e:
        print(f"  [TODO] {e}")

    messages = [
        {"role": "system", "content": "Ban la tro ly AI."},
        {"role": "user", "content": "RAG la gi?"},
    ]
    try:
        total = count_messages_tokens(messages)
        print(f"  Messages token count: {total}")
    except NotImplementedError as e:
        print(f"  [TODO] {e}")

    # --- 4.2: Chi phi ---
    print("\n[4.2] Uoc tinh chi phi")
    try:
        cost = estimate_cost(input_tokens=500, output_tokens=200, model="gpt-4o-mini")
        print(f"  500 input + 200 output tokens (gpt-4o-mini):")
        print(f"  Input cost:  ${cost['input_cost_usd']:.6f}")
        print(f"  Output cost: ${cost['output_cost_usd']:.6f}")
        print(f"  Total:       ${cost['total_cost_usd']:.6f}")
    except NotImplementedError as e:
        print(f"  [TODO] {e}")

    # --- 4.3: Truncate ---
    print("\n[4.3] Truncate text")
    long_text = " ".join(SAMPLE_CHUNKS)
    try:
        truncated = truncate_to_token_limit(long_text, max_tokens=50)
        original_tokens = count_tokens(long_text)
        truncated_tokens = count_tokens(truncated)
        print(f"  Goc: {original_tokens} tokens")
        print(f"  Sau khi cat (<= 50 tokens): {truncated_tokens} tokens")
        print(f"  Preview: '{truncated[:80]}...'")
    except NotImplementedError as e:
        print(f"  [TODO] {e}")

    # --- 4.4: Build context ---
    print("\n[4.4] Build context within limit")
    try:
        context = build_context_within_limit(SAMPLE_CHUNKS, max_context_tokens=200)
        ctx_tokens = count_tokens(context)
        print(f"  Tong chunk: {len(SAMPLE_CHUNKS)}, token limit: 200")
        print(f"  Context tokens: {ctx_tokens}")
        print(f"  So chunk duoc them: {context.count('---') + 1}")
    except NotImplementedError as e:
        print(f"  [TODO] {e}")

    # --- 4.5: Analyze request ---
    print("\n[4.5] Phan tich request")
    rag_messages = [
        {"role": "system", "content": "Tra loi dua tren tai lieu."},
        {"role": "user", "content": "Tai lieu:\n" + "\n\n".join(SAMPLE_CHUNKS[:4]) + "\n\nCau hoi: RAG la gi?"},
    ]
    try:
        analysis = analyze_request(rag_messages, expected_output_tokens=300, model="gpt-4o-mini")
        print(f"  Model:           {analysis['model']}")
        print(f"  Input tokens:    {analysis['input_tokens']}")
        print(f"  Total expected:  {analysis['total_expected_tokens']}")
        print(f"  Context usage:   {analysis['context_usage_pct']:.2f}%")
        print(f"  Fits in context: {analysis['fits_in_context']}")
        print(f"  Est. cost:       ${analysis['estimated_cost']['total_cost_usd']:.6f}")
    except NotImplementedError as e:
        print(f"  [TODO] {e}")


if __name__ == "__main__":
    exercise_4_4()
