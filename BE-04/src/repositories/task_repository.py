"""
In memory tasks
tasks = [
    {"id": 1, "title": "Play LMU", "done": False},
    {"id": 2, "title": "Workout", "done": True},
    {"id": 3, "title": "Walk the puppies", "done": False}
]"""
from src.database.connection import get_conn

class TasksRepository:
    @staticmethod
    def get_all_tasks():
        with get_conn() as con:
            cur = con.cursor()
            cur.execute("SELECT id, title, done FROM tasks")
            return cur.fetchall()

    @staticmethod
    def get_by_id(task_id: int):
        with get_conn() as con:
            cur = con.cursor()
            cur.execute("SELECT id, title, done FROM tasks WHERE id= %s", (task_id,))
            return cur.fetchone()

    @staticmethod
    def create_task(new_task: dict):
        with get_conn() as con:
            cur = con.cursor()
            cur.execute("INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING *", (new_task["title"], bool(new_task["done"])))
            con.commit()
            return cur.fetchone()

    @staticmethod
    def update(task_id: int, updated_data: dict):
        with get_conn() as con:
            cur = con.cursor()
            cur.execute("SELECT id, title, done FROM tasks WHERE id = %s", (task_id,))
            row = cur.fetchone()
            if not row:
                return None

            current_data = dict(row)

            new_title = updated_data.get("title", current_data["title"])
            new_done = bool(updated_data.get("done", current_data["done"]))

            cur.execute("UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING *", (new_title, new_done, task_id))
            con.commit()
            return cur.fetchone()
            
        
    @staticmethod
    def delete(task: dict):
        with get_conn() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM tasks WHERE id = %s RETURNING *", (task["id"],))
            con.commit()
    
    

