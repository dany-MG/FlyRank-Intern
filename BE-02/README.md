
# BE-02 A2 Connecting to the database

A simple RESTful API built with **FastAPI** and Python to manage a task list (full CRUD).

## Installation and Execution

To install the necessary dependencies and start the server locally, run the following command in your terminal:

```bash
pip install fastapi uvicorn pydantic && uvicorn main:app --reload
```

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | Shows the main API information. |
| `GET` | `/health` | Checks the server status. |
| `GET` | `/tasks` | Retrieves the complete list of tasks. |
| `GET` | `/tasks/{id}` | Finds and returns a specific task by ID. |
| `POST` | `/tasks` | Creates a new task. |
| `PUT` | `/tasks/{id}` | Updates the title or status of an existing task. |
| `DELETE` | `/tasks/{id}` | Permanently deletes a task. |

## Example Query (SQLite)
```
DELETE FROM tasks WHERE done = 1;
```
Execution Result
``` 
Execution finished without errors.
Result: query executed successfully. Took 0ms, 6 rows affected
At line 1:
DELETE FROM tasks WHERE done = 1;
```


