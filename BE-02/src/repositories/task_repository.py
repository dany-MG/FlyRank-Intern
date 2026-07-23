tasks = [
    {"id": 1, "title": "Play LMU", "done": False},
    {"id": 2, "title": "Workout", "done": True},
    {"id": 3, "title": "Walk the puppies", "done": False}
]

class TasksRepository:
    @staticmethod
    def get_all_tasks():
        return tasks

    @staticmethod
    def get_by_id(task_id: int):
        for t in tasks:
            if t["id"] == task_id:
                return t
        return None

    @staticmethod
    def create_task(new_task: dict):
        tasks.append(new_task)
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

    

