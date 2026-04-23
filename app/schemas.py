
from pydantic import BaseModel
from typing import Optional

class PlayerUpdate(BaseModel):
    name: Optional[str] = None
    team: Optional[str] = None
