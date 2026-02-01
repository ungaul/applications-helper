import os
import json
import re
from datetime import datetime
from openai import OpenAI
from docx import Document

def get_ai_client():
    return OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("AI_ENDPOINT", "https://api.openai.com/v1")
    )

def _chat(system: str, user: str, temperature: float = 0) -> str:
    client = get_ai_client()
    response = client.chat.completions.create(
        model=os.getenv("GPT_MODEL", "gpt-4.1-mini"),
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        temperature=temperature
    )
    return response.choices[0].message.content.strip()

def get_company_name(job_posting: str) -> str:
    return _chat("Extract only the company name. Respond with the name only, nothing else.", job_posting)

def get_position_title(job_posting: str) -> str:
    return _chat("Extract only the job position/title. Respond with the title only, nothing else.", job_posting)

def get_job_location(job_posting: str) -> str:
    return _chat(
        "Extract only the job location (city, country or remote). Respond with the location only, nothing else. If not specified, respond with 'Not specified'.",
        job_posting
    )

def detect_language(job_posting: str) -> str:
    return _chat(
        "Detect the language of the text and respond with only the ISO 639-1 language code (e.g., 'fr', 'en', 'de', 'es', 'ja', etc.). Return ONLY the 2-letter code, nothing else.",
        job_posting[:500]
    ).lower()

def get_cover_letter_label(language: str) -> str:
    return _chat(f"Return only the translation of 'Cover Letter' in the language with ISO code '{language}'. Return ONLY the translation, nothing else.", "Cover Letter")

def get_email_subject(language: str) -> str:
    return _chat(f"Return only the translation of 'Application' (job application) in the language with ISO code '{language}'. Return ONLY the translation, nothing else.", "Application")

def get_cv_updates(job_posting: str, language: str) -> dict:
    todays_date = datetime.now().strftime("%Y-%m-%d")
    prompt = f"""Extract CV header updates from this job posting.
JOB POSTING: {job_posting}
TODAY'S DATE: {todays_date}
Return JSON with:
- "job_field": The SECTOR/DOMAIN of the position, NOT the job title. Use 1-2 words maximum. Examples: Financial Analyst → "Finance", Management Controller → "Controlling". Keep it in the SAME LANGUAGE as the job posting (ISO code: {language}).
- "start_date": Start month in the format and language of the job posting. If not specified, use current month+1.
Return ONLY valid JSON."""

    content = _chat("Return only valid JSON. No other text.", prompt)
    content = content.replace('```json', '').replace('```', '').strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON from GPT: {content}")
        return {"job_field": "Finance", "start_date": "February"}

def get_new_cover_letter_paragraphs(job_posting: str, company_name: str, template_path, language: str) -> list:
    doc = Document(template_path)
    original_paragraphs = [p.text for p in doc.paragraphs]
    todays_date = datetime.now().strftime("%Y-%m-%d")

    prompt = f"""Return a JSON array of paragraph texts (strings) for a cover letter, matching the exact structure and number of paragraphs from the example. CRITICAL: Copy the ENTIRE example EXACTLY except for these specific changes: 1) Company address block (company name, department, city - do NOT invent street addresses or building names), 2) Date, 3) Job title in object line and intro paragraph, 4) Paragraph 3 content. EVERYTHING ELSE must be IDENTICAL to the example - same personal info (name, address, phone, email), same experiences, same wording, same closing. DO NOT modify, add, or invent ANY information that is not in the original example. For paragraph 3: Start exactly like the example opening phrase, then list 2-3 technical skills from the EXAMPLE TEMPLATE that are also relevant to this job (do NOT invent new skills - only use skills already mentioned in the example). Then add ONE or TWO short, personal sentences in first person about what YOU genuinely like about this type of work - be specific and authentic. Talk about what interests you personally in the work itself, what you enjoy doing, what problems you like solving - NOT about "contributing", "supporting", "optimizing processes", or other abstract corporate goals. Keep it grounded, direct, and conversational. Max 3-4 sentences total for paragraph 3. Match the example's natural, personal tone exactly - avoid pompous or overly formal corporate language. Keep it authentic and down-to-earth.

IMPORTANT: 
- The cover letter MUST be written in the SAME LANGUAGE as the job posting (ISO code: {language}).
- After the subject line, there MUST be an empty paragraph (empty string "") before the salutation
- The signature at the end should appear ONLY ONCE (just the name, no duplication)
- Preserve the exact number of paragraphs as the original template

JOB POSTING: {job_posting}
COMPANY: {company_name}
TODAY'S DATE: {todays_date}
ORIGINAL PARAGRAPHS:
{chr(10).join(f'{i}: "{p}"' for i, p in enumerate(original_paragraphs))}

Return a JSON array with EXACTLY {len(original_paragraphs)} elements, preserving empty strings where the original has them."""

    content = _chat("Return only a valid JSON array of strings. No other text.", prompt, temperature=0.5)
    content = content.replace('```json', '').replace('```', '').strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        content = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', content)
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            print("Failed to parse. Returning original paragraphs.")
            return original_paragraphs


def generate_email_body(company_name: str, position_title: str, language: str, template_path) -> str:
    doc = Document(template_path)
    candidate_name = doc.paragraphs[0].text.strip()

    phone_number = ""
    for para in doc.paragraphs[:5]:
        phone_match = re.search(r'\+?\d[\d\s\-\(\)]{8,}', para.text)
        if phone_match:
            phone_number = phone_match.group(0)
            break

    prompt = f"""Generate a professional, natural email body for a job application.
COMPANY: {company_name}
POSITION: {position_title}
LANGUAGE: ISO code {language}

The email should be short (3-4 sentences), natural, mention the position and attachments.
End with just the closing phrase. Return ONLY the email body text."""

    email_body = _chat("Generate a natural, personalized email body. Return only the email text.", prompt, temperature=0.5)
    signature = f"\n\n{candidate_name}"
    if phone_number:
        signature += f"\n{phone_number}"

    return email_body + signature

def find_and_replace_fields(text: str, updates: dict) -> str:
    if not text.strip():
        return text
    
    prompt = f"""Text: "{text}"

TASK: If this text contains a business domain word (Finance, Marketing, Audit, Risk, Controlling, Commerce, Management, Data, etc.), REPLACE that word with "{updates.get('job_field', '')}".
If this text contains a month name (in any language), REPLACE that month with "{updates.get('start_date', '')}".

CRITICAL RULES:
- REPLACE means substitute, NOT append or concatenate
- Keep all other text exactly the same
- If no replacement needed, return the original text unchanged
- Return ONLY the final text, no explanations"""

    return _chat("Return only the modified text, nothing else.", prompt)