# ==============================================================================
# F1 Betting Pool - Production Dockerfile
# ==============================================================================
# Multi-stage build for smaller, more secure production images
# Test files and development dependencies are excluded

# Stage 1: Node.js Builder - Build Tailwind CSS
FROM node:20-alpine as node-builder

WORKDIR /build

# Copy package files
COPY package.json package-lock.json* ./

# Install Node dependencies
RUN npm ci --only=production || npm install

# Copy Tailwind configuration and source files
COPY tailwind.config.js postcss.config.js ./
COPY static/css/input.css ./static/css/
COPY templates ./templates

# Build Tailwind CSS for production
RUN npm run build:css

# Stage 2: Python Builder - Install dependencies
FROM python:3.12-slim as python-builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Install system dependencies required for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install production dependencies only
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 3: Runtime - Minimal production image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/home/appuser/.local/bin:$PATH

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app /app/staticfiles /app/media && \
    chown -R appuser:appuser /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python packages from python-builder
COPY --from=python-builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copy application code (excluding tests via .dockerignore)
COPY --chown=appuser:appuser . .

# Copy built Tailwind CSS from node-builder
COPY --from=node-builder --chown=appuser:appuser /build/static/css/output.css /app/static/css/output.css

# Switch to non-root user
USER appuser

# Collect static files (use base settings to avoid requiring production env vars at build time)
RUN python manage.py collectstatic --noinput --settings=f1betting.settings.base

# Expose port
EXPOSE 8000

# Health check (using dedicated endpoint for better reliability)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "from urllib.request import urlopen; urlopen('http://localhost:8000/health/', timeout=5)" || exit 1

# Run gunicorn
CMD ["gunicorn", "f1betting.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info"]
