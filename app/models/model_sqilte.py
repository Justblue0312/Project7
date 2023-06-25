import uuid

from sqlalchemy import Integer, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.models.model_base import BareBaseModel
from app.models.model_user import User


class Sqlite(BareBaseModel):
    db_name = Column(String(100), unique=True)
    db_keyname = Column(String(100), default=None, unique=True)
    owner_id = Column(Integer, ForeignKey(User.id), default=None)

    def to_dict(self):
        return {
            "id": self.id,
            "db_name": self.db_name,
            "db_keyname": self.db_keyname,
            "owner_id": self.owner_id,
        }
