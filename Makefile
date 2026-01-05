. PHONY: help build up down restart logs shell deploy

help:  ## Show this help message
        @echo 'Usage: make [target]'
        @echo ''
        @echo 'Available targets:'
        @awk 'BEGIN {FS = ":.*? ## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build Docker image
        docker compose build

up: ## Start the bot
        docker compose up -d

down: ## Stop the bot
        docker compose down

restart: ## Restart the bot
        docker compose restart

logs: ## Show bot logs
        docker compose logs -f

shell: ## Open shell in container
        docker exec -it gemini-bot /bin/bash

deploy: ## Deploy the bot
        bash deploy.sh

status: ## Show container status
        docker compose ps

clean: ## Clean up Docker resources
        docker compose down -v
        docker system prune -f