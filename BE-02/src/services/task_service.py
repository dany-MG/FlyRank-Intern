from src.repositories.task_repository import TasksRepository
from src.schemas.task_scheme import Task
from src.errors import TaskNotFoundError, InvalidTaskError

class TaskService:
    @staticmethod
    def get_all_tasks():
        return TasksRepository.get_all_tasks()

    @staticmethod
    def get_task_by_id(task_id: int):
        task = TasksRepository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(task_id)
        return task

    @staticmethod
    def create_task(task_data: Task):
        if task_data.title is None or task_data.title.strip() == "":
            raise InvalidTaskError("Task title cannot be empty")
        current_tasks = TasksRepository.get_all_tasks()
        new_id = max([task["id"] for task in current_tasks], default=0) + 1
        new_task = {"id": new_id, "title": task_data.title, "done": task_data.done}
        return TasksRepository.create_task(new_task)

    @staticmethod
    def update_task(task_id: int, task_data:Task):
        if task_data.title is None or task_data.title.strip() == "":
            raise InvalidTaskError("Task title cannot be empty")

        task_to_update = TasksRepository.get_by_id(task_id)
        if not task_to_update:
            raise TaskNotFoundError(task_id)

        update_dict = {}
        if task_data.title is not None:
            update_dict["title"] = task_data.title
        if task_data.done is not None:
            update_dict["done"] = task_data.done

        return TasksRepository.update(task_id, update_dict)

    @staticmethod
    def delete_task(task_id: int):
        task_to_delete = TasksRepository.get_by_id(task_id)
        if not task_to_delete:
            raise TaskNotFoundError(task_id)
        TasksRepository.delete(task_to_delete)