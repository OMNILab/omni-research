#!/usr/bin/env python3
"""
Skill Tree State Management
Tracks skill progress (unlocked/ready/locked/completed) and provides visualization
"""

import json
from pathlib import Path
from typing import Dict, List, Set


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
                "unlocked": [
                    "omr-bootstrap",
                    "omr-collection",
                    "omr-idea-note",
                    "omr-reconcile",
                ],
                "ready": [],
                "locked": [
                    "omr-analyze",
                    "omr-decision",
                    "omr-evaluation",
                    "omr-synthesis",
                ],
                "completed": [],
            }

        return json.loads(self.tree_state_path.read_text())

    def load_contracts(self) -> Dict[str, Dict]:
        """Load all skill contracts"""
        contracts = {}
        for contract_file in self.contracts_dir.glob("*.json"):
            contract = json.loads(contract_file.read_text())
            contracts[contract["skill"]] = contract
        return contracts

    def save_state(self):
        """Persist current state to tree-state.json"""
        self.tree_state_path.parent.mkdir(parents=True, exist_ok=True)
        self.tree_state_path.write_text(json.dumps(self.state, indent=2))

    def update_tree(self, produced_artifacts: Set[str]):
        """
        Update tree state based on newly produced artifacts

        Args:
            produced_artifacts: Set of artifact names/patterns that were produced
        """
        # Check each locked skill to see if prerequisites are now satisfied
        new_ready = []
        for skill_name in self.state["locked"]:
            contract = self.contracts.get(skill_name)
            if not contract:
                continue

            # Check if mandatory prerequisites are satisfied
            mandatory_reqs = [
                req["artifact"] for req in contract["requires"] if not req["optional"]
            ]

            # Simple check: see if required artifact exists in produced set
            # (More sophisticated check would verify actual file existence)
            satisfied = all(
                any(
                    self._artifact_matches(req, produced_artifacts)
                    for produced in produced_artifacts
                )
                for req in mandatory_reqs
            )

            if satisfied:
                new_ready.append(skill_name)

        # Move skills from locked to ready
        for skill in new_ready:
            self.state["locked"].remove(skill)
            self.state["ready"].append(skill)

        self.save_state()

    def _artifact_matches(self, required: str, produced_set: Set[str]) -> bool:
        """
        Check if a required artifact pattern matches any produced artifact

        Args:
            required: Required artifact pattern (e.g., 'evidence-map.md', 'materials/')
            produced_set: Set of produced artifact names

        Returns:
            True if match found
        """
        # Simple matching logic (can be enhanced)
        # Check exact match or pattern containment
        for produced in produced_set:
            if required == produced:
                return True
            # Handle patterns like "materials/*" or "materials/"
            if "*" in required:
                pattern = required.replace("*", "")
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
        if skill_name in self.state["unlocked"]:
            self.state["unlocked"].remove(skill_name)
        elif skill_name in self.state["ready"]:
            self.state["ready"].remove(skill_name)

        # Add to completed
        if skill_name not in self.state["completed"]:
            self.state["completed"].append(skill_name)

        self.save_state()

    # Forward dependency edges for progression visualization
    FORWARD_EDGES = [
        ("omr-bootstrap", "omr-collection"),
        ("omr-bootstrap", "omr-idea-note"),
        ("omr-bootstrap", "omr-reconcile"),
        ("omr-collection", "omr-analyze"),
        ("omr-analyze", "omr-decision"),
        ("omr-decision", "omr-evaluation"),
        ("omr-evaluation", "omr-synthesis"),
        ("omr-idea-note", "omr-decision"),
    ]

    # Reverse goal paths (skill → immediate prerequisites)
    REVERSE_PATHS = {
        "omr-synthesis": [
            "omr-collection",
            "omr-analyze",
            "omr-decision",
            "omr-evaluation",
            "omr-synthesis",
        ],
        "omr-evaluation": [
            "omr-collection",
            "omr-analyze",
            "omr-decision",
            "omr-evaluation",
        ],
    }

    def _skill_status(self, skill_name: str) -> str:
        """Return status bucket for a skill: completed|ready|unlocked|locked"""
        for status in ("completed", "ready", "unlocked", "locked"):
            if skill_name in self.state.get(status, []):
                return status
        return "locked"

    def _status_marker(self, status: str) -> str:
        return {
            "completed": "✓",
            "ready": "○",
            "unlocked": "○",
            "locked": "●",
        }.get(status, "●")

    def _skill_label(self, skill_name: str) -> str:
        """Human-readable node label with status marker and lock hints."""
        status = self._skill_status(skill_name)
        marker = self._status_marker(status)
        label = f"{skill_name} {marker}"
        if status == "locked":
            contract = self.contracts.get(skill_name, {})
            missing = [
                req["artifact"]
                for req in contract.get("requires", [])
                if not req.get("optional")
            ]
            if missing:
                hint = ", ".join(missing[:2])
                if len(missing) > 2:
                    hint += "..."
                label = f"{skill_name} ● needs {hint}"
        elif status == "ready":
            contract = self.contracts.get(skill_name, {})
            gates = contract.get("gates", [])
            if gates:
                gate_ids = ", ".join(g["id"] for g in gates)
                label = f"{skill_name} ○ Gate {gate_ids}"
        return label

    def get_visualization(self, reverse: bool = False, format: str = "mermaid") -> str:
        """
        Generate skill tree visualization

        Args:
            reverse: If True, show reverse view (goal-first planning)
            format: 'mermaid' (default) or 'ascii'

        Returns:
            Visualization string (Mermaid fenced block or ASCII art)
        """
        fmt = (format or "mermaid").lower()
        if fmt not in ("mermaid", "ascii"):
            fmt = "mermaid"

        if reverse:
            return (
                self._render_reverse_mermaid()
                if fmt == "mermaid"
                else self._render_reverse_tree()
            )
        return (
            self._render_forward_mermaid()
            if fmt == "mermaid"
            else self._render_forward_tree()
        )

    def _all_known_skills(self) -> List[str]:
        """Ordered skill list for visualization nodes."""
        seen = []
        for skill in (
            "omr-bootstrap",
            "omr-collection",
            "omr-analyze",
            "omr-decision",
            "omr-evaluation",
            "omr-synthesis",
            "omr-idea-note",
            "omr-reconcile",
        ):
            if skill in self.contracts or any(
                skill in self.state.get(s, [])
                for s in ("completed", "ready", "unlocked", "locked")
            ):
                seen.append(skill)
        # Include any extras present in state
        for bucket in ("completed", "ready", "unlocked", "locked"):
            for skill in self.state.get(bucket, []):
                if skill not in seen and skill != "omr-core":
                    seen.append(skill)
        return seen

    def _mermaid_class_defs(self) -> List[str]:
        return [
            "    classDef completed fill:#d4edda,stroke:#28a745,color:#155724",
            "    classDef ready fill:#fff3cd,stroke:#ffc107,color:#856404",
            "    classDef unlocked fill:#d1ecf1,stroke:#17a2b8,color:#0c5460",
            "    classDef locked fill:#e2e3e5,stroke:#6c757d,color:#383d41",
        ]

    def _node_id(self, skill_name: str) -> str:
        return skill_name.replace("-", "_").replace("omr_", "")

    def _render_forward_mermaid(self) -> str:
        """Render forward view as Mermaid flowchart (default)."""
        lines = [
            "📊 Skill Tree Progress (Forward View)",
            "",
            "```mermaid",
            "flowchart TD",
        ]
        lines.extend(self._mermaid_class_defs())
        lines.append("")

        for skill in self._all_known_skills():
            nid = self._node_id(skill)
            status = self._skill_status(skill)
            label = self._skill_label(skill).replace('"', "'")
            lines.append(f'    {nid}["{label}"]:::{status}')

        lines.append("")
        known = set(self._all_known_skills())
        for src, dst in self.FORWARD_EDGES:
            if src in known and dst in known:
                lines.append(f"    {self._node_id(src)} --> {self._node_id(dst)}")

        lines.append("```")
        lines.append("")
        lines.append("Legend: ✓ completed · ○ ready/unlocked · ● locked")
        return "\n".join(lines)

    def _render_reverse_mermaid(self) -> str:
        """Render reverse (goal-first) view as Mermaid flowchart."""
        lines = [
            "🎯 Skill Tree (Reverse View — Goal-First Planning)",
            "",
            "```mermaid",
            "flowchart LR",
        ]
        lines.extend(self._mermaid_class_defs())
        lines.append("")

        goals = ["omr-synthesis", "omr-evaluation"]
        for goal in goals:
            path = self.REVERSE_PATHS.get(goal, [goal])
            for skill in path:
                nid = f"{self._node_id(goal)}_{self._node_id(skill)}"
                status = self._skill_status(skill)
                label = self._skill_label(skill).replace('"', "'")
                lines.append(f'    {nid}["{label}"]:::{status}')
            for a, b in zip(path, path[1:]):
                lines.append(
                    f"    {self._node_id(goal)}_{self._node_id(a)} --> "
                    f"{self._node_id(goal)}_{self._node_id(b)}"
                )
            lines.append("")

        lines.append("```")
        lines.append("")
        lines.append("Goals: omr-synthesis · omr-evaluation")
        lines.append("Legend: ✓ completed · ○ ready/unlocked · ● locked")
        return "\n".join(lines)

    def _render_forward_tree(self) -> str:
        """Render forward view as ASCII (opt-in via --ascii / format=ascii)"""
        lines = []
        lines.append("📊 Skill Tree Progress (Forward View)")
        lines.append("=" * 50)
        lines.append("")

        # Completed skills
        if self.state["completed"]:
            lines.append("✓ Completed Skills:")
            for skill in self.state["completed"]:
                lines.append(f"  [✓] {skill}")
            lines.append("")

        # Unlocked skills (available for invocation)
        if self.state["unlocked"]:
            lines.append("🔓 Unlocked Skills (available):")
            for skill in self.state["unlocked"]:
                lines.append(f"  [○] {skill}")
            lines.append("")

        # Ready skills (prerequisites satisfied)
        if self.state["ready"]:
            lines.append("⏸ Ready Skills (prerequisites satisfied):")
            for skill in self.state["ready"]:
                # Show gate info if applicable
                contract = self.contracts.get(skill)
                gates = contract.get("gates", [])
                gate_info = ""
                if gates:
                    gate_ids = [g["id"] for g in gates]
                    gate_info = f" (Gate: {', '.join(gate_ids)})"
                lines.append(f"  [●] {skill}{gate_info}")
            lines.append("")

        # Locked skills (missing prerequisites)
        if self.state["locked"]:
            lines.append("🔒 Locked Skills (missing prerequisites):")
            for skill in self.state["locked"]:
                contract = self.contracts.get(skill)
                missing = []
                for req in contract.get("requires", []):
                    if not req["optional"]:
                        missing.append(req["artifact"])
                missing_info = f" — needs: {', '.join(missing[:2])}"
                if len(missing) > 2:
                    missing_info += "..."
                lines.append(f"  [●] {skill}{missing_info}")
            lines.append("")

        return "\n".join(lines)

    def _render_reverse_tree(self) -> str:
        """Render reverse view as ASCII (opt-in via --ascii / format=ascii)"""
        lines = []
        lines.append("🎯 Skill Tree (Reverse View — Goal-First Planning)")
        lines.append("=" * 50)
        lines.append("")
        lines.append("Select your goal:")
        lines.append("")

        # List possible goals (skills that produce final outputs)
        goals = ["omr-synthesis", "omr-evaluation"]

        for i, goal in enumerate(goals, 1):
            contract = self.contracts.get(goal)
            produces = contract.get("produces", [])
            produces_desc = produces[0]["description"] if produces else "output"
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
        total_skills = (
            len(self.state["unlocked"])
            + len(self.state["ready"])
            + len(self.state["locked"])
            + len(self.state["completed"])
        )

        return {
            "total_skills": total_skills,
            "completed": len(self.state["completed"]),
            "unlocked": len(self.state["unlocked"]),
            "ready": len(self.state["ready"]),
            "locked": len(self.state["locked"]),
            "progress_percentage": round(
                len(self.state["completed"]) / total_skills * 100, 1
            )
            if total_skills > 0
            else 0,
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
        tree_state_path.write_text(
            json.dumps(
                {
                    "unlocked": [
                        "omr-bootstrap",
                        "omr-collection",
                        "omr-idea-note",
                        "omr-reconcile",
                    ],
                    "ready": [],
                    "locked": [
                        "omr-analyze",
                        "omr-decision",
                        "omr-evaluation",
                        "omr-synthesis",
                    ],
                    "completed": [],
                },
                indent=2,
            )
        )

    tree = SkillTree(tree_state_path, contracts_dir)

    # Flags: --reverse/-r, --ascii, --format mermaid|ascii
    reverse = "--reverse" in sys.argv or "-r" in sys.argv
    fmt = "mermaid"
    if "--ascii" in sys.argv:
        fmt = "ascii"
    if "--format" in sys.argv:
        idx = sys.argv.index("--format")
        if idx + 1 < len(sys.argv):
            fmt = sys.argv[idx + 1]

    print(tree.get_visualization(reverse=reverse, format=fmt))
    print()
    stats = tree.get_progress_stats()
    print(
        f"Progress: {stats['completed']}/{stats['total_skills']} skills completed ({stats['progress_percentage']}%)"
    )


if __name__ == "__main__":
    main()
