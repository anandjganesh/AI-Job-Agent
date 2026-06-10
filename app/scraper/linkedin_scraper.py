from playwright.sync_api import sync_playwright
import time
import re


class LinkedInScraper:

    def __init__(self):

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=False
        )

        self.page = self.browser.new_page()

    def search_jobs(
        self,
        keyword="Data Analyst",
        location="India"
    ):

        url = (
            f"https://www.linkedin.com/jobs/search/"
            f"?keywords={keyword}"
            f"&location={location}"
        )

        print("\nOpening LinkedIn Jobs...")
        print(url)

        self.page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
            )

        time.sleep(8)

        print("Page loaded")

        jobs = self.page.query_selector_all(
            ".base-search-card"
        )

        print(f"Found {len(jobs)} job cards")

        results = []

        for job in jobs:

            try:

                # -----------------------
                # TITLE
                # -----------------------

                title_element = job.query_selector(
                    "h3"
                )

                title = (
                    title_element.inner_text().strip()
                    if title_element
                    else "No Title"
                )

                # -----------------------
                # COMPANY
                # -----------------------

                company_element = job.query_selector(
                    "h4"
                )

                company = (
                    company_element.inner_text().strip()
                    if company_element
                    else "No Company"
                )

                # -----------------------
                # LOCATION
                # -----------------------

                location_element = job.query_selector(
                    ".job-search-card__location"
                )

                job_location = (
                    location_element.inner_text().strip()
                    if location_element
                    else "No Location"
                )

                # -----------------------
                # URL
                # -----------------------

                link_element = job.query_selector(
                    "a.base-card__full-link"
                )

                job_url = (
                    link_element.get_attribute(
                        "href"
                    )
                    if link_element
                    else None
                )

                # -----------------------
                # POSTED TIME
                # -----------------------

                posted_time = ""

                try:

                    time_element = job.query_selector(
                        "time"
                    )

                    if time_element:

                        posted_time = (
                            time_element.inner_text()
                            .strip()
                            .lower()
                        )

                except:
                    pass

                # -----------------------
                # APPLICANTS
                # -----------------------

                applicants = None

                try:

                    full_text = (
                        job.inner_text()
                    )

                    match = re.search(
                        r"(\d+)\+?\s+applicants",
                        full_text,
                        re.IGNORECASE
                    )

                    if match:

                        applicants = int(
                            match.group(1)
                        )

                except:
                    pass

                # -----------------------
                # FILTER:
                # LAST 24 HOURS
                # -----------------------

                is_recent = False

                if posted_time:

                    recent_keywords = [

                        "hour",
                        "hours",

                        "1 day",

                        "today",

                        "just now",

                        "minute",
                        "minutes"

                    ]

                    if any(
                        x in posted_time
                        for x in recent_keywords
                    ):
                        is_recent = True

                # -----------------------
                # FILTER:
                # APPLICANTS <= 200
                # -----------------------

                applicant_ok = True

                if applicants is not None:

                    applicant_ok = (
                        applicants <= 200
                    )

                # -----------------------
                # SAVE IF PASSED
                # -----------------------

                if is_recent and applicant_ok:

                    results.append({

                        "title": title,

                        "company": company,

                        "location": job_location,

                        "url": job_url,

                        "posted_time": posted_time,

                        "applicants": applicants

                    })

            except Exception as e:

                print(
                    f"Error extracting job: {e}"
                )

        print(
            f"\nJobs after filtering: "
            f"{len(results)}"
        )

        print("\n====================")

        for job in results:

            print(
                f"\nTitle: {job['title']}"
            )

            print(
                f"Company: {job['company']}"
            )

            print(
                f"Location: {job['location']}"
            )

            print(
                f"Posted: {job['posted_time']}"
            )

            print(
                f"Applicants: {job['applicants']}"
            )

            print(
                f"URL: {job['url']}"
            )

        return results

    def close(self):

        self.browser.close()

        self.playwright.stop()