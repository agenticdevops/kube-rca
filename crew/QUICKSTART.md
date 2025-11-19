# Quick Start Guide

Get up and running with Kubernetes RCA Crew in 5 minutes.

## Prerequisites Check

Before starting, ensure you have:

- [ ] Python 3.10+ installed
- [ ] Kubernetes cluster with kubectl configured
- [ ] Node.js/npx installed
- [ ] Docker installed
- [ ] Prometheus running (optional, for metrics)
- [ ] API key for Gemini, Claude, or OpenAI

## Installation (5 minutes)

### Option 1: Automated Setup

```bash
# Run the setup script
./setup.sh

# Edit .env with your API keys
nano .env  # or use your preferred editor

# Add your API key (choose one):
# GOOGLE_API_KEY=your-key-here
# ANTHROPIC_API_KEY=your-key-here
# OPENAI_API_KEY=your-key-here
```

### Option 2: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Add your API keys
```

## Verify Installation

### 1. Test Model Configuration

```bash
python -m src.cli list-models
```

Expected output: List of available models (gemini-pro, claude-sonnet, etc.)

### 2. Test MCP Tools (Optional)

```bash
# Test Kubernetes and Prometheus connectivity
python tests/test_tools.py
```

### 3. Test Basic Agent

```bash
# Test agent creation and simple task
python tests/test_agent.py
```

## First Diagnosis

### Example 1: List Pods

```bash
python -m src.cli diagnose "List all pods in default namespace and show their status"
```

### Example 2: Diagnose a Crashing Pod

First, find a pod:
```bash
kubectl get pods --all-namespaces
```

Then diagnose it:
```bash
python -m src.cli pod-crash <pod-name> -n <namespace>
```

### Example 3: Generic Issue

```bash
python -m src.cli diagnose "Some pods are showing ImagePullBackOff errors"
```

## Common Commands

```bash
# Activate environment (if not already activated)
source venv/bin/activate

# List available models
python -m src.cli list-models

# Diagnose pod crash
python -m src.cli pod-crash my-pod -n my-namespace

# Generic diagnosis
python -m src.cli diagnose "describe the issue here"

# Use specific model
python -m src.cli --model claude-sonnet pod-crash my-pod

# Verbose output
python -m src.cli -v pod-crash my-pod
```

## Troubleshooting

### "Module not found" errors

```bash
# Ensure you're in the project root
cd /path/to/01-k8s-rca

# Activate venv
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### MCP server fails to start

**Kubernetes MCP:**
```bash
# Test manually
npx -y kubernetes-mcp-server@latest

# Check kubectl
kubectl cluster-info
```

**Prometheus MCP:**
```bash
# Test manually
docker run -i --rm -e PROMETHEUS_URL=http://localhost:9090 \
  ghcr.io/pab1it0/prometheus-mcp-server:latest

# Verify Prometheus is running
curl http://localhost:9090/api/v1/status/config
```

### Agent doesn't use tools

1. Check API key is set: `echo $GOOGLE_API_KEY` (or relevant key)
2. Verify .env file is in project root
3. Try with verbose logging: `python -m src.cli -v ...`

### API rate limits

Try switching to a different model:
```bash
# If using Gemini, try Flash
export DEFAULT_MODEL=gemini-flash

# Or use Claude
export DEFAULT_MODEL=claude-sonnet
```

## Next Steps

1. **Try real scenarios**: Use actual pods from your cluster
2. **Customize agents**: Edit `src/agents/diagnostic_agent.py`
3. **Add new tools**: Create wrappers in `src/tools/`
4. **Experiment with models**: Try different models in `config/models.yaml`
5. **Build flows**: Create custom flows in `src/flows/`

## Getting Help

- Read the full [README.md](README.md) for detailed documentation
- Check agent behavior with `--verbose` flag
- Review MCP server configurations in `config/mcp_servers.yaml`
- Inspect model configurations in `config/models.yaml`

## Project Structure Quick Reference

```
01-k8s-rca/
├── config/           # Model and MCP configurations
├── src/
│   ├── agents/      # Agent definitions (customize here)
│   ├── tools/       # MCP tool wrappers (extend here)
│   ├── models/      # Model config loader
│   └── cli.py       # CLI interface
├── tests/           # Test scripts
└── .env             # Your API keys (create from .env.example)
```

## Quick Tips

1. **Start simple**: Test with basic commands before complex diagnoses
2. **Use verbose mode**: Add `-v` flag to see what's happening
3. **Check logs**: Agents show their reasoning and tool usage
4. **Iterate**: Start with one pod, then expand to more complex scenarios
5. **Switch models**: Different models have different strengths

Happy debugging! 🚀
