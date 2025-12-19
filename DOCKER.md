# Docker Deployment Guide

This guide explains how to build and run the F1 Betting Pool application using Docker.

## Overview

The application uses a multi-stage Docker build process:

1. **Stage 1 (node-builder)**: Builds Tailwind CSS from source
2. **Stage 2 (python-builder)**: Installs Python dependencies
3. **Stage 3 (runtime)**: Creates minimal production image

This approach ensures:
- Tailwind CSS is built for production (minified)
- Smaller final image size
- No development dependencies in production
- Secure non-root user execution

## Prerequisites

- Docker 20.10 or higher
- Docker Compose 2.0 or higher (optional, for docker-compose.yml)

## Quick Start

### Using Docker Compose (Recommended)

1. **Create environment file**:
```bash
cp .env.example .env
# Edit .env and set required variables
```

2. **Start services**:
```bash
docker-compose up -d
```

3. **Check status**:
```bash
docker-compose ps
docker-compose logs -f web
```

4. **Stop services**:
```bash
docker-compose down
```

### Using Docker CLI

1. **Build the image**:
```bash
docker build -t f1betting:latest .
```

2. **Run the container**:
```bash
docker run -d \
  --name f1betting-web \
  -p 8000:8000 \
  --env-file .env \
  f1betting:latest
```

3. **View logs**:
```bash
docker logs -f f1betting-web
```

4. **Stop container**:
```bash
docker stop f1betting-web
docker rm f1betting-web
```

## Build Process Explained

### Multi-Stage Build

The Dockerfile uses three stages to optimize the build:

#### Stage 1: Node.js Builder
```dockerfile
FROM node:20-alpine as node-builder
```
- Installs Node.js dependencies from package.json
- Copies Tailwind configuration and CSS source files
- Runs `npm run build:css` to generate production CSS
- Output: `static/css/output.css` (minified)

#### Stage 2: Python Builder
```dockerfile
FROM python:3.12-slim as python-builder
```
- Installs Python dependencies from requirements.txt
- Uses pip's `--user` flag for isolated installation
- Output: Python packages in `/root/.local`

#### Stage 3: Runtime
```dockerfile
FROM python:3.12-slim
```
- Minimal base image with only runtime dependencies
- Copies Python packages from Stage 2
- Copies built CSS from Stage 1
- Copies application code
- Runs Django's `collectstatic` command
- Executes as non-root user (appuser)

### Build Arguments

You can customize the build with build arguments:

```bash
docker build \
  --build-arg VERSION=1.0.0 \
  -t f1betting:1.0.0 \
  .
```

## Environment Variables

Required environment variables (set in `.env`):

### Database
```env
POSTGRES_DB=f1betting
POSTGRES_USER=f1user
POSTGRES_PASSWORD=your_secure_password
DATABASE_URL=postgresql://f1user:your_secure_password@db:5432/f1betting
```

### Django
```env
SECRET_KEY=your_secret_key_here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
```

### Optional
```env
GUNICORN_WORKERS=4
```

## Docker Compose Services

### Database Service (db)
- **Image**: PostgreSQL 15 Alpine
- **Health Check**: Checks database readiness
- **Volume**: Persistent data storage
- **Network**: f1betting-network

### Web Service (web)
- **Build**: From local Dockerfile
- **Depends On**: Database with health check
- **Ports**: 8000:8000
- **Health Check**: HTTP request to /health/
- **Command**: Runs migrations + Gunicorn

## Production Deployment

### Building for Production

1. **Set production environment**:
```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
SECURE_SSL_REDIRECT=True
```

2. **Build with version tag**:
```bash
docker build -t f1betting:1.0.0 .
docker tag f1betting:1.0.0 f1betting:latest
```

3. **Push to registry** (if using):
```bash
docker tag f1betting:1.0.0 your-registry/f1betting:1.0.0
docker push your-registry/f1betting:1.0.0
```

### Running in Production

Use docker-compose with production settings:

```bash
# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Scale web workers (if needed)
docker-compose up -d --scale web=3
```

## Maintenance Commands

### Database Migrations

Run inside container:
```bash
docker-compose exec web python manage.py migrate
```

Or via docker run:
```bash
docker run --rm --env-file .env f1betting:latest \
  python manage.py migrate
```

### Create Superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

### Collect Static Files

Already done during build, but can be run manually:
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Shell Access

Django shell:
```bash
docker-compose exec web python manage.py shell
```

Bash shell:
```bash
docker-compose exec web bash
```

Database shell:
```bash
docker-compose exec db psql -U f1user -d f1betting
```

## Tailwind CSS in Docker

The Tailwind CSS build is integrated into the Docker build process:

### How It Works

1. **Build Stage**: Node.js container builds CSS
   ```bash
   npm run build:css
   ```
   This creates `static/css/output.css` (minified)

2. **Copy to Runtime**: Built CSS is copied to final image
   ```dockerfile
   COPY --from=node-builder /build/static/css/output.css /app/static/css/output.css
   ```

3. **Collect Static**: Django collects to staticfiles/
   ```bash
   python manage.py collectstatic
   ```

### Updating Styles

To update Tailwind CSS in production:

1. Modify `static/css/input.css` or templates locally
2. Rebuild the Docker image
3. Deploy new image

The CSS will be automatically rebuilt during the Docker build process.

## Health Checks

### Web Service Health Check
- **Endpoint**: `http://localhost:8000/health/`
- **Interval**: 30 seconds
- **Timeout**: 10 seconds
- **Retries**: 3
- **Start Period**: 40 seconds

### Database Health Check
- **Command**: `pg_isready`
- **Interval**: 10 seconds
- **Timeout**: 5 seconds
- **Retries**: 5

## Troubleshooting

### Container Won't Start

Check logs:
```bash
docker-compose logs web
```

Common issues:
- Missing environment variables
- Database not ready (wait for health check)
- Port 8000 already in use

### Database Connection Failed

1. Check database is running:
```bash
docker-compose ps db
```

2. Verify environment variables:
```bash
docker-compose exec web env | grep DATABASE
```

3. Test database connection:
```bash
docker-compose exec db psql -U f1user -d f1betting -c "SELECT 1;"
```

### CSS Not Loading

1. Check if output.css exists:
```bash
docker-compose exec web ls -la static/css/
```

2. Verify static files were collected:
```bash
docker-compose exec web ls -la staticfiles/css/
```

3. Rebuild image to regenerate CSS:
```bash
docker-compose build --no-cache
```

### Permission Issues

The container runs as non-root user (appuser, UID 1000). If you have permission issues:

1. Check file ownership in container:
```bash
docker-compose exec web ls -la
```

2. Rebuild with correct permissions (already set in Dockerfile)

## Performance Optimization

### Build Cache

Use BuildKit for faster builds:
```bash
DOCKER_BUILDKIT=1 docker build -t f1betting:latest .
```

### Image Size

Current multi-stage build optimizations:
- Node.js dependencies not in final image
- Only production Python packages
- Alpine base for Node (smaller)
- Slim base for Python (smaller than full)
- No test files or development tools

Check image size:
```bash
docker images f1betting
```

### Resource Limits

Set in docker-compose.yml:
```yaml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

## Security Best Practices

✅ **Implemented**:
- Non-root user (appuser)
- Multi-stage build (no build tools in production)
- Health checks
- Minimal base images
- .dockerignore excludes sensitive files
- Environment variables for secrets

🔒 **Recommended**:
- Use Docker secrets for sensitive data
- Scan images for vulnerabilities
- Keep base images updated
- Use specific image tags (not :latest in production)
- Enable Docker content trust

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Build image
        run: docker build -t f1betting:${{ github.sha }} .

      - name: Test image
        run: |
          docker run --rm f1betting:${{ github.sha }} python manage.py check
```

## Monitoring

### Container Stats

```bash
# Real-time stats
docker stats f1betting-web

# With docker-compose
docker-compose stats
```

### Application Logs

```bash
# Follow logs
docker-compose logs -f web

# Last 100 lines
docker-compose logs --tail=100 web

# Specific time range
docker-compose logs --since 1h web
```

## Backup and Restore

### Database Backup

```bash
docker-compose exec db pg_dump -U f1user f1betting > backup.sql
```

### Database Restore

```bash
docker-compose exec -T db psql -U f1user f1betting < backup.sql
```

### Volume Backup

```bash
docker run --rm -v f1betting_postgres_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/db-backup.tar.gz -C /data .
```

## Further Reading

- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Tailwind CSS Production Build](https://tailwindcss.com/docs/optimizing-for-production)
