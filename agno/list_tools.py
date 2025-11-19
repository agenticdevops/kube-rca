import asyncio
from agno.tools.mcp import MCPTools
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def list_mcp_tools():
    """List all available tools from the MCP server."""
    print("Initializing MCP server...")
    
    # Initialize the MCP server
    server_params = StdioServerParameters(
        command="npx",
        args=[
            "-y",
            "kubernetes-mcp-server@latest"
        ],
    )

    print("Connecting to MCP server...")
    
    try:
        # Create a client session to connect to the MCP server
        async with stdio_client(server_params) as (read, write):
            print("Connected to MCP server")
            
            async with ClientSession(read, write) as session:
                print("Created client session")
                
                # Initialize MCP tools
                mcp_tools = MCPTools(session=session)
                print("Created MCP tools instance")
                
                await mcp_tools.initialize()
                print("Initialized MCP tools")
                
                # Wait for tools to be registered
                print("Waiting for tools to be registered...")
                await asyncio.sleep(2)
                
                # Get and display available tools
                print("\nFetching available tools...")
                
                try:
                    # Get tools using session's list_tools method
                    result = await session.list_tools()
                    print("Got tools using session.list_tools()")
                    
                    print("\nAvailable MCP Tools:")
                    print("===================")
                    
                    # Get tools from the result
                    tools = result.tools
                    if not tools:
                        print("No tools found!")
                        return
                    
                    # Sort tools by name for better readability
                    tools = sorted(tools, key=lambda x: x.name)
                    
                    for tool in tools:
                        print(f"\n{tool.name}")
                        print("-" * len(tool.name))
                        print(f"Description: {tool.description}")
                        
                        # Get input schema
                        if hasattr(tool, 'inputSchema') and tool.inputSchema:
                            schema = tool.inputSchema
                            if 'properties' in schema:
                                print("\nParameters:")
                                properties = schema['properties']
                                required = schema.get('required', [])
                                
                                # Sort parameters by required first, then alphabetically
                                param_names = sorted(properties.keys())
                                param_names = sorted(param_names, key=lambda x: x in required, reverse=True)
                                
                                for param_name in param_names:
                                    param = properties[param_name]
                                    param_type = param.get('type', 'unknown')
                                    param_desc = param.get('description', 'No description')
                                    is_required = param_name in required
                                    
                                    print(f"  - {param_name} ({param_type})")
                                    print(f"    {param_desc}")
                                    if is_required:
                                        print("    [Required]")
                        print()
                except Exception as e:
                    print(f"Error getting tools: {str(e)}")
                    raise
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(list_mcp_tools())