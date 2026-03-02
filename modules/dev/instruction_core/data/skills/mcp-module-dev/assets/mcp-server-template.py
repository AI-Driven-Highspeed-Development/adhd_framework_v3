"""MCP Server implementation pattern for ADHD modules.

Canonical template — adapt names, tools, and controller imports to your module.
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP
from my_module.my_controller import MyController

mcp = FastMCP(name="my-module", instructions="Description of this MCP server")
_controller: MyController | None = None


def _get_controller() -> MyController:
    global _controller
    if _controller is None:
        _controller = MyController()
    return _controller


@mcp.tool()
def my_tool(arg: str) -> dict:
    """Tool description becomes MCP schema description.

    Args:
        arg: Description of this argument
    """
    return _get_controller().my_operation(arg)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
