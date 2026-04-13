#!/usr/bin/env python3
"""
HuggingFace Handler
Fetches README and model/dataset cards from HuggingFace Hub
"""

import hashlib
import json
import requests
from pathlib import Path
from typing import Dict
from datetime import datetime

from .base_handler import BaseHandler

class HuggingFaceHandler(BaseHandler):
    """
    Handler for HuggingFace datasets and models

    Default: README + card (no download)
    Override: --download-dataset or --download-model flags

    Minimal parsing: README markdown + card metadata
    Metadata: downloads, likes, tags, task_type
    """

    def get_source_type(self) -> str:
        return "dataset"

    def fetch(self, source: str, **kwargs) -> Dict:
        """
        Fetch README and card info from HuggingFace Hub

        Args:
            source: HF resource (e.g., "datasets/user/data" or "models/user/model")
            **kwargs: Optional flags (download_dataset=False, download_model=False)

        Returns:
            Dict with readme_content, card_info, metadata
        """
        # Extract resource type and name
        resource_type, resource_name = self._parse_source(source)

        # Fetch README
        readme_content = self._fetch_readme(resource_type, resource_name)

        # Fetch card metadata
        card_info = self._fetch_card_info(resource_type, resource_name)

        # Check for download flags
        if kwargs.get('download_dataset', False) and resource_type == 'datasets':
            dataset_path = self._download_dataset(resource_name)
            card_info['dataset_path'] = str(dataset_path)

        if kwargs.get('download_model', False) and resource_type == 'models':
            model_path = self._download_model(resource_name)
            card_info['model_path'] = str(model_path)

        return {
            "readme_content": readme_content,
            "card_info": card_info,
            "metadata": card_info,
            "resource_type": resource_type,
            "resource_name": resource_name
        }

    def _parse_source(self, source: str) -> tuple[str, str]:
        """
        Parse source to extract type and name

        Args:
            source: Input string (e.g., "datasets/user/data", "huggingface.co/datasets/user/data")

        Returns:
            (resource_type, resource_name) tuple
        """
        # Handle full URL
        if 'huggingface.co' in source:
            parts = source.split('huggingface.co/')[-1].split('/')
            if len(parts) >= 3:
                return parts[0], f"{parts[1]}/{parts[2]}"

        # Handle "datasets/user/data" or "models/user/model" format
        if source.startswith('datasets/') or source.startswith('models/'):
            parts = source.split('/')
            if len(parts) >= 3:
                return parts[0], f"{parts[1]}/{parts[2]}"

        # Handle bare "user/data" (assume dataset)
        if '/' in source:
            return 'datasets', source

        raise ValueError(f"Invalid HuggingFace source: {source}")

    def _fetch_readme(self, resource_type: str, resource_name: str) -> str:
        """
        Fetch README.md from HuggingFace Hub

        Args:
            resource_type: 'datasets' or 'models'
            resource_name: "user/name"

        Returns:
            README markdown content
        """
        # Use HF API to fetch README
        if resource_type == 'datasets':
            readme_url = f"https://huggingface.co/datasets/{resource_name}/raw/main/README.md"
        else:
            readme_url = f"https://huggingface.co/{resource_name}/raw/main/README.md"

        try:
            response = requests.get(readme_url, timeout=10)
            response.raise_for_status()
            return response.text

        except Exception:
            # Fallback: placeholder README
            return f"# {resource_name}\n\nREADME could not be fetched.\n\nSee: https://huggingface.co/{resource_type}/{resource_name}"

    def _fetch_card_info(self, resource_type: str, resource_name: str) -> Dict:
        """
        Fetch card metadata from HuggingFace API

        Args:
            resource_type: 'datasets' or 'models'
            resource_name: "user/name"

        Returns:
            Card metadata dict
        """
        # Use HF Hub API (simplified - real would use huggingface_hub library)
        if resource_type == 'datasets':
            api_url = f"https://huggingface.co/api/datasets/{resource_name}"
        else:
            api_url = f"https://huggingface.co/api/models/{resource_name}"

        try:
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()

            card_data = response.json()

            return {
                "downloads": card_data.get('downloads', 0),
                "likes": card_data.get('likes', 0),
                "tags": card_data.get('tags', []),
                "task_type": card_data.get('task_categories', ['unknown']),
                "card_url": f"https://huggingface.co/{resource_type}/{resource_name}",
                "resource_type": resource_type
            }

        except Exception:
            # Fallback metadata
            return {
                "downloads": 0,
                "likes": 0,
                "tags": [],
                "task_type": "unknown",
                "card_url": f"https://huggingface.co/{resource_type}/{resource_name}",
                "resource_type": resource_type
            }

    def _download_dataset(self, resource_name: str) -> Path:
        """
        Download full dataset from HuggingFace Hub

        Args:
            resource_name: "user/name"

        Returns:
            Path to downloaded dataset
        """
        # Use huggingface_hub library (if available)
        try:
            from huggingface_hub import snapshot_download

            dataset_dir = self.raw_dir / "dataset" / resource_name.split('/')[-1]
            dataset_dir.mkdir(parents=True, exist_ok=True)

            # Download dataset
            snapshot_download(
                repo_id=resource_name,
                repo_type="dataset",
                local_dir=str(dataset_dir),
                local_dir_use_symlinks=False
            )

            return dataset_dir

        except ImportError:
            raise RuntimeError("huggingface_hub library required for dataset download. Install: pip install huggingface_hub")

    def _download_model(self, resource_name: str) -> Path:
        """
        Download full model from HuggingFace Hub

        Args:
            resource_name: "user/name"

        Returns:
            Path to downloaded model
        """
        try:
            from huggingface_hub import snapshot_download

            model_dir = self.raw_dir / "dataset" / resource_name.split('/')[-1]
            model_dir.mkdir(parents=True, exist_ok=True)

            # Download model
            snapshot_download(
                repo_id=resource_name,
                repo_type="model",
                local_dir=str(model_dir),
                local_dir_use_symlinks=False
            )

            return model_dir

        except ImportError:
            raise RuntimeError("huggingface_hub library required for model download. Install: pip install huggingface_hub")

    def convert(self, fetched_data: Dict) -> str:
        """
        Combine README and metadata into markdown artifact

        Args:
            fetched_data: Data from fetch()

        Returns:
            Markdown content
        """
        readme = fetched_data['readme_content']
        card_info = fetched_data['card_info']
        resource_type = fetched_data['resource_type']
        resource_name = fetched_data['resource_name']

        # Create header with metadata
        header = self._create_metadata_header(resource_type, resource_name, card_info)

        # Combine header + README
        full_markdown = header + "\n\n" + readme

        return full_markdown

    def _create_metadata_header(self,
                                 resource_type: str,
                                 resource_name: str,
                                 card_info: Dict) -> str:
        """
        Create metadata header for HuggingFace resource markdown

        Args:
            resource_type: 'datasets' or 'models'
            resource_name: "user/name"
            card_info: Card metadata

        Returns:
            Header markdown string
        """
        type_label = "Dataset" if resource_type == 'datasets' else "Model"

        lines = [
            f"# HuggingFace {type_label}: {resource_name}",
            "",
            f"**URL**: {card_info.get('card_url', '')}",
            "",
            f"**Downloads**: {card_info.get('downloads', 0)}",
            "",
            f"**Likes**: {card_info.get('likes', 0)}",
            "",
            f"**Tags**: {', '.join(card_info.get('tags', []))}",
            "",
            f"**Task Type**: {', '.join(card_info.get('task_type', ['unknown']))}",
            ""
        ]

        if card_info.get('dataset_path'):
            lines.append(f"**Dataset Path**: {card_info['dataset_path']}")
            lines.append("")

        if card_info.get('model_path'):
            lines.append(f"**Model Path**: {card_info['model_path']}")
            lines.append("")

        lines.append("---")
        lines.append("")
        lines.append("## README")
        lines.append("")

        return "\n".join(lines)

    def get_output_path(self, source: str) -> Path:
        """
        Generate output path for HuggingFace resource

        datasets/user/data → hf-dataset-data.md
        models/user/model → hf-model-model.md

        Args:
            source: Resource identifier

        Returns:
            Path to markdown file in raw/dataset/
        """
        dataset_dir = self.raw_dir / "dataset"
        dataset_dir.mkdir(parents=True, exist_ok=True)

        # Parse source
        resource_type, resource_name = self._parse_source(source)

        # Create filename: hf-dataset-name.md or hf-model-name.md
        name_part = resource_name.split('/')[-1]
        type_prefix = "dataset" if resource_type == 'datasets' else "model"

        filename = f"hf-{type_prefix}-{name_part}.md"

        return dataset_dir / filename

def main():
    """Test HuggingFace handler"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: huggingface_handler.py <workspace> <resource>")
        print("Example: huggingface_handler.py /tmp/test-project datasets/openai/gpt2")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    resource = sys.argv[2]

    handler = HuggingFaceHandler(workspace)

    try:
        print(f"Fetching HuggingFace resource {resource}...")
        fetched = handler.fetch(resource)

        print(f"Converting to markdown...")
        markdown = handler.convert(fetched)

        print(f"Storing...")
        result = handler.store(
            source=resource,
            markdown_content=markdown,
            metadata=fetched['card_info']
        )

        print(f"✓ HuggingFace resource collected")
        print(f"  File: {result['file_path']}")
        print(f"  ID: {result['artifact_id']}")
        print(f"  Downloads: {fetched['card_info'].get('downloads', 0)}")

    except Exception as e:
        print(f"✗ Error: {str(e)}")

if __name__ == "__main__":
    main()