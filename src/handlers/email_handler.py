from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def create_eml_file(output_path: Path, email_body: str, cv_pdf: Path, cl_pdf: Path, subject: str):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = ""
    msg['To'] = ""

    msg.attach(MIMEText(email_body, 'plain', 'utf-8'))

    for pdf_path in [cv_pdf, cl_pdf]:
        with open(pdf_path, 'rb') as f:
            attachment = MIMEApplication(f.read(), _subtype='pdf')
            attachment.add_header('Content-Disposition', 'attachment', filename=pdf_path.name)
            msg.attach(attachment)

    with open(output_path, 'w') as f:
        f.write(msg.as_string())