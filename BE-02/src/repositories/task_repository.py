"""
In memory tasks
tasks = [
    {"id": 1, "title": "Play LMU", "done": False},
    {"id": 2, "title": "Workout", "done": True},
    {"id": 3, "title": "Walk the puppies", "done": False}
]"""
import sqlite3

def get_conn():
    con = sqlite3.connect("./src/database/tasks.db")
    con.row_factory = sqlite3.Row
    return con

class TasksRepository:
    @staticmethod
    def get_all_tasks():
        with get_conn() as con:
            cur = con.cursor()
            res = cur.execute("SELECT * FROM tasks")
            return [dict(row) for row in res.fetchall()]

    @staticmethod
    def get_by_id(task_id: int):
        with get_conn() as con:
            cur = con.cursor()
            res = cur.execute("SELECT id, title, done from tasks WHERE id = ?", (task_id,))
            row = res.fetchone()
            return dict(row) if row else None

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
        for t in tasks:
            if t.get("id") == task_id:
                t.update(updated_data)
                return t
        return None

    @staticmethod
    def delete(task: dict):
        tasks.remove(task)

    

