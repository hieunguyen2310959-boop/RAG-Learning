"""
Phase 3 - Exercise 4 (Self-practice)
Attach metadata to chunks and save as JSON.
"""

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import json


@dataclass
class ChunkRecord:
    chunk_id: str
    text: str
    source: str
    page_number: int | None
    chunk_index: int
    created_at: str


def build_chunk_records(chunks: list[str], source: str, page_number: int | None = None) -> list[ChunkRecord]:
    # TODO:
    # 1. Tao created_at dang ISO time
    # 2. Loop qua chunks va tao ChunkRecord
    # 3. chunk_id theo mau: <source_stem>_chunk_<index>
    # Hint nho: datetime.now(timezone.utc).isoformat()
    created_at = datetime.now(timezone.utc).isoformat()
    source_stem = Path(source).stem

    result: list[ChunkRecord] = []
    for i, text in enumerate(chunks):
        chunk_id = f"{source_stem}_chunk_{i}"
        result.append(
            ChunkRecord(
                chunk_id=chunk_id,
                text=text,
                source=source,
                page_number=page_number,
                chunk_index=i,
                created_at=created_at,
            )
        )
    return result


def save_records(records: list[ChunkRecord], output_path: Path):
    # TODO: convert dataclass -> dict roi save JSON ra file
    # Hint nho: asdict(record)
    json_file = []
    for record in records:
        temp = asdict(record)
        json_file.append(temp)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(json_file, f, ensure_ascii=False, indent=2)



def exercise_3_4():
    print("=" * 60)
    print("PHASE 3 - EXERCISE 4: CHUNK METADATA")
    print("=" * 60)

    sample_chunks = [
        "Chunk one text for demo.",
        "Chunk two text for demo.",
        "Chunk three text for demo.",
    ]

    records = build_chunk_records(
        chunks=sample_chunks,
        source="sample_document.txt",
        page_number=1,
    )

    output_path = Path("phase_3_data_file_handling/chunk_records_demo.json")
    save_records(records, output_path)

    print(f"Saved {len(records)} records to: {output_path}")
    if records:
        print("First record:")
        print(asdict(records[0]))

    # TODO:
    # 1. Dung ket qua chunking that tu exercise_3_chunking_strategies.py
    # 2. Gan page_number dung voi du lieu that
    # 3. Them truong metadata neu can (author, category, language)
    

if __name__ == "__main__":
    exercise_3_4()
