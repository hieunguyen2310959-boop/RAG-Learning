# Phase 3 - Data and File Handling Exercises (Self-practice)

Muc tieu phase nay:
- Doc du lieu tu nhieu dinh dang file cho RAG ingestion
- Lam sach van ban
- Chia chunk co overlap
- Luu metadata cho retrieval
- Xay dung mini pipeline document loader

## Danh sach bai tap

Luu y: cac file duoi day la dang bai tap de tu lam.
- Co khung ham
- Co TODO
- Chi co goi y nho, khong co loi giai day du

1. `exercise_1_file_readers.py`
- Doc `.txt`, `.json`, `.pdf`, `.docx`, `.csv`, va web HTML

2. `exercise_2_text_cleaning.py`
- Chuan hoa whitespace
- Xoa page number va header/footer don gian
- Xu ly ky tu dac biet thong dung

3. `exercise_3_chunking_strategies.py`
- Fixed-size chunking
- Sliding window chunking (co overlap)
- Chunking theo cau

4. `exercise_4_chunk_metadata.py`
- Tao model metadata cho chunk
- Gan source file, page_number, chunk_index, timestamp
- Luu/Doc JSON

5. `exercise_5_document_loader_pipeline.py`
- Mini project: ingest file `.txt` hoac `.pdf`
- Clean -> chunk -> attach metadata -> save JSON

## Chay tung bai

```bash
python phase_3_data_file_handling/exercise_1_file_readers.py
python phase_3_data_file_handling/exercise_2_text_cleaning.py
python phase_3_data_file_handling/exercise_3_chunking_strategies.py
python phase_3_data_file_handling/exercise_4_chunk_metadata.py
python phase_3_data_file_handling/exercise_5_document_loader_pipeline.py
```

## Thu vien can thiet

- pypdf
- python-docx
- pandas
- beautifulsoup4
- lxml

Neu mot dinh dang file khong co san trong may, bai tap van cho phep bo qua va in canh bao.
