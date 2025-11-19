"""Simple non-interactive agent test.

Tests basic agent creation without requiring API keys or user input.
"""

import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agents.diagnostic_agent import DiagnosticAgentFactory, create_pod_crash_analyzer
from src.tools.mcp_helpers import get_all_diagnostic_tools

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def test_agent_creation():
    """Test that agents can be created successfully."""
    print("\n" + "=" * 80)
    print("Testing Agent Creation")
    print("=" * 80 + "\n")

    try:
        # Test basic agent creation
        print("Creating basic diagnostic agent...")
        agent = DiagnosticAgentFactory.create_agent()
        print(f"✅ Basic agent created: {agent.role}")

        # Test pod crash analyzer
        print("\nCreating pod crash analyzer...")
        crash_agent = create_pod_crash_analyzer()
        print(f"✅ Pod crash analyzer created: {crash_agent.role}")

        return True

    except Exception as e:
        logger.error(f"Agent creation test failed: {e}", exc_info=True)
        print(f"\n❌ Agent creation test failed: {e}")
        return False


def test_tools_available():
    """Test that MCP tools are accessible."""
    print("\n" + "=" * 80)
    print("Testing Tools Availability")
    print("=" * 80 + "\n")

    try:
        print("Getting diagnostic tools...")
        tools = get_all_diagnostic_tools()

        print(f"✅ Retrieved {len(tools)} tools")

        if tools:
            print("\nAvailable tools:")
            for tool in tools[:5]:  # Show first 5
                print(f"   - {tool.name}")
            if len(tools) > 5:
                print(f"   ... and {len(tools) - 5} more")

        return len(tools) > 0

    except Exception as e:
        logger.error(f"Tools availability test failed: {e}", exc_info=True)
        print(f"\n❌ Tools availability test failed: {e}")
        return False


def test_agent_has_tools():
    """Test that agents are created with tools."""
    print("\n" + "=" * 80)
    print("Testing Agent Tool Assignment")
    print("=" * 80 + "\n")

    try:
        print("Creating agent with tools...")
        agent = DiagnosticAgentFactory.create_agent()

        tool_count = len(agent.tools) if hasattr(agent, 'tools') and agent.tools else 0
        print(f"✅ Agent has {tool_count} tools assigned")

        if tool_count > 0:
            print("\nAgent's tools:")
            for tool in agent.tools[:5]:
                print(f"   - {tool.name}")
            if tool_count > 5:
                print(f"   ... and {tool_count - 5} more")

        return tool_count > 0

    except Exception as e:
        logger.error(f"Agent tool assignment test failed: {e}", exc_info=True)
        print(f"\n❌ Agent tool assignment test failed: {e}")
        return False


def main():
    """Run all non-interactive agent tests."""
    print("\n" + "=" * 80)
    print("AGENT TESTS (Non-Interactive)")
    print("=" * 80)
    print("\nNote: These tests check agent creation and tool availability.")
    print("API keys are NOT required for these tests.\n")

    results = {}

    # Test agent creation
    results["agent_creation"] = test_agent_creation()

    # Test tools availability
    results["tools_available"] = test_tools_available()

    # Test agent has tools
    results["agent_has_tools"] = test_agent_has_tools()

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
        print("\nNext steps:")
        print("1. Add API key to .env file")
        print("2. Run: .venv/bin/python tests/test_agent.py (for full interactive test)")
        print("3. Or try: make list-models")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the logs above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
