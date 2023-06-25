import logging
import os
from contextlib import contextmanager
from typing import Any, Callable, List, Union, Optional, Dict

import sqlalchemy.types as ST
from sqlalchemy import Column, create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool

from app.core.config import BASE_DIR
from app.models.model_base import BareBaseModel

logger = logging.getLogger()

STORAGE_DIR = os.path.join(BASE_DIR, "storages")
os.makedirs(STORAGE_DIR, exist_ok=True)

_type_mapping = {
    module.__name__.lower(): getattr(ST, module.__name__)
    for module in ST.__dict__.values()
    if isinstance(module, type)
    and not module.__name__.startswith("__")
    and not module.__name__.startswith("_")
    and module.__name__.istitle()
}


class SqliteManager(object):
    def __init__(self, db_name: str, pool_size: int = 5):
        self.db_name: str = db_name
        self.db_url: str = f"sqlite:///{STORAGE_DIR}/{db_name}"
        self.pool_size: int = pool_size
        self.engine: Optional[Engine] = None
        self.Session = None

    def get_db_url(self) -> str:
        return self.db_url

    def __enter__(self) -> "SqliteManager":
        self.engine = create_engine(
            self.db_url,
            connect_args={"check_same_thread": False},
            poolclass=QueuePool,
            pool_size=self.pool_size,
            max_overflow=0,
        )
        self.Session = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.engine:
            self.engine.dispose()

    def bind_tables(self, models: Union[List[Callable], Callable]):
        if not isinstance(models, list):
            models = [models]
        for model in models:
            if not hasattr(model, "__table__"):
                raise AttributeError(
                    f"Model '{model.__name__}' does not have a '__table__' attribute"
                )
            model.metadata.create_all(self.engine)

    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            logger.error(e)
            session.rollback()
            raise
        finally:
            session.close()

    def execute_query(self, query_func: Callable[[Session], any]) -> Any:
        with self.session_scope() as session:
            return query_func(session)

    def create_db(self) -> None:
        BareBaseModel.metadata.create_all(self.engine)

    def drop_db(self) -> None:
        BareBaseModel.metadata.drop_all(self.engine)


class DatabaseHandler(object):
    def __init__(self, db_name: str, db_manager: SqliteManager):
        self.db_name = db_name
        self.db_manager = db_manager

    def execute_query(self, query_func: Callable[[Session], any]) -> Any:
        with self.db_manager.session_scope() as session:
            return query_func(session)

    def create_db(self) -> None:
        self.db_manager.create_db()

    def drop_db(self) -> None:
        self.db_manager.drop_db()


class TableHandler(object):
    def __init__(self, db_name: str, db_manager: SqliteManager):
        self.db_name = db_name
        self.db_manager = db_manager

    def bind_models(self, models: Union[List[Callable], Callable]):
        self.db_manager.bind_tables(models)

    def query_raw(
            self, query: str, is_committed: bool = False, is_fetched: bool = False
    ) -> list[dict[Any, Any]]:
        with self.db_manager.session_scope() as session:
            try:
                result = session.execute(query)
                if is_committed:
                    session.commit()
                if is_fetched:
                    rows = result.fetchall()
                    return [dict(row) for row in rows]
            except Exception as e:
                logger.error(str(e))
            finally:
                session.close()

    def create_tbl(self, table_name: str, columns: Dict[str, Column]) -> None:

        table = type(table_name, (BareBaseModel,), {"__tablename__": table_name, **columns})

        with self.db_manager.session_scope() as session:
            table.__table__.create(bind=session.connection(), checkfirst=True)

    def del_tbl(self, table_name: str):
        self.query_raw(f"DROP TABLE `{table_name}`;")

    def truncate_tbl(self, table_name: str):
        self.query_raw(f"TRUNCATE TABLE `{table_name}`;")

    def add_col(self):
        pass

    def remove_col(self):
        pass
