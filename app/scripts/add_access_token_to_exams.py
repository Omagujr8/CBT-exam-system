from sqlalchemy import text
from ..core.db import SessionLocal

def add_access_token_column():
    db = SessionLocal()
    try:
        # Check if the column already exists
        result = db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='exams'"
        ).fetchone()
        
        if result:
            # Check if the column already exists
            result = db.execute(
                "PRAGMA table_info(exams)"
            ).fetchall()
            
            column_names = [row[1] for row in result]
            if 'access_token' not in column_names:
                # Add the new column
                db.execute(
                    text("ALTER TABLE exams ADD COLUMN access_token TEXT UNIQUE")
                )
                db.commit()
                print("Successfully added access_token column to exams table")
                
                # Generate tokens for existing exams
                db.execute(
                    text("""
                    UPDATE exams 
                    SET access_token = 'exam_' || id || '_' || substr(
                        lower(hex(randomblob(16))), 1, 8
                    )
                    WHERE access_token IS NULL
                    """)
                )
                db.commit()
                print("Generated access tokens for existing exams")
            else:
                print("access_token column already exists")
        else:
            print("exams table does not exist")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_access_token_column()
