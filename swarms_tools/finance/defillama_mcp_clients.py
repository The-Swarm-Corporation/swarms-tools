from contextlib import AsyncExitStack
from typing import List, Dict, Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    def __init__(self):
        """Initialize MCP client"""
        self.session = None
        self.exit_stack = AsyncExitStack()
        self.tools = []

    async def connect_to_server(
        self,
        server_script_path="./swarms_tools/finance/defillama_mcp_tools.py",
    ):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script
        """
        server_params = StdioServerParameters(
            command="python", args=[server_script_path], env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        self.tools = response.tools
        print(
            "\nConnected to server with tools:",
            [tool.name for tool in self.tools],
        )
        return self.tools

    async def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools with their details"""
        if not self.session:
            raise ValueError(
                "Not connected to server. Call connect_to_server() first."
            )

        tool_details = []
        for tool in self.tools:
            tool_info = {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema,
            }
            tool_details.append(tool_info)

        return tool_details

    async def call_tool(
        self, tool_name: str, tool_args: Dict[str, Any]
    ) -> Any:
        """Call a tool with the given arguments

        Args:
            tool_name: Name of the tool to call
            tool_args: Arguments to pass to the tool

        Returns:
            Tool execution result
        """
        if not self.session:
            raise ValueError(
                "Not connected to server. Call connect_to_server() first."
            )

        result = await self.session.call_tool(tool_name, tool_args)
        return result

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()


# async def test_client():
#     """Test function to demonstrate client usage"""
#     client = MCPClient()
#     try:
#         # Connect to the server
#         await client.connect_to_server()

#         # List and print all available tools
#         tools = await client.list_tools()
#         print("\n=== Available Tools ===")
#         for i, tool in enumerate(tools, 1):
#             print(f"\n{i}. {tool['name']}")
#             print(f"   Description: {tool['description']}")
#             print(f"   Input Schema: {tool['input_schema']}")

#         # Example of tool calls
#         print("\n=== Example Tool Calls ===")

#         # Call get_protocols tool
#         print("\nCalling get_protocols...")
#         protocols_result = await client.call_tool("get_protocols", {})
#         print(
#             f"Result: {protocols_result.content[:500]}..."
#         )  # Truncate for readability

#         # Call get_token_prices with a token
#         print("\nCalling get_token_prices...")
#         token_result = await client.call_tool(
#             "get_token_prices",
#             {
#                 "token": (
#                     "ethereum:0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
#                 )
#             },
#         )
#         print(
#             f"Result: {token_result.content[:500]}..."
#         )  # Truncate for readability

#     finally:
#         # Clean up resources
#         await client.cleanup()


# if __name__ == "__main__":
#     asyncio.run(test_client())
