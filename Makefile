.PHONY: install sync run test lint format typecheck gateway docker-up

install:
	uv add -r requirements.txt
	uv add --dev pytest pytest-asyncio pytest-cov ruff mypy pre-commit ipykernel
	uv sync

sync:
	uv sync

run:
	uv run uvicorn api.main:app --reload

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	uv run mypy src api

gateway:
	uv run litellm --config gateway/config.yaml --port 4000

docker-up:
	docker compose up --build