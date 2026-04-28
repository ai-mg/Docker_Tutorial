# Iris Classifier — Lab Starter

This is the starting point for the in-class labs. The Python code (`app/`,
`requirements.txt`, `tests/`) is complete and works. The Docker setup is
intentionally broken — your job across the three labs is to fix it.

## What you'll build

A FastAPI service that classifies iris flowers using scikit-learn, logs every
prediction to a Postgres database, and runs as a multi-container stack via
docker-compose, packaged in an optimized multi-stage image running as a
non-root user.

## The labs

### Lab 0.5 — Build your first tiny image (~10 min)
Open `hello-docker/`. Two files, five lines. Build and run:

```bash
cd hello-docker
docker build -t hello-docker .
docker run --rm hello-docker
```

You should see `Hello from inside a container!`. Then change the message in
`app.py`, rebuild, and watch which layers are cached.

### Lab 1 — Containerize the API (~40 min)
Open `Dockerfile`. Find and fix six TODO markers. Then build and run:

```bash
docker build -t iris-api .
docker run -p 8000:8000 iris-api
curl http://localhost:8000/health
```

### Lab 2 — Add Postgres with docker-compose (~50 min)
Open `docker-compose.yml`. Wire the API up to a Postgres service so
predictions are logged. Six TODOs to address.

```bash
docker compose up --build
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}'
curl http://localhost:8000/predictions
```

### Lab 3 — Optimize with multi-stage + non-root (~35 min)
Note your current image size:
```bash
docker images iris-api
```
Then refactor `Dockerfile` using the template in `Dockerfile.lab3` so the
runtime image drops to ~250 MB and runs as `appuser`. Verify:
```bash
docker images iris-api          # should be ~4× smaller
docker compose exec api whoami  # should print "appuser"
```

## If you get stuck

The full reference implementation is in `../solution/`. Try the lab first —
you'll learn far more from a 5-minute struggle than from copy-pasting.

## Useful commands

```bash
docker compose up --build       # build + start
docker compose up -d            # detached
docker compose logs -f api      # tail logs
docker compose exec api bash    # shell into the running API
docker compose down             # stop (volumes survive)
docker compose down -v          # stop + delete the DB volume
docker images                   # list images
docker ps                       # list running containers
docker system df                # see what's using disk
```
