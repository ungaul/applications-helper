import os
from datetime import datetime
from pathlib import Path
from docx import Document

from handlers.ai_handler import (
    detect_language, get_cover_letter_label, get_company_name,
    get_position_title, get_job_location, get_cv_updates,
    get_new_cover_letter_paragraphs, generate_email_body, get_email_subject
)
from handlers.document_handler import modify_cv_header, modify_cover_letter
from handlers.email_handler import create_eml_file
from handlers.file_utils import get_unique_filename, convert_to_pdf


def process_job_posting(job_posting: str, url: str = None) -> dict:
    template_cv = Path(os.getenv("TEMPLATE_CV", "Template/CV.docx"))
    template_cl = Path(os.getenv("TEMPLATE_COVER_LETTER", "Template/Cover Letter.docx"))
    output_base = Path(os.getenv("OUTPUT_BASE_DIR", "."))

    if not template_cl.exists():
        print("Error: Template cover letter not found")
        return {}

    doc = Document(template_cl)
    candidate_name = doc.paragraphs[0].text.strip()

    language = detect_language(job_posting)
    cover_letter_label = get_cover_letter_label(language)

    company_name = get_company_name(job_posting)
    position_title = get_position_title(job_posting)
    job_location = get_job_location(job_posting)

    print(f"Company: {company_name}, Position: {position_title}, Location: {job_location}, Language: {language}")

    company_dir = output_base / company_name
    company_dir.mkdir(exist_ok=True, parents=True)

    print("Getting CV updates...")
    cv_updates = get_cv_updates(job_posting, language)

    print("Generating cover letter...")
    new_paragraphs = get_new_cover_letter_paragraphs(job_posting, company_name, template_cl, language)

    output_cl_docx = get_unique_filename(company_dir / f"{candidate_name} {cover_letter_label}.docx")
    modify_cover_letter(template_cl, output_cl_docx, new_paragraphs)

    output_cl_pdf = output_cl_docx.with_suffix('.pdf')
    convert_to_pdf(output_cl_docx, output_cl_pdf)

    if template_cv.exists():
        output_cv_docx = get_unique_filename(company_dir / f"{candidate_name} CV.docx")
        modify_cv_header(template_cv, output_cv_docx, cv_updates)

        output_cv_pdf = output_cv_docx.with_suffix('.pdf')
        convert_to_pdf(output_cv_docx, output_cv_pdf)

        print("Generating email...")
        email_body = generate_email_body(company_name, position_title, language, template_cl)
        email_subject = get_email_subject(position_title, cv_updates.get("job_field", ""), candidate_name, language)
        output_eml = get_unique_filename(company_dir / f"{candidate_name} Email.eml")
        create_eml_file(output_eml, email_body, output_cv_pdf, output_cl_pdf, email_subject)

        print(f"Files: {output_cl_docx.name}, {output_cl_pdf.name}, {output_cv_docx.name}, {output_cv_pdf.name}, {output_eml.name}\n")
    else:
        print(f"Files: {output_cl_docx.name}, {output_cl_pdf.name}\n")

    return {
        'company': company_name,
        'position': position_title,
        'location': job_location,
        'language': language,
        'date_processed': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'status': 'done'
    }