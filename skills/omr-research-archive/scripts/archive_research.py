#!/usr/bin/env python3
"""
omr-research-archive Implementation
Creates timestamped snapshots of research progress
"""

import json
import shutil
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List

def archive_research(workspace_root: Path) -> Dict:
    """
    Create snapshot of current research state

    Args:
        workspace_root: Project workspace

    Returns:
        Dict with archive path and metadata
    """
    docs_dir = workspace_root / 'docs'
    archive_dir = docs_dir / 'archive'
    archive_dir.mkdir(parents=True, exist_ok=True)

    # Generate timestamp
    timestamp = datetime.now().strftime('%Y%m%dT%H%M%S')
    archive_id = f"snapshot-{timestamp}"

    # Create archive directory
    archive_session = archive_dir / archive_id
    archive_session.mkdir(parents=True)

    # Collect artifacts
    artifacts = collect_artifacts(docs_dir)

    # Copy to archive
    copied_files = []
    for artifact in artifacts:
        try:
            if artifact.is_file():
                dst = archive_session / artifact.name
                shutil.copy2(artifact, dst)
                copied_files.append(artifact.name)
            elif artifact.is_dir():
                dst = archive_session / artifact.name
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(artifact, dst)
                copied_files.append(f"{artifact.name}/")
        except Exception as e:
            print(f"Warning: Failed to copy {artifact}: {e}")

    # Generate metadata
    metadata = generate_archive_metadata(
        archive_id=archive_id,
        workspace_root=workspace_root,
        copied_files=copied_files
    )

    metadata_path = archive_session / 'METADATA.json'
    metadata_path.write_text(json.dumps(metadata, indent=2))

    # Generate summary report
    summary_path = archive_session / 'SUMMARY.md'
    summary_text = generate_summary_report(metadata)
    summary_path.write_text(summary_text)

    return {
        'status': 'success',
        'archive_path': str(archive_session),
        'metadata_path': str(metadata_path),
        'summary_path': str(summary_path),
        'artifacts_archived': len(copied_files)
    }

def collect_artifacts(docs_dir: Path) -> List[Path]:
    """Collect all research artifacts"""
    artifacts = []

    # Collect docs subdirectories
    subdirs = ['survey', 'report', 'manuscript', 'brief', 'plans', 'ideas', 'index']

    for subdir in subdirs:
        subdir_path = docs_dir / subdir
        if subdir_path.exists() and subdir_path.is_dir():
            # Check if directory has content
            if any(subdir_path.iterdir()):
                artifacts.append(subdir_path)

    # Collect key files in docs root
    key_files = [
        'research-brief.md',
        'evidence-map.md',
        'judgment-summary.md',
        'research-plan.md',
        'architecture-decision.md',
        'experiment-spec.md',
        'evaluation-report.md'
    ]

    for filename in key_files:
        file_path = docs_dir / filename
        if file_path.exists():
            artifacts.append(file_path)

    return artifacts

def generate_archive_metadata(archive_id: str, workspace_root: Path, copied_files: list) -> Dict:
    """Generate archive metadata JSON"""

    # Read tree state
    tree_state_path = workspace_root / 'skills' / 'tree-state.json'
    tree_state = {}
    if tree_state_path.exists():
        try:
            tree_state = json.loads(tree_state_path.read_text())
        except Exception as e:
            print(f"Warning: Failed to read tree state: {e}")

    # Read pattern config
    pattern_config_path = workspace_root / 'skills' / 'pattern-config.json'
    pattern_config = {}
    if pattern_config_path.exists():
        try:
            pattern_config = json.loads(pattern_config_path.read_text())
        except Exception as e:
            print(f"Warning: Failed to read pattern config: {e}")

    # Count evidence claims
    evidence_map_path = workspace_root / 'docs' / 'evidence-map.md'
    claims_count = 0
    if evidence_map_path.exists():
        try:
            content = evidence_map_path.read_text()
            # Count claim markers like **C-123**
            claims_count = content.count('**C-')
        except Exception as e:
            print(f"Warning: Failed to read evidence map: {e}")

    # Count raw materials
    raw_dir = workspace_root / 'raw'
    raw_count = 0
    if raw_dir.exists():
        for subdir in ['paper', 'web', 'github', 'dataset']:
            subdir_path = raw_dir / subdir
            if subdir_path.exists():
                raw_count += len(list(subdir_path.glob('*.md')))

    return {
        'archive_id': archive_id,
        'created_at': datetime.now().isoformat(),
        'artifacts_archived': copied_files,
        'total_files': len(copied_files),
        'skill_tree_state': tree_state,
        'pattern_detected': pattern_config.get('pattern_detected', 'unknown'),
        'research_progress': {
            'claims_count': claims_count,
            'raw_materials_count': raw_count,
            'skills_completed': len(tree_state.get('completed', [])),
            'skills_locked': len(tree_state.get('locked', [])),
            'skills_ready': len(tree_state.get('ready', []))
        },
        'workspace_path': str(workspace_root)
    }

def generate_summary_report(metadata: Dict) -> str:
    """Generate human-readable summary markdown"""

    archive_id = metadata['archive_id']
    created_at = metadata['created_at']
    artifacts = metadata['artifacts_archived']
    progress = metadata['research_progress']
    tree_state = metadata.get('skill_tree_state', {})

    summary = f"""# Research Archive: {archive_id}

**Created**: {created_at}

---

## Artifacts Archived

Total files: {len(artifacts)}

{format_artifact_list(artifacts)}

---

## Research Progress

- **Evidence claims**: {progress.get('claims_count', 0)}
- **Raw materials**: {progress.get('raw_materials_count', 0)}
- **Skills completed**: {progress.get('skills_completed', 0)}
- **Skills ready**: {progress.get('skills_ready', 0)}
- **Skills locked**: {progress.get('skills_locked', 0)}

---

## Skill Tree State

**Completed**: {', '.join(tree_state.get('completed', []))}

**Ready**: {', '.join(tree_state.get('ready', [])) if tree_state.get('ready') else 'None'}

**Locked**: {', '.join(tree_state.get('locked', [])) if tree_state.get('locked') else 'None'}

---

## Pattern Detected

{metadata.get('pattern_detected', 'unknown')}

---

_Generated by omr-research-archive_
"""

    return summary

def format_artifact_list(artifacts: List[str]) -> str:
    """Format artifact list for markdown"""
    lines = []
    for artifact in artifacts:
        if artifact.endswith('/'):
            lines.append(f"- 📁 {artifact}")
        else:
            lines.append(f"- 📄 {artifact}")
    return '\n'.join(lines)

def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: archive_research.py <workspace>")
        print("Example: archive_research.py /path/to/workspace")
        sys.exit(1)

    workspace = Path(sys.argv[1])

    print(f"Archiving research progress...")
    result = archive_research(workspace)

    print(f"✓ Archive created")
    print(f"  Path: {result['archive_path']}")
    print(f"  Metadata: {result['metadata_path']}")
    print(f"  Summary: {result['summary_path']}")
    print(f"  Artifacts: {result['artifacts_archived']}")

if __name__ == "__main__":
    main()