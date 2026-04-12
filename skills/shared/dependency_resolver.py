#!/usr/bin/env python3
"""
Dependency Resolver for Skill Invocation
Checks prerequisites, validates artifacts, and unlocks downstream skills
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

class DependencyResolver:
    """
    Resolves skill dependencies based on artifact requirements
    """

    def __init__(self, contracts_dir: Path, workspace_root: Path, tree_state_path: Path):
        """
        Initialize dependency resolver

        Args:
            contracts_dir: Path to skill contract files
            workspace_root: Path to research project root
            tree_state_path: Path to skill tree state file
        """
        self.contracts_dir = contracts_dir
        self.workspace_root = workspace_root
        self.tree_state_path = tree_state_path
        self.contracts = self.load_contracts()
        self.tree_state = self.load_tree_state()

    def load_contracts(self) -> Dict[str, Dict]:
        """Load all skill contracts"""
        contracts = {}
        for contract_file in self.contracts_dir.glob("*.json"):
            contract_data = json.loads(contract_file.read_text())
            contracts[contract_data['skill']] = contract_data
        return contracts

    def load_tree_state(self) -> Dict:
        """Load current skill tree state"""
        if not self.tree_state_path.exists():
            # Default initial state
            return {
                "unlocked": ["omr-bootstrap", "omr-collection", "omr-idea-note"],
                "ready": [],
                "locked": ["omr-evidence", "omr-research-plan", "omr-decision",
                           "omr-evaluation", "omr-synthesis", "omr-wiki",
                           "omr-reconcile", "omr-research-archive"],
                "completed": []
            }
        return json.loads(self.tree_state_path.read_text())

    def save_tree_state(self):
        """Persist updated tree state"""
        self.tree_state_path.write_text(json.dumps(self.tree_state, indent=2))

    def can_invoke_skill(self,
                          skill_name: str,
                          pattern_overrides: Dict = None) -> Tuple[bool, List[str]]:
        """
        Check if a skill can be invoked based on prerequisite artifacts

        Args:
            skill_name: Skill to check
            pattern_overrides: Optional pattern-specific contract overrides
                              (e.g., Experiment-First allows omr-evaluation without prior decision)

        Returns:
            (can_invoke, missing_artifacts)
        """
        contract = self.contracts.get(skill_name)
        if not contract:
            return False, [f"Skill '{skill_name}' not found in contracts"]

        # Apply pattern overrides if provided
        if pattern_overrides and skill_name in pattern_overrides:
            contract = self._apply_overrides(contract, pattern_overrides[skill_name])

        # Check mandatory prerequisites
        missing = []
        for requirement in contract.get('requires', []):
            if not requirement['optional']:
                artifact = requirement['artifact']
                if not self._check_artifact_exists(artifact):
                    missing.append(artifact)

        can_invoke = len(missing) == 0
        return can_invoke, missing

    def _apply_overrides(self, contract: Dict, overrides: Dict) -> Dict:
        """
        Apply pattern-specific contract overrides

        Args:
            contract: Original contract
            overrides: Override values (e.g., {'requires': []})

        Returns:
            Modified contract
        """
        modified_contract = contract.copy()
        for key, value in overrides.items():
            modified_contract[key] = value
        return modified_contract

    def _check_artifact_exists(self, artifact_pattern: str) -> bool:
        """
        Check if an artifact exists in workspace

        Args:
            artifact_pattern: Artifact name or pattern
                            (e.g., 'evidence-map.md', 'raw/*', 'materials in raw/')

        Returns:
            True if artifact exists
        """
        # Handle different artifact patterns
        if artifact_pattern.endswith('.md'):
            # Specific markdown file
            # Check docs/ directory
            artifact_path = self.workspace_root / 'docs' / artifact_pattern
            if artifact_path.exists():
                return True

            # Check if it's a specific named file anywhere in docs/
            for subdir in ['', 'ideas', 'archive', 'survey', 'report', 'manuscript', 'brief']:
                potential_path = self.workspace_root / 'docs' / subdir / artifact_pattern
                if potential_path.exists():
                    return True

        elif artifact_pattern.startswith('raw/') or 'raw/' in artifact_pattern:
            # Check raw/ directory for materials
            raw_dir = self.workspace_root / 'raw'

            if artifact_pattern == 'raw/*':
                # Any materials in raw/
                return any(raw_dir.iterdir())

            elif 'materials in raw/' in artifact_pattern:
                # Check if any subdirectory has content
                for subdir in ['paper', 'web', 'github', 'dataset', 'search']:
                    subdir_path = raw_dir / subdir
                    if subdir_path.exists() and any(subdir_path.iterdir()):
                        return True

            elif artifact_pattern.startswith('raw/'):
                # Specific raw subdirectory
                subdir = artifact_pattern.split('/')[1]
                subdir_path = raw_dir / subdir
                return subdir_path.exists() and any(subdir_path.iterdir())

        elif 'workspace' in artifact_pattern:
            # Workspace itself exists
            return self.workspace_root.exists()

        elif 'OR' in artifact_pattern:
            # Multiple alternatives (e.g., 'evaluation-report.md OR judgment-summary.md')
            alternatives = [alt.strip() for alt in artifact_pattern.split('OR')]
            return any(self._check_artifact_exists(alt) for alt in alternatives)

        elif 'any' in artifact_pattern:
            # Generic check (e.g., 'any artifact', 'any synthesis chapter')
            # Simplistic check: see if docs/ has any files
            docs_dir = self.workspace_root / 'docs'
            return docs_dir.exists() and any(
                f for f in docs_dir.rglob('*.md')
                if 'index' not in str(f)  # Exclude index files
            )

        return False

    def update_downstream_skills(self,
                                  produced_artifacts: List[str],
                                  pattern_overrides: Dict = None):
        """
        Unlock downstream skills after artifact production

        Args:
            produced_artifacts: List of artifacts that were produced
            pattern_overrides: Optional pattern overrides to apply when checking prerequisites
        """
        produced_set = set(produced_artifacts)

        # Check each locked skill
        new_ready = []
        for skill_name in self.tree_state['locked']:
            contract = self.contracts.get(skill_name)
            if not contract:
                continue

            # Apply pattern overrides
            if pattern_overrides and skill_name in pattern_overrides:
                contract = self._apply_overrides(contract, pattern_overrides[skill_name])

            # Check if mandatory prerequisites are now satisfied
            mandatory_reqs = [
                req['artifact'] for req in contract.get('requires', [])
                if not req['optional']
            ]

            # Check if all mandatory requirements satisfied by produced artifacts
            satisfied = all(
                self._matches_produced(req, produced_set)
                for req in mandatory_reqs
            )

            if satisfied:
                new_ready.append(skill_name)

        # Move skills from locked to ready
        for skill in new_ready:
            self.tree_state['locked'].remove(skill)
            self.tree_state['ready'].append(skill)

        self.save_tree_state()

    def _matches_produced(self, required: str, produced_set: Set[str]) -> bool:
        """
        Check if a required artifact matches any produced artifact

        Args:
            required: Required artifact pattern
            produced_set: Set of produced artifacts

        Returns:
            True if match found
        """
        # Exact match
        if required in produced_set:
            return True

        # Pattern match (e.g., 'raw/*' matches 'raw/paper/')
        for produced in produced_set:
            if '*' in required:
                pattern = required.replace('*', '')
                if pattern in produced:
                    return True
            if required in produced or produced in required:
                return True

        # OR alternatives
        if 'OR' in required:
            alternatives = [alt.strip() for alt in required.split('OR')]
            return any(alt in produced_set for alt in alternatives)

        return False

    def mark_skill_completed(self, skill_name: str):
        """
        Mark a skill as completed after successful execution

        Args:
            skill_name: Skill that was completed
        """
        # Remove from unlocked or ready
        if skill_name in self.tree_state['unlocked']:
            self.tree_state['unlocked'].remove(skill_name)
        elif skill_name in self.tree_state['ready']:
            self.tree_state['ready'].remove(skill_name)

        # Add to completed
        if skill_name not in self.tree_state['completed']:
            self.tree_state['completed'].append(skill_name)

        self.save_tree_state()

    def get_unlockable_skills(self) -> List[str]:
        """
        Get list of skills that would unlock if specific artifacts were produced

        Returns:
            List of skills and their required artifacts
        """
        unlockable = []
        for skill_name in self.tree_state['locked']:
            contract = self.contracts.get(skill_name)
            if not contract:
                continue

            missing = [
                req['artifact'] for req in contract.get('requires', [])
                if not req['optional'] and not self._check_artifact_exists(req['artifact'])
            ]

            if missing:
                unlockable.append({
                    'skill': skill_name,
                    'missing_artifacts': missing
                })

        return unlockable

def main():
    """CLI entry point for dependency resolver"""
    import argparse

    parser = argparse.ArgumentParser(description="Dependency resolver for skill invocation")
    parser.add_argument("skill", help="Skill name to check or invoke")
    parser.add_argument("--workspace", help="Workspace root path", default=".")
    parser.add_argument("--check", action="store_true", help="Check if skill can be invoked")
    parser.add_argument("--complete", action="store_true", help="Mark skill as completed")
    parser.add_argument("--pattern", help="Pattern name for contract overrides")

    args = parser.parse_args()

    # Setup paths
    workspace_root = Path(args.workspace)
    skills_dir = Path(__file__).parent.parent
    contracts_dir = skills_dir / "contracts"
    tree_state_path = workspace_root / "skills" / "tree-state.json"

    # Ensure tree state exists
    if not tree_state_path.exists():
        tree_state_path.parent.mkdir(parents=True, exist_ok=True)
        tree_state_path.write_text(json.dumps({
            "unlocked": ["omr-bootstrap", "omr-collection", "omr-idea-note"],
            "ready": [],
            "locked": ["omr-evidence", "omr-research-plan", "omr-decision",
                       "omr-evaluation", "omr-synthesis", "omr-wiki",
                       "omr-reconcile", "omr-research-archive"],
            "completed": []
        }, indent=2))

    resolver = DependencyResolver(contracts_dir, workspace_root, tree_state_path)

    # Load pattern overrides if specified
    pattern_overrides = None
    if args.pattern:
        patterns_dir = skills_dir / "patterns"
        pattern_file = patterns_dir / f"{args.pattern}.json"
        if pattern_file.exists():
            pattern = json.loads(pattern_file.read_text())
            pattern_overrides = pattern.get('contract_overrides', {})

    if args.check:
        # Check if skill can be invoked
        can_invoke, missing = resolver.can_invoke_skill(args.skill, pattern_overrides)

        if can_invoke:
            print(f"✓ Skill '{args.skill}' can be invoked")
            print(f"  All prerequisites satisfied")
            sys.exit(0)
        else:
            print(f"✗ Skill '{args.skill}' cannot be invoked")
            print(f"  Missing artifacts:")
            for artifact in missing:
                print(f"    - {artifact}")
            sys.exit(1)

    elif args.complete:
        # Mark skill as completed
        resolver.mark_skill_completed(args.skill)
        print(f"✓ Skill '{args.skill}' marked as completed")
        sys.exit(0)

    else:
        # Default: show what would unlock
        unlockable = resolver.get_unlockable_skills()
        print(f"Locked skills and their requirements:")
        for item in unlockable:
            print(f"  {item['skill']}:")
            for artifact in item['missing_artifacts']:
                print(f"    - {artifact}")

if __name__ == "__main__":
    main()