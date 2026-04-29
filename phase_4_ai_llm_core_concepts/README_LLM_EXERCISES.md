# Phase 4 - AI & LLM Core Concepts (Self-practice)

Muc tieu phase nay:
- Goi LLM API (OpenAI / Gemini) va hieu cau truc request/response
- Ky thuat Prompt Engineering co ban va nang cao
- Tao va su dung Text Embeddings voi sentence-transformers
- Quan ly Token va Context Window hieu qua
- Xay dung mini QA pipeline ket hop embedding + LLM

## Danh sach bai tap

Luu y: cac file duoi day la dang bai tap de tu lam.
- Co khung ham
- Co TODO
- Chi co goi y nho, khong co loi giai day du

1. `exercise_1_llm_api_basics.py`
   - Goi chat completion API (OpenAI hoac Gemini)
   - Hieu cac tham so: temperature, max_tokens, top_p
   - Xu ly response va streaming
   - Retry va error handling cho LLM

2. `exercise_2_prompt_engineering.py`
   - System prompt va User prompt
   - Few-shot prompting
   - Chain-of-Thought (CoT)
   - Tao structured output (JSON) tu LLM

3. `exercise_3_text_embeddings.py`
   - Tao embedding voi sentence-transformers
   - Tinh cosine similarity giua cac van ban
   - Tim van ban tuong dong nhat (nearest neighbor thu cong)
   - Hieu anh huong cua model embedding den ket qua

4. `exercise_4_token_context_management.py`
   - Dem token voi tiktoken (OpenAI) hoac tokenizer cua Gemini
   - Tinh chi phi uoc tinh cho 1 request
   - Cat/chon chunks phu hop voi context window
   - Build context string khong vuot qua token limit

5. `exercise_5_mini_qa_pipeline.py`
   - Mini project: nhan cau hoi -> embed -> tim chunk lien quan -> goi LLM -> in tra loi
   - Ket hop exercise 3 (embeddings) + exercise 1 (LLM call)
   - Danh gia chat luong tra loi don gian

## Chay tung bai

```bash
python phase_4_ai_llm_core_concepts/exercise_1_llm_api_basics.py
python phase_4_ai_llm_core_concepts/exercise_2_prompt_engineering.py
python phase_4_ai_llm_core_concepts/exercise_3_text_embeddings.py
python phase_4_ai_llm_core_concepts/exercise_4_token_context_management.py
python phase_4_ai_llm_core_concepts/exercise_5_mini_qa_pipeline.py
```

## Thu vien can thiet

```
openai
google-generativeai
sentence-transformers
tiktoken
numpy
python-dotenv
```

Cai dat:
```bash
pip install openai google-generativeai sentence-transformers tiktoken numpy python-dotenv
```

## Bien moi truong can thiet

Tao file `.env` trong thu muc goc hoac phase_4_ai_llm_core_concepts/:
```
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AI...
```

Luu y: co the chi dung 1 trong 2 key. Cac bai tap co phan chon OPENAI hoac GEMINI.

## Ghi chu

- Neu khong co API key that, dung mock/stub de luyen ham logic (cac bai co cung cap mock)
- sentence-transformers chay local, khong can API key
- tiktoken cung chay local
