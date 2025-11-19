.PHONY: help setup install test test-tools test-agent clean run list-models

help:
	@echo "Kubernetes RCA Crew - Available Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make setup        - Initial setup (create venv, install deps)"
	@echo "  make install      - Install/update dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test         - Run all tests"
	@echo "  make test-tools   - Test MCP tool integration"
	@echo "  make test-agent   - Test agent functionality"
	@echo ""
	@echo "Running:"
	@echo "  make list-models  - List available models"
	@echo "  make run POD=<name> [NS=<namespace>] - Diagnose a pod crash"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean        - Remove temporary files and cache"
	@echo ""
	@echo "Examples:"
	@echo "  make run POD=my-pod NS=default"
	@echo "  make run POD=my-pod NS=production MODEL=claude-sonnet"

setup:
	@echo "Setting up Kubernetes RCA Crew..."
	@bash setup.sh

install:
	@echo "Installing dependencies..."
	@pip install -r requirements.txt

test: test-tools test-agent

test-tools:
	@echo "Testing MCP tools..."
	@.venv/bin/python tests/test_tools.py

test-agent:
	@echo "Testing agents..."
	@.venv/bin/python tests/test_agent_simple.py

test-agent-full:
	@echo "Testing agents (interactive, requires API key)..."
	@.venv/bin/python tests/test_agent.py

list-models:
	@.venv/bin/python -m src.cli list-models

run:
	@if [ -z "$(POD)" ]; then \
		echo "Error: POD variable required. Usage: make run POD=<pod-name> [NS=<namespace>] [MODEL=<model>]"; \
		exit 1; \
	fi
	@.venv/bin/python -m src.cli $(if $(MODEL),--model $(MODEL)) pod-crash $(POD) $(if $(NS),-n $(NS),-n default)

diagnose:
	@if [ -z "$(ISSUE)" ]; then \
		echo "Error: ISSUE variable required. Usage: make diagnose ISSUE='describe the issue'"; \
		exit 1; \
	fi
	@.venv/bin/python -m src.cli $(if $(MODEL),--model $(MODEL)) diagnose "$(ISSUE)"

clean:
	@echo "Cleaning up..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .pytest_cache 2>/dev/null || true
	@echo "Cleanup complete"

format:
	@echo "Formatting code..."
	@black src/ tests/
	@ruff check --fix src/ tests/

lint:
	@echo "Linting code..."
	@ruff check src/ tests/
	@black --check src/ tests/
