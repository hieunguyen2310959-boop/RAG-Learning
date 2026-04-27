"""
Phase 3 - Exercise 3 (Self-practice)
Chunking strategies for RAG ingestion.
"""

import re




def chunk_by_words_sliding_window(text: str, chunk_size: int = 80, overlap: int = 12):
    # TODO:
    # Chia chunk co overlap
    # Hint nho: step = max(1, chunk_size - overlap)
    words = text.split()
    if not words:
        return []

    step = max(1, chunk_size - overlap)
    chunks = []

    for start in range(0, len(words), step):
        window = words[start : start + chunk_size]
        if not window:
            break
        chunks.append(" ".join(window))
        if start + chunk_size >= len(words):
            break

    return chunks


def chunk_by_sentence(text: str, max_chars: int = 450):
    # TODO:
    # 1. Tach text theo cau
    # 2. Ghep cac cau vao chunk toi da max_chars
    # Hint nho: re.split(r"(?<=[.!?])\\s+", text)
    text = text.strip()
    if not text:
        return []

    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    if not sentences:
        return []

    chunks = []
    current = ""

    for sentence in sentences:
        candidate = sentence if not current else f"{current} {sentence}"

        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                chunks.append(current)

            # Nếu 1 câu quá dài thì vẫn giữ nguyên như 1 chunk riêng.
            if len(sentence) > max_chars:
                chunks.append(sentence)
                current = ""
            else:
                current = sentence

    if current:
        chunks.append(current)

    return chunks


def exercise_3_3():
    print("=" * 60)
    print("PHASE 3 - EXERCISE 3: CHUNKING STRATEGIES")
    print("=" * 60)

    text = (
        "RAG systems need good chunks. "
        "Chunk size affects retrieval quality. "
        "Too small chunks may lose context. "
        "Too large chunks may include irrelevant details. "
        "Overlapping chunks help preserve continuity between segments. "
        "Sentence-aware chunking often improves readability. "
    ) * 6

    # TODO:
    # 1. Goi 3 ham chunking
    # 2. In so luong chunk cua tung cach
    # 3. In chunk dau tien de so sanh
    chunks_word_no_overlap = chunk_by_words_sliding_window(text, chunk_size=80, overlap=0)
    chunks_word_overlap = chunk_by_words_sliding_window(text, chunk_size=80, overlap=12)
    chunks_sentence = chunk_by_sentence(text, max_chars=450)

    print("Word chunks (no overlap):", len(chunks_word_no_overlap))
    print("Word chunks (overlap=12):", len(chunks_word_overlap))
    print("Sentence chunks:", len(chunks_sentence))

    if chunks_word_no_overlap:
        print("\nFirst word chunk (no overlap):")
        print(chunks_word_no_overlap[0])

    if chunks_word_overlap:
        print("\nFirst word chunk (with overlap):")
        print(chunks_word_overlap[0])

    if chunks_sentence:
        print("\nFirst sentence chunk:")
        print(chunks_sentence[0])

    # TODO:
    # 1. Thu nghiem cac gia tri chunk_size, overlap khac nhau
    # 2. In do dai tung chunk de so sanh
    # 3. Chon cau hinh phu hop cho tai lieu cua ban
    print("\n" + "-" * 60)
    test_configs = [
        (40, 0),
        (60, 10),
        (80, 12),
    ]
    for chunk_size, overlap in test_configs:
        test_chunks = chunk_by_words_sliding_window(text, chunk_size=chunk_size, overlap=overlap)
        lengths = [len(chunk.split()) for chunk in test_chunks]
        print(f"chunk_size={chunk_size}, overlap={overlap} -> chunks={len(test_chunks)}")
        print("chunk lengths:", lengths)


if __name__ == "__main__":
    exercise_3_3()
