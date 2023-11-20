from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from user.api import router as user_router
from todo.api import router as todo_router

from database.connection import engine, get_db
from database.orm import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

get_db = get_db

origins = [
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router)
app.include_router(todo_router)

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}