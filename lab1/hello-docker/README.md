# Lab 0.5 — Build your first image

Two files, five lines, your first Docker image.

## Steps

```bash
cd hello-docker
docker build -t hello-docker .
docker run --rm hello-docker
# Hello from inside a container!
```

## Then play with it

1. Edit `app.py`. change the message.
2. Rebuild: `docker build -t hello-docker .`
3. Watch which layers are CACHED and which RUN. The `FROM`, `WORKDIR`, and `COPY app.py` layers cached the first time; only the changed file invalidates.
4. List the image: `docker images hello-docker`. Note the size (it's mostly the python:3.12-slim base).

## What each line does

| Instruction | Purpose |
|---|---|
| `FROM python:3.12-slim` | base image. provides the Python interpreter. |
| `WORKDIR /app` | cd into `/app` inside the image, creates it if missing. |
| `COPY app.py .` | put `app.py` from your folder into `/app/` in the image. |
| `CMD ["python", "app.py"]` | what runs when you `docker run` the image. |

## What's next

Lab 1 takes the same shape and applies it to a real FastAPI app with dependencies.
