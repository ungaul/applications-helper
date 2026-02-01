import os
import csv
from pathlib import Path

CSV_FIELDNAMES = ['url', 'status', 'company', 'position', 'location', 'language', 'date_processed', 'notes']


def get_tracker_file():
    return Path(os.getenv("TRACKER_FILE", "list.csv"))


def read_csv_entries() -> list[dict]:
    tracker = get_tracker_file()
    if not tracker.exists():
        with open(tracker, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
            writer.writeheader()
        return []
    with open(tracker, 'r', newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def write_csv_entries(entries: list[dict]):
    cleaned_entries = []
    for entry in entries:
        cleaned = {k: v for k, v in entry.items() if k and k in CSV_FIELDNAMES}
        for field in CSV_FIELDNAMES:
            if field not in cleaned:
                cleaned[field] = ''
        cleaned_entries.append(cleaned)

    with open(get_tracker_file(), 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        writer.writerows(cleaned_entries)


def update_csv_entry(url: str, updates: dict):
    entries = read_csv_entries()
    for entry in entries:
        if entry['url'] == url:
            entry.update(updates)
            break
    write_csv_entries(entries)

def add_csv_entry(url: str):
    entries = read_csv_entries()
    entries.append({'url': url})
    write_csv_entries(entries)