from typing import Dict, Any

from fastapi import HTTPException
from fastapi_sqlalchemy import db

import sqlalchemy.types as ST
from sqlalchemy import Column

from app.core.config import STORAGE_DIR
from app.db.sqlite_handler import SqliteManager, TableHandler, _type_mapping
from app.libs.file import delete_file
from app.libs.utils import generate_keyname
from app.models import Sqlite, User
from app.schemas.sche_sqlite import CreateDatabaseRequest, CreateTablePayload


class SqliteService(object):
    @staticmethod
    def create_database(current_user: User, data: CreateDatabaseRequest):
        new_db = Sqlite(
            db_name=data.db_name,
            db_keyname=generate_keyname(),
            owner_id=current_user.id,
        )  # type: ignore
        db.session.add(new_db)
        db.session.commit()

        with SqliteManager(data.db_name) as db_manager: # type: ignore
            db_manager.create_db()
        return new_db

    @staticmethod
    def drop_database(current_user: User, data: CreateDatabaseRequest):
        db.session.query(Sqlite).filter_by(db_name=data.db_name).filter_by(
            owner_id=current_user.id
        ).delete()
        delete_file(data.db_name, STORAGE_DIR)

    @staticmethod
    def create_table(current_user: User, payload: CreateTablePayload) -> None:
        data: dict = payload.dict()
        if not data.get("table_name") or not data.get("form"):
            raise HTTPException(status_code=400, detail="Incorrect input format.")

        db_data = db.session.query(Sqlite).filter_by(owner_id=current_user.id).first()
        if not db_data:
            raise HTTPException(status_code=400, detail="Database not found.")

        columns: Dict[str, Any] = {
            "id": Column(
                _type_mapping["integer"],
                primary_key=True,
                unique=True,
                autoincrement="auto",
            )
        }

        for _, value in data["form"].items():
            if _type_mapping.get(value["data_type"]):
                column = Column(
                    value["name"], _type_mapping.get(value["data_type"], ST.Text)
                )
            else:
                raise ValueError(
                    f"Invalid column type for {value['name']}: {value['data_type']}"
                )

            columns[value["name"]] = column
        table_name: str = data["table_name"]
        if table_name and columns:
            with SqliteManager(db_data.db_name) as db_manager: # type: ignore
                TableHandler(db_data.db_name, db_manager).create_tbl(table_name, columns)  # type: ignore
