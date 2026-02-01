import shutil
from pathlib import Path
from docx import Document

from handlers.ai_handler import find_and_replace_fields


def modify_cv_header(cv_path: Path, output_path: Path, updates: dict):
    shutil.copy(cv_path, output_path)
    doc = Document(output_path)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    for run in para.runs:
                        if run.text.strip():
                            run.text = find_and_replace_fields(run.text, updates)

    doc.save(output_path)


def modify_cover_letter(template_path: Path, output_path: Path, new_paragraphs: list):
    shutil.copy(template_path, output_path)
    doc = Document(output_path)

    for i, para in enumerate(doc.paragraphs):
        if i < len(new_paragraphs):
            for run in para.runs[1:]:
                run.text = ""
            if para.runs:
                para.runs[0].text = new_paragraphs[i]
            else:
                para.text = new_paragraphs[i]

    doc.save(output_path)