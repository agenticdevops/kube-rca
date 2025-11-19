"""Test script for diagnostic agent.

This script tests the diagnostic agent to ensure it can use tools
and reason about Kubernetes issues.
"""

import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from crewai import Crew, Task

from src.agents.diagnostic_agent import DiagnosticAgentFactory, create_pod_crash_analyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def test_basic_agent():
    """Test basic agent creation and task execution."""
    print("\n" + "=" * 80)
    print("Testing Basic Diagnostic Agent")
    print("=" * 80 + "\n")

    try:
        # Create agent
        agent = DiagnosticAgentFactory.create_agent()
        logger.info("Agent created successfully")

        # Create a simple task
        task = Task(
            description=(
                "List all pods in the default namespace and report their status. "
                "Identify any pods that are not in Running state."
            ),
            expected_output="A summary of pod status in the default namespace",
            agent=agent,
        )

        # Create crew and execute
        print("\n--- Creating crew and executing task ---")
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )

        result = crew.kickoff()

        print("\n--- Task Result ---")
        print(result)

        print("\n✅ Basic agent test completed")
        return True

    except Exception as e:
        logger.error(f"Basic agent test failed: {e}", exc_info=True)
        print(f"\n❌ Basic agent test failed: {e}")
        return False


def test_pod_crash_analyzer():
    """Test pod crash analyzer agent."""
    print("\n" + "=" * 80)
    print("Testing Pod Crash Analyzer Agent")
    print("=" * 80 + "\n")

    try:
        # Create agent
        agent = create_pod_crash_analyzer()
        logger.info("Pod crash analyzer created successfully")

        # Get pod name from user or use a test pod
        pod_name = input(
            "\nEnter a pod name to analyze (or press Enter to skip): "
        ).strip()

        if not pod_name:
            print("Skipping pod crash analysis test (no pod name provided)")
            return True

        namespace = input("Enter namespace (default: default): ").strip() or "default"

        # Create a task to analyze the pod
        task = Task(
            description=(
                f"Analyze the pod '{pod_name}' in namespace '{namespace}'. "
                "Check if it's crashing or restarting, examine logs, events, "
                "and resource usage. Provide a root cause analysis and recommendations."
            ),
            expected_output=(
                "A comprehensive RCA report with:\n"
                "1. Pod status and restart count\n"
                "2. Key events and log messages\n"
                "3. Resource usage analysis\n"
                "4. Root cause identification\n"
                "5. Remediation recommendations"
            ),
            agent=agent,
        )

        # Create crew and execute
        print("\n--- Creating crew and executing pod crash analysis ---")
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )

        result = crew.kickoff()

        print("\n--- Analysis Result ---")
        print(result)

        print("\n✅ Pod crash analyzer test completed")
        return True

    except Exception as e:
        logger.error(f"Pod crash analyzer test failed: {e}", exc_info=True)
        print(f"\n❌ Pod crash analyzer test failed: {e}")
        return False


def main():
    """Run all agent tests."""
    print("\n" + "=" * 80)
    print("DIAGNOSTIC AGENT TEST")
    print("=" * 80)
    print("\nNote: This test requires:")
    print("1. A running Kubernetes cluster with kubectl configured")
    print("2. Prometheus accessible (if testing metrics)")
    print("3. API keys configured in .env file")

    proceed = input("\nReady to proceed? (y/n): ").strip().lower()
    if proceed != "y":
        print("Test cancelled.")
        return 0

    results = {}

    # Test basic agent
    results["basic_agent"] = test_basic_agent()

    # Test pod crash analyzer
    test_crash = input("\nTest pod crash analyzer? (y/n): ").strip().lower()
    if test_crash == "y":
        results["pod_crash_analyzer"] = test_pod_crash_analyzer()

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")

    all_passed = all(results.values())
    if all_passed:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n⚠️ Some tests failed. Check the logs above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
