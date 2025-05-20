.PHONY: help test lint format typecheck run

help:
	@echo "Available commands:"
	@echo "  make test         Run tests with coverage"
	@echo "  make lint         Lint and auto-fix code with Ruff"
	@echo "  make format       Format code with Ruff"
	@echo "  make typecheck    Run type checking with MyPy"
	@echo "  make run path=./path/to/java/project  Run the crawler on a Java project"

test:
	pytest -v --cov=crawler --cov-report=term-missing

lint:
	ruff check . --fix

format:
	ruff format .

typecheck:
	mypy .

run:
	python main.py $(path)
