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
        Execute search with fallback strategy across multiple sources

        Strategy: Chrome MCP (Google Scholar) → arxiv SDK → arxiv API fallback
        Prioritization: arxiv SDK results preferred for download (most reliable)

        Args:
            query: Search query string
            top_per_source: Top results per source (default: 10)

        Returns:
            Dict with google_scholar, arxiv, prioritized results
        """
        results = {
            'query': query,
            'google_scholar': [],
            'arxiv': [],
            'github': [],
            'huggingface': [],
            'prioritized': [],
            'total_found': 0,
            'searched_at': datetime.now().isoformat()
        }

        # Try Chrome MCP search first (Google Scholar)
        gs_results = self._search_google_scholar_via_mcp(query, top_per_source)
        results['google_scholar'] = gs_results

        # Always search arxiv (SDK preferred, API fallback)
        arxiv_results = self._search_arxiv_sdk(query, top_per_source)
        results['arxiv'] = arxiv_results

        # Also search GitHub and HuggingFace (API-based)
        github_results = self._search_github(query, top_per_source)
        results['github'] = github_results

        hf_results = self._search_huggingface(query, top_per_source)
        results['huggingface'] = hf_results

        # Prioritize arxiv results for download (user preference: reliable papers)
        results['prioritized'] = arxiv_results[:top_per_source]

        # If arxiv empty but Google Scholar has results, use those
        if not arxiv_results and gs_results:
            results['prioritized'] = gs_results[:top_per_source]

        results['total_found'] = len(results['prioritized'])

        return results

    def _search_google_scholar_via_mcp(self, query: str, max_results: int) -> List[Dict]:
        """
        Search Google Scholar using Chrome MCP automation

        Args:
            query: Search query
            max_results: Maximum results

        Returns:
            List of Google Scholar paper results (empty if MCP unavailable)
        """
        try:
            import sys
            sys.path.insert(0, str(Path(__file__).parent))
            from mcp_client import ChromeMCPClient

            client = ChromeMCPClient()
            if not client.detect_server():
                return []  # Fallback to arxiv SDK

            # Use MCP client for Google Scholar search
            # (Currently returns empty - placeholder for future implementation)
            return client.search_google_scholar(query, max_results)

        except (ImportError, Exception):
            # Fallback: use arxiv SDK/API
            return []

    def _search_arxiv_sdk(self, query: str, max_results: int) -> List[Dict]:
        """
        Search arxiv using official SDK (preferred over API)

        Args:
            query: Search query
            max_results: Maximum results

        Returns:
            List of arxiv paper results with rich metadata
        """
        try:
            import arxiv

            # Configure client
            client = arxiv.Client(
                page_size=max_results,
                delay_seconds=3.0,
                num_retries=2
            )

            # Search query
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )

            # Extract results
            results = []
            for result in client.results(search):
                arxiv_id = result.entry_id.split('/')[-1]

                paper_info = {
                    'arxiv_id': arxiv_id,
                    'title': result.title,
                    'authors': [author.name for author in result.authors],
                    'published': result.published.strftime("%Y-%m-%d"),
                    'categories': list(result.categories) if result.categories else [],
                    'doi': result.doi,
                    'source': 'arxiv',
                    'source_url': result.entry_id,
                    'abstract': result.summary[:200] + "..." if len(result.summary) > 200 else result.summary
                }

                results.append(paper_info)

            return results

        except ImportError:
            # Fallback to API search (existing implementation)
            return self._search_arxiv(query, max_results)

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
        Collect approved search results (prioritized arxiv-first strategy)

        Args:
            search_results: Search results dict with prioritized list
            selection: User selection ('default' or custom override)

        Returns:
            Collection results
        """
        query = search_results['query']

        # Use prioritized results (arxiv-first by default)
        prioritized = search_results.get('prioritized', [])

        # Parse selection
        if selection == 'default':
            # Top-N from prioritized (arxiv-first)
            papers_to_download = prioritized[:10]

        else:
            # Parse custom selection (e.g., "top-5", "top-3 arxiv, top-2 github")
            papers_to_download = []

            # Simplified: if numeric, use that count
            if selection.isdigit():
                count = int(selection)
                papers_to_download = prioritized[:count]
            else:
                # Parse complex selection (placeholder)
                parts = selection.split(',')
                for part in parts:
                    part = part.strip()
                    if 'arxiv' in part or 'paper' in part:
                        count = int(part.split('-')[1]) if '-' in part else 5
                        papers_to_download = prioritized[:count]
                    elif 'top' in part:
                        count = int(part.split('-')[1]) if '-' in part else 10
                        papers_to_download = prioritized[:count]

        # Collect papers using PaperHandler (arxiv SDK preferred)
        collection_results = []

        for paper in papers_to_download:
            # Extract arxiv ID or URL
            if paper['source'] == 'arxiv':
                source_id = paper['arxiv_id']
            else:
                source_id = paper.get('source_url', paper.get('url', ''))

            # Collect single paper
            result = self.orchestrator._collect_single(
                source=source_id,
                handler_name='paper',
                extracted_id=source_id,
                override_flags={},
                max_retries=2,
                retry_delay=2.0
            )

            collection_results.append(result)

        # Create search-specific output directory
        query_hash = hashlib.md5(query.encode()).hexdigest()[:8]
        search_dir = self.workspace_root / 'raw' / 'search' / f'query-{query_hash}'
        search_dir.mkdir(parents=True, exist_ok=True)

        # Save search metadata
        query_metadata = {
            'query_hash': query_hash,
            'query': query,
            'sources_searched': ['google_scholar', 'arxiv', 'github', 'huggingface'],
            'results_per_source': {
                'google_scholar': {'found': len(search_results['google_scholar']), 'collected': 0},
                'arxiv': {'found': len(search_results['arxiv']), 'collected': len([p for p in papers_to_download if p['source'] == 'arxiv'])},
                'github': {'found': len(search_results['github']), 'collected': 0},
                'huggingface': {'found': len(search_results['huggingface']), 'collected': 0}
            },
            'prioritized_count': len(papers_to_download),
            'user_selection': selection,
            'collection_method': 'search_prioritized',
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

        # Summary
        successful = len([r for r in collection_results if r['status'] == 'success'])
        failed = len([r for r in collection_results if r['status'] == 'failed'])

        return {
            'collected': collection_results,
            'search_metadata': query_metadata,
            'search_dir': str(search_dir),
            'summary': {
                'total_attempted': len(papers_to_download),
                'successful': successful,
                'failed': failed
            }
        }

def main():
    """Test search collector with arxiv SDK integration"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: search.py <workspace> <query>")
        print("Example: search.py /tmp/test-project 'agent memory mechanisms'")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    query = sys.argv[2]

    collector = SearchCollector(workspace)

    # Check search capabilities
    try:
        import arxiv
        print(f"Using arxiv SDK (enhanced search)")
    except ImportError:
        print(f"Using arxiv API fallback (SDK not installed)")

    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from mcp_client import ChromeMCPClient
        client = ChromeMCPClient()
        if client.detect_server():
            print(f"Chrome MCP available (Google Scholar search)")
        else:
            print(f"Chrome MCP not available (arxiv-only search)")
    except ImportError:
        print(f"MCP SDK not installed (arxiv-only search)")

    print(f"\nSearching: '{query}'...")
    results = collector.search(query)

    print(f"\nFound {results['total_found']} prioritized results")
    print(f"  - Google Scholar: {len(results['google_scholar'])} papers")
    print(f"  - arxiv: {len(results['arxiv'])} papers")
    print(f"  - GitHub: {len(results['github'])} repos")
    print(f"  - HuggingFace: {len(results['huggingface'])} datasets/models")
    print(f"  - Prioritized (for download): {len(results['prioritized'])} papers")

    if results['prioritized']:
        print(f"\nTop 5 prioritized papers:")
        for i, paper in enumerate(results['prioritized'][:5], 1):
            print(f"  {i}. {paper.get('title', 'Unknown')[:60]}...")
            print(f"     arxiv ID: {paper.get('arxiv_id', 'N/A')}")
            print(f"     Published: {paper.get('published', 'N/A')}")

if __name__ == "__main__":
    main()