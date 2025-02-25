import enum


class UserTypeEnum(enum.Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    STAFF = "staff"
    ORG_USER = "org_user"
