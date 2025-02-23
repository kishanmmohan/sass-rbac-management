# Functional Requirements for the RBAC System

This document outlines the essential functions that the RBAC system must support to manage user access, groups, roles,
and organizational boundaries effectively.

---

## Table of Contents

1. [User, User Type, and User-Organization Relationship](#1-user-user-type-and-user-organization-relationship)
2. [Group](#2-group)
3. [Role](#3-role)
4. [Organization](#4-organization)
5. [Module and Module Permissions](#5-module-and-module-permissions)
6. [Auditing and Administration](#6-auditing-and-administration)

---

## 1. User, User Type, and User-Organization Relationship

### User Account Creation and Management

- The system shall allow administrators to create, update, and deactivate user accounts.

### User-Organization Relationship

- A user can be associated with multiple organizations, with their role and permissions determined independently within
  each organization.
- The system shall maintain a user-organization mapping, ensuring that access control is applied per organization.

### User Type Assignment

The system defines user types to distinguish global users (who have system-wide access) from organization-specific
users (who have access only within assigned organizations).

#### Global User Types (Stored at the User Level):

- Super Admin: A single, system-wide authority with unrestricted access across all organizations and system
  configurations.
- Admin: Internal users responsible for overarching system management and operations across all organizations.
- Staff: Internal users who handle internal support and operational tasks across all organizations.
- Org User: A general user of the system who does not have system-wide administrative privileges. Their specific
  permissions are determined based on their roles within organizations.

#### Organization-Specific User Types (Stored in the User-Organization Table):

- Org-Owner: The designated owner of an organization, holding full control over its settings, user management, and
  policies. There can be only one owner per organization.
- Org-Admin: The designated admin of an organization, holding full control over its settings, user management, and
  policies. They have access to all organization-specific features except for the ability to delete the organization and
  update the owner.
- Org-Staff: Organization-specific staff members who perform day-to-day operational tasks only within their assigned
  organization. Their permissions are granted through roles and groups.

### Organization-Specific Access Control

- Users must be explicitly associated with one or more organizations.
- User type is determined per organization, allowing users to have different roles in different organizations.
- Super Admin has universal access across all organizations.
- Admins and Staff have access across all organizations as internal users.
- Owners and Org-Staff are restricted to their respective organizations.

---

## 2. Group

### Group Creation and Configuration

- Groups shall be created within each organization to enable the collective management of user permissions.

### User Group Assignment

- Administrators can add or remove users from groups, ensuring that group memberships are organization-specific.

### Group-Based Permission Management

- Groups serve as a means to apply predefined permission sets (via roles) to multiple users at once within an
  organization.

---

## 3. Role

### Role Definition

- Roles are defined as a set of permissions tailored for each organization. They specify what actions users or groups
  can perform within the system.

### Assignment of Roles

Roles can be assigned via two primary paths:

1. Direct Role Assignment to Users (Permission > Role > User): Roles containing bundled permissions may be assigned
   directly to individual users.
2. Role Assignment to Groups (Permission > Role > Group > User): Roles may be assigned to groups, with users inheriting
   the permissions through their group membership.

### Organizational Ties

- Both roles and groups exist strictly within the boundaries of each organization, ensuring that permissions are
  contextually relevant and isolated.

---

## 4. Organization

### Multi-Organization Support

- The system shall support multiple organizations (tenants) and allow users to be associated with more than one
  organization.

### Per-Organization Role and Permissions

- A user can have different roles in different organizations. Their permissions should be evaluated within the context
  of the active organization they are operating in.

### Access Restrictions

- Users are granted access only to the organizations they are assigned to, with global roles like Super Admin and Admin
  having broader access.

---

## 5. Module and Module Permissions

### Module Definition

- The system is divided into modules representing different features or functional areas.

### CRUD Permission Levels

Each module has defined permissions for:

- Read
- Create
- Update
- Delete

### Permission Assignment Paths

The system supports three distinct methods for granting permissions:

1. Permission > User: Permissions can be directly assigned to individual users.
2. Permission > Role > User: Permissions are bundled into roles, which can then be directly assigned to users.
3. Permission > Role > Group > User: Permissions are bundled into roles that can be assigned to groups, and users
   inherit these permissions through their group membership.

---

## 6. Auditing and Administration

### Change Tracking

- All modifications to user accounts, group memberships, role assignments, and permission settings must be tracked and
  auditable to ensure accountability.

### Administrative Oversight

- Super Admins, Admins, Owners, and Org-Staff (through their assigned roles and groups) shall have tools to review and
  modify permission settings, maintaining a consistent and secure access control framework.

