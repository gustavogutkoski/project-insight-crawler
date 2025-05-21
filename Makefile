.PHONY: help test test_xml lint format typecheck run

help:
	@echo "Available commands:"
	@echo "  make test         Run tests with coverage"
	@echo "  make test_xml     Run tests with coverage and generate report in XML"
	@echo "  make lint         Lint and auto-fix code with Ruff"
	@echo "  make format       Format code with Ruff"
	@echo "  make typecheck    Run type checking with MyPy"
	@echo "  make run path=./path/to/java/project  Run the crawler on a Java project"

test:
	poetry run pytest -v --cov=crawler --cov-report=term-missing

test_xml:
	poetry run pytest -v --cov=crawler --cov-report=xml

lint:
	poetry run ruff check . --fix

format:
	poetry run ruff format .

typecheck:
	poetry run mypy .

run:
	poetry run python main.py $(path)
