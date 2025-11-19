"""CLI interface for Kubernetes RCA Crew.

Provides command-line interface for running diagnostic agents.
"""

import argparse
import logging
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from crewai import Crew, Task

from src.agents.diagnostic_agent import (
    DiagnosticAgentFactory,
    create_pod_crash_analyzer,
    create_resource_analyzer,
)
from src.models.config import get_model_config_manager

# Load environment variables
load_dotenv()

# Rich console for better output
console = Console()


def setup_logging(verbose: bool = False):
    """Setup logging configuration.

    Args:
        verbose: Enable verbose logging
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )


def diagnose_pod_crash(pod_name: str, namespace: str = "default", model: str = None):
    """Diagnose a crashing pod.

    Args:
        pod_name: Name of the pod
        namespace: Kubernetes namespace
        model: Model to use for diagnosis
    """
    console.print(
        Panel.fit(
            f"[bold cyan]Kubernetes Pod Crash Analysis[/bold cyan]\n\n"
            f"Pod: [yellow]{pod_name}[/yellow]\n"
            f"Namespace: [yellow]{namespace}[/yellow]\n"
            f"Model: [yellow]{model or 'default'}[/yellow]",
            border_style="cyan",
        )
    )

    try:
        # Create agent
        with Progress(
            SpinnerColumn(), TextColumn("[progress.description]{task.description}")
        ) as progress:
            progress.add_task(description="Initializing diagnostic agent...", total=None)
            agent = create_pod_crash_analyzer(model_id=model)

        # Create task
        task = Task(
            description=(
                f"Analyze the pod '{pod_name}' in namespace '{namespace}'. "
                "Perform a comprehensive root cause analysis:\n"
                "1. Check pod status, phase, and restart count\n"
                "2. Review recent Kubernetes events for this pod\n"
                "3. Examine container logs for errors and exceptions\n"
                "4. Analyze resource usage (CPU, memory) from Prometheus\n"
                "5. Check if resource limits/requests are appropriate\n"
                "6. Identify patterns in crash timing\n"
                "7. Determine the root cause with evidence\n"
                "8. Provide specific, actionable remediation steps\n\n"
                "Be thorough and systematic in your investigation."
            ),
            expected_output=(
                "A comprehensive RCA report including:\n"
                "1. Executive Summary\n"
                "2. Current Status (pod phase, restart count, etc.)\n"
                "3. Key Findings (events, logs, metrics)\n"
                "4. Root Cause Analysis (with evidence)\n"
                "5. Remediation Recommendations (specific steps)\n"
                "6. Prevention Measures"
            ),
            agent=agent,
        )

        # Create crew and execute
        console.print("\n[bold]Starting diagnosis...[/bold]\n")
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=False
        )
        result = crew.kickoff()

        # Display result
        console.print(
            Panel(
                str(result),
                title="[bold green]Diagnosis Complete[/bold green]",
                border_style="green",
            )
        )

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        logging.exception("Diagnosis failed")
        return 1

    return 0


def diagnose_generic(description: str, model: str = None):
    """Run generic Kubernetes diagnosis.

    Args:
        description: Description of the issue
        model: Model to use for diagnosis
    """
    console.print(
        Panel.fit(
            f"[bold cyan]Kubernetes Diagnostics[/bold cyan]\n\n"
            f"Issue: [yellow]{description}[/yellow]\n"
            f"Model: [yellow]{model or 'default'}[/yellow]",
            border_style="cyan",
        )
    )

    try:
        # Create agent
        with Progress(
            SpinnerColumn(), TextColumn("[progress.description]{task.description}")
        ) as progress:
            progress.add_task(description="Initializing diagnostic agent...", total=None)
            agent = DiagnosticAgentFactory.create_agent(model_id=model)

        # Create task
        task = Task(
            description=(
                f"Investigate the following Kubernetes issue:\n\n{description}\n\n"
                "Perform a systematic diagnosis:\n"
                "1. Gather relevant information from the cluster\n"
                "2. Check resource status and configurations\n"
                "3. Review logs and events\n"
                "4. Analyze metrics if applicable\n"
                "5. Identify the root cause\n"
                "6. Provide remediation recommendations"
            ),
            expected_output="A detailed analysis with root cause and recommendations",
            agent=agent,
        )

        # Create crew and execute
        console.print("\n[bold]Starting diagnosis...[/bold]\n")
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=False
        )
        result = crew.kickoff()

        # Display result
        console.print(
            Panel(
                str(result),
                title="[bold green]Diagnosis Complete[/bold green]",
                border_style="green",
            )
        )

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        logging.exception("Diagnosis failed")
        return 1

    return 0


def list_models():
    """List available models."""
    config_manager = get_model_config_manager()
    models = config_manager.list_models()

    console.print(Panel.fit("[bold cyan]Available Models[/bold cyan]", border_style="cyan"))
    console.print()

    for model_id in models:
        model = config_manager.get_model(model_id)
        console.print(f"  • [yellow]{model_id}[/yellow]: {model.model_name} ({model.provider})")

    console.print()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Kubernetes Root Cause Analysis using CrewAI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    parser.add_argument("--model", "-m", help="Model to use (default: from config)")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Pod crash command
    crash_parser = subparsers.add_parser("pod-crash", help="Diagnose a crashing pod")
    crash_parser.add_argument("pod_name", help="Name of the pod")
    crash_parser.add_argument(
        "--namespace", "-n", default="default", help="Kubernetes namespace"
    )

    # Generic diagnose command
    diagnose_parser = subparsers.add_parser("diagnose", help="Run generic diagnosis")
    diagnose_parser.add_argument("description", help="Description of the issue")

    # List models command
    subparsers.add_parser("list-models", help="List available models")

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.verbose)

    # Handle commands
    if args.command == "pod-crash":
        return diagnose_pod_crash(args.pod_name, args.namespace, args.model)
    elif args.command == "diagnose":
        return diagnose_generic(args.description, args.model)
    elif args.command == "list-models":
        list_models()
        return 0
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
