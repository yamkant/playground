from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.pool import StaticPool

from project.apps.database import orm, connection
from project.apps.main import app, get_db

TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="session")
def test_db():
    print("데이터베이스 연결 실행 1")
    test_db_url = TEST_DATABASE_URL
    if not database_exists(test_db_url):
        create_database(test_db_url)

    engine = create_engine(test_db_url)
    orm.Base.metadata.create_all(engine)
    # metadata.create_all(engine)
    try:
        yield engine
    finally:
        orm.Base.metadata.drop_all(engine)
        # metadata.drop_all(engine)


@pytest.fixture(scope="function")
def test_session(test_db):
    print("데이터베이스 연결 실행 2")
    connection = test_db.connect()

    trans = connection.begin()
    session = sessionmaker()(bind=connection)

    session.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        """
        Each time that SAVEPOINT ends, reopen it
        """
        if transaction.nested and not transaction._parent.nested:
            session.begin_nested()

    yield session

    session.close()
    trans.rollback()
    connection.close()


@pytest.fixture
def client():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    orm.Base.metadata.create_all(bind=engine)

    def override_get_db():
        try:
            db = TestSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)