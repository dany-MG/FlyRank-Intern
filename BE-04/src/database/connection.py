import os
from src.schemas.task_scheme import Task 
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

def init_db():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL
                )
            ''')

        cur.execute(
            '''SELECT COUNT(*) FROM tasks'''
        )
        count = cur.fetchone()["count"]

        if count == 0:
            cur.execute("INSERT INTO tasks (title, done) VALUES (%s, %s)", ("Play LMU on the sim", False))
            cur.execute("INSERT INTO tasks (title, done) VALUES (%s, %s)", ("Go to the gym", False))
            cur.execute("INSERT INTO tasks (title, done) VALUES (%s, %s)", ("Walk the dog", False))  
            conn.commit()

init_db()
