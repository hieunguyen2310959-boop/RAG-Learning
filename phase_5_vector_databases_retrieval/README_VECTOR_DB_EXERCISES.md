# Phase 5 - Vector Databases & Retrieval (Self-practice)

Muc tieu phase nay:
- Hieu vector database la gi va tai sao can trong RAG
- Lam viec voi ChromaDB: tao collection, ingest, query
- Implement cac chien luoc retrieval: top-k, threshold, metadata filter
- Xay dung hybrid search (semantic + BM25) bang RRF
- Xay dung retrieval engine hoan chinh, san sang cho Phase 6

## Danh sach bai tap

Luu y: cac file la bai tap de tu lam.
- Co khung ham + TODO + hint chi tiet
- Mot so ham da implement san de minh hoa, mot so yeu cau tu lam
- Chay `python <file>` de kiem tra tung bai

---

### 1. `exercise_1_chromadb_basics.py`
**Chu de: Lam quen ChromaDB**
- Tao in-memory va persistent client
- Get-or-create collection voi cosine similarity
- Add / upsert documents voi metadata
- Query bang text va embedding
- Format ket qua: chuyen distance -> similarity score
- Delete document theo id

**Khai niem hoc duoc:** Collection, ANN search, distance vs score, metadata filter

---

### 2. `exercise_2_document_indexing.py`
**Chu de: Nap tai lieu vao vector index**
- Load ChunkRecord tu file JSON (output Phase 3) hoac tu list text
- Embed chunks bang sentence-transformers (co batch va progress bar)
- Ingest vao ChromaDB: add vs upsert
- Xoa tai lieu theo source (metadata filter)
- Lay thong ke index: tong chunks, so nguon

**Khai niem hoc duoc:** Ingestion pipeline, upsert idempotency, index stats

---

### 3. `exercise_3_retrieval_strategies.py`
**Chu de: Cac chien luoc tim kiem**
- Top-k retrieval: lay K ket qua gan nhat
- Threshold filtering: chi giu ket qua co score >= nguong
- Source filter: chi tim trong 1 tai lieu cu the
- Page range filter: chi tim trong khoang trang
- So sanh cac gia tri k -> hieu precision/recall
- Tim nguong toi uu cho corpus cu the

**Khai niem hoc duoc:** Precision vs Recall, nguong ky thuat, metadata filtering

---

### 4. `exercise_4_hybrid_search.py`
**Chu de: Hybrid Search = Semantic + BM25**
- BM25Index: keyword search khong can vector DB (rank-bm25)
- Semantic search wrapper
- Reciprocal Rank Fusion (RRF): ket hop 2 danh sach ket qua
- Full hybrid_search pipeline
- So sanh 3 phuong phap tren cac loai query khac nhau

**Khai niem hoc duoc:** BM25, RRF, khi nao dung hybrid vs pure semantic

---

### 5. `exercise_5_mini_retrieval_system.py` *(Mini Project)*
**Chu de: He thong retrieval hoan chinh**
- `DocumentIngestor`: chunk -> embed -> upsert vao ChromaDB
- `RetrievalEngine`: search semantic / hybrid, threshold, source filter
- `RetrievedChunk` + `RetrievalResult`: data models ro rang
- Xu ly edge case: khong co ket qua, score qua thap
- `format_context_for_llm()`: chuoi context san sang cho Phase 6
- Luu ket qua ra JSON de debug

**Day la bai tap quan trong nhat.** Sau khi hoan thanh, ban co retrieval engine thuc su.

---

## Chay tung bai

```bash
python phase_5_vector_databases_retrieval/exercise_1_chromadb_basics.py
python phase_5_vector_databases_retrieval/exercise_2_document_indexing.py
python phase_5_vector_databases_retrieval/exercise_3_retrieval_strategies.py
python phase_5_vector_databases_retrieval/exercise_4_hybrid_search.py
python phase_5_vector_databases_retrieval/exercise_5_mini_retrieval_system.py
```

## Thu vien can cai dat

```
chromadb
sentence-transformers
rank-bm25
numpy
```

Cai nhanh:
```bash
pip install chromadb sentence-transformers rank-bm25 numpy
```

## Luu y quan trong

| Dieu can nho | Ly do |
|---|---|
| Dung CUNG 1 embedding model khi ingest va query | Khac model -> vector khong so sanh duoc |
| `hnsw:space: cosine` khi tao collection | RAG dung cosine, khong phai L2 |
| Upsert thay vi add khi chay lai pipeline | Tranh loi duplicate ID |
| ChromaDB tra ve `distance`, khong phai `score` | Score = 1 - distance (voi cosine) |
| Threshold 0.4-0.6 la an toan | Qua cao = miss ket qua tot; qua thap = nhieu rac |

## Lien ket voi cac phase khac

```
Phase 3 (chunking) --> Phase 5 exercise_2 (ingest)
Phase 4 (embeddings) --> Phase 5 exercise_2, 3, 4, 5
Phase 5 (retrieval) --> Phase 6 (full RAG = retrieval + LLM generation)
```

Phase 5 exercise_5 la "retrieval half" cua RAG.
Phase 6 se them "generation half" (goi LLM voi context da retrieve).
