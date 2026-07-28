# BE-02 A2 Connecting to the database

A simple RESTful API built with **FastAPI** and Python to manage a task list (full CRUD).

## Why SQLite?
For this project, **SQLite** was chosen as the database engine. It provides a lightweight, serverless, and zero-setup solution. Because it stores the entire database in a single file, it is incredibly easy to maintain while still ensuring that all data survives server restarts. 

## Database Location & Setup
The database lives entirely in a file named `tasks.db` located at the root of the project. 
* **Automatic Creation:** You do not need to set it up manually. The file is created automatically the first time the application runs.
* **Fresh Starts:** `tasks.db` is included in our `.gitignore` file. This means the database is not uploaded to GitHub, ensuring that anyone who clones this repository starts with a fresh, empty shelf that will be automatically seeded with example tasks upon their first run.

## Installation and Execution

To install the necessary dependencies and start the server locally, run the following command in your terminal:

```bash
pip install fastapi uvicorn pydantic && uvicorn main:app --reload
```

To run this app, write down the following command in your terminal:
```bash
python src/database/connection.py && python main.py
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


