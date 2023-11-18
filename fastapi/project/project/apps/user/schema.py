from pydantic import BaseModel
from apps.todo.schema import TodoSchema

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    todos: list[TodoSchema] = []

    class Config:
        orm_mode = True