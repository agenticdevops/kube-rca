# Kubernetes RCA Crew

An intelligent Root Cause Analysis (RCA) system for Kubernetes using CrewAI and MCP servers.

## Overview

This project provides AI-powered diagnostic capabilities for Kubernetes clusters. It uses CrewAI agents with access to Kubernetes and Prometheus data through MCP (Model Context Protocol) servers to automatically diagnose issues, analyze metrics, and provide actionable remediation steps.

## Features

- **Switchable LLM Backends**: Easily switch between Gemini, Claude, OpenAI, or other models via configuration
- **MCP Integration**: Uses Model Context Protocol for reliable tool integration
- **Pod Crash Analysis**: Specialized agent for diagnosing pod crashes and restarts
- **Resource Analysis**: Analyze CPU, memory, and other resource issues
- **Systematic Investigation**: Agents follow structured diagnostic approaches
- **Evidence-Based Analysis**: All conclusions backed by cluster data and metrics

## Architecture

```
├── config/                  # Configuration files
│   ├── models.yaml         # LLM model configurations
│   └── mcp_servers.yaml    # MCP server configurations
├── src/
│   ├── agents/             # CrewAI agent definitions
│   ├── flows/              # CrewAI flows (future)
│   ├── models/             # Model configuration loader
│   ├── tools/              # MCP tool wrappers
│   └── cli.py              # CLI interface
└── tests/                  # Test scripts
```

## Prerequisites

1. **Kubernetes cluster** with kubectl configured
2. **Prometheus** running and accessible (default: http://localhost:9090)
3. **Node.js/npx** installed (for Kubernetes MCP server)
4. **Docker** installed (for Prometheus MCP server)
5. **Python 3.10+**
6. **API keys** for your chosen LLM provider(s)

## Installation

### 1. Clone and setup

```bash
cd /path/to/01-k8s-rca
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

Copy the example environment file and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```bash
# Choose your primary model
DEFAULT_MODEL=gemini-pro

# Add corresponding API key
GOOGLE_API_KEY=your-key-here
# ANTHROPIC_API_KEY=your-key-here
# OPENAI_API_KEY=your-key-here

# Kubernetes and Prometheus
KUBECONFIG=~/.kube/config
PROMETHEUS_URL=http://localhost:9090
```

### 3. Configure models (optional)

Edit `config/models.yaml` to:
- Add new models
- Change model parameters (temperature, max_tokens)
- Assign specific models to different agents

### 4. Test the setup

```bash
# Test MCP tools
python tests/test_tools.py

# Test agents
python tests/test_agent.py
```

## Usage

### CLI Interface

#### Diagnose a crashing pod

```bash
python -m src.cli pod-crash my-pod-name -n my-namespace
```

#### Generic diagnosis

```bash
python -m src.cli diagnose "Pods are failing with ImagePullBackOff error"
```

#### List available models

```bash
python -m src.cli list-models
```

#### Use a specific model

```bash
python -m src.cli pod-crash my-pod --model claude-sonnet
```

#### Enable verbose logging

```bash
python -m src.cli -v pod-crash my-pod
```

### Programmatic Usage

```python
from src.agents.diagnostic_agent import create_pod_crash_analyzer
from crewai import Task

# Create agent
agent = create_pod_crash_analyzer(model_id="gemini-pro")

# Create task
task = Task(
    description="Analyze why pod 'my-app-123' in namespace 'production' is crashing",
    expected_output="Root cause analysis with remediation steps",
    agent=agent
)

# Execute
result = task.execute()
print(result)
```

## Switching Models

### Method 1: Environment variable

```bash
export DEFAULT_MODEL=claude-sonnet
python -m src.cli pod-crash my-pod
```

### Method 2: CLI flag

```bash
python -m src.cli --model gpt-4o pod-crash my-pod
```

### Method 3: Edit config file

Edit `config/models.yaml`:

```yaml
default: claude-sonnet  # Change this line
```

## MCP Servers

### Kubernetes MCP Server

Automatically started when needed. Uses:
```bash
npx -y kubernetes-mcp-server@latest
```

Configuration in `config/mcp_servers.yaml`:
```yaml
servers:
  kubernetes:
    enabled: true
    env:
      KUBECONFIG: "${KUBECONFIG:-~/.kube/config}"
```

### Prometheus MCP Server

Automatically started when needed. Uses:
```bash
docker run -i --rm -e PROMETHEUS_URL=http://localhost:9090 \
  ghcr.io/pab1it0/prometheus-mcp-server:latest
```

Configuration in `config/mcp_servers.yaml`:
```yaml
servers:
  prometheus:
    enabled: true
    args:
      - "run"
      - "-i"
      - "--rm"
      - "-e"
      - "PROMETHEUS_URL=${PROMETHEUS_URL:-http://localhost:9090}"
```

## Diagnostic Capabilities

### Current (Phase 1)

- ✅ Pod crash and restart analysis
- ✅ Resource usage analysis (CPU, memory)
- ✅ Event correlation
- ✅ Log analysis
- ✅ Prometheus metrics integration

### Planned (Phase 2-4)

- 🚧 Network and service issues
- 🚧 Storage and PVC problems
- 🚧 Configuration mismatches
- 🚧 Security policy issues
- 🚧 Loki log aggregation
- 🚧 Automated remediation (HILT workflow)
- 🚧 GitOps integration for fixes

## Development Workflow

### Iteration 1: Foundation ✅

- [x] Project structure
- [x] Model configuration system
- [x] MCP tool wrappers (K8s, Prometheus)
- [x] Basic diagnostic agent
- [x] Test suite

### Iteration 2: Pod Crash RCA (In Progress)

- [ ] Enhanced pod crash flow
- [ ] Rich CLI output
- [ ] Real-world testing
- [ ] Documentation refinement

### Iteration 3: Multi-Agent System (Future)

- [ ] Specialized agents (network, storage, security)
- [ ] Agent collaboration flows
- [ ] Multiple scenario support

## Troubleshooting

### MCP server connection fails

1. Check that npx/docker are installed and accessible
2. Verify Prometheus URL is correct
3. Check kubectl configuration: `kubectl cluster-info`
4. Enable verbose logging: `python -m src.cli -v ...`

### Agent not using tools

1. Verify API keys are set correctly in `.env`
2. Check model has sufficient context window
3. Try adjusting temperature in `config/models.yaml`
4. Review logs for tool execution errors

### Import errors

```bash
# Ensure you're in the project root
cd /path/to/01-k8s-rca

# Reinstall dependencies
pip install -r requirements.txt
```

## Project Structure

```
01-k8s-rca/
├── config/
│   ├── models.yaml              # LLM model configurations
│   └── mcp_servers.yaml         # MCP server configurations
├── src/
│   ├── agents/
│   │   └── diagnostic_agent.py  # Agent definitions
│   ├── flows/                   # Future: CrewAI flows
│   ├── models/
│   │   └── config.py            # Model config loader
│   ├── tools/
│   │   ├── base.py              # Base MCP tool wrapper
│   │   ├── kubernetes.py        # K8s MCP tool
│   │   └── prometheus.py        # Prometheus MCP tool
│   └── cli.py                   # CLI interface
├── tests/
│   ├── test_tools.py            # Tool integration tests
│   └── test_agent.py            # Agent tests
├── .env.example                 # Environment template
├── .gitignore
├── pyproject.toml               # Project metadata
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## Contributing

This project follows an iterative development approach:

1. **Test as you go**: Each feature is tested before moving forward
2. **Keep it simple**: Prioritize clarity and maintainability
3. **Document decisions**: Comment why, not just what
4. **Real-world validation**: Test with actual cluster issues

## License

MIT License

## Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) - Multi-agent framework
- [MCP](https://modelcontextprotocol.io/) - Model Context Protocol
- [Kubernetes MCP Server](https://github.com/Flux159/kubernetes-mcp-server)
- [Prometheus MCP Server](https://github.com/pab1it0/prometheus-mcp-server)
