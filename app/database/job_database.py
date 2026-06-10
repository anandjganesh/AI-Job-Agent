import sqlite3


class JobDatabase:

    def __init__(self, db_name="jobs.db"):

        self.conn = sqlite3.connect(
            db_name,
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()

        self.create_table()

    def create_table(self):

        self.cursor.execute("""

            CREATE TABLE IF NOT EXISTS jobs (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                role TEXT,

                title TEXT,

                company TEXT,

                location TEXT,

                score REAL,

                recommendation TEXT,

                status TEXT DEFAULT 'Pending',

                applied_at TIMESTAMP,

                notes TEXT,

                url TEXT UNIQUE,

                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )



        """)

        self.conn.commit()

    def insert_job(self, job):

        try:

            self.cursor.execute("""

            INSERT OR IGNORE INTO jobs (

                role,
                title,
                company,
                location,
                score,
                recommendation,
                url

            )

            VALUES (?, ?, ?, ?, ?, ?, ?)

            """, (

                job.get("role", ""),
                job.get("title", ""),
                job.get("company", ""),
                job.get("location", ""),
                float(job.get("score", 0)),
                job.get("recommendation", ""),
                job.get("url", "")

            ))

            self.conn.commit()

        except Exception as e:

            print(
                f"Database Insert Error: {e}"
            )

    def get_all_jobs(self):

        self.cursor.execute("""

        SELECT
            role,
            title,
            company,
            location,
            score,
            recommendation,
            url,
            scraped_at

        FROM jobs

        ORDER BY score DESC

        """)

        return self.cursor.fetchall()

    def get_top_jobs(self, limit=20):

        self.cursor.execute("""

        SELECT
            role,
            title,
            company,
            location,
            score,
            recommendation,
            url

        FROM jobs

        ORDER BY score DESC

        LIMIT ?

        """, (limit,))

        return self.cursor.fetchall()

    def close(self):

        self.conn.commit()

        self.conn.close()