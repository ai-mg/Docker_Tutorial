# Docker for Complete Beginners

## 1. What Docker is

Docker is a tool for packaging and running applications in isolated environments called **containers**.

A container includes:

- Your application code
- The runtime, for example Python, Node.js, Java
- Dependencies and libraries
- System tools needed by the app
- A default command to start the app

The main benefit is:

> If it runs in the container on your machine, it should run the same way on another machine.

This helps solve the classic problem:

> “It works on my machine.”

---

## 2. The problem Docker solves

Imagine you build a Python app.

Your app needs:

- Python 3.12
- FastAPI
- Uvicorn
- Pandas
- A certain operating system library
- A Postgres database

Without Docker, every developer or server must install the right versions manually.

That often causes problems:

- One person has Python 3.10, another has Python 3.12
- Someone forgot to install a dependency
- The production server behaves differently from your laptop
- Updating one project breaks another project
- Databases and services are painful to install locally

Docker solves this by packaging the environment.

Instead of saying:

```text
Please install Python, install these packages, configure Postgres, set up paths...
```

You say:

```bash
docker compose up
```

And the app starts in the same way for everyone.

---

# 3. Core Docker concepts

Docker has three concepts you must understand first:

| Concept | Meaning | Analogy |
|---|---|---|
| **Image** | A packaged template for an application | A recipe or blueprint |
| **Container** | A running instance of an image | A cooked meal from the recipe |
| **Registry** | A place where images are stored | GitHub for Docker images |

---

## 3.1 Image

An **image** is a read-only package that contains everything needed to run something.

Example images:

```text
python:3.12-slim
nginx:alpine
postgres:16
ubuntu:24.04
redis:7
```

You can download images from Docker Hub:

```bash
docker pull python:3.12-slim
```

---

## 3.2 Container

A **container** is a running instance of an image.

If an image is like a class, a container is like an object.

Example:

```bash
docker run python:3.12-slim python --version
```

This command:

1. Downloads the Python image if needed
2. Creates a container from it
3. Runs `python --version`
4. Stops the container when the command finishes

---

## 3.3 Registry

A **registry** stores images.

Popular registries include:

- Docker Hub
- GitHub Container Registry
- Amazon Elastic Container Registry
- Google Artifact Registry
- Azure Container Registry

When you run:

```bash
docker pull python:3.12-slim
```

Docker downloads that image from a registry.

When you run:

```bash
docker push my-image
```

Docker uploads your image to a registry.

---

# 4. Docker mental model

```mermaid
flowchart TD
    D[Dockerfile] --> I[Docker image]
    I --> C1[Container one]
    I --> C2[Container two]
    I --> C3[Container three]
    R[Registry] --> I
    I --> R
```

A typical workflow is:

```text
Write Dockerfile
Build image
Run container
Push image to registry
Pull image on server
Run container in production
```

---

# 5. Installing Docker

For most beginners, install **Docker Desktop**.

Download it from:

```text
https://www.docker.com/products/docker-desktop/
```

After installing, test:

```bash
docker version
docker info
docker run hello-world
```

If this works, Docker is ready.

---

# 6. Your first Docker commands

## 6.1 Run hello-world

```bash
docker run hello-world
```

This checks whether Docker can:

1. Contact Docker Hub
2. Download an image
3. Create a container
4. Run the container

---

## 6.2 Run Python without installing Python locally

```bash
docker run -it --rm python:3.12-slim python
```

You will enter a Python shell:

```python
print("Hello from Docker")
```

Exit with:

```python
exit()
```

Important flags:

| Flag | Meaning |
|---|---|
| `-it` | Interactive terminal |
| `--rm` | Remove the container after it exits |
| `python:3.12-slim` | Image name |
| `python` | Command to run inside the container |

---

## 6.3 List images

```bash
docker images
```

Shows images downloaded or built on your machine.

---

## 6.4 List running containers

```bash
docker ps
```

Shows currently running containers.

---

## 6.5 List all containers

```bash
docker ps -a
```

Shows running and stopped containers.

---

# 7. Running containers

## 7.1 Run a container in the foreground

```bash
docker run nginx
```

This starts Nginx, but your terminal is attached to it.

Stop it with:

```text
Ctrl + C
```

---

## 7.2 Run a container in the background

```bash
docker run -d nginx
```

The `-d` means detached mode.

Docker returns a container ID.

---

## 7.3 Give a container a name

```bash
docker run -d --name my-nginx nginx
```

Now you can refer to it as `my-nginx`.

---

## 7.4 Stop a container

```bash
docker stop my-nginx
```

---

## 7.5 Remove a container

```bash
docker rm my-nginx
```

If it is still running:

```bash
docker rm -f my-nginx
```

---

# 8. Port mapping

Containers have their own internal network.

If a web server inside a container listens on port `80`, that does **not** automatically make it available on your laptop.

You must map a host port to a container port.

Example:

```bash
docker run -d --name web -p 8080:80 nginx
```

This means:

```text
localhost:8080 on your laptop
goes to
port 80 inside the container
```

Open:

```text
http://localhost:8080
```

Port syntax:

```bash
-p HOST_PORT:CONTAINER_PORT
```

Example:

```bash
-p 8000:8000
-p 8080:80
-p 5432:5432
```

---

# 9. Logs and debugging

## 9.1 View logs

```bash
docker logs web
```

Follow logs live:

```bash
docker logs -f web
```

---

## 9.2 Execute a command inside a running container

```bash
docker exec -it web sh
```

This opens a shell inside the container.

For some containers, use `bash`:

```bash
docker exec -it my-container bash
```

For minimal images, `sh` is more likely to work:

```bash
docker exec -it my-container sh
```

---

## 9.3 Inspect a container

```bash
docker inspect web
```

This shows detailed JSON information about the container.

---

# 10. Building your first Docker image

Now let us build our own image.

Create a folder:

```bash
mkdir hello-docker
cd hello-docker
```

Create a file called `app.py`:

```python
print("Hello from my own Docker image")
```

Create a file called `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app.py .

CMD ["python", "app.py"]
```

Build the image:

```bash
docker build -t hello-docker .
```

Run it:

```bash
docker run hello-docker
```

You should see:

```text
Hello from my own Docker image
```

---

# 11. Understanding the Dockerfile

A **Dockerfile** is a recipe for building a Docker image.

Example:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app.py .

CMD ["python", "app.py"]
```

Line by line:

| Instruction | Meaning |
|---|---|
| `FROM python:3.12-slim` | Start from an existing Python image |
| `WORKDIR /app` | Set working directory inside the image |
| `COPY app.py .` | Copy local `app.py` into the image |
| `CMD ["python", "app.py"]` | Default command when the container starts |

---

# 12. Common Dockerfile instructions

## 12.1 `FROM`

Every Dockerfile usually starts with `FROM`.

```dockerfile
FROM python:3.12-slim
```

This says:

> Build my image on top of the official Python 3.12 slim image.

Other examples:

```dockerfile
FROM node:22-alpine
FROM nginx:alpine
FROM ubuntu:24.04
FROM postgres:16
```

---

## 12.2 `WORKDIR`

```dockerfile
WORKDIR /app
```

This sets the working directory inside the image.

After this, commands run from `/app`.

It is similar to:

```bash
cd /app
```

---

## 12.3 `COPY`

```dockerfile
COPY app.py .
```

Copies files from your computer into the image.

Example:

```dockerfile
COPY requirements.txt .
COPY app/ ./app/
```

---

## 12.4 `RUN`

```dockerfile
RUN pip install -r requirements.txt
```

Runs a command while building the image.

Common examples:

```dockerfile
RUN apt-get update
RUN pip install --no-cache-dir -r requirements.txt
RUN npm install
```

---

## 12.5 `CMD`

```dockerfile
CMD ["python", "app.py"]
```

Defines the default command when a container starts.

Important: use the JSON array form.

Good:

```dockerfile
CMD ["python", "app.py"]
```

Less recommended:

```dockerfile
CMD python app.py
```

---

## 12.6 `EXPOSE`

```dockerfile
EXPOSE 8000
```

This documents that the app listens on port `8000`.

Important:

> `EXPOSE` does not publish the port by itself.

You still need:

```bash
docker run -p 8000:8000 my-image
```

---

## 12.7 `ENV`

```dockerfile
ENV PYTHONUNBUFFERED=1
```

Sets environment variables inside the image.

Example:

```dockerfile
ENV APP_ENV=production
ENV PORT=8000
```

---

# 13. Docker images are built in layers

Each Dockerfile instruction creates a layer.

Example:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app/ ./app/
CMD ["python", "app/main.py"]
```

Docker caches layers.

If nothing changes in a layer, Docker reuses it.

This makes builds faster.

---

## 13.1 Why order matters

Bad Dockerfile:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
```

Problem:

- Every code change invalidates the `COPY . .` layer
- Then Docker must reinstall all dependencies

Better Dockerfile:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

Better because:

- Dependencies are installed first
- Docker only reruns `pip install` when `requirements.txt` changes
- Code changes do not reinstall dependencies

---

# 14. `.dockerignore`

When you build an image, Docker sends the current folder to the Docker daemon.

This is called the **build context**.

If your folder contains unnecessary files, builds become slow and images may accidentally include secrets.

Create a `.dockerignore` file:

```gitignore
__pycache__/
*.pyc
.venv/
.git/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.env
*.db
.vscode/
.idea/
node_modules/
dist/
build/
```

This is similar to `.gitignore`.

Important:

> Never copy secrets into a Docker image.

Avoid including:

- `.env`
- API keys
- SSH keys
- Database dumps
- Private credentials

---

# 15. Container lifecycle

A container has a lifecycle.

```mermaid
flowchart TD
    C[Create container] --> S[Start container]
    S --> R[Running]
    R --> T[Stop container]
    T --> X[Stopped]
    X --> D[Remove container]
```

Common commands:

```bash
docker create image-name
docker start container-name
docker stop container-name
docker restart container-name
docker rm container-name
```

Usually, you use:

```bash
docker run image-name
```

because `docker run` creates and starts a container in one command.

---

# 16. Images versus containers

This is one of the most important distinctions.

## Image

An image is the packaged template.

Example:

```bash
docker images
```

You might see:

```text
python       3.12-slim
nginx        alpine
hello-docker latest
```

## Container

A container is a running or stopped instance of an image.

Example:

```bash
docker ps -a
```

You might see:

```text
hello-docker container exited
nginx container running
```

You can create many containers from one image.

---

# 17. Removing images and containers

## Remove stopped containers

```bash
docker container prune
```

## Remove unused images

```bash
docker image prune
```

## Remove more unused Docker data

```bash
docker system prune
```

More aggressive:

```bash
docker system prune -a
```

Be careful: this removes unused images too.

---

# 18. Volumes and persistence

Containers are meant to be disposable.

If a container writes data inside itself and then you delete the container, the data is gone.

Example:

```bash
docker run -it --name temp python:3.12-slim sh
```

Inside the container:

```bash
echo "important data" > data.txt
exit
```

Remove the container:

```bash
docker rm temp
```

The data is gone.

To persist data, use **volumes**.

---

## 18.1 Named volumes

Create a named volume:

```bash
docker volume create my-data
```

Use it:

```bash
docker run -it --name test -v my-data:/data python:3.12-slim sh
```

Inside the container:

```bash
echo "hello" > /data/file.txt
exit
```

Remove the container:

```bash
docker rm test
```

Start another container with the same volume:

```bash
docker run -it -v my-data:/data python:3.12-slim sh
```

Inside:

```bash
cat /data/file.txt
```

The data is still there.

---

## 18.2 Bind mounts

A bind mount connects a folder on your computer to a folder in the container.

Example:

```bash
docker run -it --rm -v "$(pwd)":/app python:3.12-slim sh
```

This maps your current folder to `/app` inside the container.

Bind mounts are useful for development.

Named volumes are useful for databases.

---

## 18.3 Volumes versus bind mounts

| Feature | Named volume | Bind mount |
|---|---|---|
| Managed by Docker | Yes | No |
| Uses host path directly | No | Yes |
| Good for databases | Yes | Sometimes |
| Good for live development | Sometimes | Yes |
| Easy to move around | Yes | Less so |

---

# 19. Environment variables

Environment variables configure containers at runtime.

Example:

```bash
docker run -e APP_ENV=development my-image
```

Inside the app, you can read `APP_ENV`.

For Python:

```python
import os

app_env = os.getenv("APP_ENV", "production")
```

For databases:

```bash
docker run \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=mypassword \
  -e POSTGRES_DB=mydb \
  postgres:16
```

Important:

> Environment variables are better than hardcoding config into your image.

But do not treat plain environment variables as perfect secret management in serious production systems.

---

# 20. Docker networking

Each container has its own network environment.

A container has its own:

- IP address
- Network interfaces
- Localhost
- Ports

Important beginner mistake:

> `localhost` inside a container means the container itself, not your laptop.

---

## 20.1 Container to host

If your app runs inside a container and needs to reach something on your laptop, `localhost` may not work.

On Docker Desktop, you can often use:

```text
host.docker.internal
```

Example:

```text
http://host.docker.internal:8000
```

---

## 20.2 Container to container

Containers can talk to each other if they are on the same Docker network.

Create a network:

```bash
docker network create app-net
```

Run Postgres:

```bash
docker run -d \
  --name db \
  --network app-net \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=mypassword \
  -e POSTGRES_DB=mydb \
  postgres:16
```

Run another container on the same network:

```bash
docker run -it --rm \
  --network app-net \
  postgres:16 \
  psql -h db -U myuser -d mydb
```

The hostname is:

```text
db
```

because the container is named `db`.

---

# 21. Docker Compose

Docker Compose lets you define multi-container applications in one YAML file.

Instead of running many long `docker run` commands, you write:

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: mydb
```

Then start everything:

```bash
docker compose up
```

Stop everything:

```bash
docker compose down
```

---

# 22. Example Docker Compose project

Project structure:

```text
my-api/
├── app/
│   └── main.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## 22.1 `app/main.py`

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Docker"}

@app.get("/health")
def health():
    return {"status": "ok"}
```

---

## 22.2 `requirements.txt`

```text
fastapi
uvicorn[standard]
```

---

## 22.3 `Dockerfile`

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 22.4 `docker-compose.yml`

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
```

---

## 22.5 Run the project

```bash
docker compose up --build
```

Open:

```text
http://localhost:8000
```

Or test:

```bash
curl http://localhost:8000/health
```

Stop:

```bash
docker compose down
```

---

# 23. Docker Compose with Postgres

A more realistic setup:

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: apppassword
      POSTGRES_DB: appdb
    volumes:
      - db_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  api:
    build: .
    environment:
      DATABASE_URL: postgresql://appuser:apppassword@db:5432/appdb
    ports:
      - "8000:8000"
    depends_on:
      - db

volumes:
  db_data:
```

Important:

- The API connects to Postgres using hostname `db`
- `db` is the Compose service name
- The database data is stored in the named volume `db_data`

---

# 24. `depends_on` warning

This is important.

```yaml
depends_on:
  - db
```

This means:

> Start the `db` container before the `api` container.

But it does **not** mean:

> Wait until Postgres is fully ready.

For that, use a healthcheck.

Better:

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: apppassword
      POSTGRES_DB: appdb
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser -d appdb"]
      interval: 5s
      timeout: 3s
      retries: 10

  api:
    build: .
    depends_on:
      db:
        condition: service_healthy
```

---

# 25. Useful Compose commands

Start services:

```bash
docker compose up
```

Start and rebuild:

```bash
docker compose up --build
```

Start in background:

```bash
docker compose up -d
```

Stop services:

```bash
docker compose down
```

Stop and remove volumes:

```bash
docker compose down -v
```

View logs:

```bash
docker compose logs
```

Follow logs:

```bash
docker compose logs -f
```

View logs for one service:

```bash
docker compose logs -f api
```

Run a shell inside a service:

```bash
docker compose exec api sh
```

List services:

```bash
docker compose ps
```

---

# 26. CMD versus ENTRYPOINT

This confuses many beginners.

## CMD

`CMD` defines the default command.

```dockerfile
CMD ["python", "app.py"]
```

You can override it:

```bash
docker run my-image python other_script.py
```

---

## ENTRYPOINT

`ENTRYPOINT` defines the fixed executable.

```dockerfile
ENTRYPOINT ["python"]
CMD ["app.py"]
```

When you run:

```bash
docker run my-image other_script.py
```

Docker runs:

```bash
python other_script.py
```

Beginner rule:

> Use `CMD` most of the time. Learn `ENTRYPOINT` later when you need fixed command behavior.

---

# 27. Common beginner mistakes

## Mistake 1: App binds to `127.0.0.1`

Inside a container, this is wrong for web apps:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Use:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Why?

`127.0.0.1` means only inside the container.

`0.0.0.0` means listen on all network interfaces inside the container.

---

## Mistake 2: Forgetting port mapping

Wrong:

```bash
docker run my-api
```

The API may be running, but your laptop cannot reach it.

Correct:

```bash
docker run -p 8000:8000 my-api
```

---

## Mistake 3: Thinking containers keep data forever

Containers are disposable.

Use volumes for persistent data.

---

## Mistake 4: Using `localhost` between containers

Wrong:

```text
postgresql://user:pass@localhost:5432/db
```

From inside the API container, `localhost` means the API container itself.

Correct in Compose:

```text
postgresql://user:pass@db:5432/db
```

where `db` is the Compose service name.

---

## Mistake 5: Copying everything into the image

Bad:

```dockerfile
COPY . .
```

without `.dockerignore`.

You may accidentally copy:

- `.git`
- `.env`
- virtual environments
- datasets
- secrets
- cache folders

Use `.dockerignore`.

---

## Mistake 6: Reinstalling dependencies on every build

Bad:

```dockerfile
COPY . .
RUN pip install -r requirements.txt
```

Better:

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

---

# 28. Docker image size

Image size matters because smaller images:

- Download faster
- Build faster
- Deploy faster
- Have less attack surface
- Take less disk space

Compare:

| Image | Typical use |
|---|---|
| `python:3.12` | Full Python image, larger |
| `python:3.12-slim` | Good default |
| `python:3.12-alpine` | Smaller, but can cause dependency issues |
| Distroless images | Advanced production use |

Beginner recommendation:

```dockerfile
FROM python:3.12-slim
```

---

# 29. Multi-stage builds

Multi-stage builds let you use one image for building and another image for running.

This keeps production images smaller and cleaner.

Example:

```dockerfile
FROM python:3.12-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt

COPY app/ ./app/


FROM python:3.12-slim AS runtime

ENV PATH=/root/.local/bin:$PATH

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY --from=builder /build/app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

The final image only contains what you copy from the builder stage.

---

# 30. Running as non-root

By default, many containers run as root.

For better security, create a non-root user.

Example:

```dockerfile
FROM python:3.12-slim

RUN useradd --system --create-home appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

USER appuser

CMD ["python", "app/main.py"]
```

Check who you are inside the container:

```bash
docker exec -it container-name whoami
```

You want to see:

```text
appuser
```

not:

```text
root
```

---

# 31. Tags and versions

Images have tags.

Example:

```bash
python:3.12-slim
nginx:alpine
postgres:16
my-api:1.0.0
```

Build with a tag:

```bash
docker build -t my-api:1.0.0 .
```

Run:

```bash
docker run my-api:1.0.0
```

Tag as latest:

```bash
docker tag my-api:1.0.0 my-api:latest
```

Beginner rule:

> Use explicit versions for serious work. Avoid relying on `latest`.

---

# 32. Pushing images to a registry

Example with Docker Hub:

```bash
docker login
```

Build:

```bash
docker build -t yourusername/my-api:1.0.0 .
```

Push:

```bash
docker push yourusername/my-api:1.0.0
```

On another machine:

```bash
docker pull yourusername/my-api:1.0.0
docker run -p 8000:8000 yourusername/my-api:1.0.0
```

---

# 33. Docker in development

Docker is useful in development because it lets you run services without installing them manually.

Examples:

Run Postgres:

```bash
docker run -d \
  --name dev-postgres \
  -e POSTGRES_USER=dev \
  -e POSTGRES_PASSWORD=dev \
  -e POSTGRES_DB=devdb \
  -p 5432:5432 \
  postgres:16
```

Run Redis:

```bash
docker run -d \
  --name dev-redis \
  -p 6379:6379 \
  redis:7
```

Run a temporary Linux shell:

```bash
docker run -it --rm ubuntu:24.04 bash
```

Run a temporary Python environment:

```bash
docker run -it --rm -v "$(pwd)":/app -w /app python:3.12-slim bash
```

---

# 34. Docker in production

In production, Docker images are often used with:

- Docker Compose on small servers
- Kubernetes
- AWS ECS
- AWS Fargate
- Google Cloud Run
- Azure Container Apps
- GitHub Actions
- GitLab CI
- Jenkins

The typical production flow:

```mermaid
flowchart TD
    A[Developer commits code] --> B[CI builds image]
    B --> C[CI runs tests]
    C --> D[CI scans image]
    D --> E[CI pushes image]
    E --> F[Server pulls image]
    F --> G[Container starts]
```

Main idea:

> Build once, run the same image everywhere.

---

# 35. Security basics

At minimum:

## 35.1 Do not bake secrets into images

Do not do this:

```dockerfile
ENV API_KEY=my-secret-key
COPY .env .
```

Bad because secrets become part of the image history.

Use runtime environment variables or a secrets manager.

---

## 35.2 Use non-root users

Add:

```dockerfile
USER appuser
```

---

## 35.3 Keep images updated

Rebuild images regularly to receive security updates.

---

## 35.4 Use trusted base images

Prefer official images:

```dockerfile
FROM python:3.12-slim
FROM node:22-slim
FROM postgres:16-alpine
```

---

## 35.5 Scan images

Common tools:

```bash
docker scout cves my-image
```

or:

```bash
trivy image my-image
```

---

# 36. Most important Docker commands

## Images

```bash
docker images
docker pull image-name
docker build -t name:tag .
docker rmi image-name
docker image prune
```

## Containers

```bash
docker run image-name
docker run -d image-name
docker run -it image-name sh
docker ps
docker ps -a
docker stop container-name
docker start container-name
docker restart container-name
docker rm container-name
docker logs container-name
docker exec -it container-name sh
```

## Volumes

```bash
docker volume ls
docker volume create volume-name
docker volume inspect volume-name
docker volume rm volume-name
docker volume prune
```

## Networks

```bash
docker network ls
docker network create network-name
docker network inspect network-name
docker network rm network-name
```

## Compose

```bash
docker compose up
docker compose up --build
docker compose up -d
docker compose down
docker compose down -v
docker compose logs -f
docker compose ps
docker compose exec service-name sh
```

## Cleanup

```bash
docker container prune
docker image prune
docker volume prune
docker network prune
docker system prune
docker system prune -a
```

---

# 37. Practical mini project

Build a small FastAPI app in Docker.

## Project structure

```text
docker-fastapi-demo/
├── app/
│   └── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .dockerignore
```

---

## `app/main.py`

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    name: str

@app.get("/")
def root():
    return {"message": "Hello from Docker"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/hello")
def hello(message: Message):
    return {"message": f"Hello, {message.name}"}
```

---

## `requirements.txt`

```text
fastapi
uvicorn[standard]
pydantic
```

---

## `.dockerignore`

```gitignore
__pycache__/
*.pyc
.venv/
.git/
.env
.pytest_cache/
.vscode/
.idea/
```

---

## `Dockerfile`

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## `docker-compose.yml`

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
```

---

## Run it

```bash
docker compose up --build
```

Test it:

```bash
curl http://localhost:8000/health
```

POST request:

```bash
curl -X POST http://localhost:8000/hello \
  -H "content-type: application/json" \
  -d '{"name": "Docker Student"}'
```

Expected response:

```json
{
  "message": "Hello, Docker Student"
}
```

Stop:

```bash
docker compose down
```

---

# 38. How to think when debugging Docker

Use this checklist.

## Problem: Container exits immediately

Check logs:

```bash
docker logs container-name
```

Common causes:

- App crashed
- Wrong command
- Missing dependency
- Wrong file path
- Environment variable missing

---

## Problem: Cannot access app in browser

Check:

1. Is the container running?

```bash
docker ps
```

2. Did you map the port?

```bash
-p 8000:8000
```

3. Is the app listening on `0.0.0.0`?

Correct:

```bash
--host 0.0.0.0
```

Wrong:

```bash
--host 127.0.0.1
```

---

## Problem: Database connection fails

Check:

1. Are both services in the same Compose file?
2. Are you using service name as hostname?
3. Is the database ready?
4. Are credentials correct?
5. Is there a healthcheck?

Correct Compose database URL:

```text
postgresql://user:password@db:5432/mydb
```

---

## Problem: Changes do not appear

Maybe you forgot to rebuild:

```bash
docker compose up --build
```

Or:

```bash
docker build --no-cache -t my-image .
```

---

## Problem: Disk space is full

Check Docker disk usage:

```bash
docker system df
```

Cleanup:

```bash
docker system prune
```

More aggressive:

```bash
docker system prune -a
```

---

# 39. What you should learn first

If you are a novice, learn in this order:

1. What images and containers are
2. `docker run`
3. Port mapping with `-p`
4. Logs with `docker logs`
5. Shell access with `docker exec`
6. Writing a basic Dockerfile
7. Building images with `docker build`
8. `.dockerignore`
9. Volumes
10. Docker Compose
11. Container networking
12. Multi-stage builds
13. Non-root containers
14. Image tagging and pushing
15. Production deployment basics

---

# 40. Beginner learning path

## Day 1

Learn:

```bash
docker run
docker ps
docker images
docker logs
docker stop
docker rm
```

Practice:

```bash
docker run hello-world
docker run -it --rm python:3.12-slim python
docker run -d -p 8080:80 nginx
```

---

## Day 2

Learn Dockerfiles.

Build a simple Python image.

Practice:

```bash
docker build -t hello-docker .
docker run hello-docker
```

---

## Day 3

Learn ports, volumes, and environment variables.

Practice running:

```bash
postgres
redis
nginx
```

---

## Day 4

Learn Docker Compose.

Create:

```yaml
services:
  api:
    build: .
  db:
    image: postgres:16
```

---

## Day 5

Learn production concepts:

- Multi-stage builds
- Non-root user
- Image tags
- Registry push
- Security scanning

---

# 41. Final cheat sheet

## Build and run

```bash
docker build -t my-app .
docker run my-app
docker run -p 8000:8000 my-app
```

## Debug

```bash
docker ps
docker ps -a
docker logs container-name
docker exec -it container-name sh
```

## Clean up

```bash
docker stop container-name
docker rm container-name
docker image prune
docker system prune
```

## Compose

```bash
docker compose up --build
docker compose up -d
docker compose logs -f
docker compose exec api sh
docker compose down
docker compose down -v
```

---

# 42. The most important Docker lesson

Docker is not mainly about commands.

Docker is about this idea:

> Package your application and its environment once, then run that same package anywhere.

If you understand images, containers, Dockerfiles, ports, volumes, networking, and Compose, you understand the foundation of Docker.

Everything else is refinement.