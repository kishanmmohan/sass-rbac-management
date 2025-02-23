from typing import List, Optional, Type

from models import Organization, UserOrganization
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.components.users.models import User


class OrganizationRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_organization(self, name: str, slug: str, created_by_id: int) -> Organization:
        organization = Organization(name=name, slug=slug, created_by_id=created_by_id)
        self.db_session.add(organization)
        self.db_session.commit()
        self.db_session.refresh(organization)
        return organization

    def get_organization_by_id(self, org_id: int) -> Optional[Organization]:
        return self.db_session.query(Organization).filter(Organization.id == org_id).first()

    def get_all_organizations(self, is_super_admin: bool, user_id: Optional[int] = None,
                              search_query: Optional[str] = None, limit: int = 10, offset: int = 0) -> List[
        Type[Organization]]:
        query = self.db_session.query(Organization)
        if not is_super_admin and user_id:
            query = query.join(UserOrganization).filter(UserOrganization.user_id == user_id)
        elif not is_super_admin:
            raise Exception("Unauthorized action - User ID required for non-super admin.")
        if search_query:
            query = query.filter(Organization.name.ilike(f"%{search_query}%"))
        return query.order_by(Organization.id).offset(offset).limit(limit).all()

    def assign_user_to_organization(self, user_id: int, organization_id: int) -> UserOrganization:
        mapping = UserOrganization(user_id=user_id, organization_id=organization_id)
        self.db_session.add(mapping)
        self.db_session.commit()
        return mapping

    def get_users_in_organization(self, org_id: int, search_query: Optional[str] = None, limit: int = 10,
                                  offset: int = 0) -> List[Type[User]]:
        query = self.db_session.query(User).join(UserOrganization).filter(UserOrganization.organization_id == org_id)
        if search_query:
            query = query.filter(or_(User.name.ilike(f"%{search_query}%"), User.email.ilike(f"%{search_query}%")))
        return query.order_by(User.id).offset(offset).limit(limit).all()
