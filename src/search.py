import os

from handlers.csv_handler import read_csv_entries, add_csv_entry

SCRAPERS = {
    "1": ("adzuna", "Adzuna (API, requires ADZUNA_APP_ID/KEY)"),
    "2": ("francetravail", "France Travail"),
    "3": ("hellowork", "HelloWork"),
    "4": ("linkedin", "LinkedIn"),
    "5": ("wttj", "Welcome to the Jungle"),
}


def search_with_scraper(scraper_name, keywords, location, radius_km):
    max_results = int(os.getenv("JOB_SEARCHES", "5"))

    if scraper_name == "adzuna":
        country = input("Country code [fr]: ").strip() or "fr"
        from scrapers.adzuna import AdzunaScraper, SearchCriteria
        scraper = AdzunaScraper()
        criteria = SearchCriteria(keywords=keywords, location=location, country=country, radius_km=radius_km, max_results=max_results)
    elif scraper_name == "francetravail":
        from scrapers.francetravail import FranceTravailScraper, SearchCriteria
        scraper = FranceTravailScraper()
        criteria = SearchCriteria(keywords=keywords, location=location, radius_km=radius_km, max_results=max_results)
    elif scraper_name == "hellowork":
        from scrapers.hellowork import HelloWorkScraper, SearchCriteria
        scraper = HelloWorkScraper()
        criteria = SearchCriteria(keywords=keywords, location=location, radius_km=radius_km, max_results=max_results)
    elif scraper_name == "linkedin":
        contract = input("Contract type (cdi/cdd/stage/alternance, optional): ").strip()
        workplace = input("Workplace (remote/on_site/hybrid, optional): ").strip()
        from scrapers.linkedin import LinkedInScraper, SearchCriteria
        scraper = LinkedInScraper()
        criteria = SearchCriteria(
            keywords=keywords, location=location, radius_km=radius_km,
            contract_types=[contract] if contract else [],
            workplace_types=[workplace] if workplace else [],
            max_results=max_results
        )
    elif scraper_name == "wttj":
        contract = input("Contract type (cdi/cdd/stage/alternance, optional): ").strip()
        workplace = input("Workplace (remote/on_site, optional): ").strip()
        from scrapers.wttj import WTTJScraper, SearchCriteria
        scraper = WTTJScraper()
        criteria = SearchCriteria(
            keywords=keywords, location=location,
            contract_types=[contract] if contract else [],
            workplace_types=[workplace] if workplace else [],
            max_results=max_results
        )
    else:
        return

    return scraper.search(criteria)


def prompt_job_search():
    print("\n--- Job Search ---")
    print("Available sources:")
    for key, (_, desc) in SCRAPERS.items():
        print(f"  {key}. {desc}")
    
    choice = input("Choose source [1-5]: ").strip()
    if choice not in SCRAPERS:
        print("Invalid choice")
        return 0

    scraper_name = SCRAPERS[choice][0]
    
    if scraper_name == "adzuna" and (not os.getenv("ADZUNA_APP_ID") or not os.getenv("ADZUNA_APP_KEY")):
        print("Adzuna credentials not configured")
        return 0

    job_title = input("Job title/type: ").strip()
    if not job_title:
        return 0
    
    location = input("Location [France]: ").strip() or "France"
    radius = input("Radius in km (optional): ").strip()
    radius_km = int(radius) if radius.isdigit() else None
    keywords = [k.strip() for k in job_title.split(",")]

    print("Searching...\n")

    try:
        jobs = search_with_scraper(scraper_name, keywords, location, radius_km)
        existing_urls = {e.get('url') for e in read_csv_entries()}
        added = 0

        for job in jobs:
            if job.url in existing_urls:
                continue
            
            print(f"  {job.title} @ {job.company} ({job.location})")
            add = input("  Add? [Y/n]: ").strip().lower()
            if add != 'n':
                add_csv_entry(job.url)
                existing_urls.add(job.url)
                added += 1

        print(f"\nAdded {added} job(s)")
        return added
    except Exception as e:
        print(f"Search failed: {e}")
        return 0


def main():
    while True:
        prompt_job_search()
        more = input("\nSearch more? [y/N]: ").strip().lower()
        if more != 'y':
            break


if __name__ == "__main__":
    main()