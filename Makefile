SHELL := /bin/bash

.PHONY: help up down backend planner executor ui format lint

help:
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

up: ## Start the full stack via Docker Compose
	@docker compose -f infra/docker-compose.yml up --build

down: ## Stop the stack
	@docker compose -f infra/docker-compose.yml down

backend: ## Run backend locally
	@cd backend && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

planner: ## Run planner CLI demo
	@cd planner && poetry run python -m planner.service

executor: ## Run executor demo with program.json
	@cd executor && poetry run python -m executor.runtime

ui: ## Run the React dashboard
	@cd ui && npm install && npm run dev

format: ## Run formatters (ruff + black + prettier)
	@cd backend && poetry run ruff check app --fix && poetry run black app
	@cd executor && poetry run ruff check executor --fix && poetry run black executor
	@cd planner && poetry run ruff check planner --fix && poetry run black planner
	@cd ui && npx prettier --write "src/**/*.{ts,tsx}"

lint: ## Run linters
	@cd backend && poetry run ruff check app
	@cd executor && poetry run ruff check executor
	@cd planner && poetry run ruff check planner
	@cd ui && npx prettier --check "src/**/*.{ts,tsx}"

