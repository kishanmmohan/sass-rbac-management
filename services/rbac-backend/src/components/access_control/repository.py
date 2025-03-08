from typing import Dict, List, Optional, Type

from sqlalchemy.orm import Session
from src.components.access_control.models import (
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
from src.components.organizations.models import OrgUserTypeEnum, UserOrganization


class RBACRepository:
    def __init__(self, db_session: Session, org_id: Optional[int] = None, is_super_admin: bool = False,
                 user_id: Optional[int] = None):
        self.db_session = db_session
        self.org_id = org_id
        self.is_super_admin = is_super_admin
        self.user_id = user_id
        self.org_user_type = self._get_org_user_type() if not is_super_admin and org_id and user_id else None

    def _get_org_user_type(self) -> Optional[str]:
        user_org = self.db_session.query(UserOrganization).filter(
            UserOrganization.user_id == self.user_id,
            UserOrganization.organization_id == self.org_id
        ).first()
        return user_org.user_type if user_org else None

    def create_role(self, name: str, created_by_id: int) -> Optional[Role]:
        if self.is_super_admin or self.org_user_type in [OrgUserTypeEnum.ORG_OWNER.value,
                                                         OrgUserTypeEnum.ORG_ADMIN.value]:
            role = Role(name=name, organization_id=self.org_id, created_by_id=created_by_id)
            self.db_session.add(role)
            self.db_session.commit()
            self.db_session.refresh(role)
            return role
        raise Exception("Unauthorized action - Only OrgOwner or OrgAdmin can create roles.")

    def assign_role_to_user(self, user_id: int, role_id: int) -> Optional[UserRole]:
        if self._get_org_user_type() == OrgUserTypeEnum.ORG_STAFF.value:
            user_role = UserRole(user_id=user_id, role_id=role_id)
            self.db_session.add(user_role)
            self.db_session.commit()
            return user_role
        raise Exception("Unauthorized action - Only OrgStaff can have roles assigned.")

    def assign_role_to_group(self, group_id: int, role_id: int) -> Optional[GroupRole]:
        if self.is_super_admin or self.org_user_type in [OrgUserTypeEnum.ORG_OWNER.value,
                                                         OrgUserTypeEnum.ORG_ADMIN.value]:
            group_role = GroupRole(group_id=group_id, role_id=role_id)
            self.db_session.add(group_role)
            self.db_session.commit()
            return group_role
        raise Exception("Unauthorized action - Only OrgOwner or OrgAdmin can assign roles to groups.")

    def get_roles_for_user(self, user_id: int, search_query: Optional[str] = None, limit: int = 10, offset: int = 0,
                           sort_by: Optional[str] = None, sort_order: str = 'asc') -> List[Type[Role]]:
        query = self.db_session.query(Role).join(UserRole).filter(Role.organization_id == self.org_id)
        if self._get_org_user_type() == OrgUserTypeEnum.ORG_STAFF.value:
            query = query.filter(UserRole.user_id == user_id)
        if search_query:
            query = query.filter(Role.name.ilike(f"%{search_query}%"))
        if sort_by:
            query = query.order_by(
                getattr(Role, sort_by).desc() if sort_order == 'desc' else getattr(Role, sort_by).asc())
        else:
            query = query.order_by(Role.id)
        return query.offset(offset).limit(limit).all()

    def create_group(self, name: str) -> Optional[Group]:
        if self.is_super_admin or self.org_user_type in [OrgUserTypeEnum.ORG_OWNER.value,
                                                         OrgUserTypeEnum.ORG_ADMIN.value]:
            group = Group(name=name, organization_id=self.org_id)
            self.db_session.add(group)
            self.db_session.commit()
            self.db_session.refresh(group)
            return group
        raise Exception("Unauthorized action - Only OrgOwner or OrgAdmin can create groups.")

    def assign_user_to_group(self, user_id: int, group_id: int) -> Optional[UserGroup]:
        if self._get_org_user_type() == OrgUserTypeEnum.ORG_STAFF.value:
            user_group = UserGroup(user_id=user_id, group_id=group_id)
            self.db_session.add(user_group)
            self.db_session.commit()
            return user_group
        raise Exception("Unauthorized action - Only OrgStaff can be assigned to groups.")

    def get_groups_for_user(self, user_id: int, search_query: Optional[str] = None, limit: int = 10, offset: int = 0,
                            sort_by: Optional[str] = None, sort_order: str = 'asc') -> List[Type[Group]]:
        query = self.db_session.query(Group).join(UserGroup).filter(Group.organization_id == self.org_id)
        if self._get_org_user_type() == OrgUserTypeEnum.ORG_STAFF.value:
            query = query.filter(UserGroup.user_id == user_id)
        if search_query:
            query = query.filter(Group.name.ilike(f"%{search_query}%"))
        if sort_by:
            query = query.order_by(
                getattr(Group, sort_by).desc() if sort_order == 'desc' else getattr(Group, sort_by).asc())
        else:
            query = query.order_by(Group.id)
        return query.offset(offset).limit(limit).all()

    def assign_permission_to_role(self, role_id: int, permission_id: int) -> Optional[RolePermission]:
        if self.is_super_admin or self.org_user_type in [OrgUserTypeEnum.ORG_OWNER.value,
                                                         OrgUserTypeEnum.ORG_ADMIN.value]:
            role_permission = RolePermission(role_id=role_id, permission_id=permission_id)
            self.db_session.add(role_permission)
            self.db_session.commit()
            return role_permission
        raise Exception("Unauthorized action - Only OrgOwner or OrgAdmin can assign permissions to roles.")

    def assign_permission_to_user(self, user_id: int, permission_id: int) -> Optional[UserPermission]:
        if self.is_super_admin or self.org_user_type in [OrgUserTypeEnum.ORG_OWNER.value,
                                                         OrgUserTypeEnum.ORG_ADMIN.value]:
            user_permission = UserPermission(user_id=user_id, permission_id=permission_id)
            self.db_session.add(user_permission)
            self.db_session.commit()
            return user_permission
        raise Exception("Unauthorized action - Only OrgOwner or OrgAdmin can assign permissions to users.")

    def get_permissions_for_user(self, user_id: int) -> Dict[str, List[str]]:
        if self._get_org_user_type() != OrgUserTypeEnum.ORG_STAFF.value:
            return {}
        direct_permissions = self.db_session.query(Permission.module_id, Permission.action).join(UserPermission).filter(
            UserPermission.user_id == user_id)
        role_permissions = self.db_session.query(Permission.module_id, Permission.action).join(RolePermission).join(
            UserRole, RolePermission.role_id == UserRole.role_id).filter(UserRole.user_id == user_id)
        group_permissions = self.db_session.query(Permission.module_id, Permission.action).join(RolePermission).join(
            GroupRole, RolePermission.role_id == GroupRole.role_id).join(UserGroup,
                                                                         GroupRole.group_id == UserGroup.group_id).filter(
            UserGroup.user_id == user_id)
        all_permissions = direct_permissions.union(role_permissions).union(group_permissions).distinct().all()
        module_permissions = {}
        for module_id, action in all_permissions:
            module = self.db_session.query(FeatureModule.name).filter(FeatureModule.id == module_id).scalar()
            if module not in module_permissions:
                module_permissions[module] = []
            module_permissions[module].append(action)
        return module_permissions
