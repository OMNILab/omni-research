#!/usr/bin/env python3
"""
Collection Orchestrator
Coordinates handler execution, retry logic, fallback mechanism, and error handling
"""

import time
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Setup imports for package structure
skill_root = Path(__file__).parent.parent
if str(skill_root) not in sys.path:
    sys.path.insert(0, str(skill_root))

from scripts.input_router import InputRouter, InputType
from handlers import GenericWebHandler, PaperHandler, GitHubHandler, HuggingFaceHandler
from handlers.base_handler import BaseHandler

class CollectionOrchestrator:
    """
    Orchestrates material collection with retry + fallback + error handling
    """

    def __init__(self, workspace_root: Path):
        """
        Initialize orchestrator

        Args:
            workspace_root: Path to research project root
        """
        self.workspace_root = workspace_root
        self.router = InputRouter()

        # Initialize handlers
        self.handlers = {
            'paper': PaperHandler(workspace_root),
            'github': GitHubHandler(workspace_root),
            'huggingface': HuggingFaceHandler(workspace_root),
            'generic_web': GenericWebHandler(workspace_root)
        }

    def collect(self,
                sources: List[str],
                override_flags: Dict = None,
                max_retries: int = 2,
                retry_delay: float = 2.0) -> Dict:
        """
        Collect materials from multiple sources with error handling

        Args:
            sources: List of source identifiers (URLs, DOIs, IDs, etc.)
            override_flags: Optional flags (--full-repo, --download-dataset, etc.)
            max_retries: Maximum retry attempts (default: 2)
            retry_delay: Delay between retries in seconds (default: 2.0)

        Returns:
            Dict with collected artifacts, failed sources, summary
        """
        override_flags = override_flags or {}

        # Route inputs to handlers
        routed = self.router.route_inputs(sources)

        # Process each source
        results = {
            'collected': [],
            'failed': [],
            'search_triggered': None
        }

        # Check if search mode triggered
        search_items = [item for item in routed if item['is_search']]
        if search_items:
            # Handle search separately
            search_query = search_items[0]['extracted_id']
            results['search_triggered'] = search_query
            # Note: Search collection handled separately by search.py
            return results

        # Process direct inputs
        for item in routed:
            if item['is_search']:
                continue  # Skip search items (handled above)

            source = item['input']
            handler_name = item['handler']
            extracted_id = item['extracted_id']

            # Attempt collection with retry + fallback
            result = self._collect_single(
                source=source,
                handler_name=handler_name,
                extracted_id=extracted_id,
                override_flags=override_flags,
                max_retries=max_retries,
                retry_delay=retry_delay
            )

            if result['status'] == 'success':
                results['collected'].append(result)
            else:
                results['failed'].append(result)

        # Generate summary
        results['summary'] = {
            'total_sources': len(sources),
            'collected_count': len(results['collected']),
            'failed_count': len(results['failed']),
            'collected_at': datetime.now().isoformat()
        }

        # Update skill tree (unlock downstream)
        self._update_skill_tree(results['collected'])

        return results

    def _collect_single(self,
                        source: str,
                        handler_name: str,
                        extracted_id: str,
                        override_flags: Dict,
                        max_retries: int,
                        retry_delay: float) -> Dict:
        """
        Collect single source with retry + fallback

        Args:
            source: Original source string
            handler_name: Handler to use
            extracted_id: Extracted identifier
            override_flags: Override flags
            max_retries: Max retry attempts
            retry_delay: Retry delay

        Returns:
            Result dict with status, metadata, error info
        """
        handler = self.handlers.get(handler_name)

        if not handler:
            return {
                'status': 'failed',
                'source': source,
                'error_type': 'no_handler',
                'error_message': f"No handler for {handler_name}",
                'retry_attempts': 0,
                'fallback_attempted': False
            }

        # Attempt primary handler with retry
        retry_attempts = 0
        last_error = None

        for attempt in range(max_retries + 1):
            try:
                # Fetch materials
                fetched = handler.fetch(extracted_id, **override_flags)

                # Convert to markdown
                markdown = handler.convert(fetched)

                # Store artifact
                stored = handler.store(
                    source=source,
                    markdown_content=markdown,
                    metadata=fetched.get('metadata', {}),
                    **override_flags
                )

                return {
                    'status': 'success',
                    'source': source,
                    'handler': handler_name,
                    'artifact_id': stored['artifact_id'],
                    'file_path': stored['file_path'],
                    'metadata': stored['metadata'],
                    'retry_attempts': retry_attempts
                }

            except Exception as e:
                last_error = str(e)
                retry_attempts = attempt

                if attempt < max_retries:
                    # Wait before retry
                    time.sleep(retry_delay)
                    continue

        # Primary handler failed after retries
        # Try fallback (Generic Web)
        fallback_attempted = False
        fallback_handler = self.handlers.get('generic_web')

        if fallback_handler and handler_name != 'generic_web':
            fallback_attempted = True

            try:
                # Fallback: Generic Web snapshot
                fetched = fallback_handler.fetch(source, **override_flags)
                markdown = fallback_handler.convert(fetched)
                stored = fallback_handler.store(
                    source=source,
                    markdown_content=markdown,
                    metadata=fetched.get('metadata', {}),
                    **override_flags
                )

                return {
                    'status': 'success',
                    'source': source,
                    'handler': 'generic_web (fallback)',
                    'artifact_id': stored['artifact_id'],
                    'file_path': stored['file_path'],
                    'metadata': stored['metadata'],
                    'retry_attempts': retry_attempts,
                    'fallback_attempted': True
                }

            except Exception as fallback_error:
                last_error = str(fallback_error)

        # All attempts failed
        # Create error artifact
        handler.create_error_artifact(
            source=source,
            error_type='collection_failed',
            error_message=last_error,
            retry_attempts=retry_attempts,
            fallback_attempted=fallback_attempted
        )

        return {
            'status': 'failed',
            'source': source,
            'error_type': 'collection_failed',
            'error_message': last_error,
            'retry_attempts': retry_attempts,
            'fallback_attempted': fallback_attempted
        }

    def _update_skill_tree(self, collected: List[Dict]):
        """
        Update skill tree state after successful collection

        Args:
            collected: List of successfully collected artifacts
        """
        if not collected:
            return

        # Import dependency resolver
        import sys
        sys.path.insert(0, str(self.workspace_root / 'skills' / 'shared'))
        from dependency_resolver import DependencyResolver

        # Load tree state and contracts
        tree_state_path = self.workspace_root / 'skills' / 'tree-state.json'
        contracts_dir = self.workspace_root / 'skills' / 'shared' / 'contracts'

        resolver = DependencyResolver(contracts_dir, self.workspace_root, tree_state_path)

        # Get produced artifacts
        produced_artifacts = set()
        for item in collected:
            file_path = item.get('file_path', '')
            if file_path:
                # Extract artifact pattern (e.g., 'raw/paper/')
                if 'raw/paper/' in file_path:
                    produced_artifacts.add('materials in raw/')
                elif 'raw/web/' in file_path:
                    produced_artifacts.add('materials in raw/')
                elif 'raw/github/' in file_path:
                    produced_artifacts.add('materials in raw/')

        # Update downstream skills
        resolver.update_downstream_skills(list(produced_artifacts))

    def print_summary(self, results: Dict):
        """
        Print collection summary to console

        Args:
            results: Collection results dict
        """
        summary = results.get('summary', {})

        print(f"\n{'=' * 80}")
        print(f"Collection Summary")
        print(f"{'=' * 80}\n")

        if results['collected']:
            print(f"✓ Collected {len(results['collected'])} artifacts")

            # Group by source type
            by_type = {}
            for item in results['collected']:
                source_type = item['metadata'].get('source_type', 'unknown')
                by_type[source_type] = by_type.get(source_type, 0) + 1

            for source_type, count in by_type.items():
                print(f"  - {source_type}: {count}")

        if results['failed']:
            print(f"\n⚠ Failed: {len(results['failed'])} sources")
            for item in results['failed']:
                print(f"  - {item['source']} ({item['error_type']})")

        if results['search_triggered']:
            print(f"\n🔍 Search triggered: '{results['search_triggered']}'")
            print(f"  Run search collection separately")

        print(f"\n{'=' * 80}\n")

def main():
    """Test collection orchestrator"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: orchestrator.py <workspace> <sources>")
        print("Example: orchestrator.py /tmp/test-project 2402.12345 github.com/user/repo")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    sources = sys.argv[2:]

    orchestrator = CollectionOrchestrator(workspace)

    print(f"Collecting {len(sources)} sources...")
    results = orchestrator.collect(sources)

    orchestrator.print_summary(results)

if __name__ == "__main__":
    main()