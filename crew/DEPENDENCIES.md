# Dependencies Overview

## Core Dependencies

### CrewAI Framework
```
crewai[cli,google-genai]>=0.80.0
```

**Extras Included**:
- `cli` - CrewAI CLI tools for project scaffolding and management
- `google-genai` - Google Gemini integration (gemini-2.0-flash support)

**Provides**:
- Multi-agent orchestration
- Task management
- Agent collaboration
- Flow-based workflows

### CrewAI Tools
```
crewai-tools[mcp]>=0.12.0
```

**Extras Included**:
- `mcp` - Model Context Protocol support (includes mcpadapt)

**Provides**:
- MCPServerAdapter for MCP server integration
- Built-in tools collection
- Tool adapters for various services

### Model Context Protocol
```
mcp>=1.0.0
```

**Provides**:
- MCP client/server implementation
- StdioServerParameters for process management
- JSON-RPC communication layer

## LLM Providers

### Google Gemini
```
google-generativeai>=0.3.0
```

**Models Available**:
- gemini-2.0-flash (default)
- gemini-1.5-pro
- gemini-1.5-flash

### Anthropic Claude
```
anthropic>=0.18.0
```

**Models Available**:
- claude-3-5-sonnet-20241022
- claude-3-opus-20240229

### OpenAI (via LiteLLM)
```
litellm>=1.0.0
```

**Models Available**:
- gpt-4o
- gpt-4-turbo-preview

## Utility Libraries

### Pydantic
```
pydantic>=2.0.0
```
- Data validation
- Settings management
- Type safety

### PyYAML
```
pyyaml>=6.0.0
```
- Configuration file parsing (models.yaml, mcp_servers.yaml)

### Rich
```
rich>=13.0.0
```
- Terminal formatting
- Progress bars
- Panels and tables

### Python-dotenv
```
python-dotenv>=1.0.0
```
- Environment variable loading from .env files

## Installation

### Using uv (Recommended)
```bash
uv pip install -r requirements.txt
```

### Using pip
```bash
pip install -r requirements.txt
```

### Using setup script
```bash
./setup.sh
```

## Optional Dev Dependencies

For development and testing:
```bash
uv pip install -e ".[dev]"
```

Includes:
- pytest>=7.0.0
- pytest-asyncio>=0.21.0
- black>=23.0.0
- ruff>=0.1.0

## Extras Explained

### CrewAI Extras

**`[cli]`**
- Enables `crewai` command-line tool
- Project scaffolding: `crewai create`
- Crew management commands
- Development utilities

**`[google-genai]`**
- Native Gemini integration
- Optimized for Google's models
- Automatic retry and rate limiting
- Streaming support

### CrewAI Tools Extras

**`[mcp]`**
- Installs `mcpadapt` package
- Enables MCPServerAdapter
- MCP protocol support
- Seamless tool integration

## Version Requirements

- **Python**: >=3.10
- **Node.js**: Latest LTS (for Kubernetes MCP server)
- **Docker**: Latest stable (for Prometheus MCP server)

## MCP Servers (External)

These are not Python packages but external services:

### Kubernetes MCP Server
```bash
npx -y kubernetes-mcp-server@latest
```
- Provides 19 Kubernetes operations
- Accessed via MCP protocol
- Auto-started by MCPServerAdapter

### Prometheus MCP Server
```bash
docker run -i --rm \
  -e PROMETHEUS_URL=http://localhost:9090 \
  ghcr.io/pab1it0/prometheus-mcp-server:latest
```
- Provides 6 Prometheus query operations
- Accessed via MCP protocol
- Auto-started by MCPServerAdapter

## Dependency Tree

```
k8s-rca-crew
├── crewai[cli,google-genai]
│   ├── langchain-core
│   ├── google-generativeai
│   └── CLI utilities
├── crewai-tools[mcp]
│   ├── mcpadapt
│   └── mcp
├── pydantic (validation)
├── pyyaml (config)
├── rich (UI)
├── python-dotenv (env)
├── litellm (multi-provider)
├── google-generativeai (Gemini)
└── anthropic (Claude)
```

## Update Commands

To update dependencies:

```bash
# Update all packages
uv pip install -U -r requirements.txt

# Update specific package
uv pip install -U crewai

# Sync with pyproject.toml
uv pip sync
```

## Troubleshooting

### If MCP imports fail
```bash
uv pip install "crewai-tools[mcp]"
```

### If Gemini fails
```bash
uv pip install "crewai[google-genai]" google-generativeai
```

### If CLI commands don't work
```bash
uv pip install "crewai[cli]"
```

### Clean install
```bash
# Remove venv
rm -rf .venv

# Recreate
python3 -m venv .venv
source .venv/bin/activate  # or with uv

# Install
uv pip install -r requirements.txt
```

## Package Sizes (Approximate)

- crewai: ~50MB
- crewai-tools: ~30MB
- google-generativeai: ~10MB
- anthropic: ~5MB
- Total: ~150MB (with dependencies)

## License Compatibility

All dependencies use permissive licenses:
- MIT: crewai, pydantic, rich, python-dotenv
- Apache 2.0: google-generativeai, anthropic
- BSD: pyyaml

---

Last Updated: 2025-11-11
