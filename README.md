# Task Manager API

A Django REST Framework API for managing tasks with JWT authentication, SQLite, role-based access control (Admin/User), and Docker.

## Features

- User registration and JWT authentication (login/refresh)
- Task CRUD operations with role-based access
- Admin: can manage all tasks; User: can only manage their own tasks
- Pagination, filtering (by status, owner), search (by title/description), ordering (by date)
- Rate limiting, structured logging
- SQLite database
- Production-ready with gunicorn

## Quick Start (Docker)

```bash
docker compose up --build
```

The app will be available at `http://localhost:8000/`. The SQLite database is persisted via a Docker volume.

## Local Development (without Docker)

### Prerequisites
- Python 3.9+

### Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

```bash
python manage.py migrate
python manage.py setup_roles
python manage.py runserver
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Login, returns access + refresh tokens |
| POST | `/api/auth/refresh/` | Refresh access token |

#### Register

```json
POST /api/auth/register/
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "strongpassword123"
}
```

#### Login

```json
POST /api/auth/login/
{
    "username": "johndoe",
    "password": "strongpassword123"
}
```

Response:
```json
{
    "access": "<access_token>",
    "refresh": "<refresh_token>"
}
```

#### Using tokens

Include the access token in all task requests:

```
Authorization: Bearer <access_token>
```

### Tasks

All task endpoints require `Authorization: Bearer <token>` header.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks/` | List tasks (Admin: all; User: own only) |
| POST | `/api/tasks/` | Create a task |
| GET | `/api/tasks/<id>/` | Retrieve a task |
| PUT | `/api/tasks/<id>/` | Full update a task |
| PATCH | `/api/tasks/<id>/` | Partial update a task |
| DELETE | `/api/tasks/<id>/` | Delete a task |

#### Create a task

```json
POST /api/tasks/
{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "due_date": "2025-12-31"
}
```

#### Query parameters (GET /api/tasks/)

- `?status=true` — filter by completion status
- `?owner=<id>` — filter by owner (Admin only)
- `?search=<term>` — search title/description
- `?ordering=due_date` — sort by field (prefix `-` for descending)

### Roles

Two roles are defined via Django groups:

- **Admin** — can view, create, update, and delete **any** task
- **User** — can only manage their **own** tasks

New users are automatically assigned the **User** role on registration.

### Assign a role

Via Django admin (`/admin/`) or the shell:

```python
python manage.py shell
>>> from django.contrib.auth.models import User, Group
>>> user = User.objects.get(username='johndoe')
>>> user.groups.add(Group.objects.get(name='Admin'))
```

## Production Deployment

The following environment variables **must** be configured correctly before deploying to production.

| Variable | Production Value | Impact if Misconfigured |
|----------|-----------------|------------------------|
| `DJANGO_DEBUG` | `False` | If `True`, Django displays detailed error pages with stack traces, SQL queries, and environment variables — leaking sensitive information to end users. |
| `DJANGO_ALLOWED_HOSTS` | Your domain(s), e.g. `api.example.com` | If `*`, the server is vulnerable to **Host header attacks** (cache poisoning, password reset poisoning). |
| `DJANGO_SECRET_KEY` | A long, unique random string | If weak or leaked, session forging, CSRF token forgery, and signed-data tampering become possible. Rotate if ever exposed. |

## Docker

The project runs a single service:

- **web** — The Django app served by gunicorn (4 workers). SQLite database persisted via a named volume.

```bash
# Build and start
docker compose up --build

# Run migrations manually (if needed)
docker compose run --rm web python manage.py migrate

# Create an admin user
docker compose run --rm web python manage.py createsuperuser
```

## Module Documentation

See the [`docs/`](docs/) folder for detailed module-level documentation:

- [Architecture](docs/architecture.md) — Project structure and data flow
- [Accounts](docs/accounts.md) — Authentication, JWT, role management
- [Tasks](docs/tasks.md) — Task model, CRUD API, permissions
- [Deployment](docs/deployment.md) — Docker, environment variables, production guide
