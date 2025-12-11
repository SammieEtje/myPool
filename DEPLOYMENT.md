# Deployment Guide - F1 Betting Pool

## Overview

This guide covers deploying the F1 Betting Pool using **immutable Docker builds**. Test files, development dependencies, and test data are automatically excluded from production deployments.

## Deployment Features

✅ **Immutable builds** - Docker images are built once and deployed anywhere
✅ **No test files** - Automatically excluded via `.dockerignore`
✅ **No test data** - Production doesn't run seed commands
✅ **Multi-stage builds** - Smaller, more secure images
✅ **Non-root user** - Enhanced security
✅ **Health checks** - Automatic container monitoring
✅ **CI/CD automated** - Builds on every merge to main

## Quick Start - Docker Compose

### 1. Prepare Environment Variables

```bash
# Copy the template and fill in your values
cp .env.production.template .env.production

# Edit with your production values
nano .env.production
```

**Critical settings to change:**
- `SECRET_KEY` - Generate a new random key
- `POSTGRES_PASSWORD` - Strong database password
- `ALLOWED_HOSTS` - Your domain name
- `EMAIL_*` - Your email provider credentials

### 2. Build and Deploy

```bash
# Build the immutable Docker image
docker-compose build

# Start services
docker-compose --env-file .env.production up -d

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Check logs
docker-compose logs -f web
```

### 3. Access Your Application

```
http://your-domain.com:8000
```

## Production Deployment Options

### Option 1: GitHub Container Registry (Recommended)

The CI/CD pipeline automatically builds and pushes images to GitHub Container Registry on every merge to `main`.

**1. Pull the latest image:**
```bash
docker pull ghcr.io/sammieenje/mypool:latest
```

**2. Run with Docker Compose:**
```yaml
services:
  web:
    image: ghcr.io/sammieenje/mypool:latest
    # ... rest of config
```

**3. Deploy:**
```bash
docker-compose --env-file .env.production up -d
```

### Option 2: Azure Container Registry

**1. Create Azure Container Registry:**
```bash
az acr create \
  --resource-group myResourceGroup \
  --name f1bettingregistry \
  --sku Basic
```

**2. Build and push:**
```bash
# Login
az acr login --name f1bettingregistry

# Build with tag
docker build -t f1bettingregistry.azurecr.io/f1betting:v1.0.0 .

# Push
docker push f1bettingregistry.azurecr.io/f1betting:v1.0.0
```

**3. Deploy to Azure Container Instances:**
```bash
az container create \
  --resource-group myResourceGroup \
  --name f1betting-app \
  --image f1bettingregistry.azurecr.io/f1betting:v1.0.0 \
  --cpu 2 \
  --memory 4 \
  --registry-login-server f1bettingregistry.azurecr.io \
  --registry-username <username> \
  --registry-password <password> \
  --dns-name-label f1betting \
  --ports 8000 \
  --environment-variables \
    SECRET_KEY='your-secret-key' \
    DEBUG='False' \
    ALLOWED_HOSTS='f1betting.azurecontainer.io'
```

### Option 3: Azure App Service (Container)

**1. Create App Service Plan:**
```bash
az appservice plan create \
  --name f1betting-plan \
  --resource-group myResourceGroup \
  --is-linux \
  --sku B1
```

**2. Create Web App:**
```bash
az webapp create \
  --resource-group myResourceGroup \
  --plan f1betting-plan \
  --name f1betting \
  --deployment-container-image-name ghcr.io/sammieenje/mypool:latest
```

**3. Configure environment variables:**
```bash
az webapp config appsettings set \
  --resource-group myResourceGroup \
  --name f1betting \
  --settings \
    SECRET_KEY='your-secret-key' \
    DEBUG='False' \
    ALLOWED_HOSTS='f1betting.azurewebsites.net' \
    WEBSITES_PORT=8000
```

## What's Excluded from Production Builds

The `.dockerignore` file excludes:

### Test Files
- `**/tests/` - All test directories
- `**/test_*.py` - All test files
- `pytest.ini`, `.pytest_cache/` - Pytest configuration
- `.coverage`, `coverage.xml` - Coverage reports

### Development Files
- `requirements-dev.txt` - Dev dependencies
- `.env.development` - Dev environment
- `.vscode/`, `.idea/` - IDE configurations

### Documentation
- `*.md` files (README, guides, etc.)
- Reduces image size significantly

### Build Artifacts
- `__pycache__/`, `*.pyc` - Python cache
- `*.sqlite3` - Local database files
- `.git/` - Git history

## Database Migrations

**Always run migrations after deploying:**

```bash
# With Docker Compose
docker-compose exec web python manage.py migrate

# Direct container
docker exec -it f1betting-web python manage.py migrate
```

## Static Files

Static files are collected during Docker build:

```dockerfile
RUN python manage.py collectstatic --noinput
```

For better performance, serve static files with nginx or Azure CDN.

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | ✅ Yes | - | Django secret key |
| `DEBUG` | ✅ Yes | False | Must be False in production |
| `ALLOWED_HOSTS` | ✅ Yes | - | Comma-separated domains |
| `DATABASE_URL` | No | SQLite | PostgreSQL connection string |
| `EMAIL_HOST` | No | - | SMTP server |
| `EMAIL_PORT` | No | 587 | SMTP port |
| `EMAIL_HOST_USER` | No | - | SMTP username |
| `EMAIL_HOST_PASSWORD` | No | - | SMTP password |

## Security Checklist

Before deploying to production:

- [ ] `DEBUG=False` in environment
- [ ] Strong random `SECRET_KEY` generated
- [ ] `ALLOWED_HOSTS` configured with your domain
- [ ] PostgreSQL database (not SQLite)
- [ ] Email backend configured for MFA
- [ ] HTTPS/SSL certificates installed
- [ ] Database backups configured
- [ ] Container health checks working
- [ ] No test data in production database
- [ ] Secrets stored securely (Azure Key Vault, etc.)

## Monitoring

**Check application health:**
```bash
curl http://your-domain:8000/admin/
```

**View logs:**
```bash
docker-compose logs -f web
```

**Check container status:**
```bash
docker-compose ps
```

## Rollback

If something goes wrong:

```bash
# Stop current version
docker-compose down

# Pull previous version
docker pull ghcr.io/sammieenje/mypool:v1.0.0

# Update docker-compose.yml with previous tag
# Then restart
docker-compose up -d
```

## Troubleshooting

**Container won't start:**
```bash
# Check logs
docker-compose logs web

# Verify environment variables
docker-compose config
```

**Database connection errors:**
```bash
# Check database is running
docker-compose ps db

# Test connection
docker-compose exec web python manage.py check --database default
```

**Static files not loading:**
```bash
# Rebuild image to recollect static files
docker-compose build --no-cache web
docker-compose up -d
```

## CI/CD Pipeline

The GitHub Actions workflow automatically:

1. ✅ Runs tests
2. ✅ Checks code quality
3. ✅ Builds Docker image
4. ✅ Pushes to GitHub Container Registry
5. ✅ Tags with version and SHA

**Image tags created:**
- `latest` - Latest from main branch
- `main` - Main branch builds
- `sha-<commit>` - Specific commit
- `v1.0.0` - Semantic versioning (if tagged)

## Scaling

**Increase workers:**
```yaml
services:
  web:
    deploy:
      replicas: 3
```

**Use load balancer:**
- Add nginx service (included in docker-compose.yml)
- Configure nginx for load balancing
- Enable with: `docker-compose --profile production up`

## Support

For deployment issues, check:
- Container logs: `docker-compose logs`
- Health checks: `docker inspect <container>`
- GitHub Actions: Check build logs
- Azure Portal: Container insights

---

**Your production deployment is now fully automated, secure, and immutable!** 🎉
