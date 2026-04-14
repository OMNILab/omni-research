#!/usr/bin/env python3
"""
MCP Client Utility for Chrome Automation
Provides Chrome MCP server integration for webpage capture and search automation
"""

import asyncio
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class ChromeMCPClient:
    """
    Manages Chrome MCP server connection via stdio transport

    Features:
    - Server detection (npm package check)
    - Webpage capture (screenshot PNG + markdown)
    - Search automation (Google Scholar)
    - Async wrappers for sync API compatibility
    """

    def __init__(self):
        """Initialize MCP client"""
        self.available = False
        self.server_package = "@anthropic/chrome-mcp-server"

    def detect_server(self) -> bool:
        """
        Check if Chrome MCP server is available

        Returns:
            True if npm package installed, False otherwise
        """
        try:
            # Check if npm package installed globally
            result = subprocess.run(
                ["npm", "list", "-g", self.server_package],
                capture_output=True,
                text=True,
                timeout=5
            )

            # If package found, returncode is 0
            self.available = result.returncode == 0

            if self.available:
                return True

            # Also try local installation
            result = subprocess.run(
                ["npm", "list", self.server_package],
                capture_output=True,
                text=True,
                timeout=5
            )

            self.available = result.returncode == 0
            return self.available

        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            # npm not installed or other error
            self.available = False
            return False

    async def capture_webpage_async(self, url: str) -> Dict[str, Any]:
        """
        Capture webpage with screenshot + markdown via MCP (async)

        Args:
            url: Web URL to capture

        Returns:
            Dict with screenshot_png (bytes), markdown (str), metadata

        Raises:
            ImportError: MCP SDK not installed
            RuntimeError: MCP server not available or tool execution failed
        """
        # Import MCP SDK (will raise ImportError if not installed)
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        # Configure server parameters for stdio transport
        server_params = StdioServerParameters(
            command="npx",
            args=["-y", self.server_package],
            env=None
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize session
                await session.initialize()

                # Navigate to URL
                await session.call_tool("navigate", {"url": url})

                # Wait for page load
                await asyncio.sleep(2)

                # Try to capture screenshot (graceful fallback)
                screenshot_png = None
                try:
                    screenshot_result = await session.call_tool("screenshot", {})
                    # Extract image data from result
                    if screenshot_result.content:
                        # Handle different content formats
                        for content_block in screenshot_result.content:
                            if hasattr(content_block, 'data'):
                                # Binary data format
                                screenshot_png = content_block.data
                                break
                            elif isinstance(content_block, dict) and 'data' in content_block:
                                screenshot_png = content_block['data']
                                break
                except Exception as e:
                    # Screenshot failed, continue with markdown only
                    pass

                # Read page content as markdown
                content_result = await session.call_tool("read_page", {"format": "markdown"})
                markdown = ""

                if content_result.content:
                    for content_block in content_result.content:
                        if hasattr(content_block, 'text'):
                            markdown = content_block.text
                            break
                        elif isinstance(content_block, dict) and 'text' in content_block:
                            markdown = content_block['text']
                            break

                return {
                    "screenshot_png": screenshot_png,
                    "markdown": markdown,
                    "metadata": {
                        "captured_at": datetime.now().isoformat(),
                        "screenshot_available": screenshot_png is not None
                    }
                }

    async def search_google_scholar_async(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search Google Scholar via Chrome MCP automation (async)

        Args:
            query: Search query
            max_results: Maximum results to extract

        Returns:
            List of paper results with title, url, citations, authors, year

        Note:
            This is a placeholder implementation. Real implementation would
            use Chrome MCP tools to navigate, type, click, and extract results.
            Currently returns empty list to trigger fallback to arxiv SDK.
        """
        # TODO: Implement full Google Scholar search automation
        # Requires Chrome MCP tools for:
        # - navigate(url)
        # - type(selector, text)
        # - click(selector)
        # - extract_results(selector, max_results)

        # For now, return empty list to use arxiv SDK fallback
        return []

    def capture_webpage(self, url: str) -> Dict[str, Any]:
        """
        Sync wrapper for capture_webpage_async

        Args:
            url: Web URL

        Returns:
            Dict with screenshot_png, markdown, metadata
        """
        return asyncio.run(self.capture_webpage_async(url))

    def search_google_scholar(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Sync wrapper for search_google_scholar_async

        Args:
            query: Search query
            max_results: Max results

        Returns:
            List of search results
        """
        return asyncio.run(self.search_google_scholar_async(query, max_results))


def check_mcp_sdk_available() -> bool:
    """
    Check if MCP Python SDK is installed

    Returns:
        True if mcp package available
    """
    try:
        import mcp
        return True
    except ImportError:
        return False


def check_chrome_mcp_server_available() -> bool:
    """
    Check if Chrome MCP server npm package is installed

    Returns:
        True if server available
    """
    client = ChromeMCPClient()
    return client.detect_server()


def main():
    """Test MCP client"""
    import sys

    print("Chrome MCP Client Test")
    print("=" * 60)

    # Check SDK
    sdk_available = check_mcp_sdk_available()
    print(f"MCP Python SDK: {'✓ Installed' if sdk_available else '✗ Not installed'}")

    # Check server
    server_available = check_chrome_mcp_server_available()
    print(f"Chrome MCP Server: {'✓ Installed' if server_available else '✗ Not installed'}")

    if not sdk_available:
        print("\nTo install MCP SDK:")
        print("  pip install mcp")

    if not server_available:
        print("\nTo install Chrome MCP server:")
        print("  npm install -g @anthropic/chrome-mcp-server")
        print("  # Or use npx (no install): npx -y @anthropic/chrome-mcp-server")

    if sdk_available and server_available:
        print("\n✓ All dependencies available")
        print("Ready to capture webpages and perform search automation")

    # Test capture if both available
    if len(sys.argv) > 1 and sdk_available and server_available:
        url = sys.argv[1]
        print(f"\nCapturing: {url}")

        client = ChromeMCPClient()
        try:
            result = client.capture_webpage(url)

            print(f"\n✓ Capture successful")
            print(f"  Screenshot: {'Available' if result['screenshot_png'] else 'Not available'}")
            print(f"  Markdown: {len(result['markdown'])} characters")

            # Save to temp file for testing
            if result['screenshot_png']:
                test_dir = Path("/tmp/mcp-test")
                test_dir.mkdir(exist_ok=True)

                screenshot_path = test_dir / "screenshot.png"
                screenshot_path.write_bytes(result['screenshot_png'])
                print(f"  Saved screenshot: {screenshot_path}")

                markdown_path = test_dir / "content.md"
                markdown_path.write_text(result['markdown'])
                print(f"  Saved markdown: {markdown_path}")

        except Exception as e:
            print(f"\n✗ Capture failed: {str(e)}")


if __name__ == "__main__":
    main()