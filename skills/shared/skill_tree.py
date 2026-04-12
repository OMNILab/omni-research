#!/usr/bin/env python3
"""
Skill Tree State Management
Tracks skill progress (unlocked/ready/locked/completed) and provides visualization
"""

import json
from pathlib import Path
from typing import List, Dict, Set

class SkillTree:
    """
    Manages skill tree state showing progress through research workflow
    """

    def __init__(self, tree_state_path: Path, contracts_dir: Path):
        """
        Initialize skill tree from state file and contracts

        Args:
            tree_state_path: Path to tree-state.json
            contracts_dir: Path to directory containing skill contracts
        """
        self.tree_state_path = tree_state_path
        self.contracts_dir = contracts_dir
        self.state = self.load_state()
        self.contracts = self.load_contracts()

    def load_state(self) -> Dict:
        """Load current tree state from JSON file"""
        if not self.tree_state_path.exists():
            # Initialize default state
            return {
                "unlocked": ["omr-bootstrap", "omr-collection", "omr-idea-note"],
                "ready": [],
                "locked": ["omr-evidence", "omr-research-plan", "omr-decision",
                           "omr-evaluation", "omr-synthesis", "omr-wiki",
                           "omr-reconcile", "omr-research-archive"],
                "completed": []
            }

        return json.loads(self.tree_state_path.read_text())

    def load_contracts(self) -> Dict[str, Dict]:
        """Load all skill contracts"""
        contracts = {}
        for contract_file in self.contracts_dir.glob("*.json"):
            contract = json.loads(contract_file.read_text())
            contracts[contract['skill']] = contract
        return contracts

    def save_state(self):
        """Persist current state to tree-state.json"""
        self.tree_state_path.write_text(json.dumps(self.state, indent=2))

    def update_tree(self, produced_artifacts: Set[str]):
        """
        Update tree state based on newly produced artifacts

        Args:
            produced_artifacts: Set of artifact names/patterns that were produced
        """
        # Check each locked skill to see if prerequisites are now satisfied
        new_ready = []
        for skill_name in self.state['locked']:
            contract = self.contracts.get(skill_name)
            if not contract:
                continue

            # Check if mandatory prerequisites are satisfied
            mandatory_reqs = [req['artifact'] for req in contract['requires']
                            if not req['optional']]

            # Simple check: see if required artifact exists in produced set
            # (More sophisticated check would verify actual file existence)
            satisfied = all(any(self._artifact_matches(req, produced_artifacts)
                               for produced in produced_artifacts)
                           for req in mandatory_reqs)

            if satisfied:
                new_ready.append(skill_name)

        # Move skills from locked to ready
        for skill in new_ready:
            self.state['locked'].remove(skill)
            self.state['ready'].append(skill)

        self.save_state()

    def _artifact_matches(self, required: str, produced_set: Set[str]) -> bool:
        """
        Check if a required artifact pattern matches any produced artifact

        Args:
            required: Required artifact pattern (e.g., 'evidence-map.md', 'materials in raw/')
            produced_set: Set of produced artifact names

        Returns:
            True if match found
        """
        # Simple matching logic (can be enhanced)
        # Check exact match or pattern containment
        for produced in produced_set:
            if required == produced:
                return True
            # Handle patterns like "raw/*" or "materials in raw/"
            if '*' in required:
                pattern = required.replace('*', '')
                if pattern in produced:
                    return True
            if required in produced or produced in required:
                return True
        return False

    def mark_completed(self, skill_name: str):
        """
        Mark a skill as completed (successfully executed)

        Args:
            skill_name: Name of completed skill
        """
        # Remove from current state (unlocked or ready)
        if skill_name in self.state['unlocked']:
            self.state['unlocked'].remove(skill_name)
        elif skill_name in self.state['ready']:
            self.state['ready'].remove(skill_name)

        # Add to completed
        if skill_name not in self.state['completed']:
            self.state['completed'].append(skill_name)

        self.save_state()

    def get_visualization(self, reverse: bool = False) -> str:
        """
        Generate ASCII visualization of skill tree

        Args:
            reverse: If True, show reverse view (goal-first planning)

        Returns:
            ASCII art skill tree
        """
        if reverse:
            return self._render_reverse_tree()
        else:
            return self._render_forward_tree()

    def _render_forward_tree(self) -> str:
        """Render forward view (explore what's possible)"""
        lines = []
        lines.append("📊 Skill Tree Progress (Forward View)")
        lines.append("=" * 50)
        lines.append("")

        # Completed skills
        if self.state['completed']:
            lines.append("✓ Completed Skills:")
            for skill in self.state['completed']:
                lines.append(f"  [✓] {skill}")
            lines.append("")

        # Unlocked skills (available for invocation)
        if self.state['unlocked']:
            lines.append("🔓 Unlocked Skills (available):")
            for skill in self.state['unlocked']:
                lines.append(f"  [○] {skill}")
            lines.append("")

        # Ready skills (prerequisites satisfied)
        if self.state['ready']:
            lines.append("⏸ Ready Skills (prerequisites satisfied):")
            for skill in self.state['ready']:
                # Show gate info if applicable
                contract = self.contracts.get(skill)
                gates = contract.get('gates', [])
                gate_info = ""
                if gates:
                    gate_ids = [g['id'] for g in gates]
                    gate_info = f" (Gate: {', '.join(gate_ids)})"
                lines.append(f"  [●] {skill}{gate_info}")
            lines.append("")

        # Locked skills (missing prerequisites)
        if self.state['locked']:
            lines.append("🔒 Locked Skills (missing prerequisites):")
            for skill in self.state['locked']:
                contract = self.contracts.get(skill)
                missing = []
                for req in contract.get('requires', []):
                    if not req['optional']:
                        missing.append(req['artifact'])
                missing_info = f" — needs: {', '.join(missing[:2])}"
                if len(missing) > 2:
                    missing_info += "..."
                lines.append(f"  [●] {skill}{missing_info}")
            lines.append("")

        return "\n".join(lines)

    def _render_reverse_tree(self) -> str:
        """Render reverse view (goal-first planning)"""
        lines = []
        lines.append("🎯 Skill Tree (Reverse View — Goal-First Planning)")
        lines.append("=" * 50)
        lines.append("")
        lines.append("Select your goal:")
        lines.append("")

        # List possible goals (skills that produce final outputs)
        goals = ["omr-synthesis", "omr-wiki", "omr-evaluation"]

        for i, goal in enumerate(goals, 1):
            contract = self.contracts.get(goal)
            produces = contract.get('produces', [])
            produces_desc = produces[0]['description'] if produces else "output"
            lines.append(f"  [{i}] {goal} — {produces_desc}")

        lines.append("")
        lines.append("Enter goal number to see prerequisite chain...")
        lines.append("")

        return "\n".join(lines)

    def get_progress_stats(self) -> Dict:
        """
        Get statistics about skill tree progress

        Returns:
            Dict with counts for each state
        """
        total_skills = (len(self.state['unlocked']) +
                       len(self.state['ready']) +
                       len(self.state['locked']) +
                       len(self.state['completed']))

        return {
            "total_skills": total_skills,
            "completed": len(self.state['completed']),
            "unlocked": len(self.state['unlocked']),
            "ready": len(self.state['ready']),
            "locked": len(self.state['locked']),
            "progress_percentage": round(len(self.state['completed']) / total_skills * 100, 1)
                               if total_skills > 0 else 0
        }

def main():
    """CLI entry point for skill tree visualization"""
    import sys

    # Default paths
    skills_dir = Path(__file__).parent.parent
    tree_state_path = skills_dir / "tree" / "tree-state.json"
    contracts_dir = skills_dir / "contracts"

    # Create default tree state if doesn't exist
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

    tree = SkillTree(tree_state_path, contracts_dir)

    # Check for reverse flag
    reverse = "--reverse" in sys.argv or "-r" in sys.argv

    print(tree.get_visualization(reverse=reverse))
    print()
    stats = tree.get_progress_stats()
    print(f"Progress: {stats['completed']}/{stats['total_skills']} skills completed ({stats['progress_percentage']}%)")

if __name__ == "__main__":
    main()