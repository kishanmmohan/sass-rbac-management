# ruff: noqa: F401
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Default to a file-based database
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///rbac.sqlite")

# Create engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# noinspection PyUnresolvedReferences
def init_db():
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

    # Create all tables in the provided engine
    Base.metadata.create_all(bind=engine)
    print("Database created and tables ensured!")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
