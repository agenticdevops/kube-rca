"""Diagnostic agent for Kubernetes RCA.

Provides the initial diagnostic agent that can analyze Kubernetes issues
using cluster data and metrics.
"""

import logging
from typing import Any, List, Optional

from crewai import Agent

from src.models.config import get_llm_config
from src.tools.mcp_helpers import get_all_diagnostic_tools

logger = logging.getLogger(__name__)


class DiagnosticAgentFactory:
    """Factory for creating diagnostic agents with appropriate tools."""

    @staticmethod
    def create_agent(
        model_id: Optional[str] = None, tools: Optional[List[Any]] = None
    ) -> Agent:
        """Create a diagnostic agent.

        Args:
            model_id: Model identifier (uses default if None)
            tools: List of tools (uses default tools if None)

        Returns:
            Configured Agent instance
        """
        if tools is None:
            tools = get_all_diagnostic_tools()

        # Get model configuration
        llm_config = get_llm_config(model_id)

        agent = Agent(
            role="Kubernetes Diagnostics Specialist",
            goal=(
                "Diagnose and analyze Kubernetes cluster issues by examining "
                "pod status, logs, events, metrics, and configurations. "
                "Provide clear root cause analysis and actionable recommendations."
            ),
            backstory=(
                "You are an expert Site Reliability Engineer (SRE) with deep knowledge "
                "of Kubernetes, container orchestration, and distributed systems. "
                "You excel at systematically diagnosing issues by gathering relevant data, "
                "analyzing patterns, and identifying root causes. "
                "\n\n"
                "Your approach:\n"
                "1. Gather comprehensive information about the issue\n"
                "2. Analyze logs, events, and metrics systematically\n"
                "3. Correlate data from multiple sources\n"
                "4. Identify the root cause with evidence\n"
                "5. Provide clear, actionable remediation steps\n"
                "\n"
                "You are thorough, methodical, and always back your conclusions with data."
            ),
            tools=tools,
            verbose=True,
            allow_delegation=False,
            llm=llm_config.get("model"),
            max_iter=15,  # Allow multiple tool calls for thorough investigation
        )

        logger.info(f"Created diagnostic agent with model: {llm_config.get('model')}")
        return agent


def create_pod_crash_analyzer(model_id: Optional[str] = None) -> Agent:
    """Create an agent specialized in pod crash analysis.

    Args:
        model_id: Model identifier

    Returns:
        Configured Agent instance
    """
    tools = get_all_diagnostic_tools()
    llm_config = get_llm_config(model_id)

    agent = Agent(
        role="Pod Crash Analysis Specialist",
        goal=(
            "Investigate why pods are crashing or restarting. "
            "Analyze pod status, container logs, resource usage, and events "
            "to determine the root cause of crashes."
        ),
        backstory=(
            "You are a Kubernetes expert specializing in container crashes and restarts. "
            "You know that common causes include:\n"
            "- Out of Memory (OOM) kills\n"
            "- Application errors and exceptions\n"
            "- Liveness/readiness probe failures\n"
            "- Resource constraints (CPU throttling)\n"
            "- Configuration errors\n"
            "- Node issues\n"
            "\n"
            "Your systematic approach:\n"
            "1. Check pod status and restart count\n"
            "2. Review recent events for the pod\n"
            "3. Examine container logs for errors\n"
            "4. Check resource usage (CPU, memory)\n"
            "5. Analyze resource limits and requests\n"
            "6. Look for patterns in crash timing\n"
            "7. Identify the root cause\n"
            "8. Recommend specific fixes\n"
            "\n"
            "You always provide evidence-based analysis and practical remediation steps."
        ),
        tools=tools,
        verbose=True,
        allow_delegation=False,
        llm=llm_config.get("model"),
        max_iter=20,
    )

    logger.info(f"Created pod crash analyzer with model: {llm_config.get('model')}")
    return agent


def create_resource_analyzer(model_id: Optional[str] = None) -> Agent:
    """Create an agent specialized in resource analysis.

    Args:
        model_id: Model identifier

    Returns:
        Configured Agent instance
    """
    tools = get_all_diagnostic_tools()
    llm_config = get_llm_config(model_id)

    agent = Agent(
        role="Resource Analysis Specialist",
        goal=(
            "Analyze Kubernetes resource usage and constraints. "
            "Identify resource-related issues like CPU throttling, memory pressure, "
            "quota violations, and provide optimization recommendations."
        ),
        backstory=(
            "You are a Kubernetes resource management expert. "
            "You understand resource requests, limits, quality of service (QoS), "
            "and how they affect pod scheduling and runtime behavior. "
            "\n"
            "You analyze:\n"
            "- CPU and memory usage patterns\n"
            "- Resource requests vs actual usage\n"
            "- Resource limits and throttling\n"
            "- Namespace quotas and limit ranges\n"
            "- Node capacity and allocation\n"
            "\n"
            "You provide data-driven recommendations for right-sizing resources "
            "and optimizing cluster utilization."
        ),
        tools=tools,
        verbose=True,
        allow_delegation=False,
        llm=llm_config.get("model"),
        max_iter=15,
    )

    logger.info(f"Created resource analyzer with model: {llm_config.get('model')}")
    return agent
