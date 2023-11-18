from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from ..apps.database.orm import Base
from ..apps.main import app


@pytest.fixture(scope="session")
def test_db():
    test_db_url = "sqlite:///./test.db"
    if not database_exists(test_db_url):
        create_database(test_db_url)

    engine = create_engine(test_db_url)
    Base.metadata.create_all(engine)
    try:
        yield engine
    finally:
        Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def test_session(test_db):
    connection = test_db.connect()

    trans = connection.begin()
    session = sessionmaker()(bind=connection)

    session.begin_nested()  # SAVEPOINT

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        """
        Each time that SAVEPOINT ends, reopen it
        """
        if transaction.nested and not transaction._parent.nested:
            session.begin_nested()

    yield session

    session.close()
    trans.rollback()  # roll back to the SAVEPOINT
    connection.close()


@pytest.fixture
def client():
    return TestClient(app)