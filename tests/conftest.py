import os
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import StaticPool

from src.config import Settings, get_settings
from src.core.db import Base, get_db
from src.main import create_application


# Override settings for testing
def get_settings_override():
    return Settings(testing=True)


# Fixture to initialize the FastAPI app for testing
@pytest.fixture(scope="module")
def test_app():
    # Set up: override settings for testing
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override  # noqa

    # Create the TestClient and yield it for use in tests
    with TestClient(app) as test_client:
        yield test_client


def get_test_db_url():
    """Generate a unique database file name for each test"""
    unique_id = str(uuid.uuid4())
    return f"sqlite:///./test_{os.getpid()}_{unique_id}.db"


@pytest.fixture(scope="function")
def test_app_with_db():
    """Fixture that creates a fresh database for each test function"""
    # Create a unique database URL for this test
    database_url = get_test_db_url()

    # Create engine with SQLite-specific configurations
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool  # Ensures single connection for testing
    )

    # Create test session
    local_test_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    test_session = scoped_session(local_test_session)

    # Create all tables in the test database
    Base.metadata.create_all(bind=engine)

    # Create FastAPI application
    app = create_application()

    # Override the dependency
    def override_get_db():
        try:
            db = test_session()
            yield db
        finally:
            db.close()  # noqa: F823 (Referenced before assignment)

    app.dependency_overrides[get_db] = override_get_db  # noqa

    # Create TestClient
    with TestClient(app) as test_client:
        yield test_client

    # Cleanup
    test_session.remove()
    engine.dispose()
    Base.metadata.drop_all(bind=engine)

    # Remove the test database file
    db_file = database_url.replace("sqlite:///", "")
    if os.path.exists(db_file):
        os.remove(db_file)
