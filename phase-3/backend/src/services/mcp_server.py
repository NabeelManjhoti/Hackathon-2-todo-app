"""MCP server initialization for AI chatbot tools."""

from typing import Any, Dict

# MCP server will be initialized here
# This is a placeholder for the embedded MCP server configuration
# Tools will be registered in mcp_tools.py

class MCPServer:
    """Embedded MCP server for managing chatbot tools."""

    def __init__(self):
        """Initialize MCP server."""
        self.tools: Dict[str, Any] = {}

    def register_tool(self, name: str, tool: Any) -> None:
        """Register a tool with the MCP server.

        Args:
            name: Tool name
            tool: Tool function or callable
        """
        self.tools[name] = tool

    def get_tool(self, name: str) -> Any:
        """Get a registered tool by name.

        Args:
            name: Tool name

        Returns:
            Tool function or None if not found
        """
        return self.tools.get(name)

    def list_tools(self) -> list[str]:
        """List all registered tool names.

        Returns:
            List of tool names
        """
        return list(self.tools.keys())


# Global MCP server instance
mcp_server = MCPServer()
