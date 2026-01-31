# Applications Helper

> This project if a WIP, please wait for these major fixes to be done:
- Add support for Windows.
- Improve logging and error handling.
- AIO app/webUI?

## Features
- Web fetch (ollama Cloud)
- CSV applications tracker
- Automatically generate CV, Cover Letters, and email for applications in a separate folder for each company.

## Privacy

- I advise you to set `AI_ENDPOINT` to a local LLM url (such as Ollama), because you probably don't want to send all your details to OpenAI.
- Ollama cloud requires a FREE API key but only fetches specified pages without storing extra data.

## Installation (only Linux supported for now)
1. Install [LibreOffice](https://www.libreoffice.org/get-help/install-howto/) and [Python](https://www.python.org/downloads/).
2. Clone this repository
   ```bash
   git clone https://github.com/ungaul/applications-helper && cd applications-helper
   ```
3. Create/activate Python virtual environment, and install requirements
   ```bash
   python -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```
4. Configure `.env`
   ```bash
   OLLAMA_API_KEY=PASTEYOURKEYHERE
   OPENAI_API_KEY=PASTEYOURKEYHERE
   AI_ENDPOINT=https://openrouter.ai/api/v1
   GPT_MODEL=gpt-4.1-mini

   TEMPLATE_CV="$HOME/Documents/Internships/Template/$USER CV.docx"
   TEMPLATE_COVER_LETTER_EXAMPLE="$HOME/Documents/Internships/Template/$USER Cover Letter.docx"
   OUTPUT_BASE_DIR="$HOME/Documents/Internships"
   TRACKER_FILE=list.csv

   COVER_LETTER_PROMPT=Return a JSON array of paragraph texts (strings) for a cover letter, matching the exact structure and number of paragraphs from the example. CRITICAL: Copy the ENTIRE example EXACTLY except for these specific changes: 1) Company address block (company name, department, city - do NOT invent street addresses or building names), 2) Date, 3) Job title in object line and intro paragraph, 4) Paragraph 3 content. EVERYTHING ELSE must be IDENTICAL to the example - same personal info (name, address, phone, email), same experiences, same wording, same closing. DO NOT modify, add, or invent ANY information that is not in the original example. For paragraph 3: Start exactly like the example opening phrase, then list 2-3 technical skills from the EXAMPLE TEMPLATE that are also relevant to this job (do NOT invent new skills - only use skills already mentioned in the example). Then add ONE or TWO short, personal sentences in first person about what YOU genuinely like about this type of work - be specific and authentic. Talk about what interests you personally in the work itself, what you enjoy doing, what problems you like solving - NOT about "contributing", "supporting", "optimizing processes", or other abstract corporate goals. Keep it grounded, direct, and conversational. Max 3-4 sentences total for paragraph 3. Match the example's natural, personal tone exactly - avoid pompous or overly formal corporate language. This is for an internship, keep it authentic and down-to-earth.
   ```

## Usage
Add job posting URLs to `list.csv` under `url`, then
```bash
python main.py
```

## Contribution
Feel free to contribute to this repository!