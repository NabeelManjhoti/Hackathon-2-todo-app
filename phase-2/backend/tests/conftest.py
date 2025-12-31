import pytest
from sqlmodel import create_engine, Session, SQLModel
from sqlmodel.pool import StaticPool
from fastapi.testclient import TestClient
from src.main import create_app
from src.database.session import get_session, engine
from src.models import *  # Import all models


@pytest.fixture(name="session")
def session_fixture():
    test_engine = create_engine(
        "sqlite://",  # Use in-memory SQLite for tests
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=test_engine)
    with Session(test_engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session):
    def get_test_session():
        return session

    app = create_app()
    app.dependency_overrides[get_session] = get_test_session

    client = TestClient(app)
    yield client