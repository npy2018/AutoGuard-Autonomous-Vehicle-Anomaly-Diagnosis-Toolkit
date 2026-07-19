.PHONY: install test lint run demo docker

install:
	pip install -e .[dev]

test:
	pytest

lint:
	ruff check .

run:
	uvicorn app.main:app --reload

demo:
	python scripts/run_demo.py

docker:
	docker compose up --build
