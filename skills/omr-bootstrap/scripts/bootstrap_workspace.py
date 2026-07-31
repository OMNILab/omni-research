#!/usr/bin/env python3
"""
Workspace Bootstrap Script

Creates only the minimal workspace files required at init:
  - AGENTS.md
  - .omr/tree-state.json

Content directories (materials/, docs/, wiki/, src/, ...) are created on demand
by the skills that write into them.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


def _write_text(path: Path, content: str) -> Path:
    """Write a text file, creating parent directories only when needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return path


def create_workspace(project_name: str,
                     research_question: Optional[str] = None,
                     output_dir: Path = None) -> dict:
    """
    Initialize a minimal omr research workspace.

    Args:
        project_name: Name of the research project
        research_question: Optional research question to document
        output_dir: Where to create workspace (defaults to current directory)

    Returns:
        Dict with created paths and metadata
    """
    if output_dir is None:
        output_dir = Path.cwd()

    workspace_path = output_dir / project_name
    skills_dir = Path(__file__).parent.parent

    tree_state = {
        "unlocked": ["omr-bootstrap", "omr-collection", "omr-idea-note", "omr-reconcile"],
        "ready": [],
        "locked": ["omr-analyze", "omr-decision",
                   "omr-evaluation", "omr-synthesis"],
        "completed": ["omr-bootstrap"]
    }

    tree_state_path = _write_text(
        workspace_path / ".omr" / "tree-state.json",
        json.dumps(tree_state, indent=2),
    )

    template_path = skills_dir / "assets" / "AGENTS.md.template"
    agents_md = generate_agents_md(
        template_path=template_path,
        project_name=project_name,
        research_question=research_question or "Not yet defined",
        tree_state=tree_state,
    )
    agents_md_path = _write_text(workspace_path / "AGENTS.md", agents_md)

    return {
        "workspace_path": str(workspace_path),
        "agents_md_path": str(agents_md_path),
        "tree_state_path": str(tree_state_path),
    }


def generate_agents_md(template_path: Path,
                       project_name: str,
                       research_question: str,
                       tree_state: dict) -> str:
    """Generate AGENTS.md from template with filled values"""

    template = template_path.read_text()
    now = datetime.now().isoformat()

    unlocked = "\n".join([f"- `{skill}`" for skill in tree_state['unlocked']])
    ready = "\n".join([f"- `{skill}`" for skill in tree_state['ready']]) if tree_state['ready'] else "None"
    locked = "\n".join([f"- `{skill}`" for skill in tree_state['locked']])
    completed = "\n".join([f"- `{skill}`" for skill in tree_state['completed']])

    next_steps = """
Since this is a new project, here are recommended starting points:

1. **If you have papers to collect**: Start with `/omr-collection` to gather materials
   Example: `/omr-collection "https://arxiv.org/abs/2402.12345"`

2. **If you have an idea to explore**: Start with `/omr-idea-note` to capture your insight
   Example: `/omr-idea-note "Hybrid memory architecture combining vector and graph approaches"`

3. **If you have a decision to validate**: Start with `/omr-decision` to document your architecture stance
   Example: `/omr-decision` (will require evidence later)

4. **If you have a hypothesis to test**: Start with `/omr-evaluation` to build and test
   Example: `/omr-evaluation` (Experiment-First pattern, no prior decision required)

5. **If you're exploring**: No specific goal — invoke any unlocked skill and the pattern will emerge
"""

    agents_md = template.replace("{{project_name}}", project_name)
    agents_md = agents_md.replace("{{research_question}}", research_question)
    agents_md = agents_md.replace("{{status}}", "initialized")
    agents_md = agents_md.replace("{{active_pattern}}", "Not yet detected (will emerge after 3+ skill invocations)")
    agents_md = agents_md.replace("{{created_at}}", now)
    agents_md = agents_md.replace("{{last_updated}}", now)
    agents_md = agents_md.replace("{{unlocked_skills}}", unlocked)
    agents_md = agents_md.replace("{{ready_skills}}", ready)
    agents_md = agents_md.replace("{{locked_skills}}", locked)
    agents_md = agents_md.replace("{{completed_skills}}", completed)
    agents_md = agents_md.replace("{{next_steps}}", next_steps)

    return agents_md


def main():
    """CLI entry point for bootstrap script"""
    if len(sys.argv) < 2:
        print("Usage: bootstrap_workspace.py <project-name> [research-question]")
        print("Example: bootstrap_workspace.py agent-memory-survey 'How do AI agents manage memory?'")
        sys.exit(1)

    project_name = sys.argv[1]
    research_question = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"Creating workspace: {project_name}")
    if research_question:
        print(f"Research question: {research_question}")
    print()

    result = create_workspace(project_name, research_question)

    print("✓ Workspace created successfully")
    print(f"  Path: {result['workspace_path']}")
    print(f"  AGENTS.md: {result['agents_md_path']}")
    print(f"  Tree state: {result['tree_state_path']}")
    print()
    print("Directories such as materials/, docs/, wiki/, and src/ are created on demand")
    print("by skills when they first write content.")
    print()
    print("Next: Start collecting materials with /omr-collection or capture ideas with /omr-idea-note")


if __name__ == "__main__":
    main()
