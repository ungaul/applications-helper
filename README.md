# Applications Helper

> This project if a WIP.

## Features

- Fetches job postings from URLs (Ollama Cloud)
- CSV-based application tracker
- Customized CV, cover letter, and email per company

## Privacy

- I advise you to set `AI_ENDPOINT` to a local OpenAI-compatible LLM API (e.g. Ollama) to avoid sending data to third parties
- Ollama Cloud only fetches specified pages without storing data (free API key required)

## Installation

1. Install [Docker](https://docs.docker.com/get-docker/)
2. Make a template folder containing your CV and your Cover Letter in .docx format.
3. Download [docker-compose-example.yml](docker-compose-example.yml), and add your OLLAMA_API_KEY and OPENAI_API_KEY.
4. Adjust the file bindings to match your template and output folder (which will contain a subfolder for each company)

## Usage
Open a terminal from the folder containing your file, and
```bash
docker compose up
```

## Contribution

Feel free to contribute!