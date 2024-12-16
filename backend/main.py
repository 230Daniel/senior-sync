
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return "hello, I am the backend, I speak for the trees"
