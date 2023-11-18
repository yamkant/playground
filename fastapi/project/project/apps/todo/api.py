from fastapi import APIRouter, Depends, Body, HTTPException
from apps.database.connection import SessionLocal
from apps.database import orm
from apps.todo import schema

router = APIRouter(prefix="/todos")

@router.get("/")
def get_todos(
    skip: int = 0,
    limit: int = 10,
):
    db = SessionLocal()
    return db.query(orm.Todo).offset(skip).limit(limit).all()

@router.post("/")
async def create_todos(
    todo: schema.CreateTodoRequest = Body(),
):
    db = SessionLocal()
    new_todo = orm.Todo(content=todo.content, is_completed="N")
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo
