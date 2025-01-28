from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None
    fullname: str
    alias: str
    age: int