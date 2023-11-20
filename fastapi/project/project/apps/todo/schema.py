from typing import List, Optional
from pydantic import BaseModel
from pydantic import BaseModel

class CreateTodoRequest(BaseModel):
    content: str

class TodoSchema(BaseModel):
    id: int
    content: str
    is_completed: str

    class Config:
        orm_mode = True