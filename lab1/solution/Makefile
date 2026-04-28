.PHONY: build up down logs shell test predict clean rebuild

build:
	docker compose build

up:
	docker compose up -d
	@echo "API: http://localhost:8000  |  Docs: http://localhost:8000/docs"

down:
	docker compose down

logs:
	docker compose logs -f api

shell:
	docker compose exec api /bin/bash

test:
	pytest tests/

predict:
	curl -s -X POST http://localhost:8000/predict \
		-H "Content-Type: application/json" \
		-d '{"sepal_length":5.1,"sepal_width":3.5,"petal_length":1.4,"petal_width":0.2}' \
		| python -m json.tool

clean:
	docker compose down -v
	docker image rm iris-api:latest 2>/dev/null || true

rebuild: clean build up
