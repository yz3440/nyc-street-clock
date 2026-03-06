import sqlite3
import json
import os

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "process.db")
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT * FROM panoramas WHERE approved = 1 ORDER BY text ASC")
rows = [dict(row) for row in cursor.fetchall()]
# for row in rows:
#     print(row['text'])
conn.close()

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "approved.json")
with open(output_path, "w") as f:
    json.dump(rows, f, indent=2)

print(f"Exported {len(rows)} approved rows to {output_path}")
