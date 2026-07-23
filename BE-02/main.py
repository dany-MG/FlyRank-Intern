import uvicorn
from src.app import app

if __name__ == "__main__":
    # Inicia el servidor usando uvicorn cuando ejecutas 'python main.py'
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True)
