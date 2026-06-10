import fitz
import re


class ResumeParser:

    def __init__(self, filepath):

        self.filepath = filepath

    # -----------------------------------
    # EXTRACT PDF TEXT
    # -----------------------------------

    def extract_text(self):

        doc = fitz.open(self.filepath)

        text = ""

        for page in doc:

            text += page.get_text()

        return text

    # -----------------------------------
    # EXTRACT SKILLS
    # -----------------------------------

    def extract_skills(self, text):

        skills_database = [

            # Programming
            "python",
            "sql",
            "r",

            # Data Tools
            "power bi",
            "tableau",
            "excel",
            "pandas",
            "numpy",

            # Databases
            "mysql",
            "postgresql",
            "mongodb",

            # Analytics
            "data analysis",
            "machine learning",
            "statistics",
            "data visualization",
            "dashboard",
            "etl",

            # Cloud
            "aws",
            "azure",

            # AI
            "nlp",
            "llm",
            "chatgpt",

            # Other
            "git",
            "api"
        ]

        text = text.lower()

        found_skills = []

        for skill in skills_database:

            if re.search(r"\b" + re.escape(skill) + r"\b", text):

                found_skills.append(skill)

        return list(set(found_skills))