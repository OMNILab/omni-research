#!/usr/bin/env python3
"""
Base Handler Class
Abstract base class for all collection handlers
"""

import hashlib
import json
from pathlib import Path
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Dict, Optional

class BaseHandler(ABC):
    """
    Abstract base class for collection handlers

    Each handler implements:
    - detect(): Check if input matches this handler
    - fetch(): Retrieve materials from source
    - convert(): Transform to markdown format
    - store(): Save to workspace with metadata
    """

    def __init__(self, workspace_root: Path):
        """
        Initialize handler with workspace root

        Args:
            workspace_root: Path to research project root
        """
        self.workspace_root = workspace_root
        self.raw_dir = workspace_root / "raw"
        self.index_dir = workspace_root / "docs" / "index"

    @abstractmethod
    def fetch(self, source: str, **kwargs) -> Dict:
        """
        Fetch materials from source

        Args:
            source: Source identifier (URL, DOI, ID, etc.)
            **kwargs: Additional parameters (override flags, etc.)

        Returns:
            Dict with fetched content and metadata
        """
        pass

    @abstractmethod
    def convert(self, fetched_data: Dict) -> str:
        """
        Convert fetched data to markdown format

        Args:
            fetched_data: Data from fetch()

        Returns:
            Markdown content string
        """
        pass

    @abstractmethod
    def get_output_path(self, source: str) -> Path:
        """
        Generate deterministic output path for source

        Args:
            source: Source identifier

        Returns:
            Path for markdown artifact
        """
        pass

    @abstractmethod
    def get_source_type(self) -> str:
        """
        Get source type identifier

        Returns:
            Source type string (paper/web/github/dataset)
        """
        pass

    def store(self,
              source: str,
              markdown_content: str,
              metadata: Dict,
              **kwargs) -> Dict:
        """
        Store markdown artifact and update index

        Args:
            source: Original source identifier
            markdown_content: Markdown content to save
            metadata: Source-specific metadata
            **kwargs: Additional parameters

        Returns:
            Dict with file_path, metadata, status
        """
        # Generate deterministic output path
        output_path = self.get_output_path(source)

        # Ensure directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write markdown content
        output_path.write_text(markdown_content)

        # Generate unique ID
        artifact_id = self._generate_id(source)

        # Build core metadata
        core_metadata = {
            "id": artifact_id,
            "title": metadata.get('title', self._extract_title(markdown_content)),
            "url": source,
            "source_type": self.get_source_type(),
            "collected_at": datetime.now().isoformat(),
            "collected_by": "omr-collection",
            "file_path": str(output_path.relative_to(self.workspace_root))
        }

        # Merge with source-specific metadata
        full_metadata = {**core_metadata, **metadata}

        # Update index
        self._update_index(full_metadata)

        return {
            "status": "success",
            "file_path": str(output_path),
            "metadata": full_metadata,
            "artifact_id": artifact_id
        }

    def _generate_id(self, source: str) -> str:
        """
        Generate unique ID for artifact

        Args:
            source: Source identifier

        Returns:
            Unique ID based on source type
        """
        # Use hash-based ID for determinism
        source_hash = hashlib.md5(source.encode()).hexdigest()[:8]
        return f"{self.get_source_type()}-{source_hash}"

    def _extract_title(self, markdown_content: str) -> str:
        """
        Extract title from markdown content

        Args:
            markdown_content: Markdown text

        Returns:
            Title string (first heading or 'Unknown Title')
        """
        lines = markdown_content.split('\n')
        for line in lines[:20]:  # Check first 20 lines
            if line.startswith('#'):
                return line.lstrip('#').strip()

        return "Unknown Title"

    def _update_index(self, metadata: Dict):
        """
        Update source-specific index file

        Args:
            metadata: Artifact metadata to add
        """
        source_type = self.get_source_type()
        index_file = self._get_index_file(source_type)

        # Load existing index or create new
        if index_file.exists():
            index_data = json.loads(index_file.read_text())
        else:
            index_data = {
                "artifacts": [],
                "last_updated": datetime.now().isoformat()
            }

        # Append new artifact
        index_data['artifacts'].append(metadata)
        index_data['last_updated'] = datetime.now().isoformat()

        # Write updated index
        index_file.write_text(json.dumps(index_data, indent=2))

    def _get_index_file(self, source_type: str) -> Path:
        """
        Get index file path for source type

        Args:
            source_type: Source type (paper/web/github/dataset)

        Returns:
            Path to index JSON file
        """
        index_map = {
            'paper': 'papers-index.json',
            'web': 'blogs-index.json',
            'github': 'repos-index.json',
            'dataset': 'datasets-index.json',
            'failed': 'failed-index.json'
        }

        index_name = index_map.get(source_type, 'unknown-index.json')
        return self.index_dir / index_name

    def create_error_artifact(self,
                               source: str,
                               error_type: str,
                               error_message: str,
                               retry_attempts: int,
                               fallback_attempted: bool) -> Dict:
        """
        Create error artifact for failed collection

        Args:
            source: Original source
            error_type: Error classification
            error_message: Detailed error message
            retry_attempts: Number of retries attempted
            fallback_attempted: Whether fallback was tried

        Returns:
            Dict with error artifact path and metadata
        """
        # Generate error artifact path
        source_hash = hashlib.md5(source.encode()).hexdigest()[:8]
        error_path = self.raw_dir / "failed" / f"url-{source_hash}-error.md"
        error_path.parent.mkdir(parents=True, exist_ok=True)

        # Create error markdown
        error_content = f"""# Collection Failure

**URL**: {source}
**Source Type**: {self.get_source_type()}
**Status**: failed
**Error**: {error_type}: {error_message}
**Retry Attempts**: {retry_attempts}
**Fallback Attempted**: {fallback_attempted}
**Collected At**: {datetime.now().isoformat()}
"""

        error_path.write_text(error_content)

        # Create error metadata
        error_metadata = {
            "id": f"failed-{source_hash}",
            "url": source,
            "source_type": "failed",
            "error_type": error_type,
            "error_message": error_message,
            "retry_attempts": retry_attempts,
            "fallback_attempted": fallback_attempted,
            "collected_at": datetime.now().isoformat(),
            "collected_by": "omr-collection",
            "file_path": str(error_path.relative_to(self.workspace_root))
        }

        # Update failed index
        self._update_error_index(error_metadata)

        return {
            "status": "failed",
            "file_path": str(error_path),
            "metadata": error_metadata
        }

    def _update_error_index(self, error_metadata: Dict):
        """
        Update failed artifacts index

        Args:
            error_metadata: Error artifact metadata
        """
        failed_index = self.index_dir / "failed-index.json"

        # Load existing index or create new
        if failed_index.exists():
            index_data = json.loads(failed_index.read_text())
        else:
            index_data = {
                "artifacts": [],
                "last_updated": datetime.now().isoformat()
            }

        # Append error artifact
        index_data['artifacts'].append(error_metadata)
        index_data['last_updated'] = datetime.now().isoformat()

        # Write updated index
        failed_index.write_text(json.dumps(index_data, indent=2))