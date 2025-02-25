import enum

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.db import Base


class OrgUserTypeEnum(enum.Enum):
    ORG_OWNER = "org_owner"
    ORG_ADMIN = "org_admin"
    ORG_STAFF = "org_staff"


class Organization(Base):
    __tablename__ = "organization"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    created_by_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"))
    updated_by_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"))

    users = relationship("UserOrganization", back_populates="organization")


class UserOrganization(Base):
    __tablename__ = "user_organization"

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.id", ondelete="CASCADE"), primary_key=True)
    user_type = Column(Enum(OrgUserTypeEnum), nullable=False)

    user = relationship("User", back_populates="organizations")
    organization = relationship("Organization", back_populates="users")
