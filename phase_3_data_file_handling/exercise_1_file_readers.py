"""
Phase 3 - Exercise 1 (Self-practice)
Doc file tu cac dinh dang pho bien cho RAG ingestion.
"""

import json
from pathlib import Path
from pypdf import PdfReader
from docx import Document
import pandas as pd
from bs4 import BeautifulSoup
def read_txt(path: Path) -> str:
    # TODO: doc text tu file .txt voi UTF-8
    # Hint nho: path.read_text(encoding="utf-8")
    p = Path(path)
    result = p.read_text(encoding="utf-8")
    return result


def read_json(path: Path) -> str:
    # TODO: doc file JSON va tra ve chuoi dep de debug
    # Hint nho: json.loads(...) + json.dumps(..., indent=2)
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    pretty = json.dumps(data, indent=2, ensure_ascii=False)
    return pretty


def read_pdf(path: Path) -> str:
    # TODO: dung pypdf.PdfReader de extract text moi page
    # Hint nho: "\n".join(...)
    pdf = PdfReader(path)
    text = "\n".join(page.extract_text() for page in pdf.pages)
    return text




def read_docx(path: Path) -> str:
    # TODO: dung python-docx de ghep text cua paragraphs
    doc = Document(path)
    text = "\n".join(para.text for para in doc.paragraphs)
    return text


def read_csv(path: Path) -> str:
    # TODO: doc CSV thanh DataFrame, sau do convert thanh string
    df = pd.read_csv(path)
    text = df.to_string(index=False)
    return text


def read_html(path: Path) -> str:
    # TODO: parse HTML va lay plain text
    # Hint nho: BeautifulSoup(...).get_text(" ", strip=True)
    html = path.read_text(encoding="utf-8")
    text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
    return text


def exercise_3_1():
    print("=" * 60)
    print("PHASE 3 - EXERCISE 1: FILE READERS")
    print("=" * 60)

    # TODO:
    # 1. Tao thu muc test_data trong phase_3_data_file_handling
    # 2. Dat vao do 1-2 file mau (txt/json/csv/pdf/docx/html)
    # 3. Goi cac ham read_* de doc du lieu
    # 4. In ra 300 ky tu dau tien cua moi file

    base = Path(__file__).parent / "test_data"
    if not base.exists():
        print("test_data folder not found. Create it to practice this exercise.")
        return

    handlers = {
        ".txt": read_txt,
        ".json": read_json,
        ".pdf": read_pdf,
        ".docx": read_docx,
        ".csv": read_csv,
        ".html": read_html,
        ".htm": read_html,
    }

    # TODO:
    # 1. Duyet qua tung file trong test_data
    # 2. Chon reader dua tren extension
    # 3. In preview 300 ky tu dau
    # Hint nho: dung handlers.get(file_path.suffix.lower())
    for file_path in sorted(base.iterdir()):
        if not file_path.is_file():
            continue

        reader = handlers.get(file_path.suffix.lower())
        if reader is None:
            print(f"[SKIP] {file_path.name}: unsupported extension")
            continue

        try:
            content = reader(file_path)
            preview = content[:300]
            print(f"\n[{file_path.name}]")
            print(preview)
        except Exception as exc:
            print(f"[ERROR] {file_path.name}: {exc}")


if __name__ == "__main__":
    exercise_3_1()
