#!/usr/bin/env python3
"""
GitHub Handler
Fetches README and release info from GitHub repositories
"""

import hashlib
import json
import requests
from pathlib import Path
from typing import Dict
from datetime import datetime

from .base_handler import BaseHandler

class GitHubHandler(BaseHandler):
    """
    Handler for GitHub repositories

    Default: README + latest release (no full clone)
    Override: --full-repo flag for shallow clone (depth=1)

    Minimal parsing: README markdown + metadata only
    Metadata: stars, language, license, release_tag, last_updated
    """

    def get_source_type(self) -> str:
        return "github"

    def fetch(self, source: str, **kwargs) -> Dict:
        """
        Fetch README and release info from GitHub repo

        Args:
            source: Repo identifier (e.g., "user/repo" or full URL)
            **kwargs: Optional flags (full_repo=False)

        Returns:
            Dict with readme_content, release_info, metadata
        """
        # Extract repo name from source
        repo = self._extract_repo_name(source)

        # Fetch README
        readme_content = self._fetch_readme(repo)

        # Fetch release info
        release_info = self._fetch_release_info(repo)

        # Fetch repo metadata
        repo_metadata = self._fetch_repo_metadata(repo)

        # Check for full-repo flag
        if kwargs.get('full_repo', False):
            # Clone full repository (shallow, depth=1)
            repo_path = self._clone_repo(repo)
            repo_metadata['full_repo_path'] = str(repo_path)

        return {
            "readme_content": readme_content,
            "release_info": release_info,
            "metadata": repo_metadata,
            "repo": repo
        }

    def _extract_repo_name(self, source: str) -> str:
        """
        Extract repo name from various formats

        Args:
            source: Input in various formats

        Returns:
            Repo name "user/repo"
        """
        # Handle full URL
        if 'github.com' in source:
            parts = source.split('github.com/')[-1].split('/')
            if len(parts) >= 2:
                return f"{parts[0]}/{parts[1]}"

        # Handle "user/repo" format
        if '/' in source and not source.startswith('http'):
            return source.strip()

        raise ValueError(f"Invalid GitHub source: {source}")

    def _fetch_readme(self, repo: str) -> str:
        """
        Fetch README.md from GitHub repo

        Args:
            repo: Repo name "user/repo"

        Returns:
            README markdown content
        """
        readme_url = f"https://api.github.com/repos/{repo}/readme"

        try:
            # GitHub API returns JSON with content (base64 encoded)
            response = requests.get(readme_url, timeout=10)
            response.raise_for_status()

            readme_data = response.json()

            # Decode base64 content
            import base64
            readme_content = base64.b64decode(readme_data['content']).decode('utf-8')

            return readme_content

        except Exception as e:
            # Fallback: try raw.githubusercontent.com
            try:
                raw_url = f"https://raw.githubusercontent.com/{repo}/main/README.md"
                response = requests.get(raw_url, timeout=10)
                response.raise_for_status()
                return response.text
            except Exception:
                # Ultimate fallback: placeholder README
                return f"# {repo}\n\nREADME could not be fetched.\n\nSee: https://github.com/{repo}"

    def _fetch_release_info(self, repo: str) -> Dict:
        """
        Fetch latest release info from GitHub API

        Args:
            repo: Repo name "user/repo"

        Returns:
            Release metadata dict
        """
        releases_url = f"https://api.github.com/repos/{repo}/releases/latest"

        try:
            response = requests.get(releases_url, timeout=10)

            if response.status_code == 200:
                release_data = response.json()
                return {
                    "release_tag": release_data.get('tag_name', 'unknown'),
                    "release_name": release_data.get('name', 'unknown'),
                    "release_url": release_data.get('html_url', ''),
                    "release_date": release_data.get('published_at', '')
                }
            else:
                # No releases
                return {
                    "release_tag": "none",
                    "release_name": "none",
                    "release_url": "",
                    "release_date": ""
                }

        except Exception:
            return {
                "release_tag": "unknown",
                "release_name": "unknown",
                "release_url": "",
                "release_date": ""
            }

    def _fetch_repo_metadata(self, repo: str) -> Dict:
        """
        Fetch repo metadata from GitHub API

        Args:
            repo: Repo name "user/repo"

        Returns:
            Metadata dict (stars, language, license, etc.)
        """
        repo_url = f"https://api.github.com/repos/{repo}"

        try:
            response = requests.get(repo_url, timeout=10)
            response.raise_for_status()

            repo_data = response.json()

            return {
                "stars": repo_data.get('stargazers_count', 0),
                "language": repo_data.get('language', 'Unknown'),
                "license": repo_data.get('license', {}).get('spdx_id', 'Unknown') if repo_data.get('license') else 'Unknown',
                "description": repo_data.get('description', ''),
                "last_updated": repo_data.get('updated_at', ''),
                "repo_url": repo_data.get('html_url', f"https://github.com/{repo}")
            }

        except Exception as e:
            # Fallback metadata
            return {
                "stars": 0,
                "language": "Unknown",
                "license": "Unknown",
                "description": "",
                "last_updated": "",
                "repo_url": f"https://github.com/{repo}"
            }

    def _clone_repo(self, repo: str) -> Path:
        """
        Clone full repository (shallow clone, depth=1)

        Args:
            repo: Repo name "user/repo"

        Returns:
            Path to cloned repo
        """
        import subprocess

        repo_dir = self.raw_dir / "github" / repo.split('/')[-1]
        repo_dir.mkdir(parents=True, exist_ok=True)

        clone_url = f"https://github.com/{repo}.git"

        try:
            # Shallow clone (depth=1)
            subprocess.run(
                ['git', 'clone', '--depth=1', clone_url, str(repo_dir)],
                check=True,
                capture_output=True,
                timeout=60
            )

            return repo_dir

        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Git clone failed: {e.stderr.decode()}")
        except Exception as e:
            raise RuntimeError(f"Git clone error: {str(e)}")

    def convert(self, fetched_data: Dict) -> str:
        """
        Combine README and metadata into markdown artifact

        Args:
            fetched_data: Data from fetch()

        Returns:
            Markdown content
        """
        readme = fetched_data['readme_content']
        release = fetched_data['release_info']
        metadata = fetched_data['metadata']
        repo = fetched_data['repo']

        # Create header with metadata
        header = self._create_metadata_header(repo, metadata, release)

        # Combine header + README
        full_markdown = header + "\n\n" + readme

        return full_markdown

    def _create_metadata_header(self, repo: str, metadata: Dict, release: Dict) -> str:
        """
        Create metadata header for GitHub repo markdown

        Args:
            repo: Repo name
            metadata: Repo metadata
            release: Release info

        Returns:
            Header markdown string
        """
        lines = [
            f"# GitHub Repository: {repo}",
            "",
            f"**URL**: {metadata.get('repo_url', f'https://github.com/{repo}')}",
            "",
            f"**Stars**: {metadata.get('stars', 0)}",
            "",
            f"**Language**: {metadata.get('language', 'Unknown')}",
            "",
            f"**License**: {metadata.get('license', 'Unknown')}",
            "",
            f"**Last Updated**: {metadata.get('last_updated', 'Unknown')}",
            "",
            f"**Latest Release**: {release.get('release_tag', 'none')}",
            ""
        ]

        if metadata.get('description'):
            lines.append("**Description**: " + metadata['description'])
            lines.append("")

        if release.get('release_url'):
            lines.append(f"**Release URL**: {release['release_url']}")
            lines.append("")

        lines.append("---")
        lines.append("")
        lines.append("## README")
        lines.append("")

        return "\n".join(lines)

    def get_output_path(self, source: str) -> Path:
        """
        Generate output path for GitHub repo

        user/repo → github-user-project.md

        Args:
            source: Repo identifier

        Returns:
            Path to markdown file in raw/github/
        """
        github_dir = self.raw_dir / "github"
        github_dir.mkdir(parents=True, exist_ok=True)

        # Extract repo name
        repo = self._extract_repo_name(source)

        # Create filename: github-user-project.md
        filename = f"github-{repo.replace('/', '-')}.md"

        return github_dir / filename

def main():
    """Test GitHub handler"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: github_handler.py <workspace> <repo>")
        print("Example: github_handler.py /tmp/test-project anthropics/anthropic-sdk-python")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    repo = sys.argv[2]

    handler = GitHubHandler(workspace)

    try:
        print(f"Fetching repo {repo}...")
        fetched = handler.fetch(repo)

        print(f"Converting to markdown...")
        markdown = handler.convert(fetched)

        print(f"Storing...")
        result = handler.store(
            source=repo,
            markdown_content=markdown,
            metadata=fetched['metadata']
        )

        print(f"✓ GitHub repo collected")
        print(f"  File: {result['file_path']}")
        print(f"  ID: {result['artifact_id']}")
        print(f"  Stars: {fetched['metadata'].get('stars', 0)}")

    except Exception as e:
        print(f"✗ Error: {str(e)}")

if __name__ == "__main__":
    main()