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
            res = cur.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (new_task["title"], new_task["done"]))
            con.commit()
            new_task["id"] = res.lastrowid
            return new_task

    @staticmethod
    def update(task_id: int, updated_data: dict):
        with get_conn() as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cur.fetchone()
            if not row:
                return None

            current_data = dict(row)

            new_title = updated_data.get("title", current_data["title"])
            new_done = updated_data.get("done", current_data["done"])

            cur.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?", (new_title, new_done, task_id))
            con.commit()
            return {"id": task_id, "title": new_title, "done": new_done}
            
        
    @staticmethod
    def delete(task: dict):
        with get_conn() as con:
            cur = con.cursor()
            cur.execute("DELETE FROM tasks WHERE id = ?", (task["id"],))

    

