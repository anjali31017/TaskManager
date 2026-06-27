# Architecture

## Project Structure

```
TaskManager/
├── config/              # Django project configuration
│   ├── settings.py      # Settings (DB, auth, throttling, logging)
│   ├── urls.py          # Root URL routing
│   ├── wsgi.py          # WSGI entry point (gunicorn)
│   └── asgi.py          # ASGI entry point
├── accounts/            # User authentication app
│   ├── views.py         # Registration endpoint
│   ├── serializers.py   # Registration + auto-role assignment
│   ├── urls.py          # Auth routes (/register, /login, /refresh)
│   ├── admin.py         # Custom User admin display
│   └── management/commands/setup_roles.py  # Creates Admin/User groups
├── tasks/               # Task management app
│   ├── models.py        # Task model
│   ├── views.py         # TaskViewSet (full CRUD)
│   ├── serializers.py   # Task serializer
│   ├── permissions.py   # IsAdminUser, IsOwnerOrAdmin
│   ├── urls.py          # Task routes (via DRF router)
│   └── admin.py         # Task admin display
├── docs/                # Module documentation
├── Dockerfile           # Production image (gunicorn)
├── docker-compose.yml   # Web service with SQLite volume
├── entrypoint.sh        # Init: migrate + setup_roles → exec CMD
└── .env                 # Environment variables (gitignored)
```

## Request Lifecycle

```
Client → HTTP Request
  → Nginx (reverse proxy, in production)
    → gunicorn (WSGI server, 4 workers)
      → Django middleware stack
        → URL router (config/urls.py)
          → View/TaskViewSet
            → Permission check (IsAuthenticated + IsOwnerOrAdmin)
              → Serializer (validate/deserialize)
                → Database (SQLite)
```

## Data Flow

1. **Authentication**: User registers → JWT tokens issued → tokens sent in `Authorization: Bearer` header for all subsequent requests
2. **Task CRUD**: Authenticated request → role-based queryset filtering → permission check → serialization → response
3. **Role Enforcement**: `get_queryset()` limits visible records; `IsOwnerOrAdmin` enforces object-level access
