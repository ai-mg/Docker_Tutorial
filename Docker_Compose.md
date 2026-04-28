# Docker Compose Explained in Detail

Docker Compose is a tool for running **multiple Docker containers together** using one configuration file.

Instead of typing long `docker run` commands for every container, you describe your application in a file called:

```text
docker-compose.yml
```

Then you start everything with:

```bash
docker compose up
```

---

# 1. Why Docker Compose exists

A real application often needs more than one container.

For example, a Python web application may need:

- A FastAPI API container
- A Postgres database container
- A Redis cache container
- A background worker container
- An Nginx reverse proxy container

Without Docker Compose, you would need to run each container manually.

Example without Compose:

```bash
docker network create app_net

docker volume create db_data

docker run -d \
  --name db \
  --network app_net \
  -e POSTGRES_USER=appuser \
  -e POSTGRES_PASSWORD=apppassword \
  -e POSTGRES_DB=appdb \
  -v db_data:/var/lib/postgresql/data \
  postgres:16-alpine

docker run -d \
  --name api \
  --network app_net \
  -e DATABASE_URL=postgresql://appuser:apppassword@db:5432/appdb \
  -p 8000:8000 \
  my-api
```

That is a lot of commands.

With Docker Compose, you write the setup once:

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

  api:
    build: .
    environment:
      DATABASE_URL: postgresql://appuser:apppassword@db:5432/appdb
    ports:
      - "8000:8000"

volumes:
  db_data:
```

Then run:

```bash
docker compose up
```

Docker Compose creates the network, containers, and volume for you.

---

# 2. Dockerfile versus Docker Compose

This distinction is very important.

## Dockerfile

A `Dockerfile` describes how to build **one image**.

Example:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

This answers:

> How do I package my application into an image?

---

## Docker Compose file

A `docker-compose.yml` describes how to run **one or more containers**.

Example:

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
```

This answers:

> How do I run my application container, with ports, environment variables, volumes, networks, and other services?

---

## Simple summary

```text
Dockerfile
  → builds one image

docker-compose.yml
  → runs one or more containers
```

Or:

```text
Dockerfile = packaging recipe
Docker Compose = application running recipe
```

---

# 3. Basic Docker Compose mental model

```mermaid
flowchart TD
    F[docker-compose.yml] --> A[API service]
    F --> D[Database service]
    F --> V[Named volume]
    F --> N[Docker network]
    A --> D
    D --> V
```

The Compose file describes:

- Which containers should run
- Which images to use
- Which images to build
- Which ports to expose
- Which environment variables to pass
- Which volumes to create
- Which services depend on each other
- Which network the services use

---

# 4. A minimal Docker Compose example

Create this file:

```text
docker-compose.yml
```

Inside it:

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
```

Run:

```bash
docker compose up
```

Open:

```text
http://localhost:8080
```

You should see the default Nginx page.

---

# 5. What happened?

This Compose file:

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
```

is equivalent to something like:

```bash
docker run -p 8080:80 nginx:alpine
```

But Compose gives you a reusable file.

Instead of remembering the command, you save the configuration.

---

# 6. Main structure of a Compose file

A typical Compose file looks like this:

```yaml
services:
  service_name:
    image: some-image
    ports:
      - "HOST_PORT:CONTAINER_PORT"
    environment:
      VARIABLE_NAME: value
    volumes:
      - volume_name:/path/inside/container

volumes:
  volume_name:
```

The most common top-level sections are:

| Section | Meaning |
|---|---|
| `services` | Defines the containers you want to run |
| `volumes` | Defines persistent storage |
| `networks` | Defines custom networks, optional |
| `configs` | Advanced configuration feature |
| `secrets` | Advanced secret handling feature |

For beginners, the most important ones are:

```yaml
services:
volumes:
```

---

# 7. What is a service?

In Docker Compose, a **service** is a container definition.

Example:

```yaml
services:
  api:
    build: .
```

Here, `api` is the service name.

When you run:

```bash
docker compose up
```

Compose creates a container for the `api` service.

You then refer to the service by name:

```bash
docker compose logs api
docker compose exec api sh
docker compose restart api
```

---

# 8. Service name versus container name

In Compose, you usually work with **service names**, not exact container names.

Example:

```yaml
services:
  api:
    build: .
```

The service is named:

```text
api
```

But the actual container might be named something like:

```text
myproject-api-1
```

Compose creates that full container name automatically.

You usually do not need to care about it.

Use:

```bash
docker compose logs api
```

not:

```bash
docker logs myproject-api-1
```

---

# 9. `image` in Docker Compose

Use `image` when you want to run an existing image.

Example:

```yaml
services:
  db:
    image: postgres:16-alpine
```

This means:

> Run a container from the existing `postgres:16-alpine` image.

If the image is not on your computer, Docker downloads it.

Common images:

```text
postgres:16-alpine
redis:7-alpine
nginx:alpine
mysql:8
python:3.12-slim
```

---

# 10. `build` in Docker Compose

Use `build` when you want Compose to build your own image from a Dockerfile.

Example:

```yaml
services:
  api:
    build: .
```

This means:

> Build the image using the Dockerfile in the current directory.

Project structure:

```text
my-api/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── app/
    └── main.py
```

Here:

```yaml
build: .
```

means:

> The build context is the current folder.

---

# 11. `image` versus `build`

| Compose option | Meaning | Example use |
|---|---|---|
| `image` | Use an existing image | Postgres, Redis, Nginx |
| `build` | Build an image from your Dockerfile | Your own app |

Common pattern:

```yaml
services:
  api:
    build: .

  db:
    image: postgres:16-alpine
```

Meaning:

- `api` is your code, so Compose builds it
- `db` is official Postgres, so Compose pulls it

---

# 12. `ports`

Ports expose a container to your computer.

Example:

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
```

The format is:

```text
HOST_PORT:CONTAINER_PORT
```

So:

```yaml
ports:
  - "8000:8000"
```

means:

```text
localhost:8000 on your laptop
goes to
port 8000 inside the container
```

---

## Example with Nginx

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
```

This means:

```text
localhost:8080 on your laptop
goes to
port 80 inside the Nginx container
```

Then open:

```text
http://localhost:8080
```

---

# 13. `environment`

Environment variables configure containers at runtime.

Example:

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: apppassword
      POSTGRES_DB: appdb
```

These values are passed into the Postgres container.

Postgres uses them to create:

- A database user
- A password
- A database name

---

## Environment variables for your API

```yaml
services:
  api:
    build: .
    environment:
      APP_ENV: development
      DATABASE_URL: postgresql://appuser:apppassword@db:5432/appdb
```

Inside Python:

```python
import os

database_url = os.getenv("DATABASE_URL")
```

---

# 14. Why environment variables are useful

You should avoid hardcoding configuration into your application code.

Bad:

```python
DATABASE_URL = "postgresql://appuser:apppassword@db:5432/appdb"
```

Better:

```python
import os

DATABASE_URL = os.getenv("DATABASE_URL")
```

Then Compose provides the value:

```yaml
environment:
  DATABASE_URL: postgresql://appuser:apppassword@db:5432/appdb
```

This makes the app more flexible.

---

# 15. `.env` files with Compose

Instead of writing values directly in `docker-compose.yml`, you can put them in a `.env` file.

Example `.env`:

```env
POSTGRES_USER=appuser
POSTGRES_PASSWORD=apppassword
POSTGRES_DB=appdb
```

Then use them in Compose:

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
```

Docker Compose automatically reads `.env` from the same folder.

Important:

```text
Do not commit real secrets to Git.
```

Add `.env` to `.gitignore`:

```gitignore
.env
```

---

# 16. Docker Compose networking

This is one of the most important parts.

Docker Compose automatically creates a private network for your services.

Example:

```yaml
services:
  api:
    build: .

  db:
    image: postgres:16-alpine
```

Compose creates a network where:

```text
api can reach db using hostname db
db can reach api using hostname api
```

You do not need to know container IP addresses.

---

# 17. Service names become hostnames

Look at this:

```yaml
services:
  db:
    image: postgres:16-alpine

  api:
    build: .
    environment:
      DATABASE_URL: postgresql://appuser:apppassword@db:5432/appdb
```

The hostname is:

```text
db
```

Why?

Because the service is named:

```yaml
db:
```

So from the `api` container, this works:

```text
db:5432
```

That means:

> Connect to the container running the `db` service on port `5432`.

---

# 18. Do not use `localhost` between containers

This is a very common beginner mistake.

Wrong:

```yaml
DATABASE_URL: postgresql://appuser:apppassword@localhost:5432/appdb
```

Why is it wrong?

Inside the API container:

```text
localhost
```

means:

```text
the API container itself
```

It does not mean the database container.

Correct:

```yaml
DATABASE_URL: postgresql://appuser:apppassword@db:5432/appdb
```

Because `db` is the Compose service name.

---

# 19. Do you need to expose the database port?

In many cases, no.

Example:

```yaml
services:
  db:
    image: postgres:16-alpine

  api:
    build: .
```

The API can reach the database internally using:

```text
db:5432
```

even if you do not write:

```yaml
ports:
  - "5432:5432"
```

You only need to expose Postgres to your host machine if you want to connect from your laptop using tools like:

- DBeaver
- DataGrip
- pgAdmin
- local `psql`

For internal container-to-container communication, Compose networking is enough.

---

# 20. `volumes`

Containers are disposable.

If a database stores data only inside the container and you delete the container, the data may be lost.

Volumes solve this.

Example:

```yaml
services:
  db:
    image: postgres:16-alpine
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

This creates a Docker-managed named volume called:

```text
db_data
```

and attaches it to:

```text
/var/lib/postgresql/data
```

inside the Postgres container.

That is where Postgres stores database files.

---

# 21. Volume syntax

```yaml
volumes:
  - db_data:/var/lib/postgresql/data
```

The format is:

```text
SOURCE:TARGET
```

So:

```text
db_data:/var/lib/postgresql/data
```

means:

| Part | Meaning |
|---|---|
| `db_data` | Named volume on the Docker host |
| `/var/lib/postgresql/data` | Folder inside the container |

---

# 22. Declaring named volumes

If you use a named volume, declare it at the bottom:

```yaml
volumes:
  db_data:
```

Full example:

```yaml
services:
  db:
    image: postgres:16-alpine
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

This tells Docker Compose:

> Create and manage a named volume called `db_data`.

---

# 23. Bind mounts in Compose

A bind mount maps a folder from your computer into the container.

Example:

```yaml
services:
  api:
    build: .
    volumes:
      - ./app:/app/app
```

This means:

```text
local ./app folder
goes into
container /app/app folder
```

So if you edit a file on your computer:

```text
./app/main.py
```

the change appears inside the container at:

```text
/app/app/main.py
```

This is useful for development.

---

# 24. Named volume versus bind mount

| Feature | Named volume | Bind mount |
|---|---|---|
| Managed by Docker | Yes | No |
| Uses exact host folder | No | Yes |
| Good for databases | Yes | Sometimes |
| Good for live code editing | Not usually | Yes |
| Example | `db_data:/var/lib/postgresql/data` | `./app:/app/app` |

Use named volumes for database data.

Use bind mounts for local development code.

---

# 25. `depends_on`

`depends_on` controls startup order.

Example:

```yaml
services:
  api:
    build: .
    depends_on:
      - db

  db:
    image: postgres:16-alpine
```

This means:

> Start `db` before `api`.

But there is an important warning.

---

# 26. `depends_on` does not mean ready

This:

```yaml
depends_on:
  - db
```

only means:

> Start the database container before the API container.

It does **not** mean:

> Wait until Postgres is fully ready to accept connections.

Postgres may take several seconds to initialize.

Your API might start too early and fail to connect.

---

# 27. Healthchecks

A healthcheck lets Docker check whether a service is actually ready.

Example:

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
```

This uses:

```bash
pg_isready
```

to check if Postgres is ready.

---

# 28. `depends_on` with healthcheck

Better Compose setup:

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

This means:

> Start the API only after the database is healthy.

---

# 29. Understanding the healthcheck fields

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U appuser -d appdb"]
  interval: 5s
  timeout: 3s
  retries: 10
```

| Field | Meaning |
|---|---|
| `test` | Command used to check health |
| `interval` | How often to run the check |
| `timeout` | How long each check may take |
| `retries` | How many failures before marking unhealthy |

---

# 30. Complete FastAPI plus Postgres Compose example

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
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser -d appdb"]
      interval: 5s
      timeout: 3s
      retries: 10

  api:
    build: .
    environment:
      DATABASE_URL: postgresql://appuser:apppassword@db:5432/appdb
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy

volumes:
  db_data:
```

---

# 31. Line-by-line explanation

## `services`

```yaml
services:
```

This starts the list of services.

Each service usually becomes one container.

---

## `db`

```yaml
  db:
```

This defines a service named `db`.

Other containers can reach it using hostname:

```text
db
```

---

## `image`

```yaml
    image: postgres:16-alpine
```

This says:

> Use the existing Postgres image.

Docker will pull it if necessary.

---

## `environment`

```yaml
    environment:
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: apppassword
      POSTGRES_DB: appdb
```

These variables configure Postgres.

Postgres creates:

- user: `appuser`
- password: `apppassword`
- database: `appdb`

---

## `volumes`

```yaml
    volumes:
      - db_data:/var/lib/postgresql/data
```

This stores database files in a persistent named volume.

Even if the container is removed, the volume usually remains.

---

## `healthcheck`

```yaml
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser -d appdb"]
      interval: 5s
      timeout: 3s
      retries: 10
```

This checks whether Postgres is ready.

---

## `api`

```yaml
  api:
```

This defines your API service.

Other services can reach it using hostname:

```text
api
```

---

## `build`

```yaml
    build: .
```

This tells Compose:

> Build the API image from the Dockerfile in the current directory.

---

## API environment

```yaml
    environment:
      DATABASE_URL: postgresql://appuser:apppassword@db:5432/appdb
```

This gives your API the database connection string.

Important part:

```text
@db:5432
```

`db` is the service name.

---

## `ports`

```yaml
    ports:
      - "8000:8000"
```

This exposes the API to your laptop.

You can open:

```text
http://localhost:8000
```

---

## `depends_on`

```yaml
    depends_on:
      db:
        condition: service_healthy
```

This tells Compose:

> Wait until the database healthcheck passes before starting the API.

---

## Top-level `volumes`

```yaml
volumes:
  db_data:
```

This declares the named volume.

---

# 32. What happens when you run `docker compose up`?

When you run:

```bash
docker compose up
```

Compose does several things:

1. Reads `docker-compose.yml`
2. Creates a project network
3. Creates named volumes if needed
4. Pulls external images, for example Postgres
5. Builds local images, for example your API
6. Starts containers
7. Shows logs in your terminal

---

# 33. What happens when you run `docker compose up --build`?

```bash
docker compose up --build
```

This tells Compose:

> Build images before starting containers.

Use it when you changed:

- Dockerfile
- requirements.txt
- app code copied into the image
- image build configuration

For development, this is common:

```bash
docker compose up --build
```

---

# 34. What happens when you run `docker compose up -d`?

```bash
docker compose up -d
```

The `-d` means detached mode.

It starts containers in the background.

Your terminal is returned immediately.

Then you can check:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f
```

---

# 35. What happens when you run `docker compose down`?

```bash
docker compose down
```

This stops and removes:

- containers created by Compose
- the default Compose network

But it usually keeps:

- named volumes
- images

So database data usually survives.

---

# 36. What happens when you run `docker compose down -v`?

```bash
docker compose down -v
```

The `-v` means:

> Also remove volumes.

This can delete database data.

Be careful.

Use:

```bash
docker compose down -v
```

only when you intentionally want to reset everything.

---

# 37. Useful Docker Compose commands

## Start services

```bash
docker compose up
```

## Start and rebuild

```bash
docker compose up --build
```

## Start in background

```bash
docker compose up -d
```

## Stop and remove containers

```bash
docker compose down
```

## Stop and remove containers plus volumes

```bash
docker compose down -v
```

## See running services

```bash
docker compose ps
```

## See logs

```bash
docker compose logs
```

## Follow logs

```bash
docker compose logs -f
```

## Logs for one service

```bash
docker compose logs -f api
```

## Enter a running service

```bash
docker compose exec api sh
```

## Restart one service

```bash
docker compose restart api
```

## Build one service

```bash
docker compose build api
```

---

# 38. `docker compose exec` versus `docker compose run`

These are different.

## `docker compose exec`

Use this to run a command inside an already running service.

Example:

```bash
docker compose exec api sh
```

Meaning:

> Enter the running `api` container.

---

## `docker compose run`

Use this to start a new one-off container from a service definition.

Example:

```bash
docker compose run api python --version
```

Meaning:

> Start a temporary new container based on the `api` service and run `python --version`.

For beginners, you will most often use:

```bash
docker compose exec api sh
```

---

# 39. `command` in Compose

Compose can override the Dockerfile `CMD`.

Dockerfile:

```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Compose override:

```yaml
services:
  api:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

This is useful for development.

For example, `--reload` restarts FastAPI when code changes.

---

# 40. Compose with live reload for development

Example:

```yaml
services:
  api:
    build: .
    volumes:
      - ./app:/app/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ports:
      - "8000:8000"
```

This does three things:

1. Builds your API image.
2. Mounts your local `./app` folder into the container.
3. Runs Uvicorn with auto-reload.

Now when you edit:

```text
./app/main.py
```

the container sees the change immediately.

---

# 41. Development versus production Compose files

For development:

```yaml
services:
  api:
    build: .
    volumes:
      - ./app:/app/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ports:
      - "8000:8000"
```

For production:

```yaml
services:
  api:
    image: my-api:1.0.0
    ports:
      - "8000:8000"
```

In production, you usually:

- build the image in CI/CD
- push it to a registry
- pull the finished image on the server
- avoid bind mounts
- avoid `--reload`

---

# 42. Full beginner project example

Project structure:

```text
compose-demo/
├── app/
│   └── main.py
├── Dockerfile
├── requirements.txt
└── docker-compose.yml
```

---

## `app/main.py`

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Docker Compose"}

@app.get("/health")
def health():
    return {"status": "ok"}
```

---

## `requirements.txt`

```text
fastapi
uvicorn[standard]
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

Open:

```text
http://localhost:8000
```

Or test:

```bash
curl http://localhost:8000/health
```

Stop it:

```bash
docker compose down
```

---

# 43. Full FastAPI plus Postgres example

Project structure:

```text
compose-postgres-demo/
├── app/
│   └── main.py
├── Dockerfile
├── requirements.txt
└── docker-compose.yml
```

Compose file:

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
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U appuser -d appdb"]
      interval: 5s
      timeout: 3s
      retries: 10

  api:
    build: .
    environment:
      DATABASE_URL: postgresql://appuser:apppassword@db:5432/appdb
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy

volumes:
  db_data:
```

---

# 44. What this full example gives you

| Service | Purpose |
|---|---|
| `api` | Runs your FastAPI application |
| `db` | Runs Postgres |
| `db_data` | Stores database files persistently |
| Default Compose network | Lets `api` talk to `db` using hostname `db` |

---

# 45. Common Docker Compose mistakes

## Mistake 1: Using `localhost` for another container

Wrong:

```yaml
DATABASE_URL: postgresql://appuser:apppassword@localhost:5432/appdb
```

Correct:

```yaml
DATABASE_URL: postgresql://appuser:apppassword@db:5432/appdb
```

---

## Mistake 2: Forgetting port mapping

If you forget:

```yaml
ports:
  - "8000:8000"
```

your app may run inside Docker, but your laptop cannot access it at:

```text
http://localhost:8000
```

---

## Mistake 3: Thinking `depends_on` waits for readiness

This:

```yaml
depends_on:
  - db
```

does not wait until Postgres is ready.

Better:

```yaml
depends_on:
  db:
    condition: service_healthy
```

with a healthcheck.

---

## Mistake 4: Accidentally deleting database data

This deletes named volumes:

```bash
docker compose down -v
```

If your database uses a named volume, that can delete the database data.

Use carefully.

---

## Mistake 5: Not rebuilding after changes

If your code is copied into the image:

```dockerfile
COPY app/ ./app/
```

and you change the code, rebuild:

```bash
docker compose up --build
```

If you use a bind mount:

```yaml
volumes:
  - ./app:/app/app
```

then code changes may appear without rebuilding.

---

# 46. Debugging Docker Compose

## Check services

```bash
docker compose ps
```

---

## View all logs

```bash
docker compose logs -f
```

---

## View logs for API only

```bash
docker compose logs -f api
```

---

## View logs for database only

```bash
docker compose logs -f db
```

---

## Enter the API container

```bash
docker compose exec api sh
```

Then inspect:

```sh
pwd
ls
env
```

---

## Enter the database container

```bash
docker compose exec db sh
```

If Postgres tools are available:

```sh
psql -U appuser -d appdb
```

---

## Restart one service

```bash
docker compose restart api
```

---

## Rebuild one service

```bash
docker compose build api
```

---

# 47. Compose project names

Docker Compose groups resources under a project name.

By default, the project name is usually the folder name.

If your folder is:

```text
my-api
```

Compose may create containers like:

```text
my-api-api-1
my-api-db-1
```

Pattern:

```text
project-service-number
```

You can set a custom project name:

```bash
docker compose -p demo up
```

Then containers may be named:

```text
demo-api-1
demo-db-1
```

---

# 48. Why Compose is useful for teaching and development

Compose is excellent for local development because it makes the full stack reproducible.

Instead of saying:

> Install Python, install Postgres, create a database, set passwords, configure networking...

You say:

```bash
docker compose up --build
```

This is especially useful in a classroom because every student can run the same environment.

---

# 49. Docker Compose cheat sheet

```bash
# Start services
docker compose up

# Start services and rebuild images
docker compose up --build

# Start services in the background
docker compose up -d

# Stop and remove services
docker compose down

# Stop and remove services plus volumes
docker compose down -v

# Show running Compose services
docker compose ps

# Show logs
docker compose logs

# Follow logs
docker compose logs -f

# Show logs for one service
docker compose logs -f api

# Enter a service container
docker compose exec api sh

# Restart a service
docker compose restart api

# Build services
docker compose build

# Build one service
docker compose build api
```

---

# 50. Final mental model

Docker Compose is a way to describe your whole application stack in one file.

A Dockerfile answers:

```text
How do I build this application image?
```

Docker Compose answers:

```text
How do I run this application together with its database, network, volumes, ports, and environment variables?
```

Remember these key ideas:

1. `services` define containers.
2. `image` uses an existing image.
3. `build` builds your own Dockerfile.
4. `ports` expose containers to your laptop.
5. `environment` passes configuration.
6. `volumes` persist data.
7. Compose creates a network automatically.
8. Services can reach each other by service name.
9. Use `db`, not `localhost`, between containers.
10. `depends_on` controls startup order, but healthchecks are needed for readiness.

The most useful beginner command is:

```bash
docker compose up --build
```

The most useful cleanup command is:

```bash
docker compose down
```

And the dangerous reset command is:

```bash
docker compose down -v
```

because it also removes volumes.