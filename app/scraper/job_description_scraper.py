import requests
from bs4 import BeautifulSoup


class JobDescriptionScraper:

    def __init__(self):
        pass

    def get_job_description(self, url):

        try:

            if not url or url == "No URL":
                return ""

            print("Fetching job description...")

            headers = {
                "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }

            response = requests.get(
                url,
                headers=headers,
                timeout=15
            )

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            selectors = [

                ".show-more-less-html__markup",

                ".jobs-description-content__text",

                ".description",

                ".jobs-box__html-content"

            ]

            for selector in selectors:

                element = soup.select_one(
                    selector
                )

                if element:

                    return element.get_text(
                        separator=" ",
                        strip=True
                    )

            return soup.get_text(
                separator=" ",
                strip=True
            )[:5000]

        except Exception as e:

            print(
                f"JD Scraper Error: {e}"
            )

            return ""

    def close(self):
        pass