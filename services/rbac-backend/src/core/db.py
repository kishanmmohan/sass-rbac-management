import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

# Load database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@rbac-db:5432/postgres")

# Create async database engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create session factory
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

# Base class for ORM models
Base = declarative_base()


# Dependency to get the database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# Function to initialize the database
# noinspection PyUnresolvedReferences
async def init_db():
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

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Database initialized successfully!")
