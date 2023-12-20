from pydantic import BaseModel
from typing import Optional



class User(BaseModel):
    email: Optional[str] = None
    hashed_password: Optional[str] = None
    raw_password: Optional[str] = None
    roles: Optional[list] = None
    description: Optional[str] = None
