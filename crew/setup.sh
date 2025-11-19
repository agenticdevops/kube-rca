#!/bin/bash

# Setup script for Kubernetes RCA Crew

set -e

echo "=========================================="
echo "Kubernetes RCA Crew - Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Check if version is 3.10 or higher
required_version="3.10"
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python 3.10 or higher is required"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Copy .env.example to .env if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your API keys!"
    echo ""
else
    echo ""
    echo "✅ .env file already exists"
fi

# Check for kubectl
echo ""
echo "Checking for kubectl..."
if command -v kubectl &> /dev/null; then
    echo "✅ kubectl found: $(kubectl version --client --short 2>&1 | head -n1)"
else
    echo "⚠️  kubectl not found. Please install kubectl to use Kubernetes features."
fi

# Check for npx
echo ""
echo "Checking for npx..."
if command -v npx &> /dev/null; then
    echo "✅ npx found: $(npx --version)"
else
    echo "⚠️  npx not found. Please install Node.js to use Kubernetes MCP server."
fi

# Check for docker
echo ""
echo "Checking for docker..."
if command -v docker &> /dev/null; then
    echo "✅ docker found: $(docker --version)"
else
    echo "⚠️  docker not found. Please install Docker to use Prometheus MCP server."
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API keys"
echo "2. Run tests: python tests/test_tools.py"
echo "3. Try the CLI: python -m src.cli list-models"
echo ""
echo "To activate the virtual environment in the future:"
echo "  source venv/bin/activate"
echo ""
