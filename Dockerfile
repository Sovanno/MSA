FROM python:3.11.13-alpine3.21

WORKDIR /app

# Install system dependencies including PostgreSQL client for migrations
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    postgresql-client \
    python3-dev \
    curl \
    libpq

# Copy requirements and install dependencies globally
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code including alembic
COPY . .

# Create non-root user and fix permissions
RUN addgroup -S appuser && adduser -S appuser -G appuser \
    && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run migrations and then start the application
CMD sh -c "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"