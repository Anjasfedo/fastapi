from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hewroo worldo"}

@app.get("/posts")
def get_posts():
    return {"data": "Yer post"}
