import uvicorn
from fastapi import FastAPI
import time

app = FastAPI()


@app.get("/slow")
def test():
    time.sleep(0.5)
    return {"status": 200, "message": "success"}


@app.get("/fast")
def root():
    return {"status": 200, "message": "success"}
