from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from apps.database import orm, connection
from apps.todo import schema, repository

router = APIRouter(prefix="/todos")

@router.get("/", response_model=list[schema.TodoSchema])
def get_todos(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(connection.get_db),
):
    _todo_list = repository.get_todo_list(db, skip, limit)
    return _todo_list

@router.post("/", response_model=schema.TodoSchema)
async def post_todos(
    todo: schema.CreateTodoRequest = Body(),
    db: Session = Depends(connection.get_db),
):
    new_todo = repository.create_todo(db, todo)
    return new_todo