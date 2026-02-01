import os
import subprocess
from pathlib import Path
import ollama


def get_unique_filename(base_path: Path) -> Path:
    if not base_path.exists():
        return base_path
    counter = 2
    while True:
        new_path = base_path.parent / f"{base_path.stem}-{counter}{base_path.suffix}"
        if not new_path.exists():
            return new_path
        counter += 1


def fetch_job_posting_from_url(url: str) -> str:
    client = ollama.Client()
    client._client.headers['Authorization'] = f'Bearer {os.getenv("OLLAMA_API_KEY")}'
    result = client.web_fetch(url=url)
    return result.content


def convert_to_pdf(docx_path: Path, pdf_path: Path):
    try:
        subprocess.run(['pkill', '-f', 'soffice'], capture_output=True)
        subprocess.run([
            'libreoffice', '--headless', '--convert-to', 'pdf',
            '--outdir', str(pdf_path.parent), str(docx_path)
        ], check=True, capture_output=True, timeout=120)
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"Warning: PDF conversion failed: {e}")