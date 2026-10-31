# Multi-stage Dockerfile with non-root user and HEALTHCHECK
# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt || true

# Stage 2: Final Runtime
FROM python:3.11-slim AS runtime

WORKDIR /app

# Create a non-root user for security
RUN adduser --disabled-password --gecos "" appuser

# Install curl for HEALTHCHECK
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /home/appuser/.local
COPY src/ /app/src/

ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONPATH=/app/src

# Set non-root user
USER appuser

# Healthcheck configuration
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]