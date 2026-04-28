# syntax=docker/dockerfile:1.7
# ----------------------------------------------------------------------------
# Stage 1: builder — install deps and train the model.
# Heavy build-time tools (gcc, etc.) live here and never reach the final image.
# ----------------------------------------------------------------------------
FROM python:3.12-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /build

# Install build deps only in the builder layer.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first so Docker can cache the pip install layer
# when only application code changes.
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Copy source and train the model. The artifact (model.joblib) lands
# next to train.py and will be copied into the runtime stage.
COPY app/ ./app/
RUN python -m app.train

# ----------------------------------------------------------------------------
# Stage 2: runtime — slim, no build tools, runs as non-root.
# ----------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/home/appuser/.local/bin:$PATH \
    MODEL_PATH=/app/model.joblib

# Create an unprivileged user to run the app.
RUN groupadd --system app && useradd --system --gid app --create-home appuser

WORKDIR /app

# Bring over installed Python packages from the builder.
COPY --from=builder /root/.local /home/appuser/.local
# Bring over app code + trained model.
COPY --from=builder /build/app /app/app
COPY --from=builder /build/app/model.joblib /app/model.joblib

RUN chown -R appuser:app /app /home/appuser/.local

USER appuser

EXPOSE 8000

# Healthcheck used by docker-compose to gate dependent services.
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
