# Accounts Module

Handles user registration, JWT authentication, and role management.

## Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/auth/register/` | None | Create a new user account |
| POST | `/api/auth/login/` | None | Obtain JWT access + refresh tokens |
| POST | `/api/auth/refresh/` | None | Get a new access token using refresh token |

## Registration Flow

1. Client sends `POST /api/auth/register/` with `username`, `email`, `password`
2. `RegisterSerializer` validates input (password min 8 chars, write-only)
3. `create()` method creates the Django `User` and assigns them to the **User** group
4. Returns user ID, username, email

## JWT Authentication

Configured via `rest_framework_simplejwt`:

- **Access token**: 1 hour lifetime
- **Refresh token**: 1 day lifetime
- **Header format**: `Authorization: Bearer <access_token>`
- Configured as the default DRF authentication class globally

## Role Management

### Groups

Two groups are created by `python manage.py setup_roles`:

- **Admin**: Gets all Django model permissions for the `Task` model
- **User**: Gets no explicit permissions (relies on object-level checks in views)

### Assigning Roles

- **Auto on register**: New users get the **User** role
- **Via Django admin**: `/admin/auth/user/` — edit user → Groups
- **Via shell**: `user.groups.add(Group.objects.get(name='Admin'))`

## Key Files

| File | Purpose |
|------|---------|
| `views.py` | `RegisterView` — `CreateAPIView` with public access |
| `serializers.py` | `RegisterSerializer` — validates, creates user, assigns group |
| `urls.py` | Routes register, login, refresh to their views |
| `admin.py` | Custom `UserAdmin` with role column in list view |
| `management/commands/setup_roles.py` | Management command to bootstrap groups and permissions |
