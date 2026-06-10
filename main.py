from app.parser.resume_parser import ResumeParser
from app.scraper.linkedin_scraper import LinkedInScraper
from app.scraper.job_description_scraper import JobDescriptionScraper
from app.matcher.job_matcher import JobMatcher
from app.database.job_database import JobDatabase
import pandas as pd
import time


ROLE_RESUME_MAP = {

    "Data Analyst":
        "resumes/Anand Data Analyst Resume.pdf",

    "Business Analyst":
        "resumes/Anand Data Analyst Resume.pdf",

    "Data Scientist":
        "resumes/Anand Data Scientist Resume.pdf",

    "Machine Learning Engineer":
        "resumes/Anand Data Scientist Resume.pdf",

    "R Developer":
        "resumes/Anand Data Scientist Resume.pdf"
}


def main():

    print("\n========== AI JOB AGENT ==========\n")

    # -----------------------------------
    # LOAD ONCE
    # -----------------------------------

    print("Loading AI Matcher...\n")
    matcher = JobMatcher()

    print("Starting Browsers...\n")
    scraper = LinkedInScraper()
    jd_scraper = JobDescriptionScraper()
    # SQLite Database
    db = JobDatabase()
    all_matched_jobs = []

    # -----------------------------------
    # LOOP THROUGH ROLES
    # -----------------------------------

    for role, resume_path in ROLE_RESUME_MAP.items():

        print("\n====================================")
        print(f"ROLE: {role}")
        print("====================================\n")

        # -----------------------------------
        # PARSE RESUME
        # -----------------------------------

        print("Parsing Resume...\n")

        parser = ResumeParser(resume_path)

        resume_text = parser.extract_text()

        resume_skills = parser.extract_skills(
            resume_text
        )

        print("Skills Found:\n")
        print(resume_skills)

        combined_resume = f"""
        Skills:
        {' '.join(resume_skills)}

        Resume:
        {resume_text}
        """

        # -----------------------------------
        # SCRAPE JOBS
        # -----------------------------------

        print(
            f"\nSearching LinkedIn Jobs for {role}...\n"
        )

        jobs = scraper.search_jobs(
            keyword=role,
            location="India"
        )

        if not jobs:

            print(f"No jobs found for {role}")
            continue

        print(
            f"\nTotal Jobs Found: {len(jobs)}"
        )

        matched_jobs = []

        # -----------------------------------
        # MATCH JOBS
        # -----------------------------------

        for index, job in enumerate(jobs[:100]):

            try:

                print("\n-----------------------------------")

                print(
                    f"Job {index + 1}"
                )

                print(
                    f"Title   : {job['title']}"
                )

                print(
                    f"Company : {job['company']}"
                )

                # -----------------------------------
                # VALID URL CHECK
                # -----------------------------------

                if not job["url"]:

                    print("Invalid URL")
                    continue

                if "linkedin.com" not in job["url"]:

                    print("Skipping invalid URL")
                    continue

                # -----------------------------------
                # GET JOB DESCRIPTION
                # -----------------------------------

                description = (
                    jd_scraper.get_job_description(
                        job["url"]
                    )
                )

                if not description:

                    print(
                        "No description found."
                    )

                    continue

                # -----------------------------------
                # AI MATCH
                # -----------------------------------

                # -----------------------------------
                # EXTRACT JD SKILLS
                # -----------------------------------

                jd_skills = parser.extract_skills(
                    description
                    )

                print("\nJD Skills:")
                print(jd_skills)

                # -----------------------------------
                # AI MATCH
                # -----------------------------------

                score = matcher.calculate_match(
                    combined_resume,
                    description,
                    resume_skills,
                    jd_skills
                )

                recommendation = (
                    matcher.classify_match(
                        score
                    )
                )

                print(
                    f"Match Score: {score}%"
                )

                print(
                    f"Recommendation: {recommendation}"
                )

                # -----------------------------------
                # SAVE MATCHES
                # -----------------------------------

                if score >= 35:

                    job_data = {

                        "role": role,
                        "title": job["title"],
                        "company": job["company"],
                        "location": job["location"],
                        "score": score,
                        "recommendation": recommendation,
                        "url": job["url"]

                    }

                    matched_jobs.append(job_data)

                    db.insert_job({
                    "role": role,
                    "title": job["title"],
                    "company": job["company"],
                    "location": job["location"],
                    "score": score,
                    "recommendation": recommendation,
                    "url": job["url"]
                    })

                time.sleep(1)

            except Exception as e:

                print(
                    f"Error processing job: {e}"
                )

        all_matched_jobs.extend(
            matched_jobs
        )

    # -----------------------------------
    # SORT RESULTS
    # -----------------------------------

    all_matched_jobs = sorted(

        all_matched_jobs,

        key=lambda x: x["score"],

        reverse=True
    )

    # -----------------------------------
    # REMOVE DUPLICATES
    # -----------------------------------

    unique_jobs = []

    seen_urls = set()

    for job in all_matched_jobs:

        if job["url"] not in seen_urls:

            unique_jobs.append(job)

            seen_urls.add(
                job["url"]
            )

    all_matched_jobs = unique_jobs

    # -----------------------------------
    # SAVE CSV
    # -----------------------------------

    if all_matched_jobs:

        df = pd.DataFrame(
            all_matched_jobs
        )

        df.to_csv(
            "matched_jobs.csv",
            index=False
        )

        print(
            "\nResults saved to matched_jobs.csv"
        )

    # -----------------------------------
    # CLOSE BROWSERS
    # -----------------------------------

    scraper.close()
    jd_scraper.close()
    db.close()
    # -----------------------------------
    # FINAL RESULTS
    # -----------------------------------

    print(
        "\n========== FINAL MATCHED JOBS ==========\n"
    )

    if not all_matched_jobs:

        print(
            "No matching jobs found."
        )

    else:

        for job in all_matched_jobs[:30]:

            print(
                f"Role           : {job['role']}"
            )

            print(
                f"Title          : {job['title']}"
            )

            print(
                f"Company        : {job['company']}"
            )

            print(
                f"Match Score    : {job['score']}%"
            )

            print(
                f"Recommendation : {job['recommendation']}"
            )

            print(
                f"URL            : {job['url']}"
            )

            print(
                "\n-----------------------------------\n"
            )


if __name__ == "__main__":

    main()