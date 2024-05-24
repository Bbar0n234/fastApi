from fastapi import FastAPI
from views import router as person_router

app = FastAPI()
app.include_router(person_router)


@app.get("/")
def root():
    return {"message": "Hello World"}
