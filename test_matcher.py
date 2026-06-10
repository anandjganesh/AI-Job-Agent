from app.matcher.job_matcher import JobMatcher


resume_text = """
Python SQL Power BI Tableau
Machine Learning Data Analysis
PostgreSQL Excel Analytics
"""


job_description = """
We are looking for a Data Analyst
with SQL, Python, dashboards,
Power BI, analytics experience.
"""


matcher = JobMatcher()

score = matcher.calculate_match(
    resume_text,
    job_description
)

classification = matcher.classify_match(
    score
)

print("\n=========== RESULT ===========\n")

print(f"Match Score: {score}%")

print(f"Recommendation: {classification}")