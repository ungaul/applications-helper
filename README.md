# Applications Helper

> This project if a WIP. Please check the results and send an issue ticket if you have any issue/feature request.

## Features

- Fetches job postings from URLs (Ollama Cloud)
- CSV-based application tracker
- Customized CV, cover letter, and email per company
- API/Scrappers (thanks to [Zeffut](https://github.com/Zeffut/JobScraper)'s work)

## Privacy

- I advise you to set `AI_ENDPOINT` to a local OpenAI-compatible LLM API (e.g. Ollama) to avoid sending data to third parties
- Ollama Cloud, Adzuna and scrapers only fetches specified pages without storing data (free API key required).

## Installation

1. Install [Docker](https://docs.docker.com/get-docker/)
2. Make a template folder containing your CV and your Cover Letter in .docx format
3. Download [docker-compose-example.yml](docker-compose-example.yml), add your CV heading text in `CV_HEADER_TEMPLATE` and add your `OLLAMA_API_KEY` and `OPENAI_API_KEY` (Adzuna credentials are optional). Fill `CV_HEADER_TEMPLATE` as written in your template for the script to find it and make it match with each offer.
4. Adjust the file bindings to match your template & output folder (which will contain a subfolder for each company)
5. Create the tracker file (`list.csv` in the same folder, or wherever you bind it) before starting the container

## Usage
Open a terminal from the folder containing your file, and
```bash
docker compose run --rm app
```
The program will prompt you if you want it to add job postings in the tracker.

> Please avoid using a VPN while using the app as scrapers may be blocked while fetching job postings.

## Contribution

Feel free to contribute!