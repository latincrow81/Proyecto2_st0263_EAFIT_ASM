from typing import Generator
from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy_utils import database_exists, create_database


env_config = dotenv_values(".env")


def get_database() -> str:
    db_user = env_config.get('DB_USERNAME')
    db_password = env_config.get('DB_PASSWORD')
    db_host = env_config.get('DB_HOST')
    db_name = env_config.get('DB_DATABASE')
    db_dialect = env_config.get('DB_DIALECT')
    db_port = env_config.get('DB_PORT')

    assert db_host is not None
    assert db_password is not None

    return f'{db_dialect}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'


class DbAPI:
    def __init__(self) -> None:
        db_url = get_database()
        self.engine = create_engine(db_url)
        self.session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)

    @contextmanager
    def session_local(self) -> Generator:
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def create_database(self) -> None:
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
