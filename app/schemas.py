
from pydantic import BaseModel
from typing import Optional

class PlayerUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    team: Optional[str] = None
    