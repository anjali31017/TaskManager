# Tasks Module

Handles task CRUD operations with role-based access control.

## Model: `Task`

| Field | Type | Details |
|-------|------|---------|
| `id` | BigAutoField | Auto-generated primary key |
| `title` | CharField(255) | Required |
| `description` | TextField | Optional, defaults to `''` |
| `status` | BooleanField | Default `False` (incomplete) |
| `due_date` | DateField | Optional, nullable |
| `created_at` | DateTimeField | Auto-set on creation |
| `updated_at` | DateTimeField | Auto-set on save |
| `owner` | ForeignKey(User) | Required, cascade delete |

Default ordering: `-created_at` (newest first).

## API Endpoints

All require `Authorization: Bearer <token>`.

| Method | Endpoint | Action |
|--------|----------|--------|
| GET | `/api/tasks/` | List tasks (role-filtered) |
| POST | `/api/tasks/` | Create a task |
| GET | `/api/tasks/<id>/` | Retrieve a task |
| PUT | `/api/tasks/<id>/` | Full update |
| PATCH | `/api/tasks/<id>/` | Partial update |
| DELETE | `/api/tasks/<id>/` | Delete |

## Role-Based Access Control

### Queryset Filtering (`get_queryset`)

- **Admin**: `Task.objects.all()` — sees every task
- **User**: `Task.objects.filter(owner=user)` — sees only own tasks

### Object Permission (`IsOwnerOrAdmin`)

- **Admin**: Can retrieve, update, or delete any task
- **User**: Can only access tasks where `owner == request.user`; other tasks return 404/403

## Query Parameters (GET /api/tasks/)

| Parameter | Example | Description |
|-----------|---------|-------------|
| `status` | `?status=true` | Filter by completion status |
| `owner` | `?owner=1` | Filter by owner ID (Admin only) |
| `search` | `?search=groceries` | Search title and description |
| `ordering` | `?ordering=due_date` | Sort by field (`-due_date` for descending) |
| `page` | `?page=2` | Page number (10 items per page) |

## Key Files

| File | Purpose |
|------|---------|
| `models.py` | `Task` model definition |
| `views.py` | `TaskViewSet` with role-filtered queryset and custom ordering |
| `serializers.py` | `TaskSerializer` — read-only owner field, all other fields writable |
| `permissions.py` | `IsAdminUser` (view-level), `IsOwnerOrAdmin` (object-level) |
| `urls.py` | DRF DefaultRouter registration |
| `admin.py` | Task admin with list display and filters |
