import os
from contextlib import contextmanager
from typing import Any, Callable, List, Union

from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import QueuePool

from app.core.config import BASE_DIR

STORAGE_DIR = os.path.join(BASE_DIR, "storages")
os.makedirs(STORAGE_DIR, exist_ok=True)


class _Base(DeclarativeBase):
    pass


class SqliteManager(object):
    def __init__(self, db_name: str, pool_size: int = 5):
        self.db_name = db_name
        self.db_url = f"sqlite:///{STORAGE_DIR}/{db_name}"
        self.pool_size = pool_size
        self.engine = None
        self.Session = None

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

    def __exit__(self, exc_type, exc_val, exc_tb):
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
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def execute_query(self, query_func: Callable[[Session], any]) -> Any:
        with self.session_scope() as session:
            return query_func(session)

    def create_db(self) -> None:
        _Base.metadata.create_all(self.engine)
