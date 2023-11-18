from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from apps.user.api import router as user_router
from apps.todo.api import router as todo_router

from apps.database.connection import SessionLocal, engine
from apps.database.orm import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

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

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(user_router)
app.include_router(todo_router)

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}