"""Test script for MCP tools integration.

This script tests the Kubernetes and Prometheus MCP tools to ensure
they can connect to MCP servers and are available.
"""

import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.tools.mcp_helpers import (
    get_kubernetes_mcp_adapter,
    get_prometheus_mcp_adapter,
    load_mcp_config,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def test_kubernetes_config():
    """Test Kubernetes MCP configuration loading."""
    print("\n" + "=" * 80)
    print("Testing Kubernetes Configuration")
    print("=" * 80 + "\n")

    try:
        config = load_mcp_config("kubernetes")
        print(f"✅ Config loaded successfully")
        print(f"   Enabled: {config.enabled}")
        print(f"   Type: {config.type}")
        print(f"   Command: {config.command}")
        print(f"   Args: {config.args}")
        return True
    except Exception as e:
        logger.error(f"Kubernetes config test failed: {e}")
        print(f"\n❌ Kubernetes config test failed: {e}")
        return False


def test_prometheus_config():
    """Test Prometheus MCP configuration loading."""
    print("\n" + "=" * 80)
    print("Testing Prometheus Configuration")
    print("=" * 80 + "\n")

    try:
        config = load_mcp_config("prometheus")
        print(f"✅ Config loaded successfully")
        print(f"   Enabled: {config.enabled}")
        print(f"   Type: {config.type}")
        print(f"   Command: {config.command}")
        return True
    except Exception as e:
        logger.error(f"Prometheus config test failed: {e}")
        print(f"\n❌ Prometheus config test failed: {e}")
        return False


def test_kubernetes_adapter():
    """Test Kubernetes MCP adapter."""
    print("\n" + "=" * 80)
    print("Testing Kubernetes MCP Adapter")
    print("=" * 80 + "\n")

    try:
        print("Creating Kubernetes MCP adapter...")
        with get_kubernetes_mcp_adapter() as tools:
            print(f"✅ Adapter created successfully")
            print(f"   Available tools: {len(tools)}")

            if tools:
                print("\n   Tool names:")
                for tool in tools:
                    print(f"   - {tool.name}")
            else:
                print("   ⚠️  No tools available")

            return len(tools) > 0

    except Exception as e:
        logger.error(f"Kubernetes adapter test failed: {e}", exc_info=True)
        print(f"\n❌ Kubernetes adapter test failed: {e}")
        return False


def test_prometheus_adapter():
    """Test Prometheus MCP adapter."""
    print("\n" + "=" * 80)
    print("Testing Prometheus MCP Adapter")
    print("=" * 80 + "\n")

    try:
        print("Creating Prometheus MCP adapter...")
        with get_prometheus_mcp_adapter() as tools:
            print(f"✅ Adapter created successfully")
            print(f"   Available tools: {len(tools)}")

            if tools:
                print("\n   Tool names:")
                for tool in tools:
                    print(f"   - {tool.name}")
            else:
                print("   ⚠️  No tools available")

            return len(tools) > 0

    except Exception as e:
        logger.error(f"Prometheus adapter test failed: {e}", exc_info=True)
        print(f"\n❌ Prometheus adapter test failed: {e}")
        print(f"\n   Note: Ensure Prometheus is running at the configured URL")
        return False


def main():
    """Run all tool tests."""
    print("\n" + "=" * 80)
    print("MCP TOOLS INTEGRATION TEST")
    print("=" * 80)
    print("\nNote: This test requires:")
    print("1. A running Kubernetes cluster with kubectl configured")
    print("2. Node.js/npx installed (for Kubernetes MCP server)")
    print("3. Docker installed (for Prometheus MCP server)")
    print("4. Prometheus running (optional, for Prometheus tests)")

    results = {}

    # Test configurations
    results["kubernetes_config"] = test_kubernetes_config()
    results["prometheus_config"] = test_prometheus_config()

    # Test adapters
    print("\n" + "=" * 80)
    print("Testing MCP Server Connections (this may take a moment...)")
    print("=" * 80)

    results["kubernetes_adapter"] = test_kubernetes_adapter()
    results["prometheus_adapter"] = test_prometheus_adapter()

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name.replace('_', ' ').title()}: {status}")

    all_passed = all(results.values())
    if all_passed:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n⚠️  Some tests failed. This is often normal:")
        print("   - Prometheus tests will fail if Prometheus is not running")
        print("   - MCP server tests require proper environment setup")
        print("\nCheck the logs above for specific errors.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
