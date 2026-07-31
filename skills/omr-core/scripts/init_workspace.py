#!/usr/bin/env python3
"""
Initialize Workspace Infrastructure

Creates only mutable workspace state under .omr/. Static contracts, schemas,
built-in patterns, and runtime scripts remain in the installed omr-core skill.
Empty content directories are not pre-created.
"""

import json
import sys
from pathlib import Path
from typing import Optional


def init_workspace_infrastructure(workspace_path: Path,
                                   overwrite: bool = False) -> dict:
    """
    Initialize OmniResearch infrastructure in workspace

    Args:
        workspace_path: Path to project workspace root
        overwrite: If True, overwrite existing infrastructure; if False, merge

    Returns:
        Dict with created paths and metadata
    """
    tree_state = {
        "unlocked": ["omr-bootstrap", "omr-collection", "omr-idea-note", "omr-reconcile"],
        "ready": [],
        "locked": ["omr-analyze", "omr-decision", "omr-evaluation", "omr-synthesis"],
        "completed": []
    }

    tree_state_path = workspace_path / ".omr" / "tree-state.json"
    created_dirs = []

    if tree_state_path.exists() and not overwrite:
        tree_state = json.loads(tree_state_path.read_text())
    else:
        tree_state_path.parent.mkdir(parents=True, exist_ok=True)
        created_dirs.append(str(tree_state_path.parent))
        tree_state_path.write_text(json.dumps(tree_state, indent=2))

    return {
        "workspace_path": str(workspace_path),
        "created_directories": len(created_dirs),
        "copied_contracts": 0,
        "copied_schemas": 0,
        "copied_patterns": 0,
        "copied_scripts": 0,
        "tree_state_path": str(tree_state_path),
        "artifacts_index_path": None,
        "contracts": [],
        "schemas": [],
        "patterns": [],
        "scripts": []
    }


def main():
    """CLI entry point for infrastructure initialization"""
    if len(sys.argv) < 2:
        print("Usage: init_workspace.py <workspace-path> [--overwrite]")
        print("Example: init_workspace.py /path/to/project")
        print("         init_workspace.py /path/to/project --overwrite")
        sys.exit(1)

    workspace_path = Path(sys.argv[1]).resolve()
    overwrite = "--overwrite" in sys.argv

    if not workspace_path.exists():
        print(f"Error: Workspace path does not exist: {workspace_path}")
        print("Create the workspace directory first (or run omr-bootstrap)")
        sys.exit(1)

    print(f"Initializing OmniResearch infrastructure in: {workspace_path}")
    if overwrite:
        print("Mode: OVERWRITE (will replace existing files)")
    else:
        print("Mode: MERGE (will skip existing files)")
    print()

    result = init_workspace_infrastructure(workspace_path, overwrite)

    print("✓ Infrastructure initialized successfully")
    print(f"  Tree state: {result['tree_state_path']}")
    print()
    print("Static contracts/patterns remain in installed omr-core.")
    print("Content directories are created on demand by skills.")


if __name__ == "__main__":
    main()
