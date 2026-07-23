class TaskNotFoundError(Exception):
    def __init__(self, task_id:int):
        self.message = f"Task with id {task_id} not found"
        super().__init__(self.message)

class InvalidTaskError(Exception):
    def __init__(self, message:str):
        self.message = message
        super().__init__(self.message)
