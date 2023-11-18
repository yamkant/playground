from pydantic import BaseModel
from apps.todo.schema import TodoListSchema

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    todos: TodoListSchema = []

    class Config:
        orm_mode = True