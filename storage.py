"""CSV and JSON persistence helpers."""
import csv
import json
from pathlib import Path

FIELDS = ["id", "date", "text", "sentiment", "score", "confidence"]

def ensure_data_files(csv_path: Path, json_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    if not csv_path.exists():
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
    if not json_path.exists():
        json_path.write_text("[]", encoding="utf-8")

def load_reviews(csv_path: Path) -> list:
    try:
        if not csv_path.exists():
            return []
        with csv_path.open("r", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except (OSError, csv.Error, UnicodeDecodeError):
        return []

def save_review(record: dict, csv_path: Path, json_path: Path) -> None:
    ensure_data_files(csv_path, json_path)
    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow({key: record.get(key, "") for key in FIELDS})
    current = []
    try:
        current = json.loads(json_path.read_text(encoding="utf-8"))
        if not isinstance(current, list):
            current = []
    except (OSError, json.JSONDecodeError):
        current = []
    current.append(record)
    json_path.write_text(json.dumps(current, indent=2, ensure_ascii=False), encoding="utf-8")

def export_json(records: list, json_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
