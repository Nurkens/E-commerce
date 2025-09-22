from fastapi import FastAPI
from routers import datasets

app = FastAPI(title="Data Visualization", version="1.0.0")


app.include_router(datasets.router)

@app.get("/")
def root():
    return {"message": "Working:)"}
