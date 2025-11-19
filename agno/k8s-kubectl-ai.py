import asyncio 
import os
from pathlib import Path
from textwrap import dedent

from agno.agent import Agent
from agno.tools.mcp import MCPTools

#from agno.models.ollama import Ollama
from mcp import ClientSession, StdioServerParameters
from agno.models.google import Gemini
#from agno.models.azure import AzureOpenAI

async def run_agent(message: str) -> None:
    """Run the filesystem agent with the given message."""

    #file_path = str(Path(__file__).parent.parent.parent.parent)

    # MCP server to access the filesystem (via `npx`)
    async with MCPTools(f"kubectl-ai --mcp-server") as mcp_tools:
        agent = Agent(
            #model=Ollama(id="mistral:latest"),
            #model=AzureOpenAI(id="gpt-5-mini")
            model=Gemini(id="gemini-2.0-flash"),
            tools=[mcp_tools],
            instructions=dedent("""\
                You are a kubernetes assistant. Help users manage and monitor their Kubernetes clusters.

                - Use the MCP tools to interact with Kubernetes directly
                - Execute commands through the MCP server instead of just describing them
                - List and inspect pods, deployments, and other resources
                - Monitor cluster health and resource usage
                - Provide clear explanations of Kubernetes concepts
                - Use headings to organize your responses
                - Be concise and focus on relevant information
                - Always explain what you're doing before executing commands
                - Handle errors gracefully and provide helpful error messages
                - Use headings to organize your responses
                - Be concise and focus on relevant information\
            """),
            markdown=True,
#            show_tool_calls=True,
        )

        # Run the agent
        await agent.aprint_response(message, stream=True)


# Example usage
if __name__ == "__main__":
    # Basic example - exploring project license
    asyncio.run(run_agent("List all pods in atharva-ml namespace, find out the root cause if any pod is failing"))
