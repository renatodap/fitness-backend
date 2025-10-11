"""
Garmy MCP Server - Model Context Protocol for Claude Integration

This module starts the garmy MCP server which allows Claude AI
to query health data using natural language.

Example queries Claude can handle:
- "What was my sleep quality last week?"
- "How's my HRV trending?"
- "Am I ready for a hard workout today?"
- "Show me my stress levels this month"

The MCP server automatically fetches data from the garmy local database
and formats it for Claude to understand.
"""

import logging
import asyncio
from pathlib import Path

try:
    from garmy.mcp import MCPServer
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False

logger = logging.getLogger(__name__)


class GarmyMCPService:
    """Service to manage garmy MCP server for Claude integration."""

    def __init__(self, port: int = 8001, db_path: str = "./data/garmy.db"):
        """
        Initialize MCP server.

        Args:
            port: Port to run MCP server on (default: 8001)
            db_path: Path to garmy SQLite database
        """
        if not MCP_AVAILABLE:
            logger.warning("[Garmy MCP] garmy MCP server not available")
            self.server = None
            return

        self.port = port
        self.db_path = db_path
        self.server = None

        # Ensure database directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    async def start(self):
        """Start the MCP server."""
        if not MCP_AVAILABLE:
            logger.error("[Garmy MCP] Cannot start - garmy MCP not installed")
            return

        try:
            logger.info(f"[Garmy MCP] Starting MCP server on port {self.port}")

            self.server = MCPServer(
                port=self.port,
                db_path=self.db_path
            )

            await self.server.start()

            logger.info(
                f"[Garmy MCP] MCP server running at http://localhost:{self.port}\n"
                f"Claude can now query health data!"
            )

        except Exception as e:
            logger.error(f"[Garmy MCP] Failed to start server: {e}")
            raise

    async def stop(self):
        """Stop the MCP server."""
        if self.server:
            try:
                await self.server.stop()
                logger.info("[Garmy MCP] MCP server stopped")
            except Exception as e:
                logger.error(f"[Garmy MCP] Error stopping server: {e}")

    async def query(self, user_id: str, natural_language_query: str) -> dict:
        """
        Query health data using natural language.

        Args:
            user_id: User ID to query data for
            natural_language_query: Question in natural language

        Returns:
            Dict with query results

        Example:
            result = await mcp.query(
                user_id="abc123",
                natural_language_query="What was my average sleep last week?"
            )
            # Returns: {"sleep_hours": 7.5, "sleep_score": 82, ...}
        """
        if not self.server:
            raise Exception("MCP server not started")

        try:
            result = await self.server.query(
                user_id=user_id,
                query=natural_language_query
            )

            return result

        except Exception as e:
            logger.error(f"[Garmy MCP] Query failed: {e}")
            return {"error": str(e)}


# Global MCP server instance
_mcp_server: GarmyMCPService | None = None


async def start_mcp_server(port: int = 8001, db_path: str = "./data/garmy.db"):
    """
    Start global MCP server.

    This should be called once during app startup.
    """
    global _mcp_server

    if _mcp_server is None:
        _mcp_server = GarmyMCPService(port=port, db_path=db_path)
        await _mcp_server.start()


async def stop_mcp_server():
    """Stop global MCP server."""
    global _mcp_server

    if _mcp_server:
        await _mcp_server.stop()
        _mcp_server = None


def get_mcp_server() -> GarmyMCPService:
    """Get the global MCP server instance."""
    if _mcp_server is None:
        raise Exception("MCP server not started. Call start_mcp_server() first.")

    return _mcp_server


# CLI for running MCP server standalone
if __name__ == "__main__":
    import sys

    async def main():
        """Run MCP server standalone."""
        port = int(sys.argv[1]) if len(sys.argv) > 1 else 8001

        print(f"Starting Garmy MCP Server on port {port}...")
        print("Claude can now query health data!")
        print("\nExample queries:")
        print("  - What was my sleep quality last week?")
        print("  - How's my HRV trending?")
        print("  - Am I ready for a hard workout today?")
        print("\nPress Ctrl+C to stop\n")

        server = GarmyMCPService(port=port)
        await server.start()

        # Keep running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping MCP server...")
            await server.stop()

    asyncio.run(main())
