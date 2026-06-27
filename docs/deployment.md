# Deployment Guide

## Docker Setup

The project uses a single Docker service defined in `docker-compose.yml`:

### Web Service (`web`)

- **Build**: From `Dockerfile` — dependencies installed, code baked into image
- **Server**: gunicorn with 4 workers
- **Port**: `8000:8000`
- **Database**: SQLite persisted via a named Docker volume (`sqlite_data`)
- **Init**: `entrypoint.sh` runs migrations + role setup before starting gunicorn

## Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
```

## Entrypoint Script (`entrypoint.sh`)

```bash
#!/bin/sh
set -e
python manage.py migrate --noinput
python manage.py setup_roles
python manage.py collectstatic --noinput
exec "$@"
```

Runs before gunicorn starts. Use `docker compose run --rm web python manage.py <command>` for one-off commands.

## Environment Variables

See [README](../README.md#production-deployment) for required variables.

### `.env` template (`.env.example`)

```
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*
```

## Production Checklist

Before deploying to production:

1. Set `DJANGO_DEBUG=False`
2. Set `DJANGO_ALLOWED_HOSTS` to your domain(s)
3. Generate a strong `DJANGO_SECRET_KEY`
4. Add a reverse proxy (nginx) in front of gunicorn
5. Serve static files via nginx or whitenoise
