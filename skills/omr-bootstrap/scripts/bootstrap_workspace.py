#!/usr/bin/env python3
"""
Workspace Bootstrap Script
Creates standard project directory structure and generates CLAUDE.md
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

    # Create directory structure
    directories = [
        "raw/paper",
        "raw/web",
        "raw/github",
        "raw/dataset",
        "raw/search",
        "raw/failed",
        "docs/index",
        "docs/ideas",
        "docs/archive",
        "docs/survey",
        "docs/report",
        "docs/manuscript",
        "docs/brief",
        "wiki",
        "src",
        "skills/patterns",
        "skills/contracts",
    ]

    created_dirs = []
    for dir_path in directories:
        full_path = workspace_path / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        created_dirs.append(str(full_path))

    # Copy contract files to workspace
    skills_dir = Path(__file__).parent.parent
    contracts_src = skills_dir.parent / "shared" / "contracts"
    contracts_dst = workspace_path / "skills" / "contracts"

    copied_contracts = []
    for contract_file in contracts_src.glob("*.json"):
        dst_file = contracts_dst / contract_file.name
        dst_file.write_text(contract_file.read_text())
        copied_contracts.append(contract_file.name)

    # Initialize skill tree state
    tree_state = {
        "unlocked": ["omr-bootstrap", "omr-collection", "omr-idea-note"],
        "ready": [],
        "locked": ["omr-evidence", "omr-research-plan", "omr-decision",
                   "omr-evaluation", "omr-synthesis", "omr-wiki", "omr-reconcile",
                   "omr-research-archive"],
        "completed": ["omr-bootstrap"]
    }

    tree_state_path = workspace_path / "skills" / "tree-state.json"
    tree_state_path.write_text(json.dumps(tree_state, indent=2))

    # Initialize empty metadata indexes
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
        index_path = workspace_path / "docs" / "index" / index_file
        index_path.write_text(json.dumps({"artifacts": [], "last_updated": datetime.now().isoformat()}, indent=2))
        created_indexes.append(index_file)

    # Generate CLAUDE.md from template
    template_path = skills_dir / "assets" / "CLAUDE.md.template"
    claude_md = generate_claude_md(
        template_path=template_path,
        project_name=project_name,
        research_question=research_question or "Not yet defined",
        tree_state=tree_state
    )

    claude_md_path = workspace_path / "CLAUDE.md"
    claude_md_path.write_text(claude_md)

    return {
        "workspace_path": str(workspace_path),
        "created_directories": len(created_dirs),
        "copied_contracts": len(copied_contracts),
        "created_indexes": len(created_indexes),
        "claude_md_path": str(claude_md_path),
        "tree_state_path": str(tree_state_path)
    }

def generate_claude_md(template_path: Path,
                       project_name: str,
                       research_question: str,
                       tree_state: dict) -> str:
    """Generate CLAUDE.md from template with filled values"""

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
    claude_md = template.replace("{{project_name}}", project_name)
    claude_md = claude_md.replace("{{research_question}}", research_question)
    claude_md = claude_md.replace("{{status}}", "initialized")
    claude_md = claude_md.replace("{{active_pattern}}", "Not yet detected (will emerge after 3+ skill invocations)")
    claude_md = claude_md.replace("{{created_at}}", now)
    claude_md = claude_md.replace("{{last_updated}}", now)
    claude_md = claude_md.replace("{{unlocked_skills}}", unlocked)
    claude_md = claude_md.replace("{{ready_skills}}", ready)
    claude_md = claude_md.replace("{{locked_skills}}", locked)
    claude_md = claude_md.replace("{{completed_skills}}", completed)
    claude_md = claude_md.replace("{{next_steps}}", next_steps)

    return claude_md

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
    print(f"✓ CLAUDE.md generated: {result['claude_md_path']}")
    print(f"✓ Skill tree initialized: {result['tree_state_path']}")
    print()
    print("Next: Start collecting materials with /omr-collection or capture ideas with /omr-idea-note")

if __name__ == "__main__":
    main()