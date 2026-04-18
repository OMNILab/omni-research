#!/usr/bin/env python3
"""
omr-reconcile Implementation
Iteration support when new evidence arrives
"""

import json
import shutil
from pathlib import Path
from typing import Dict
from datetime import datetime

def reconcile_evidence(workspace_root: Path) -> Dict:
    """
    Reconcile existing artifacts when new evidence arrives

    Archives old versions and re-runs evidence extraction to update state

    Args:
        workspace_root: Project workspace

    Returns:
        Dict with reconciliation status
    """
    docs_dir = workspace_root / 'docs'
    archive_dir = docs_dir / 'archive'
    raw_dir = workspace_root / 'raw'

    # Check existing artifacts
    existing_artifacts = [
        docs_dir / 'research-brief.md',
        docs_dir / 'evidence-map.md',
        docs_dir / 'judgment-summary.md',
        docs_dir / 'research-plan.md',
        docs_dir / 'architecture-decision.md',
        docs_dir / 'experiment-spec.md',
        docs_dir / 'evaluation-report.md'
    ]

    artifacts_to_reconcile = [a for a in existing_artifacts if a.exists()]

    if not artifacts_to_reconcile:
        return {
            'status': 'no_artifacts',
            'message': 'No existing artifacts to reconcile'
        }

    # Step 1: Archive previous versions
    archive_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    archive_session_dir = archive_dir / f'reconciliation-{timestamp}'
    archive_session_dir.mkdir(parents=True)

    archived_files = []
    for artifact in artifacts_to_reconcile:
        archived_path = archive_session_dir / artifact.name
        shutil.copy2(artifact, archived_path)
        archived_files.append(artifact.name)

    # Create archive metadata
    archive_metadata = {
        'archive_id': f'reconciliation-{timestamp}',
        'created_at': datetime.now().isoformat(),
        'reason': 'Evidence reconciliation triggered',
        'archived_files': archived_files,
        'total_files': len(archived_files)
    }

    metadata_path = archive_session_dir / 'RECONCILIATION-METADATA.json'
    metadata_path.write_text(json.dumps(archive_metadata, indent=2))

    # Step 2: Check if new materials exist in raw/
    new_materials = False
    for subdir in ['paper', 'web', 'github', 'dataset']:
        subdir_path = raw_dir / subdir
        if subdir_path.exists():
            # Check if directory has files
            if any(subdir_path.glob('*.md')):
                new_materials = True
                break

    # Step 3: Re-run evidence extraction if new materials
    reconciliation_actions = []

    if new_materials:
        # Call omr-evidence skill to re-extract
        try:
            import subprocess
            evidence_script = workspace_root.parent.parent / 'skills' / 'omr-evidence' / 'extract_evidence.py'

            if evidence_script.exists():
                result = subprocess.run(
                    ['python3', str(evidence_script), str(workspace_root)],
                    capture_output=True,
                    text=True,
                    timeout=60
                )

                if result.returncode == 0:
                    reconciliation_actions.append('evidence-extraction-updated')
                else:
                    reconciliation_actions.append(f'evidence-extraction-failed: {result.stderr}')
            else:
                reconciliation_actions.append('evidence-script-not-found')

        except Exception as e:
            reconciliation_actions.append(f'evidence-extraction-error: {str(e)}')

    # Step 4: Generate reconciliation report
    report = generate_reconciliation_report(
        archived_files=archived_files,
        actions=reconciliation_actions,
        new_materials=new_materials
    )

    report_path = archive_session_dir / 'RECONCILIATION-REPORT.md'
    report_path.write_text(report)

    # Step 5: Update skill tree
    update_tree_state(workspace_root)

    # Step 6: Create traceability update note
    traceability_note = create_traceability_update_note(archived_files)
    traceability_path = docs_dir / 'index' / 'reconciliation-log.md'
    traceability_path.parent.mkdir(parents=True, exist_ok=True)

    if traceability_path.exists():
        existing_log = traceability_path.read_text()
        traceability_path.write_text(existing_log + "\n\n" + traceability_note)
    else:
        traceability_path.write_text(traceability_note)

    return {
        'status': 'success',
        'archived_dir': str(archive_session_dir),
        'archived_files': len(archived_files),
        'actions': reconciliation_actions,
        'new_materials': new_materials,
        'message': f'Archived {len(archived_files)} previous versions, reconciliation complete'
    }

def generate_reconciliation_report(archived_files: list, actions: list, new_materials: bool) -> str:
    """Generate reconciliation report"""

    actions_text = "\n".join([f"- {action}" for action in actions]) if actions else "- No re-extraction performed"

    return f"""# Reconciliation Report

**Generated**: {datetime.now().isoformat()}

## Summary

Evidence reconciliation triggered to update research state.

## Archived Files

{len(archived_files)} files archived:

{chr(10).join([f"- {file}" for file in archived_files])}

## Actions Performed

{actions_text}

## New Materials

**Detected**: {'Yes' if new_materials else 'No'}

{'Evidence extraction re-run to incorporate new materials.' if new_materials else 'No new materials detected, archived existing state only.'}

## Next Steps

- Review updated evidence map
- Check if judgment summary needs revision
- Update affected decisions if evidence boundaries changed

---
_Generated by omr-reconcile_"""

def create_traceability_update_note(archived_files: list) -> str:
    """Create traceability update note"""

    return f"""## Reconciliation Entry - {datetime.now().isoformat()}

**Archived files**: {len(archived_files)}

**Files**: {', '.join(archived_files)}

**Note**: Previous versions preserved in archive directory for rollback if needed.

---"""

def update_tree_state(workspace_root: Path):
    """Update skill tree after reconciliation"""
    tree_state_path = workspace_root / 'skills' / 'tree-state.json'

    if not tree_state_path.exists():
        return

    state = json.loads(tree_state_path.read_text())

    # Mark omr-reconcile as completed
    state['completed'].append('omr-reconcile')

    tree_state_path.write_text(json.dumps(state, indent=2))

def main():
    """CLI entry point"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: reconcile_evidence.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])

    print("Reconciling existing evidence...")
    result = reconcile_evidence(workspace)

    if result['status'] == 'success':
        print(f"✓ Reconciliation complete")
        print(f"  Archived: {result['archived_dir']}")
        print(f"  Files: {result['archived_files']}")
        print(f"\n  {result['message']}")

    else:
        print(f"  {result['message']}")

if __name__ == "__main__":
    main()