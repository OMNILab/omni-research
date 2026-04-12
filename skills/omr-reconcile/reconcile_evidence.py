#!/usr/bin/env python3
"""
omr-reconcile Implementation
Iteration support when new evidence arrives
"""

import json
import shutil
from pathlib import Path
from typing import Dict
from datetime import datetime

def reconcile_evidence(workspace_root: Path) -> Dict:
    """
    Reconcile existing artifacts when new evidence arrives

    Args:
        workspace_root: Project workspace

    Returns:
        Dict with reconciliation status
    """
    docs_dir = workspace_root / 'docs'
    archive_dir = docs_dir / 'archive'

    # Check existing artifacts
    existing_artifacts = [
        docs_dir / 'research-brief.md',
        docs_dir / 'evidence-map.md',
        docs_dir / 'judgment-summary.md',
        docs_dir / 'research-plan.md',
        docs_dir / 'architecture-decision.md',
        docs_dir / 'experiment-spec.md',
        docs_dir / 'evaluation-report.md'
    ]

    artifacts_to_reconcile = [a for a in existing_artifacts if a.exists()]

    if not artifacts_to_reconcile:
        return {
            'status': 'no_artifacts',
            'message': 'No existing artifacts to reconcile'
        }

    # Archive previous versions
    archive_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    archive_session_dir = archive_dir / f'reconciliation-{timestamp}'
    archive_session_dir.mkdir(parents=True)

    archived_files = []
    for artifact in artifacts_to_reconcile:
        archived_path = archive_session_dir / artifact.name
        shutil.copy(artifact, archived_path)
        archived_files.append(str(archived_path))

    # Trigger re-evaluation (placeholder - would call downstream skills)
    # In real implementation:
    # - Re-run omr-evidence
    # - Re-run omr-research-plan
    # - Update affected decisions

    # Update skill tree
    update_tree_state(workspace_root)

    return {
        'status': 'success',
        'archived_dir': str(archive_session_dir),
        'archived_files': len(archived_files),
        'message': f'Archived {len(archived_files)} previous versions'
    }

def update_tree_state(workspace_root: Path):
    """Update skill tree after reconciliation"""
    tree_state_path = workspace_root / 'skills' / 'tree-state.json'

    if not tree_state_path.exists():
        return

    state = json.loads(tree_state_path.read_text())

    # Mark omr-reconcile as completed
    state['completed'].append('omr-reconcile')

    tree_state_path.write_text(json.dumps(state, indent=2))

def main():
    """CLI entry point"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: reconcile_evidence.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])

    print("Reconciling existing evidence...")
    result = reconcile_evidence(workspace)

    if result['status'] == 'success':
        print(f"✓ Reconciliation complete")
        print(f"  Archived: {result['archived_dir']}")
        print(f"  Files: {result['archived_files']}")
        print(f"\n  {result['message']}")

    else:
        print(f"  {result['message']}")

if __name__ == "__main__":
    main()