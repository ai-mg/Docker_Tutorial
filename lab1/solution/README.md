# Iris Classifier — Solution Reference

Reference implementation for the Docker class lab. A FastAPI service serving a
scikit-learn iris classifier, with prediction logging to Postgres, wired up via
docker-compose.

## What this demonstrates

- **Multi-stage build** — heavy build tools live in the builder stage; the
  runtime stage is slim.
- **Layer caching** — `requirements.txt` is copied before app code so pip
  installs aren't re-run on every code change.
- **Non-root user** — the runtime stage drops to `appuser`.
- **Healthchecks** — both the API and Postgres expose health probes; compose
  uses `depends_on: condition: service_healthy` so the API waits for the DB.
- **Named volumes** — `db_data` survives `docker compose down`; only `down -v`
  destroys it.
- **Service discovery via DNS** — the API connects to the DB at hostname `db`
  on the user-defined network compose creates automatically.

## Quick start

```bash
docker compose up --build
```

Then in another terminal:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'

curl http://localhost:8000/predictions
```

Or open the auto-generated docs at <http://localhost:8000/docs>.

## File map

| Path | Purpose |
|---|---|
| `app/train.py` | Trains the iris classifier and writes `model.joblib`. |
| `app/main.py` | FastAPI app: `/health`, `/predict`, `/predictions`. |
| `Dockerfile` | Multi-stage build (builder → runtime). |
| `docker-compose.yml` | Two services: `api` + `db`. |
| `.dockerignore` | Keeps build context lean. |
| `Makefile` | Common commands wrapped for convenience. |
| `tests/test_api.py` | Smoke tests against the running stack. |

## Common operations

```bash
make build       # docker compose build
make up          # start in background
make logs        # tail API logs
make shell       # exec a shell in the API container
make predict     # send a sample prediction
make down        # stop the stack (DB volume survives)
make clean       # stop AND wipe the DB volume + image
```

## Image size check

After building, compare image sizes:

```bash
docker images iris-api
docker history iris-api:latest
```

The runtime image should be roughly 200–250 MB. A naive single-stage build with
`python:3.12` (not slim) and `build-essential` left in would push that past
1 GB.
