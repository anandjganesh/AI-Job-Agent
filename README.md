# AI Job Agent

An AI-powered job discovery and matching platform that automatically finds relevant jobs, analyzes job descriptions, and ranks opportunities based on resume-job fit using semantic search and skill matching.

## Features

* Resume Parsing
* LinkedIn Job Scraping
* Job Description Extraction
* Semantic Matching using Sentence Transformers
* Skill Gap Analysis
* Job Recommendation Scoring
* SQLite Database Storage
* Interactive Streamlit Dashboard

## Architecture

Resume → Skill Extraction → LinkedIn Job Search → Job Description Scraping → Semantic Matching → Score Calculation → SQLite Database → Streamlit Dashboard

## Tech Stack

* Python
* Streamlit
* Playwright
* Sentence Transformers
* Scikit-learn
* SQLite
* Pandas

## How It Works

1. Parse resume and extract skills.
2. Search LinkedIn for relevant jobs.
3. Scrape job descriptions.
4. Generate semantic embeddings using Sentence Transformers.
5. Calculate similarity scores using cosine similarity.
6. Combine semantic relevance and skill overlap into a final match score.
7. Store results in SQLite and display them in a Streamlit dashboard.

## Project Structure

```text
app/
├── database/
├── matcher/
├── parser/
└── scraper/

main.py
requirements.txt
```

## Future Improvements

* Resume tailoring suggestions
* ATS keyword recommendations
* Job application tracking
* Automated email alerts
* Cover letter generation

## Author

Anand J Ganesh
