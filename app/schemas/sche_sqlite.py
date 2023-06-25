from typing import Optional

from pydantic import BaseModel


class CreateDatabaseRequest(BaseModel):
    db_name: Optional[str]


class UserDatabaseResponse(BaseModel):
    id: str
    db_name: str
    db_keyname: str
    owner_id: str
