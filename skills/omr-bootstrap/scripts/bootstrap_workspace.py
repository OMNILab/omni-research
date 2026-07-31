#!/usr/bin/env python3
"""
Workspace Bootstrap Script
Initializes workspace state files and generates AGENTS.md.

Directories are created on demand: rather than pre-creating a fixed set of
empty folders, each write ensures its own parent directories exist. Content
subdirectories (raw/, docs/ideas, docs/survey, wiki, src, ...) are created
by the skills that actually write into them, not by bootstrap.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

def create_workspace(project_name: str,
                     research_question: Optional[str] = None,
                     output_dir: Path = None) -> dict:
    """
    Create standard workspace structure for omr research project

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

    def write_json(path: Path, payload: dict) -> Path:
        """Write JSON, auto-creating parent directories on demand.

        This replaces the previous approach of pre-creating a fixed set of
        empty directories. Only directories that actually receive content
        at bootstrap time are created here; the content subdirectories
        (raw/papers, docs/ideas, wiki, src, etc.) are created by the skills
        that write into them when first needed.
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2))
        return path

    # Static contracts and built-in patterns stay in the installed omr-core
    # skill. Only mutable, workspace-specific OMR state belongs in .omr/.
    skills_dir = Path(__file__).parent.parent
    copied_contracts = []

    # Initialize skill tree state (creates .omr/ on demand)
    tree_state = {
        "unlocked": ["omr-bootstrap", "omr-collection", "omr-idea-note", "omr-reconcile"],
        "ready": [],
        "locked": ["omr-analyze", "omr-decision",
                   "omr-evaluation", "omr-synthesis"],
        "completed": ["omr-bootstrap"]
    }

    tree_state_path = write_json(
        workspace_path / ".omr" / "tree-state.json",
        tree_state,
    )

    # Initialize empty metadata indexes (creates docs/index/ on demand)
    index_files = [
        "papers-index.json",
        "blogs-index.json",
        "repos-index.json",
        "datasets-index.json",
        "search-queries-index.json",
        "failed-index.json"
    ]

    created_indexes = []
    for index_file in index_files:
        write_json(
            workspace_path / "docs" / "index" / index_file,
            {"artifacts": [], "last_updated": datetime.now().isoformat()},
        )
        created_indexes.append(index_file)

    # Generate AGENTS.md from template (creates workspace root on demand)
    template_path = skills_dir / "assets" / "AGENTS.md.template"
    agents_md = generate_agents_md(
        template_path=template_path,
        project_name=project_name,
        research_question=research_question or "Not yet defined",
        tree_state=tree_state
    )

    agents_md_path = workspace_path / "AGENTS.md"
    agents_md_path.parent.mkdir(parents=True, exist_ok=True)
    agents_md_path.write_text(agents_md)

    return {
        "workspace_path": str(workspace_path),
        "created_directories": 0,
        "copied_contracts": len(copied_contracts),
        "created_indexes": len(created_indexes),
        "agents_md_path": str(agents_md_path),
        "tree_state_path": str(tree_state_path)
    }

def generate_agents_md(template_path: Path,
                       project_name: str,
                       research_question: str,
                       tree_state: dict) -> str:
    """Generate AGENTS.md from template with filled values"""

    template = template_path.read_text()
    now = datetime.now().isoformat()

    # Format skill lists
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

    # Replace template placeholders
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
    print(f"  Directories: {result['created_directories']}")
    print(f"  Contracts: {result['copied_contracts']}")
    print(f"  Indexes: {result['created_indexes']}")
    print()
    print(f"✓ AGENTS.md generated: {result['agents_md_path']}")
    print(f"✓ Skill tree initialized: {result['tree_state_path']}")
    print()
    print("Next: Start collecting materials with /omr-collection or capture ideas with /omr-idea-note")

if __name__ == "__main__":
    main()