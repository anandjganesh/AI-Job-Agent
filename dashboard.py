import sqlite3
import pandas as pd


conn = sqlite3.connect("jobs.db")


while True:

    print("\n========== JOB DASHBOARD ==========")

    print("1. Top 20 Jobs")
    print("2. Jobs Above 70%")
    print("3. Jobs By Role")
    print("4. Top Companies")
    print("5. Pending Applications")
    print("6. Mark Applied")
    print("7. Mark Interview")
    print("8. Export Excel")
    print("9. Exit")

    choice = input("\nChoose: ")

    # ----------------------------------
    # TOP JOBS
    # ----------------------------------

    if choice == "1":

        query = """

        SELECT
            id,
            title,
            company,
            role,
            score,
            status

        FROM jobs

        ORDER BY score DESC

        LIMIT 20

        """

        df = pd.read_sql(query, conn)

        print(df)

    # ----------------------------------
    # JOBS ABOVE 70
    # ----------------------------------

    elif choice == "2":

        query = """

        SELECT
            id,
            title,
            company,
            role,
            score,
            status

        FROM jobs

        WHERE score >= 70

        ORDER BY score DESC

        """

        df = pd.read_sql(query, conn)

        print(df)

    # ----------------------------------
    # JOBS BY ROLE
    # ----------------------------------

    elif choice == "3":

        query = """

        SELECT
            role,
            COUNT(*) AS total_jobs,
            ROUND(AVG(score),2) AS avg_score

        FROM jobs

        GROUP BY role

        ORDER BY total_jobs DESC

        """

        df = pd.read_sql(query, conn)

        print(df)

    # ----------------------------------
    # TOP COMPANIES
    # ----------------------------------

    elif choice == "4":

        query = """

        SELECT
            company,
            COUNT(*) AS openings

        FROM jobs

        GROUP BY company

        ORDER BY openings DESC

        LIMIT 20

        """

        df = pd.read_sql(query, conn)

        print(df)

    # ----------------------------------
    # PENDING APPLICATIONS
    # ----------------------------------

    elif choice == "5":

        query = """

        SELECT
            id,
            title,
            company,
            role,
            score,
            status

        FROM jobs

        WHERE status='Pending'

        ORDER BY score DESC

        """

        df = pd.read_sql(query, conn)

        print(df)

    # ----------------------------------
    # MARK APPLIED
    # ----------------------------------

    elif choice == "6":

        job_id = input(
            "\nEnter Job ID: "
        )

        conn.execute("""

        UPDATE jobs

        SET
            status='Applied',
            applied_at=CURRENT_TIMESTAMP

        WHERE id=?

        """, (job_id,))

        conn.commit()

        print(
            "\n✅ Job marked Applied"
        )

    # ----------------------------------
    # MARK INTERVIEW
    # ----------------------------------

    elif choice == "7":

        job_id = input(
            "\nEnter Job ID: "
        )

        conn.execute("""

        UPDATE jobs

        SET
            status='Interview'

        WHERE id=?

        """, (job_id,))

        conn.commit()

        print(
            "\n✅ Job marked Interview"
        )

    # ----------------------------------
    # EXPORT EXCEL
    # ----------------------------------

    elif choice == "8":

        query = """

        SELECT *

        FROM jobs

        ORDER BY score DESC

        """

        df = pd.read_sql(
            query,
            conn
        )

        df.to_excel(
            "jobs_export.xlsx",
            index=False
        )

        print(
            "\n✅ Exported to jobs_export.xlsx"
        )

    # ----------------------------------
    # EXIT
    # ----------------------------------

    elif choice == "9":

        break

    else:

        print(
            "\nInvalid choice."
        )


conn.close()