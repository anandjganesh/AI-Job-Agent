import sqlite3

conn = sqlite3.connect("jobs.db")

cursor = conn.cursor()

cursor.execute(
    "SELECT COUNT(*) FROM jobs"
)

count = cursor.fetchone()[0]

print(f"Total Jobs: {count}")

cursor.execute("""
SELECT title,
       company,
       score
FROM jobs
ORDER BY score DESC
LIMIT 10
""")

rows = cursor.fetchall()

print("\nTop Jobs:\n")

for row in rows:

    print(row)

conn.close()