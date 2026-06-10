from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class JobMatcher:

    def __init__(self):

        print("Loading AI model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Model loaded.")

    def calculate_match(
        self,
        resume_text,
        job_description,
        resume_skills,
        jd_skills
    ):

        # -----------------------------
        # SEMANTIC MATCH
        # -----------------------------

        embeddings = self.model.encode([
            resume_text,
            job_description
        ])

        semantic_score = (
            cosine_similarity(
                [embeddings[0]],
                [embeddings[1]]
            )[0][0]
        ) * 100

        # -----------------------------
        # SKILL MATCH
        # -----------------------------

        resume_set = set(
            skill.lower()
            for skill in resume_skills
        )

        jd_set = set(
            skill.lower()
            for skill in jd_skills
        )

        overlap = len(
            resume_set.intersection(jd_set)
        )

        if len(jd_set) == 0:

            skill_score = 0

        else:

            skill_score = (
                overlap / len(jd_set)
            ) * 100

        # -----------------------------
        # FINAL SCORE
        # -----------------------------

        final_score = (

            semantic_score * 0.6 +

            skill_score * 0.4

        )

        return round(
            final_score,
            2
        )

    def classify_match(self, score):

        if score >= 80:
            return "Strong Apply"

        elif score >= 65:
            return "Apply"

        elif score >= 45:
            return "Stretch"

        else:
            return "Skip"