"""
Phase 3 - Exercise 5 (Mini Project - Self-practice)
Document loader pipeline:
extract -> clean -> chunk -> metadata -> json
"""

from dataclasses import asdict
import argparse
import json
from pathlib import Path

from pypdf import PdfReader

from exercise_2_text_cleaning import clean_text
from exercise_4_chunk_metadata import build_chunk_records


def extract_text_from_txt(path: Path) -> list[tuple[int | None, str]]:
    # TODO: doc toan bo text va return [(None, text)]
    raise NotImplementedError("Implement extract_text_from_txt")


def extract_text_from_pdf(path: Path) -> list[tuple[int | None, str]]:
    # TODO:
    # 1. Dung PdfReader doc tung trang
    # 2. Return list[(page_number, text)]
    raise NotImplementedError("Implement extract_text_from_pdf")


def chunk_by_words_sliding_window(text: str, chunk_size: int = 220, overlap: int = 30) -> list[str]:
    # TODO: cai dat sliding-window chunking theo so tu
    # Hint nho: step = max(1, chunk_size - overlap)
    raise NotImplementedError("Implement chunk_by_words_sliding_window")


def load_document(path: Path) -> list[dict]:
    # TODO:
    # 1. Chon ham extract theo extension
    # 2. clean text moi page
    # 3. chunk text va gan metadata
    # 4. return list[dict]
    # Hint nho: asdict(record)
    raise NotImplementedError("Implement load_document")


def main():
    parser = argparse.ArgumentParser(description="Phase 3 document loader mini project")
    parser.add_argument("--input", required=True, help="Path to .txt or .pdf document")
    parser.add_argument("--output", default="document_chunks.json", help="Output JSON path")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # TODO:
    # 1. Goi load_document
    # 2. save JSON ra output_path
    # 3. in thong tin tong quan


if __name__ == "__main__":
    main()
