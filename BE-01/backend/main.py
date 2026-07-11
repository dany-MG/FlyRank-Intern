from fastapi import FastAPI

app = FastAPI(
    title = "BE-01",
    description="A tiny backend with two JSON endpoints"
)

#Endpoint 1 
@app.get("/")
def read_root():
    return{
        "message": "Hello FlyRank",
        "author" : "Daniel",
        "version" : "1.0.0",
        "ready_internship" : True
    }

#Endpoint 2
@app.get("/api/intern")
def read_intern():
    return{
        "message": "I hope I'll learn a lot during this internship",
        "author" : "Daniel",
        "version" : "1.0.0",
    }

