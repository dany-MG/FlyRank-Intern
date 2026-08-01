from pydantic import BaseModel

class Task(BaseModel):
    id: int
    title: str | None = None
    done: bool = False