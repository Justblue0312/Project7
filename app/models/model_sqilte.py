import uuid

from sqlalchemy import Integer, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.models.model_base import BareBaseModel


class Sqlite(BareBaseModel):
    db_name = Column(String(100))
    db_keyname = Column(String(100), default=None)
    owner_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates="dbs")

    def __init__(self):
        self.db_name = str(uuid.uuid4())
