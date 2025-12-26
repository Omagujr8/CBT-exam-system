"""
Add `access_token` column to exams table if missing.
Run: python backend/scripts/add_exam_token_column.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'school_cbt.db')
DB_PATH = os.path.normpath(DB_PATH)

if not os.path.exists(DB_PATH):
    print(f"Database not found at {DB_PATH}. Please confirm path and run from repo root.")
    raise SystemExit(1)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Check if column exists
cur.execute("PRAGMA table_info(exams);")
cols = [r[1] for r in cur.fetchall()]
if 'access_token' in cols:
    print("Column 'access_token' already exists on exams table. Nothing to do.")
else:
    print("Adding 'access_token' column to exams table...")
    try:
        cur.execute("ALTER TABLE exams ADD COLUMN access_token TEXT;")
        conn.commit()
        print("Column added successfully.")
    except Exception as e:
        print("Failed to add column:", e)
        raise

conn.close()