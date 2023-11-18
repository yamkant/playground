from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from apps.database import orm, connection
from apps.todo import schema

router = APIRouter(prefix="/todos")

@router.get("/", response_model=list[schema.TodoSchema])
def get_todos(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(connection.get_db),
):
    _todo_list = db.query(orm.Todo).offset(skip).limit(limit).all()
    print(_todo_list)
    return _todo_list

@router.post("/", response_model=schema.TodoSchema)
async def create_todos(
    todo: schema.CreateTodoRequest = Body(),
    db: Session = Depends(connection.get_db),
):
    new_todo = orm.Todo(content=todo.content, is_completed="N")
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo
