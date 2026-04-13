#!/usr/bin/env python3
"""
Search Integration for omr-collection
Searches arxiv, GitHub, HuggingFace with hybrid confirmation
"""

import requests
import json
import hashlib
from pathlib import Path
from typing import Dict, List
from datetime import datetime

from .orchestrator import CollectionOrchestrator

class SearchCollector:
    """
    Handles search-based collection with hybrid confirmation
    """

    def __init__(self, workspace_root: Path):
        """
        Initialize search collector

        Args:
            workspace_root: Path to research project root
        """
        self.workspace_root = workspace_root
        self.orchestrator = CollectionOrchestrator(workspace_root)

    def search(self, query: str, top_per_source: int = 10) -> Dict:
        """
        Execute search across arxiv, GitHub, HuggingFace

        Args:
            query: Search query string
            top_per_source: Top results per source (default: 10)

        Returns:
            Dict with arxiv, github, huggingface results
        """
        results = {
            'query': query,
            'arxiv': [],
            'github': [],
            'huggingface': [],
            'total_found': 0,
            'searched_at': datetime.now().isoformat()
        }

        # Search arxiv
        arxiv_results = self._search_arxiv(query, top_per_source)
        results['arxiv'] = arxiv_results

        # Search GitHub
        github_results = self._search_github(query, top_per_source)
        results['github'] = github_results

        # Search HuggingFace
        hf_results = self._search_huggingface(query, top_per_source)
        results['huggingface'] = hf_results

        results['total_found'] = len(arxiv_results) + len(github_results) + len(hf_results)

        return results

    def _search_arxiv(self, query: str, max_results: int) -> List[Dict]:
        """
        Search arxiv API

        Args:
            query: Search query
            max_results: Maximum results

        Returns:
            List of arxiv paper results
        """
        # Arxiv API endpoint
        api_url = "http://export.arxiv.org/api/query"

        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results
        }

        try:
            response = requests.get(api_url, params=params, timeout=30)
            response.raise_for_status()

            # Parse XML response (simplified - real would use xml.etree)
            # For now, return placeholder structure
            # In real implementation, would parse XML properly

            results = []
            # Placeholder: would extract entries from XML
            # Each entry would have: id, title, authors, summary, arxiv_id

            return results

        except Exception as e:
            print(f"⚠ Arxiv search error: {str(e)}")
            return []

    def _search_github(self, query: str, max_results: int) -> List[Dict]:
        """
        Search GitHub API

        Args:
            query: Search query
            max_results: Maximum results

        Returns:
            List of GitHub repo results
        """
        # GitHub Search API
        api_url = "https://api.github.com/search/repositories"

        params = {
            'q': query,
            'sort': 'stars',
            'order': 'desc',
            'per_page': max_results
        }

        try:
            response = requests.get(api_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])

                results = []
                for item in items:
                    results.append({
                        'repo': item['full_name'],
                        'url': item['html_url'],
                        'description': item.get('description', ''),
                        'stars': item['stargazers_count'],
                        'language': item.get('language', 'Unknown')
                    })

                return results
            else:
                print(f"⚠ GitHub search error: HTTP {response.status_code}")
                return []

        except Exception as e:
            print(f"⚠ GitHub search error: {str(e)}")
            return []

    def _search_huggingface(self, query: str, max_results: int) -> List[Dict]:
        """
        Search HuggingFace Hub

        Args:
            query: Search query
            max_results: Maximum results

        Returns:
            List of HuggingFace resource results
        """
        # HuggingFace search API (simplified)
        # Real implementation would use huggingface_hub library

        try:
            # Placeholder: would use HF Hub search
            results = []

            # Example structure for datasets
            # Would search both datasets and models

            return results

        except Exception as e:
            print(f"⚠ HuggingFace search error: {str(e)}")
            return []

    def collect_approved(self, search_results: Dict, selection: str) -> Dict:
        """
        Collect approved search results

        Args:
            search_results: Search results dict
            selection: User selection ('default' or custom override)

        Returns:
            Collection results
        """
        query = search_results['query']

        # Parse selection
        if selection == 'default':
            # Top-N from each source
            arxiv_urls = [item['arxiv_id'] for item in search_results['arxiv'][:10]]
            github_urls = [item['repo'] for item in search_results['github'][:10]]
            hf_urls = [item['url'] for item in search_results['huggingface'][:10]]

        else:
            # Parse custom selection (e.g., "top-5 arxiv, top-3 github")
            # Simplified: parse user input
            arxiv_urls = []
            github_urls = []
            hf_urls = []

            parts = selection.split(',')
            for part in parts:
                part = part.strip()
                if 'arxiv' in part:
                    count = int(part.split('-')[1]) if '-' in part else 5
                    arxiv_urls = [item['arxiv_id'] for item in search_results['arxiv'][:count]]
                elif 'github' in part:
                    count = int(part.split('-')[1]) if '-' in part else 5
                    github_urls = [item['repo'] for item in search_results['github'][:count]]
                elif 'hf' in part or 'huggingface' in part:
                    count = int(part.split('-')[1]) if '-' in part else 5
                    hf_urls = [item['url'] for item in search_results['huggingface'][:count]]

        # Collect approved sources
        all_sources = arxiv_urls + github_urls + hf_urls

        # Create search-specific output directory
        query_hash = hashlib.md5(query.encode()).hexdigest()[:8]
        search_dir = self.workspace_root / 'raw' / 'search' / f'query-{query_hash}'
        search_dir.mkdir(parents=True, exist_ok=True)

        # Collect materials
        collection_results = self.orchestrator.collect(all_sources)

        # Save search metadata
        query_metadata = {
            'query_hash': query_hash,
            'query': query,
            'sources_searched': ['arxiv', 'github', 'huggingface'],
            'results_per_source': {
                'arxiv': {'found': len(search_results['arxiv']), 'collected': len(arxiv_urls)},
                'github': {'found': len(search_results['github']), 'collected': len(github_urls)},
                'huggingface': {'found': len(search_results['huggingface']), 'collected': len(hf_urls)}
            },
            'user_selection': selection,
            'collection_method': 'search',
            'collected_at': datetime.now().isoformat()
        }

        query_metadata_path = search_dir / 'query-metadata.json'
        query_metadata_path.write_text(json.dumps(query_metadata, indent=2))

        # Update search index
        search_index = self.workspace_root / 'docs' / 'index' / 'search-queries-index.json'

        if search_index.exists():
            index_data = json.loads(search_index.read_text())
        else:
            index_data = {'queries': [], 'last_updated': datetime.now().isoformat()}

        index_data['queries'].append(query_metadata)
        index_data['last_updated'] = datetime.now().isoformat()

        search_index.write_text(json.dumps(index_data, indent=2))

        collection_results['search_metadata'] = query_metadata
        collection_results['search_dir'] = str(search_dir)

        return collection_results

def main():
    """Test search collector"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: search.py <workspace> <query>")
        print("Example: search.py /tmp/test-project 'agent memory mechanisms'")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    query = sys.argv[2]

    collector = SearchCollector(workspace)

    print(f"Searching: '{query}'...")
    results = collector.search(query)

    print(f"\nFound {results['total_found']} results")
    print(f"  - arxiv: {len(results['arxiv'])} papers")
    print(f"  - github: {len(results['github'])} repos")
    print(f"  - huggingface: {len(results['huggingface'])} datasets/models")

if __name__ == "__main__":
    main()