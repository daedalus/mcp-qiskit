"""Entry point for running the MCP server."""

from mcp_qiskit._mcp import mcp


def main() -> int:
    """Run the MCP server."""
    mcp.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
