import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

# Load database URL from environment variables
# Use SQLite for testing to avoid PostgreSQL dependency
if os.getenv("TESTING") == "True":
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test_dummy.db")
else:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@rbac-db:5432/postgres")

# Create async database engine
engine = create_async_engine(DATABASE_URL)

# Create session factory
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

# Base class for ORM models
Base = declarative_base()


# Dependency to get the database session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


# Function to initialize models - this is the single place where models are imported
# noinspection PyUnresolvedReferences
def init_models():
    """Import all models to ensure they're registered with Base"""
    from components.access_control.models import (
        FeatureModule,
        Group,
        GroupRole,
        Permission,
        Role,
        RolePermission,
        UserGroup,
        UserPermission,
        UserRole,
    )
    from components.audit_log.models import AuditLog
    from components.organizations.models import Organization, UserOrganization
    from components.users.models import User

    # You can add a return statement if you want to confirm models were imported
    return True


# Function to initialize the database
# noinspection PyUnresolvedReferences
async def init_db():
    # Skip initialization in testing mode
    if os.getenv("TESTING") == "True":
        return

    # Initialize models
    init_models()

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Database initialized successfully!")
