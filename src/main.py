from datetime import datetime

from handlers.csv_handler import read_csv_entries, update_csv_entry
from handlers.file_utils import fetch_job_posting_from_url
from job_processor import process_job_posting


def main():
    entries = read_csv_entries()
    pending = [e for e in entries
               if (e.get('status') or '').lower() != 'done'
               and (e.get('url') or '').strip()]

    if pending:
        print(f"Found {len(pending)} pending URL(s)\n")

        for i, entry in enumerate(pending, 1):
            url = (entry.get('url') or '').strip()
            if not url:
                continue

            print(f"[{i}/{len(pending)}] Fetching: {url}")
            job_posting = fetch_job_posting_from_url(url)

            if job_posting:
                metadata = process_job_posting(job_posting, url)
                if metadata:
                    update_csv_entry(url, metadata)
            else:
                print(f"Skipped: Failed to fetch {url}\n")
                update_csv_entry(url, {'status': 'fetch_failed', 'date_processed': datetime.now().strftime("%Y-%m-%d %H:%M")})
    else:
        print("No pending URLs in list.csv")

    search = input("\nSearch for jobs? [y/N]: ").strip().lower()
    if search == 'y':
        from search import main as search_main
        search_main()


if __name__ == "__main__":
    main()