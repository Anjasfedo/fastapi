from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hewroo worldo"}


@app.get("/posts")
def get_posts():
    return {"data": "Yer post"}


@app.post("/createposts")
def create_post(payLoad: dict = Body(...)):
    print(payLoad)
    return {"new_post": payLoad}
