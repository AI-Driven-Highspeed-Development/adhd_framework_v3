"""
Refresh script for dream_mcp.

Registers this MCP server in .vscode/mcp.json.
Run via: adhd r -f -m dream_mcp
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from logger_util import Logger


def main() -> None:
    """Register this MCP in .vscode/mcp.json."""
    logger = Logger(name="dream_mcpRefresh")
    logger.info("Starting dream_mcp refresh...")

    try:
        mcp_json_path = Path.cwd() / ".vscode" / "mcp.json"

        # Ensure .vscode directory exists
        mcp_json_path.parent.mkdir(parents=True, exist_ok=True)

        # Load existing mcp.json or create new structure
        if mcp_json_path.exists():
            with open(mcp_json_path, "r", encoding="utf-8") as f:
                mcp_config = json.load(f)
        else:
            mcp_config = {"servers": {}}

        # Ensure servers key exists
        if "servers" not in mcp_config:
            mcp_config["servers"] = {}

        # MCP server configuration
        mcp_key = "dream_mcp"
        module_path = "dream_mcp.dream_mcp"

        # Only add if not already present
        if mcp_key not in mcp_config["servers"]:
            mcp_config["servers"][mcp_key] = {
                "type": "stdio",
                "command": "uv",
                "args": ["run", "python", "-m", module_path],
                "cwd": "./"
            }

            # Write back with proper formatting
            with open(mcp_json_path, "w", encoding="utf-8") as f:
                json.dump(mcp_config, f, indent=2)

            logger.info(f"Added '{mcp_key}' to {mcp_json_path}")
        else:
            logger.info(f"'{mcp_key}' already exists in {mcp_json_path}, skipping")

        logger.info("dream_mcp refresh completed successfully.")
    except Exception as e:
        logger.error(f"dream_mcp refresh failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
