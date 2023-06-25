from fastapi_sqlalchemy import db

from app.db.sqlite_handler import SqliteManager
from app.models import Sqlite, User
from app.schemas.sche_sqlite import CreateDatabaseRequest

from app.libs.utils import generate_keyname


class SqliteService(object):
    @staticmethod
    def create_database(current_user: User, data: CreateDatabaseRequest):
        new_db = Sqlite(
            db_name=data.db_name,
            db_keyname=generate_keyname(),
            owner_id=current_user.id,
        )
        db.session.add(new_db)
        db.session.commit()

        SqliteManager(data.db_name).create_db()
        return new_db
