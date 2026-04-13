#!/usr/bin/env python3
"""
Initialize Workspace Infrastructure
Sets up OmniResearch skill infrastructure in project workspace
"""

import json
import sys
import shutil
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
    # Find omr-core skill root (where this script lives)
    script_path = Path(__file__).resolve()
    omr_core_root = script_path.parent.parent

    # Infrastructure directories to create
    infrastructure_dirs = [
        "skills/contracts",
        "skills/schemas",
        "skills/patterns",
        "skills/tree",
        "skills/shared",
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

    # Copy contract files
    contracts_src = omr_core_root / "contracts"
    contracts_dst = workspace_path / "skills" / "contracts"

    copied_contracts = []
    for contract_file in contracts_src.glob("*.json"):
        dst_file = contracts_dst / contract_file.name
        if dst_file.exists() and not overwrite:
            continue
        shutil.copy2(contract_file, dst_file)
        copied_contracts.append(contract_file.name)

    # Copy schema files
    schemas_src = omr_core_root / "schemas"
    schemas_dst = workspace_path / "skills" / "schemas"

    copied_schemas = []
    for schema_file in schemas_src.glob("*.json"):
        dst_file = schemas_dst / schema_file.name
        if dst_file.exists() and not overwrite:
            continue
        shutil.copy2(schema_file, dst_file)
        copied_schemas.append(schema_file.name)

    # Copy pattern files
    patterns_src = omr_core_root / "patterns"
    patterns_dst = workspace_path / "skills" / "patterns"

    copied_patterns = []
    for pattern_file in patterns_src.glob("*.json"):
        dst_file = patterns_dst / pattern_file.name
        if dst_file.exists() and not overwrite:
            continue
        shutil.copy2(pattern_file, dst_file)
        copied_patterns.append(pattern_file.name)

    # Copy utility scripts to shared directory
    scripts_src = omr_core_root / "scripts"
    scripts_dst = workspace_path / "skills" / "shared"

    utility_scripts = [
        "dependency_resolver.py",
        "skill_tree.py",
        "validate_contract.py",
        "detect_pattern.py"
    ]

    copied_scripts = []
    for script_name in utility_scripts:
        src_file = scripts_src / script_name
        dst_file = scripts_dst / script_name
        if not src_file.exists():
            print(f"⚠ Warning: {script_name} not found in omr-core")
            continue
        if dst_file.exists() and not overwrite:
            continue
        shutil.copy2(src_file, dst_file)
        copied_scripts.append(script_name)

    # Initialize skill tree state
    tree_state = {
        "unlocked": ["omr-bootstrap", "omr-collection", "omr-idea-note", "omr-reconcile", "omr-research-archive"],
        "ready": [],
        "locked": ["omr-evidence", "omr-research-plan", "omr-decision", "omr-evaluation", "omr-synthesis", "omr-wiki"],
        "completed": []
    }

    tree_state_path = workspace_path / "skills" / "tree" / "tree-state.json"
    if tree_state_path.exists() and not overwrite:
        # Merge mode: preserve existing tree state
        existing_state = json.loads(tree_state_path.read_text())
        tree_state = existing_state
    else:
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
        "skills/contracts/.gitkeep",
        "skills/schemas/.gitkeep",
        "skills/patterns/.gitkeep"
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