#!/usr/bin/env python3
"""
Paper Handler
Fetches papers from arXiv, DOI links, and converts PDFs to markdown
"""

import hashlib
import json
import requests
from pathlib import Path
from typing import Dict
from datetime import datetime
import subprocess
import tempfile

from .base_handler import BaseHandler

class PaperHandler(BaseHandler):
    """
    Handler for academic papers (arXiv, DOI, PDF URLs)

    Minimal parsing: PDF → markdown conversion only
    Metadata: authors, date, DOI/arxiv_id, source_url
    No semantic extraction (abstract, keywords belong to omr-evidence)
    """

    def get_source_type(self) -> str:
        return "paper"

    def fetch(self, source: str, **kwargs) -> Dict:
        """
        Fetch paper from arXiv, DOI resolver, or direct PDF URL

        Args:
            source: arXiv ID, DOI, or PDF URL
            **kwargs: Optional flags (with_supplementary)

        Returns:
            Dict with pdf_path, metadata
        """
        # Detect source type
        if source.startswith('10.'):
            # DOI
            return self._fetch_from_doi(source, **kwargs)
        elif source.isdigit() or '.' in source and len(source.split('.')) == 2:
            # Likely arXiv ID (e.g., "2402.12345")
            return self._fetch_from_arxiv(source, **kwargs)
        elif source.endswith('.pdf'):
            # Direct PDF URL
            return self._fetch_pdf_direct(source, **kwargs)
        else:
            raise ValueError(f"Unknown paper source format: {source}")

    def _fetch_from_arxiv(self, arxiv_id: str, **kwargs) -> Dict:
        """
        Fetch paper from arXiv

        Args:
            arxiv_id: arXiv ID (e.g., "2402.12345")
            **kwargs: Optional flags

        Returns:
            Dict with pdf_path, metadata
        """
        # Construct arXiv PDF URL
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

        # Download PDF to temp file
        pdf_path = self._download_pdf(pdf_url)

        # Extract minimal metadata from arXiv API
        metadata = self._fetch_arxiv_metadata(arxiv_id)

        return {
            "pdf_path": pdf_path,
            "metadata": metadata
        }

    def _fetch_from_doi(self, doi: str, **kwargs) -> Dict:
        """
        Resolve DOI to PDF URL and fetch

        Args:
            doi: DOI string (e.g., "10.1234/paper")
            **kwargs: Optional flags

        Returns:
            Dict with pdf_path, metadata
        """
        # Use DOI resolver to find PDF URL
        # (Simplified implementation - real would use ContentNegotiation)
        doi_url = f"https://doi.org/{doi}"

        try:
            response = requests.head(doi_url, allow_redirects=True, timeout=10)
            final_url = response.url

            # Check if final URL is a PDF
            if final_url.endswith('.pdf'):
                pdf_path = self._download_pdf(final_url)
                metadata = {
                    "DOI": doi,
                    "source_url": final_url
                }
                return {
                    "pdf_path": pdf_path,
                    "metadata": metadata
                }
            else:
                # Fall back to trying to find PDF link
                # (Simplified - real implementation would parse HTML)
                raise ValueError(f"Could not resolve DOI {doi} to PDF")
        except Exception as e:
            raise RuntimeError(f"DOI resolution failed: {str(e)}")

    def _fetch_pdf_direct(self, pdf_url: str, **kwargs) -> Dict:
        """
        Fetch PDF from direct URL

        Args:
            pdf_url: Direct PDF URL
            **kwargs: Optional flags

        Returns:
            Dict with pdf_path, metadata
        """
        pdf_path = self._download_pdf(pdf_url)

        metadata = {
            "source_url": pdf_url
        }

        return {
            "pdf_path": pdf_path,
            "metadata": metadata
        }

    def _download_pdf(self, pdf_url: str) -> Path:
        """
        Download PDF from URL to temporary file

        Args:
            pdf_url: URL to PDF file

        Returns:
            Path to downloaded PDF
        """
        temp_dir = Path(tempfile.mkdtemp())
        pdf_path = temp_dir / "paper.pdf"

        try:
            response = requests.get(pdf_url, timeout=30, stream=True)
            response.raise_for_status()

            with open(pdf_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            return pdf_path

        except Exception as e:
            raise RuntimeError(f"PDF download failed: {str(e)}")

    def _fetch_arxiv_metadata(self, arxiv_id: str) -> Dict:
        """
        Fetch minimal metadata from arXiv API

        Args:
            arxiv_id: arXiv ID

        Returns:
            Metadata dict (authors, date, arxiv_id)
        """
        # Use arXiv API to fetch metadata
        api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"

        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()

            # Parse XML response (simplified)
            # Real implementation would use xml.etree.ElementTree
            # For now, return basic metadata
            return {
                "arxiv_id": arxiv_id,
                "source_url": f"https://arxiv.org/abs/{arxiv_id}"
            }

        except Exception as e:
            # Fallback: minimal metadata
            return {
                "arxiv_id": arxiv_id,
                "source_url": f"https://arxiv.org/abs/{arxiv_id}"
            }

    def convert(self, fetched_data: Dict) -> str:
        """
        Convert PDF to markdown using marker or pdfplumber

        Args:
            fetched_data: Data from fetch() (contains pdf_path)

        Returns:
            Markdown content
        """
        pdf_path = fetched_data['pdf_path']
        metadata = fetched_data.get('metadata', {})

        # Try marker first (better quality)
        try:
            markdown_content = self._convert_with_marker(pdf_path)
        except Exception:
            # Fallback to pdfplumber
            try:
                markdown_content = self._convert_with_pdfplumber(pdf_path)
            except Exception as e:
                # Last fallback: simple text extraction
                markdown_content = self._extract_text_simple(pdf_path)

        # Add metadata header
        header = self._create_markdown_header(metadata)
        full_markdown = header + "\n\n" + markdown_content

        return full_markdown

    def _convert_with_marker(self, pdf_path: Path) -> str:
        """
        Convert PDF to markdown using marker tool

        Args:
            pdf_path: Path to PDF file

        Returns:
            Markdown string
        """
        # Check if marker is available
        try:
            result = subprocess.run(
                ['marker_single', str(pdf_path), '--output_format', 'markdown'],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                return result.stdout
            else:
                raise RuntimeError(f"marker failed: {result.stderr}")

        except FileNotFoundError:
            # marker not installed
            raise RuntimeError("marker tool not available")

    def _convert_with_pdfplumber(self, pdf_path: Path) -> str:
        """
        Convert PDF to markdown using pdfplumber

        Args:
            pdf_path: Path to PDF file

        Returns:
            Markdown string (simplified)
        """
        try:
            import pdfplumber

            markdown_lines = []

            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        markdown_lines.append(text)
                        markdown_lines.append("\n---\n")  # Page separator

            return "\n".join(markdown_lines)

        except ImportError:
            raise RuntimeError("pdfplumber not available")

    def _extract_text_simple(self, pdf_path: Path) -> str:
        """
        Simple text extraction fallback

        Args:
            pdf_path: Path to PDF file

        Returns:
            Raw text (not proper markdown)
        """
        try:
            import PyPDF2

            text_lines = []

            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        text_lines.append(text)

            return "\n\n".join(text_lines)

        except ImportError:
            # Ultimate fallback: return placeholder
            return "PDF content extraction failed. PDF available but markdown conversion not possible."

    def _create_markdown_header(self, metadata: Dict) -> str:
        """
        Create markdown header with metadata

        Args:
            metadata: Paper metadata

        Returns:
            Header markdown string
        """
        lines = ["# Paper", ""]

        if 'title' in metadata:
            lines.append(f"**Title**: {metadata['title']}")
            lines.append("")

        if 'authors' in metadata:
            authors_str = ", ".join(metadata['authors'])
            lines.append(f"**Authors**: {authors_str}")
            lines.append("")

        if 'date' in metadata:
            lines.append(f"**Date**: {metadata['date']}")
            lines.append("")

        if 'DOI' in metadata:
            lines.append(f"**DOI**: {metadata['DOI']}")
            lines.append("")

        if 'arxiv_id' in metadata:
            lines.append(f"**arXiv**: {metadata['arxiv_id']}")
            lines.append("")

        if 'source_url' in metadata:
            lines.append(f"**Source**: {metadata['source_url']}")
            lines.append("")

        lines.append("---")
        lines.append("")
        lines.append("## Content")
        lines.append("")

        return "\n".join(lines)

    def get_output_path(self, source: str) -> Path:
        """
        Generate deterministic output path for paper

        DOI → doi-10-1234-abc.md
        arXiv ID → arxiv-2402-12345.md

        Args:
            source: DOI, arXiv ID, or URL

        Returns:
            Path to markdown file in raw/paper/
        """
        paper_dir = self.raw_dir / "paper"
        paper_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename based on source type
        if source.startswith('10.'):
            # DOI: replace slashes and dots
            doi_slug = source.replace('/', '-').replace('.', '-')
            filename = f"doi-{doi_slug}.md"
        elif source.isdigit() or '.' in source:
            # arXiv ID
            arxiv_slug = source.replace('.', '-')
            filename = f"arxiv-{arxiv_slug}.md"
        else:
            # URL: use hash
            source_hash = hashlib.md5(source.encode()).hexdigest()[:8]
            filename = f"url-{source_hash}.md"

        return paper_dir / filename

def main():
    """Test paper handler"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: paper_handler.py <workspace> <arxiv_id>")
        print("Example: paper_handler.py /tmp/test-project 2402.12345")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    arxiv_id = sys.argv[2]

    handler = PaperHandler(workspace)

    try:
        print(f"Fetching paper {arxiv_id}...")
        fetched = handler.fetch(arxiv_id)

        print(f"Converting to markdown...")
        markdown = handler.convert(fetched)

        print(f"Storing...")
        result = handler.store(
            source=arxiv_id,
            markdown_content=markdown,
            metadata=fetched.get('metadata', {})
        )

        print(f"✓ Paper collected")
        print(f"  File: {result['file_path']}")
        print(f"  ID: {result['artifact_id']}")

    except Exception as e:
        print(f"✗ Error: {str(e)}")

if __name__ == "__main__":
    main()