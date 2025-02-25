from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.db import Base


class Group(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey("organization.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    created_by_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"))
    updated_by_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"))

    users = relationship("UserGroup", back_populates="group")
    roles = relationship("GroupRole", back_populates="group")

    __table_args__ = (UniqueConstraint("name", "organization_id", name="uq_group_name_org"),)


class UserGroup(Base):
    __tablename__ = "user_group"

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    group_id = Column(Integer, ForeignKey("group.id", ondelete="CASCADE"), primary_key=True)

    user = relationship("User", back_populates="groups")
    group = relationship("Group", back_populates="users")


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey("organization.id", ondelete="CASCADE"), nullable=False)
    created_by_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"))
    updated_by_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"))

    groups = relationship("GroupRole", back_populates="role")
    users = relationship("UserRole", back_populates="role")
    permissions = relationship("RolePermission", back_populates="role")

    __table_args__ = (UniqueConstraint("name", "organization_id", name="uq_role_name_org"),)


class GroupRole(Base):
    __tablename__ = "group_role"

    group_id = Column(Integer, ForeignKey("group.id", ondelete="CASCADE"), primary_key=True)
    role_id = Column(Integer, ForeignKey("role.id", ondelete="CASCADE"), primary_key=True)

    group = relationship("Group", back_populates="roles")
    role = relationship("Role", back_populates="groups")


class UserRole(Base):
    __tablename__ = "user_role"

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    role_id = Column(Integer, ForeignKey("role.id", ondelete="CASCADE"), primary_key=True)

    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")


class FeatureModule(Base):
    __tablename__ = "feature_module"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


class Permission(Base):
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True, autoincrement=True)
    module_id = Column(Integer, ForeignKey("feature_module.id", ondelete="CASCADE"), nullable=False)
    action = Column(String, nullable=False)

    roles = relationship("RolePermission", back_populates="permission")
    users = relationship("UserPermission", back_populates="permission")

    __table_args__ = (UniqueConstraint("module_id", "action", name="uq_permission_module_action"),)


class RolePermission(Base):
    __tablename__ = "role_permission"

    role_id = Column(Integer, ForeignKey("role.id", ondelete="CASCADE"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permission.id", ondelete="CASCADE"), primary_key=True)

    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")


class UserPermission(Base):
    __tablename__ = "user_permission"

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permission.id", ondelete="CASCADE"), primary_key=True)

    user = relationship("User", back_populates="permissions")
    permission = relationship("Permission", back_populates="users")
