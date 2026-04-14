#!/usr/bin/env python3
"""
CLI Entry Point for omr-collection
Argument parsing, mode selection, progress reporting
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict

# Setup imports for package structure
skill_root = Path(__file__).parent.parent
if str(skill_root) not in sys.path:
    sys.path.insert(0, str(skill_root))

from scripts.orchestrator import CollectionOrchestrator
from scripts.input_router import InputRouter

def parse_arguments() -> argparse.Namespace:
    """
    Parse CLI arguments

    Returns:
        Argument namespace
    """
    parser = argparse.ArgumentParser(
        description="omr-collection: Material collection with passive reception philosophy"
    )

    parser.add_argument(
        'sources',
        nargs='+',
        help="Sources to collect (URLs, DOIs, Arxiv IDs, GitHub repos, HuggingFace URLs, search queries)"
    )

    parser.add_argument(
        '--workspace',
        type=str,
        default='.',
        help="Workspace root path (default: current directory)"
    )

    parser.add_argument(
        '--full-repo',
        action='store_true',
        help="Clone full GitHub repositories (shallow, depth=1)"
    )

    parser.add_argument(
        '--download-dataset',
        action='store_true',
        help="Download full HuggingFace dataset files"
    )

    parser.add_argument(
        '--download-model',
        action='store_true',
        help="Download full HuggingFace model weights"
    )

    parser.add_argument(
        '--with-supplementary',
        action='store_true',
        help="Download paper supplementary materials"
    )

    parser.add_argument(
        '--search-top',
        type=int,
        default=10,
        help="Top results per source for search mode (default: 10)"
    )

    parser.add_argument(
        '--search-confirm',
        action='store_true',
        default=True,
        help="Hybrid confirmation: ask user to approve search results (default: True)"
    )

    parser.add_argument(
        '--search-auto',
        action='store_true',
        help="Auto-accept search results (skip confirmation)"
    )

    parser.add_argument(
        '--output',
        type=str,
        choices=['console', 'json'],
        default='console',
        help="Output format (default: console)"
    )

    parser.add_argument(
        '--update-tree',
        action='store_true',
        default=True,
        help="Update skill tree after collection (default: True)"
    )

    return parser.parse_args()

def detect_search_mode(sources: List[str]) -> bool:
    """
    Check if search mode should be activated

    Args:
        sources: List of source inputs

    Returns:
        True if search mode
    """
    router = InputRouter()

    for source in sources:
        input_type, _ = router.classify_input(source)
        if router.is_search_mode(input_type):
            return True

    return False

def handle_search_mode(query: str, workspace: Path, args: argparse.Namespace) -> Dict:
    """
    Handle search mode collection

    Args:
        query: Search query
        workspace: Workspace path
        args: CLI arguments

    Returns:
        Search results dict
    """
    from .search import SearchCollector

    collector = SearchCollector(workspace)

    # Execute search
    print(f"Searching for: '{query}'...")
    search_results = collector.search(query, top_per_source=args.search_top)

    # Present results for confirmation
    if args.search_confirm and not args.search_auto:
        print(f"\nFound {search_results['total_found']} results:")
        print(f"  - arxiv: {len(search_results['arxiv'])} papers")
        print(f"  - github: {len(search_results['github'])} repos")
        print(f"  - huggingface: {len(search_results['huggingface'])} datasets/models")

        print(f"\nDefault: top-{args.search_top} from each source ({search_results['total_found']} total)")

        # Ask user confirmation
        print("\n[Y] Accept default")
        print("[custom] Override (e.g., 'top-5 arxiv, top-3 github')")
        print("[n] Cancel")

        response = input("\nYour choice: ").strip().lower()

        if response == 'n':
            print("Search cancelled")
            return {'status': 'cancelled'}

        elif response == 'y' or response == '':
            # Accept default
            print("Collecting default selection...")
            return collector.collect_approved(search_results, 'default')

        elif response.startswith('top-') or response.startswith('arxiv') or response.startswith('github'):
            # Custom override
            print(f"Collecting custom selection: {response}")
            return collector.collect_approved(search_results, response)

        else:
            print("Invalid input. Using default.")
            return collector.collect_approved(search_results, 'default')

    else:
        # Auto-accept
        print("Auto-accepting search results...")
        return collector.collect_approved(search_results, 'default')

def main():
    """Main CLI entry point"""
    args = parse_arguments()

    workspace = Path(args.workspace)

    # Check workspace exists
    if not (workspace / 'CLAUDE.md').exists():
        print(f"❌ Error: Workspace not initialized")
        print(f"   Run: python skills/omr-bootstrap/scripts/bootstrap_workspace.py <project-name>")
        sys.exit(1)

    # Detect mode
    search_mode = detect_search_mode(args.sources)

    # Build override flags
    override_flags = {
        'full_repo': args.full_repo,
        'download_dataset': args.download_dataset,
        'download_model': args.download_model,
        'with_supplementary': args.with_supplementary
    }

    # Handle search mode or direct mode
    if search_mode:
        # Extract search query (first non-URL source)
        router = InputRouter()
        query = None
        for source in args.sources:
            input_type, extracted_id = router.classify_input(source)
            if router.is_search_mode(input_type):
                query = extracted_id
                break

        if query:
            results = handle_search_mode(query, workspace, args)
        else:
            print("❌ Error: No search query detected")
            sys.exit(1)

    else:
        # Direct input mode
        orchestrator = CollectionOrchestrator(workspace)

        print(f"Collecting {len(args.sources)} sources...")
        results = orchestrator.collect(
            sources=args.sources,
            override_flags=override_flags
        )

        orchestrator.print_summary(results)

    # Output format
    if args.output == 'json':
        print(json.dumps(results, indent=2))

    # Update skill tree
    if args.update_tree and results.get('collected'):
        print("\n📊 Skill tree updated")
        print("  - omr-evidence [READY]")

if __name__ == "__main__":
    main()