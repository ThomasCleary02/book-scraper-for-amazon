from pydantic import BaseModel
from typing import List

class Book (BaseModel):
    isbn: str
    title: str
    author: List[str]
    description: str
    url: str