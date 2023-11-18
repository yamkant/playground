from typing import List, Optional
from pydantic import BaseModel
from apps.shared_kernel.response import BaseResponse
from pydantic import BaseModel

class CreateTodoRequest(BaseModel):
    content: str

class TodoSchema(BaseModel):
    id: int
    content: str
    is_complete: str

    class Config:
        orm_mode = True

class TodoListSchema(BaseResponse):
    result: List[TodoSchema]

class TodoCreateResponse(BaseResponse):
    result: TodoSchema