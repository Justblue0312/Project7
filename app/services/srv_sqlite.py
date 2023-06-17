from fastapi_sqlalchemy import db

from schemas.sche_sqlite import CreateDatabaseRequest
from models import Sqlite, User


class SqliteService(object):
    @staticmethod
    def create_database(data: CreateDatabaseRequest, current_user: User):
        new_db = Sqlite(db_name=data.db_name, owner_id=current_user.id)
        db.session.add(new_db)
        db.session.commit()
        return new_db
