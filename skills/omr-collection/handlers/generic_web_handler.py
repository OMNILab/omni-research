#!/usr/bin/env python3
"""
Generic Web Handler
Fetches web content using Chrome MCP or simple HTTP fetcher
"""

import hashlib
import requests
from pathlib import Path
from typing import Dict
from datetime import datetime
from html.parser import HTMLParser
import html2text

from .base_handler import BaseHandler

class GenericWebHandler(BaseHandler):
    """
    Handler for generic web URLs

    Primary: Chrome MCP → snapshot (PNG) + markdown
    Fallback: Simple HTTP fetcher → HTML → markdown

    Minimal parsing: HTML → markdown conversion only
    Metadata: captured_at, snapshot_path, markdown_length
    """

    def get_source_type(self) -> str:
        return "web"

    def fetch(self, source: str, **kwargs) -> Dict:
        """
        Fetch web page content

        Args:
            source: URL (HTTP/HTTPS)
            **kwargs: Optional parameters

        Returns:
            Dict with html_content, snapshot_path (if available), metadata
        """
        # Try Chrome MCP first (if available)
        try:
            return self._fetch_with_chrome_mcp(source, **kwargs)
        except Exception:
            # Fallback to simple HTTP fetcher
            return self._fetch_with_http(source, **kwargs)

    def _fetch_with_chrome_mcp(self, url: str, **kwargs) -> Dict:
        """
        Fetch using Chrome MCP (if available)

        Args:
            url: Web URL
            **kwargs: Optional parameters

        Returns:
            Dict with snapshot_path, html_content, metadata
        """
        # Chrome MCP integration (placeholder - real would use MCP client)
        # This is a placeholder for Chrome MCP integration
        # In real implementation, would call MCP server for snapshot + markdown

        raise RuntimeError("Chrome MCP not available (placeholder implementation)")

    def _fetch_with_http(self, url: str, **kwargs) -> Dict:
        """
        Fallback: Fetch using simple HTTP requests

        Args:
            url: Web URL
            **kwargs: Optional parameters

        Returns:
            Dict with html_content, metadata
        """
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            html_content = response.text

            metadata = {
                "captured_at": datetime.now().isoformat(),
                "source_url": url,
                "status_code": response.status_code,
                "content_type": response.headers.get('Content-Type', 'unknown')
            }

            return {
                "html_content": html_content,
                "snapshot_path": None,  # No snapshot in fallback mode
                "metadata": metadata
            }

        except Exception as e:
            raise RuntimeError(f"HTTP fetch failed: {str(e)}")

    def convert(self, fetched_data: Dict) -> str:
        """
        Convert HTML to markdown

        Args:
            fetched_data: Data from fetch()

        Returns:
            Markdown content
        """
        html_content = fetched_data['html_content']
        metadata = fetched_data.get('metadata', {})
        snapshot_path = fetched_data.get('snapshot_path')

        # Convert HTML to markdown
        try:
            markdown_content = self._html_to_markdown(html_content)
        except Exception:
            # Fallback: simple text extraction
            markdown_content = self._extract_text_simple(html_content)

        # Create header with metadata
        header = self._create_metadata_header(metadata, snapshot_path)

        # Combine header + markdown
        full_markdown = header + "\n\n" + markdown_content

        return full_markdown

    def _html_to_markdown(self, html_content: str) -> str:
        """
        Convert HTML to markdown using html2text

        Args:
            html_content: HTML string

        Returns:
            Markdown string
        """
        try:
            h = html2text.HTML2Text()
            h.ignore_links = False
            h.ignore_images = False
            h.body_width = 0  # No line wrapping

            markdown = h.handle(html_content)
            return markdown

        except ImportError:
            raise RuntimeError("html2text not available. Install: pip install html2text")

    def _extract_text_simple(self, html_content: str) -> str:
        """
        Simple text extraction from HTML (fallback)

        Args:
            html_content: HTML string

        Returns:
            Plain text (not proper markdown)
        """
        # Very simple: strip HTML tags
        # (Real implementation would be more sophisticated)
        import re

        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html_content)

        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def _create_metadata_header(self, metadata: Dict, snapshot_path: str) -> str:
        """
        Create metadata header for web content markdown

        Args:
            metadata: Web page metadata
            snapshot_path: Path to PNG snapshot (if available)

        Returns:
            Header markdown string
        """
        lines = [
            "# Web Content",
            "",
            f"**URL**: {metadata.get('source_url', '')}",
            "",
            f"**Captured At**: {metadata.get('captured_at', '')}",
            "",
            f"**Status Code**: {metadata.get('status_code', 'unknown')}",
            "",
            f"**Content Type**: {metadata.get('content_type', 'unknown')}",
            ""
        ]

        if snapshot_path:
            lines.append(f"**Snapshot**: {snapshot_path}")
            lines.append("")

        lines.append("---")
        lines.append("")
        lines.append("## Content")
        lines.append("")

        return "\n".join(lines)

    def get_output_path(self, source: str) -> Path:
        """
        Generate output path for web content

        URL → url-hash.md

        Args:
            source: URL

        Returns:
            Path to markdown file in raw/web/
        """
        web_dir = self.raw_dir / "web"
        web_dir.mkdir(parents=True, exist_ok=True)

        # Generate hash-based filename
        url_hash = hashlib.md5(source.encode()).hexdigest()[:8]
        filename = f"url-{url_hash}.md"

        return web_dir / filename

    def get_snapshot_path(self, source: str) -> Path:
        """
        Generate path for PNG snapshot

        Args:
            source: URL

        Returns:
            Path to PNG snapshot file in raw/web/
        """
        web_dir = self.raw_dir / "web"
        web_dir.mkdir(parents=True, exist_ok=True)

        # Generate hash-based filename
        url_hash = hashlib.md5(source.encode()).hexdigest()[:8]
        filename = f"url-{url_hash}-snapshot.png"

        return web_dir / filename

def main():
    """Test generic web handler"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: generic_web_handler.py <workspace> <url>")
        print("Example: generic_web_handler.py /tmp/test-project https://example.com/blog")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    url = sys.argv[2]

    handler = GenericWebHandler(workspace)

    try:
        print(f"Fetching web content from {url}...")
        fetched = handler.fetch(url)

        print(f"Converting to markdown...")
        markdown = handler.convert(fetched)

        print(f"Storing...")
        result = handler.store(
            source=url,
            markdown_content=markdown,
            metadata=fetched.get('metadata', {})
        )

        print(f"✓ Web content collected")
        print(f"  File: {result['file_path']}")
        print(f"  ID: {result['artifact_id']}")

    except Exception as e:
        print(f"✗ Error: {str(e)}")

if __name__ == "__main__":
    main()