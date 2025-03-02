import asyncio
import os
import uuid

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

os.environ["TESTING"] = "True"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_dummy.db"


# Define a fixture to create a unique database URL for each test
def get_test_db_url():
    """Generate a unique database file name for each test"""
    unique_id = str(uuid.uuid4())
    return f"sqlite+aiosqlite:///./test_{os.getpid()}_{unique_id}.db"


# Event loop fixture for async tests
@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


# Now we can safely import the application and database modules
from main import create_application
from core.db import Base, get_db, init_models


# Override settings for testing (if needed)
def get_settings_override():
    from config import Settings
    return Settings(testing=True)


@pytest_asyncio.fixture(scope="function")
async def test_engine():
    """Create a test database engine"""
    database_url = get_test_db_url()

    # Create async engine with SQLite
    engine = create_async_engine(
        database_url,
        connect_args={"check_same_thread": False},
        echo=False
    )

    # Initialize all models by calling the function from db.py
    init_models()

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Clean up: drop tables and dispose engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()

    # Remove the test database file
    db_file = database_url.replace("sqlite+aiosqlite:///", "")
    if os.path.exists(db_file):
        os.remove(db_file)


@pytest_asyncio.fixture(scope="function")
async def test_db_session(test_engine):
    """Create a test database session"""
    test_async_session = async_sessionmaker(
        bind=test_engine,
        expire_on_commit=False,
        class_=AsyncSession
    )

    async with test_async_session() as session:
        yield session


@pytest.fixture(scope="function")
def override_get_db(test_db_session):
    """Override the get_db dependency"""

    async def _override_get_db():
        try:
            yield test_db_session
        except Exception:
            await test_db_session.rollback()
            raise

    return _override_get_db


@pytest.fixture(scope="function")
def test_app():
    """Fixture to initialize the FastAPI app for testing without database"""
    # Set up: create application
    app = create_application()

    # If you have settings dependency to override
    try:
        from config import get_settings
        app.dependency_overrides[get_settings] = get_settings_override  # noqa
    except ImportError:
        pass

    # Create the TestClient and yield it for use in tests
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def test_app_with_db(test_app, override_get_db):
    """Fixture that creates a fresh database for each test function"""
    # Override the database dependency
    test_app.app.dependency_overrides[get_db] = override_get_db

    yield test_app

    # Reset overrides
    test_app.app.dependency_overrides = {}
