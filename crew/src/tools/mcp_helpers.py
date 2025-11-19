"""Helper functions for MCP server integration.

Uses CrewAI's built-in MCPServerAdapter for reliable MCP server management.
"""

import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List

import yaml
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class MCPServerConfig(BaseModel):
    """Configuration for an MCP server."""

    enabled: bool = Field(default=True)
    type: str = Field(..., description="Server type: npx, docker, or custom")
    command: str = Field(..., description="Command to start the server")
    args: List[str] = Field(default_factory=list)
    env: Dict[str, str] = Field(default_factory=dict)
    description: str = Field(default="")


def load_mcp_config(server_name: str) -> MCPServerConfig:
    """Load MCP server configuration from YAML.

    Args:
        server_name: Name of the MCP server

    Returns:
        MCPServerConfig instance

    Raises:
        FileNotFoundError: If config file not found
        ValueError: If server not found in config
    """
    config_path = Path(__file__).parent.parent.parent / "config" / "mcp_servers.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"MCP config not found: {config_path}")

    with open(config_path, "r") as f:
        config_data = yaml.safe_load(f)

    servers = config_data.get("servers", {})
    if server_name not in servers:
        raise ValueError(f"Server '{server_name}' not found in config")

    return MCPServerConfig(**servers[server_name])


def expand_env_var(value: str) -> str:
    """Expand environment variables and paths in a string.

    Supports ${VAR:-default} syntax and tilde expansion.

    Args:
        value: String with environment variable placeholders

    Returns:
        String with variables and paths expanded
    """
    # Pattern: ${VAR} or ${VAR:-default}
    pattern = r"\$\{([^}:]+)(?::-([^}]*))?\}"

    def replace(match):
        var_name = match.group(1)
        default_value = match.group(2) or ""
        return os.getenv(var_name, default_value)

    # Expand environment variables
    expanded = re.sub(pattern, replace, value)

    # Expand tilde (~) to home directory
    expanded = os.path.expanduser(expanded)

    return expanded


def create_mcp_server_params(server_name: str) -> StdioServerParameters:
    """Create server parameters for MCPServerAdapter.

    Args:
        server_name: Name of the MCP server

    Returns:
        StdioServerParameters instance suitable for MCPServerAdapter
    """
    config = load_mcp_config(server_name)

    if not config.enabled:
        raise ValueError(f"MCP server '{server_name}' is disabled in config")

    # Expand environment variables
    env = {}
    for key, value in config.env.items():
        env[key] = expand_env_var(value)

    # Merge with current environment
    full_env = {**os.environ, **env}

    # Build command and expand variables in args
    command = config.command
    args = [expand_env_var(arg) for arg in config.args]

    # Return StdioServerParameters for MCPServerAdapter
    return StdioServerParameters(
        command=command,
        args=args,
        env=full_env,
    )


def get_kubernetes_tools() -> List[Any]:
    """Get Kubernetes MCP tools.

    Returns:
        List of Kubernetes tools from MCP server

    Example:
        >>> with get_kubernetes_mcp_adapter() as tools:
        ...     agent = Agent(tools=tools, ...)
    """
    params = create_mcp_server_params("kubernetes")
    adapter = MCPServerAdapter(params)
    return adapter.tools


def get_prometheus_tools() -> List[Any]:
    """Get Prometheus MCP tools.

    Returns:
        List of Prometheus tools from MCP server
    """
    params = create_mcp_server_params("prometheus")
    adapter = MCPServerAdapter(params)
    return adapter.tools


def get_kubernetes_mcp_adapter() -> MCPServerAdapter:
    """Get Kubernetes MCP server adapter for use in context manager.

    Returns:
        MCPServerAdapter instance

    Example:
        >>> with get_kubernetes_mcp_adapter() as tools:
        ...     agent = Agent(tools=tools, ...)
    """
    params = create_mcp_server_params("kubernetes")
    return MCPServerAdapter(params)


def get_prometheus_mcp_adapter() -> MCPServerAdapter:
    """Get Prometheus MCP server adapter for use in context manager.

    Returns:
        MCPServerAdapter instance

    Example:
        >>> with get_prometheus_mcp_adapter() as tools:
        ...     agent = Agent(tools=tools, ...)
    """
    params = create_mcp_server_params("prometheus")
    return MCPServerAdapter(params)


def get_all_diagnostic_tools() -> List[Any]:
    """Get all diagnostic tools (Kubernetes + Prometheus).

    Returns:
        Combined list of all diagnostic tools

    Note:
        This creates adapters that need to be stopped manually.
        Prefer using context managers for proper cleanup.
    """
    tools = []

    try:
        k8s_adapter = get_kubernetes_mcp_adapter()
        tools.extend(k8s_adapter.tools)
    except Exception as e:
        logger.warning(f"Failed to load Kubernetes tools: {e}")

    try:
        prom_adapter = get_prometheus_mcp_adapter()
        tools.extend(prom_adapter.tools)
    except Exception as e:
        logger.warning(f"Failed to load Prometheus tools: {e}")

    return tools
