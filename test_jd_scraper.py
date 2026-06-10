from app.scraper.job_description_scraper import (
    JobDescriptionScraper
)


url = input("Paste LinkedIn Job URL:\n")


scraper = JobDescriptionScraper()

description = scraper.get_job_description(
    url
)

print("\n=========== JOB DESCRIPTION ===========\n")

print(description)