.PHONY: help install dev migrate test lint format check ui-build ui-watch clean

help:
	@echo "MetaTasks Development Commands"
	@echo "==============================="
	@echo "install      - Install dependencies"
	@echo "dev          - Run development server"
	@echo "migrate      - Run database migrations"
	@echo "test         - Run tests"
	@echo "lint         - Run linters"
	@echo "format       - Format code"
	@echo "check        - Run all checks (lint + type + test)"
	@echo "ui-build     - Build frontend assets"
	@echo "ui-watch     - Watch and rebuild frontend assets"
	@echo "clean        - Clean build artifacts"

install:
	pip install -e ".[dev]"
	npm install

dev:
	./scripts/dev.sh

migrate:
	python manage.py makemigrations
	python manage.py migrate

test:
	pytest

lint:
	./scripts/lint.sh

format:
	./scripts/format.sh

check: lint
	mypy apps config metatasks_lib || true
	pytest

ui-build:
	./scripts/build_frontend.sh

ui-watch:
	npm run watch

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache htmlcov .coverage
	rm -rf staticfiles static_build
