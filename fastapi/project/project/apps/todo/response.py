from typing import List

from pydantic import BaseModel
from apps.shared_kernel.response import BaseResponse

class TodoSchema(BaseModel):
    id: int
    content: str
    is_complete: str

    class Config:
        orm_mode = True

class TodoResponse(BaseResponse):
    result: List[TodoSchema]

class TodoCreateResponse(BaseResponse):
    result: TodoSchema