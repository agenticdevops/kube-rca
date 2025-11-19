import asyncio
from textwrap import dedent
from agno.agent import Agent
#from agno.models.ollama import Ollama
from agno.tools.mcp import MCPTools
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from agno.models.google import Gemini

async def interactive_chat():
    """Run an interactive chat session with the Kubernetes agent."""
    print("Initializing Kubernetes MCP server...")
    
    # Initialize the MCP server
    server_params = StdioServerParameters(
        command="kubectl-ai",
        args=["mcp-server"]
    )

    try:
        print("Starting MCP server and creating session...")
        # First create the stdio client
        async with stdio_client(server_params) as (read, write):
            print("MCP server started")
            
            # Then create the client session
            async with ClientSession(read, write) as session:
                print("Client session created")
                
                # Initialize MCP tools with the session
                mcp_tools = MCPTools(session=session)
                await mcp_tools.initialize()
                print("MCP tools initialized")
                
                try:
                    # List available tools
                    result = await session.list_tools()
                    print("\nAvailable Kubernetes tools:")
                    tools = result.tools
                    if not tools:
                        print("No tools found!")
                        return
                    
                    for tool in tools:
                        print(f"- {tool.name}: {tool.description}")
                    
                    # Create agent with the initialized mcp_tools
                    agent = Agent(
                        #model=Ollama(id="granite3.1-dense:2b"),
                        model=Gemini(id="gemini-2.0-flash"),
                        tools=[mcp_tools],
                        system_message="You are a Kubernetes assistant that MUST use the provided MCP tools to interact with the cluster. NEVER make up responses or show example code - ALWAYS execute the actual tools and show their real output.",
                        instructions=dedent("""\
                            You are a Kubernetes assistant that uses MCP tools to interact with the cluster.
                            
                            CRITICAL INSTRUCTIONS:
                            - You MUST execute the actual MCP tools to get real data from the cluster
                            - NEVER show example code or describe what you would do
                            - ALWAYS execute the tools and show their real output
                            - If a tool call fails, explain the error
                            - Format responses in markdown
                            
                            When asked about Kubernetes resources:
                            1. Execute the appropriate tool (e.g., namespaces_list, pods_list, etc.)
                            2. Show the actual tool call and its real output
                            3. Explain the results in a clear, concise way
                            
                            Available tools:
                            {}
                            
                            Remember: ALWAYS execute the tools and show real data. Never make up responses or show example code.
                            """.format("\n".join(f"- {t.name}: {t.description}" for t in tools))),
                        markdown=True,
                        show_tool_calls=True,
                    )

                    print("\nKubernetes Assistant is ready! Type 'exit' to quit.")
                    print("Example commands:")
                    print("- List all pods in the default namespace")
                    print("- Show deployments in kube-system")
                    print("- Get all namespaces")

                    while True:
                        try:
                            user_input = input("\nYou: ").strip()
                            
                            if user_input.lower() in ['exit', 'quit', 'bye']:
                                print("\nGoodbye!")
                                break
                            
                            if not user_input:
                                continue

                            print("\nAssistant: ", end="", flush=True)
                            await agent.aprint_response(user_input, stream=True)
                            
                        except Exception as e:
                            print(f"\nError processing request: {str(e)}")
                            print("Please try again.")
                except Exception as e:
                    print(f"Error getting tools: {str(e)}")
                    return

    except Exception as e:
        print(f"Error: {str(e)}")
        print("Failed to start MCP server or create session.")
        raise

if __name__ == "__main__":
    asyncio.run(interactive_chat())
