from fastapi import FastAPI
from .koneksi import engine
from . import models
from .routers import posts, users, auth
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hewroo worldo"}
