"""
Phase 4 - Exercise 1 (Self-practice)
Goi LLM API (OpenAI hoac Gemini) va hieu cau truc request/response.

Muc tieu:
- Gui chat completion request thanh cong
- Hieu y nghia cua temperature, max_tokens
- Xu ly streaming response
- Retry khi gap loi rate-limit / network
"""

import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

# -----------------------------------------------------------------------
# Cach chon provider: dat bien PROVIDER = "openai" hoac "gemini"
# Neu khong co key that, de PROVIDER = "mock" de chay voi gia lap.
# -----------------------------------------------------------------------
PROVIDER = os.getenv("LLM_PROVIDER", "mock")   # "openai" | "gemini" | "mock"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")


def _messages_to_text(messages: list[dict]) -> str:
    parts = []
    for msg in messages:
        role = msg.get("role", "user")
        content = str(msg.get("content", ""))
        parts.append(f"[{role}] {content}")
    return "\n".join(parts)


# -----------------------------------------------------------------------
# MOCK HELPER - dung khi chua co API key that
# -----------------------------------------------------------------------
def _mock_chat(messages: list[dict], temperature: float = 0.7, max_tokens: int = 256) -> dict:
    """Tra ve mot response gia lap giong cau truc OpenAI."""
    user_text = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
    return {
        "id": "mock-id-001",
        "object": "chat.completion",
        "model": "mock-gpt",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": f"[MOCK] Ban hoi: '{user_text[:60]}'. Day la phan hoi gia lap.",
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 20, "completion_tokens": 30, "total_tokens": 50},
    }


# -----------------------------------------------------------------------
# Exercise 1.1 - Gui chat request co ban
# -----------------------------------------------------------------------
def chat_completion(
    messages: list[dict],
    temperature: float = 0.7,
    max_tokens: int = 256,
) -> dict:
    """
    Gui chat completion request va tra ve response dict.

    Args:
        messages: danh sach {"role": "...", "content": "..."}
        temperature: 0.0 (deterministic) -> 2.0 (creative)
        max_tokens: so token toi da trong phan hoi

    Returns:
        response dict (cau truc tuong duong OpenAI)

    TODO:
        - Neu PROVIDER == "openai": dung openai.OpenAI() client
          Hint: client.chat.completions.create(model="gpt-4o-mini", ...)
          Sau do chuyen ve dict: response.model_dump()
        - Neu PROVIDER == "gemini": dung google.generativeai
          Hint: genai.configure(api_key=...) -> model.generate_content(...)
          Roi build dict tuong tu cau truc OpenAI de dong nhat
        - Neu PROVIDER == "mock": goi _mock_chat(...)
    """
    if PROVIDER == "mock":
        return _mock_chat(messages, temperature, max_tokens)

    if PROVIDER == "openai":
        if not OPENAI_API_KEY:
            raise ValueError("Thieu OPENAI_API_KEY. Dat key trong .env hoac dung LLM_PROVIDER=mock")
        try:
            from openai import OpenAI  # type: ignore[import-not-found]
        except ImportError as exc:
            raise ImportError("Chua cai openai. Hay chay: pip install openai") from exc

        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.model_dump()

    if PROVIDER == "gemini":
        if not GEMINI_API_KEY:
            raise ValueError("Thieu GEMINI_API_KEY. Dat key trong .env hoac dung LLM_PROVIDER=mock")

        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt = _messages_to_text(messages)
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            },
        )

        text = getattr(response, "text", "") or ""
        usage = getattr(response, "usage_metadata", None)
        prompt_tokens = getattr(usage, "prompt_token_count", 0) if usage else 0
        completion_tokens = getattr(usage, "candidates_token_count", 0) if usage else 0
        total_tokens = getattr(usage, "total_token_count", prompt_tokens + completion_tokens) if usage else 0

        return {
            "id": "gemini-response",
            "object": "chat.completion",
            "model": GEMINI_MODEL,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": text,
                    },
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
            },
        }

    raise ValueError(f"PROVIDER khong hop le: {PROVIDER}. Dung openai | gemini | mock")


# -----------------------------------------------------------------------
# Exercise 1.2 - Trich xuat noi dung tra loi
# -----------------------------------------------------------------------
def extract_reply(response: dict) -> str:
    """
    Lay chuoi noi dung phan hoi tu response dict.

    TODO:
        response["choices"][0]["message"]["content"]
    """
    return str(response["choices"][0]["message"].get("content", ""))


# -----------------------------------------------------------------------
# Exercise 1.3 - So sanh anh huong cua temperature
# -----------------------------------------------------------------------
def compare_temperatures(prompt: str, temperatures: list[float] | None = None) -> dict[float, str]:
    """
    Gui cung 1 prompt voi nhieu gia tri temperature khac nhau.
    Tra ve dict {temperature: reply_text}.

    TODO:
        1. Voi moi gia tri trong temperatures, goi chat_completion
        2. Trich xuat reply bang extract_reply
        3. Return dict ket qua
    Hint: temperatures mac dinh [0.0, 0.5, 1.0, 1.5]
    """
    if temperatures is None:
        temperatures = [0.0, 0.5, 1.0, 1.5]

    results: dict[float, str] = {}
    for temp in temperatures:
        messages = [{"role": "user", "content": prompt}]
        response = chat_completion(messages, temperature=temp, max_tokens=120)
        results[temp] = extract_reply(response)
    return results


# -----------------------------------------------------------------------
# Exercise 1.4 - Retry don gian khi gap loi
# -----------------------------------------------------------------------
def chat_with_retry(
    messages: list[dict],
    max_retries: int = 3,
    backoff_base: float = 2.0,
    **kwargs,
) -> dict:
    """
    Goi chat_completion voi co che retry exponential backoff.

    TODO:
        1. Lap toi da max_retries lan
        2. Neu thanh cong, return ngay
        3. Neu gap Exception, in canh bao, sleep(backoff_base ** attempt), roi thu lai
        4. Sau khi het lan thu, raise Exception cuoi cung
    Hint: for attempt in range(max_retries): try/except
    """
    last_exc: Exception | None = None
    for attempt in range(max_retries):
        try:
            return chat_completion(messages, **kwargs)
        except NotImplementedError:
            raise  # khong retry cho NotImplementedError khi dang lam bai
        except Exception as exc:
            last_exc = exc
            wait = backoff_base ** attempt
            print(f"  [retry {attempt + 1}/{max_retries}] loi: {exc} - cho {wait:.1f}s")
            time.sleep(wait)
    raise RuntimeError(f"That bai sau {max_retries} lan thu: {last_exc}")


# -----------------------------------------------------------------------
# Exercise 1.5 - Streaming response (OpenAI / mock)
# -----------------------------------------------------------------------
def stream_chat(messages: list[dict], max_tokens: int = 256):
    """
    Stream tung token/chunk phan hoi ra stdout.
    Sau khi xong in newline va tong so token (neu co).

    TODO:
        - Neu PROVIDER == "openai":
            dung stream=True trong client.chat.completions.create(...)
            lap qua response, in delta.content
        - Neu PROVIDER == "mock" (hoac chua implement):
            gia lap stream bang cach in tung tu trong mock reply
            Hint: for word in reply.split(): print(word, end=" ", flush=True); time.sleep(0.05)
    """
    if PROVIDER == "openai":
        if not OPENAI_API_KEY:
            raise ValueError("Thieu OPENAI_API_KEY. Dat key trong .env hoac dung LLM_PROVIDER=mock")
        try:
            from openai import OpenAI  # type: ignore[import-not-found]
        except ImportError as exc:
            raise ImportError("Chua cai openai. Hay chay: pip install openai") from exc

        client = OpenAI(api_key=OPENAI_API_KEY)
        stream = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=max_tokens,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content if chunk.choices else None
            if delta:
                print(delta, end="", flush=True)
        print()
        return

    if PROVIDER == "gemini":
        if not GEMINI_API_KEY:
            raise ValueError("Thieu GEMINI_API_KEY. Dat key trong .env hoac dung LLM_PROVIDER=mock")
        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt = _messages_to_text(messages)
        stream = client.models.generate_content_stream(
            model=GEMINI_MODEL,
            contents=prompt,
            config={"max_output_tokens": max_tokens},
        )
        for chunk in stream:
            text = getattr(chunk, "text", "")
            if text:
                print(text, end="", flush=True)
        print()
        return

    reply = extract_reply(_mock_chat(messages, max_tokens=max_tokens))
    for word in reply.split():
        print(word, end=" ", flush=True)
        time.sleep(0.05)
    print()


# -----------------------------------------------------------------------
# Ham chay demo
# -----------------------------------------------------------------------
def exercise_4_1():
    print("=" * 60)
    print("PHASE 4 - EXERCISE 1: LLM API BASICS")
    print(f"Provider: {PROVIDER}")
    print("=" * 60)

    # --- 1.1 + 1.2: Chat co ban ---
    print("\n[1.1 + 1.2] Chat co ban")
    messages = [
        {"role": "system", "content": "Ban la tro ly AI ngan gon, tra loi bang tieng Viet."},
        {"role": "user", "content": "RAG la gi? Giai thich trong 2 cau."},
    ]
    try:
        response = chat_completion(messages, temperature=0.3, max_tokens=120)
        reply = extract_reply(response)
        print(f"  Reply: {reply}")
        print(f"  Usage: {response.get('usage', {})}")
    except NotImplementedError as e:
        print(f"  [TODO] {e}")

    # --- 1.3: So sanh temperature ---
    print("\n[1.3] So sanh temperature")
    try:
        results = compare_temperatures("Dat ten cho mot chiec robot de thuong.")
        for temp, text in results.items():
            print(f"  temp={temp}: {text[:80]}")
    except NotImplementedError as e:
        print(f"  [TODO] {e}")

    # --- 1.4: Retry ---
    print("\n[1.4] Chat voi retry")
    try:
        resp = chat_with_retry(messages, max_retries=2)
        print(f"  Reply (retry): {extract_reply(resp)[:80]}")
    except NotImplementedError as e:
        print(f"  [TODO] {e}")

    # --- 1.5: Streaming ---
    print("\n[1.5] Streaming:")
    try:
        stream_chat([{"role": "user", "content": "Dem 1 den 5 bang tieng Anh."}])
    except NotImplementedError as e:
        print(f"  [TODO] {e}")


if __name__ == "__main__":
    exercise_4_1()
