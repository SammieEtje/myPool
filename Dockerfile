# ==============================================================================
# F1 Betting Pool - Production Dockerfile
# ==============================================================================
# Multi-stage build for smaller, more secure production images
# Test files and development dependencies are excluded

# Build arguments for version control
ARG PYTHON_VERSION=3.12.8
ARG NODE_VERSION=20.18.1

# Stage 1: Node.js Builder - Build Tailwind CSS
FROM node:${NODE_VERSION}-alpine AS node-builder

WORKDIR /build

# Copy package files
COPY package.json package-lock.json* ./

# Install Node dependencies
# RUN npm ci --only=production || npm install
RUN if [ -f package-lock.json ]; then npm ci --omit=dev; else npm install --production; fi


# Copy Tailwind configuration and source files
COPY tailwind.config.js postcss.config.js ./
COPY static/css/input.css ./static/css/
COPY templates ./templates

# Build Tailwind CSS for production
RUN npm run build:css

# Stage 2: Python Builder - Install dependencies
FROM python:${PYTHON_VERSION}-slim AS python-builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install production dependencies only
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 3: Runtime - Minimal production image
FROM python:${PYTHON_VERSION}-slim

# Metadata labels
LABEL org.opencontainers.image.title="F1 Betting Pool"
LABEL org.opencontainers.image.description="F1 race prediction and betting pool application"
LABEL org.opencontainers.image.vendor="F1 Betting Pool Team"
LABEL org.opencontainers.image.source="https://github.com/yourusername/myPool"
LABEL maintainer="your-email@example.com"

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
    curl \
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

# Health check (using curl for better reliability)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Default environment variables for gunicorn (can be overridden at runtime)
ENV GUNICORN_WORKERS=4 \
    GUNICORN_TIMEOUT=60 \
    GUNICORN_LOG_LEVEL=info

# Run gunicorn with environment variable support
CMD gunicorn f1betting.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers ${GUNICORN_WORKERS} \
    --timeout ${GUNICORN_TIMEOUT} \
    --access-logfile - \
    --error-logfile - \
    --log-level ${GUNICORN_LOG_LEVEL}
