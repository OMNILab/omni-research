#!/usr/bin/env python3
"""
Initialize Workspace Infrastructure
Sets up OmniResearch skill infrastructure in project workspace
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
    # Static contracts, schemas, built-in patterns, and runtime scripts remain
    # in the installed omr-core skill. The workspace stores only mutable OMR
    # state and user-defined patterns.
    infrastructure_dirs = [
        ".omr",
        ".omr/patterns",
        "docs/index/versions"
    ]

    created_dirs = []
    for dir_path in infrastructure_dirs:
        full_path = workspace_path / dir_path
        if full_path.exists() and not overwrite:
            # Merge mode: skip existing directories
            continue
        full_path.mkdir(parents=True, exist_ok=True)
        created_dirs.append(str(full_path))

    copied_contracts = []
    copied_schemas = []
    copied_patterns = []
    copied_scripts = []

    # Initialize skill tree state
    tree_state = {
        "unlocked": ["omr-bootstrap", "omr-collection", "omr-idea-note", "omr-reconcile"],
        "ready": [],
        "locked": ["omr-analyze", "omr-decision", "omr-evaluation", "omr-synthesis"],
        "completed": []
    }

    tree_state_path = workspace_path / ".omr" / "tree-state.json"
    if tree_state_path.exists() and not overwrite:
        # Merge mode: preserve existing tree state
        existing_state = json.loads(tree_state_path.read_text())
        tree_state = existing_state
    else:
        tree_state_path.parent.mkdir(parents=True, exist_ok=True)
        tree_state_path.write_text(json.dumps(tree_state, indent=2))

    # Initialize empty artifacts index
    artifacts_index_path = workspace_path / "docs" / "index" / "artifacts-index.json"
    if artifacts_index_path.exists() and not overwrite:
        existing_index = json.loads(artifacts_index_path.read_text())
        artifacts = existing_index.get("artifacts", [])
    else:
        artifacts_index_path.parent.mkdir(parents=True, exist_ok=True)
        artifacts = []
        artifacts_index_path.write_text(json.dumps({"artifacts": artifacts, "last_updated": ""}, indent=2))

    # Create .gitkeep files for empty directories
    gitkeep_locations = [
        "docs/index/versions/.gitkeep",
        ".omr/patterns/.gitkeep"
    ]

    for gitkeep_path in gitkeep_locations:
        full_path = workspace_path / gitkeep_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        if not full_path.exists():
            full_path.touch()

    return {
        "workspace_path": str(workspace_path),
        "created_directories": len(created_dirs),
        "copied_contracts": len(copied_contracts),
        "copied_schemas": len(copied_schemas),
        "copied_patterns": len(copied_patterns),
        "copied_scripts": len(copied_scripts),
        "tree_state_path": str(tree_state_path),
        "artifacts_index_path": str(artifacts_index_path),
        "contracts": copied_contracts,
        "schemas": copied_schemas,
        "patterns": copied_patterns,
        "scripts": copied_scripts
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
    print(f"  Directories: {result['created_directories']}")
    print(f"  Contracts: {result['copied_contracts']} files")
    print(f"  Schemas: {result['copied_schemas']} files")
    print(f"  Patterns: {result['copied_patterns']} files")
    print(f"  Scripts: {result['copied_scripts']} utility scripts")
    print()

    if result['contracts']:
        print(f"Contracts: {', '.join(result['contracts'][:5])}...")
    if result['scripts']:
        print(f"Utility scripts: {', '.join(result['scripts'])}")
    print()
    print(f"✓ Skill tree state: {result['tree_state_path']}")
    print(f"✓ Artifacts index: {result['artifacts_index_path']}")
    print()
    print("Infrastructure ready for OmniResearch skill invocation")

if __name__ == "__main__":
    main()