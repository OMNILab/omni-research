#!/usr/bin/env python3
"""
Runtime Utilities for OmniResearch Skills (Canonical Shared Module)
Minimal loader for omr-core infrastructure (contracts, dependency resolver, skill tree)

This is the single canonical copy of runtime_utils.py, located in omr-core/scripts/.
Domain skills carry a thin proxy stub that imports from this module, eliminating
~290 lines of duplication per skill.

Static infrastructure is loaded from the installed omr-core skill. Mutable,
workspace-specific state is loaded from workspace/.omr/.

Usage:
    from runtime_utils import load_infrastructure

    infra = load_infrastructure(workspace_root)
    resolver = infra['resolver'](infra['contracts_dir'], workspace_root, tree_state_path)
"""

import sys
from pathlib import Path
from typing import Dict, Optional, Tuple

def load_infrastructure(workspace_root: Optional[Path] = None) -> Dict:
    """
    Load static infrastructure from omr-core and state from workspace/.omr

    Args:
        workspace_root: Path to project workspace (optional)

    Returns:
        Dict with keys:
            - 'resolver': DependencyResolver class
            - 'tree': SkillTree class
            - 'contracts_dir': Path to contracts directory
            - 'tree_state_path': Path to tree-state.json

    Raises:
        ImportError: If omr-core infrastructure not found
    """
    local_core = Path(__file__).resolve().parent.parent
    core_candidates = [
        local_core,
        Path.home() / '.agents' / 'skills' / 'omr-core',
        Path.home() / '.claude' / 'skills' / 'omr-core',
    ]

    for core_root in core_candidates:
        scripts_dir = core_root / 'scripts'
        contracts_dir = core_root / 'contracts'
        if not scripts_dir.exists() or not contracts_dir.exists():
            continue

        sys.path.insert(0, str(scripts_dir))
        try:
            from dependency_resolver import DependencyResolver
            from skill_tree import SkillTree

            tree_state_path = (
                Path(workspace_root) / '.omr' / 'tree-state.json'
                if workspace_root
                else core_root / 'tree' / 'tree-state.json'
            )
            return {
                'resolver': DependencyResolver,
                'tree': SkillTree,
                'contracts_dir': contracts_dir,
                'tree_state_path': tree_state_path,
                'source': 'installed',
            }
        finally:
            sys.path.remove(str(scripts_dir))

    # Infrastructure not found
    raise ImportError(
        "OmniResearch infrastructure not found. "
        "Install omr-core skill first, then initialize workspace with omr-bootstrap. "
        "\n\n"
        "Installation:\n"
        "  1. /find-skills omr-core\n"
        "  2. /omr-bootstrap <project-name> <research-question>\n"
        "\n"
        "Install omr-core in ~/.agents/skills or ~/.claude/skills."
    )

def check_skill_dependency(skill_name: str,
                           workspace_root: Path,
                           required_artifacts: Optional[list] = None) -> Tuple[bool, list]:
    """
    Check if skill can be invoked (prerequisites satisfied)

    Args:
        skill_name: Skill identifier (e.g., 'omr-analyze')
        workspace_root: Path to project workspace
        required_artifacts: Optional list of artifact paths to check

    Returns:
        Tuple of (can_invoke, missing_artifacts)
    """
    try:
        infra = load_infrastructure(workspace_root)

        # Load dependency resolver
        resolver = infra['resolver'](
            infra['contracts_dir'],
            workspace_root,
            infra['tree_state_path']
        )

        # Check skill prerequisites
        can_invoke, missing = resolver.can_invoke_skill(skill_name)

        # Additional artifact checks if specified
        if required_artifacts:
            for artifact_path in required_artifacts:
                full_path = workspace_root / artifact_path
                if not full_path.exists():
                    missing.append(artifact_path)

        return can_invoke, missing

    except ImportError as e:
        # Infrastructure missing - cannot invoke
        return False, [str(e)]

def update_skill_tree(workspace_root: Path,
                      produced_artifacts: list,
                      skill_name: str) -> bool:
    """
    Update skill tree after successful skill execution

    Args:
        workspace_root: Path to project workspace
        produced_artifacts: List of artifacts produced by skill
        skill_name: Name of skill that executed

    Returns:
        True if tree updated successfully, False otherwise
    """
    try:
        infra = load_infrastructure(workspace_root)

        # Load dependency resolver
        resolver = infra['resolver'](
            infra['contracts_dir'],
            workspace_root,
            infra['tree_state_path']
        )

        # Update downstream skills
        resolver.update_downstream_skills(produced_artifacts)

        # Mark current skill as completed
        tree_state = resolver.tree_state

        if skill_name in tree_state['unlocked']:
            tree_state['unlocked'].remove(skill_name)
        if skill_name in tree_state['ready']:
            tree_state['ready'].remove(skill_name)

        if skill_name not in tree_state['completed']:
            tree_state['completed'].append(skill_name)

        # Save updated tree state
        import json
        infra['tree_state_path'].parent.mkdir(parents=True, exist_ok=True)
        infra['tree_state_path'].write_text(json.dumps(tree_state, indent=2))

        return True

    except Exception as e:
        print(f"⚠ Warning: Failed to update skill tree: {e}")
        return False

def get_skill_tree_visualization(workspace_root: Path,
                                  mode: str = 'forward') -> str:
    """
    Get skill tree visualization (forward or reverse view)

    Args:
        workspace_root: Path to project workspace
        mode: 'forward' (dependency view) or 'reverse' (producer view)

    Returns:
        ASCII visualization string
    """
    try:
        infra = load_infrastructure(workspace_root)

        # Load skill tree
        tree = infra['tree'](infra['tree_state_path'], infra['contracts_dir'])

        return tree.get_visualization(reverse=(mode == 'reverse'))

    except Exception as e:
        return f"Error: Failed to generate skill tree visualization: {e}"

def validate_contract(skill_name: str,
                      workspace_root: Optional[Path] = None) -> bool:
    """
    Validate skill contract against schema

    Args:
        skill_name: Skill identifier
        workspace_root: Optional workspace path (uses global if not provided)

    Returns:
        True if contract valid, False otherwise
    """
    try:
        infra = load_infrastructure(workspace_root)

        # Find contract file
        contract_file = infra['contracts_dir'] / f"{skill_name}.json"

        if not contract_file.exists():
            print(f"Error: Contract not found: {contract_file}")
            return False

        # Import validation module
        sys.path.insert(0, str(infra['contracts_dir'].parent / 'scripts'))
        from validate_contract import validate_contract_file

        # Validate
        is_valid, errors = validate_contract_file(contract_file)

        if not is_valid:
            print(f"Contract validation failed: {errors}")
            return False

        return True

    except Exception as e:
        print(f"Error: Failed to validate contract: {e}")
        return False

# Convenience function for skills without workspace context
def load_global_infrastructure() -> Dict:
    """
    Load omr-core infrastructure from global marketplace installation

    Use this when skill doesn't require workspace context

    Returns:
        Dict with infrastructure components
    """
    return load_infrastructure(workspace_root=None)

if __name__ == "__main__":
    # CLI test mode
    print("Runtime Utils - Infrastructure Loader Test")
    print("=" * 50)

    if len(sys.argv) > 1:
        test_workspace = Path(sys.argv[1])
        print(f"\nTesting workspace: {test_workspace}")
    else:
        test_workspace = None
        print("\nTesting global infrastructure (no workspace)")

    try:
        infra = load_infrastructure(test_workspace)
        print(f"\n✓ Infrastructure loaded from: {infra['source']}")
        print(f"  Contracts directory: {infra['contracts_dir']}")
        print(f"  Tree state path: {infra['tree_state_path']}")
        print(f"  Resolver: {infra['resolver'].__name__}")
        print(f"  Tree: {infra['tree'].__name__}")

        if test_workspace:
            print(f"\nSkill tree visualization:")
            print(get_skill_tree_visualization(test_workspace))

    except ImportError as e:
        print(f"\n❌ Error: {e}")