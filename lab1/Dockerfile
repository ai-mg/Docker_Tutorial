# Lab 1 — Containerize the iris API.
#
# This Dockerfile has 6 issues. Fix them so that:
#   docker build -t iris-api .
#   docker run -p 8000:8000 iris-api
# starts the API and `curl http://localhost:8000/health` returns ok.
#
# Refer to the slides / cheatsheet. There is a working reference in
# ../solution/Dockerfile if you get stuck — but try first.

# TODO 1: Pick a sensible base image. `python` (default tag) is ~1 GB.
#         Choose a slim variant.
FROM python

# TODO 2: Set a working directory. Without one, COPY lands in / and that's
#         a mess.

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /build

# Install build deps only in the builder layer.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# TODO 3: We want pip to NOT cache wheels (smaller image) and Python to
#         NOT write .pyc files (cleaner image). Set the right ENV vars.

# TODO 4: Copy ONLY requirements.txt first, then `pip install`. This is
#         the layer-caching trick — code changes won't re-run pip.
#         Then copy the rest of the source.
COPY . .
RUN pip install -r requirements.txt

# TODO 5: Train the model at build time so it ends up baked into the image.
#         (Hint: `python -m app.train`)

# Document the port the app listens on.
EXPOSE 8000

# TODO 6: Start uvicorn. The container needs to listen on 0.0.0.0, not
#         the default 127.0.0.1, otherwise the host can't reach it.
CMD ["python", "-m", "app.main"]
