#!/usr/bin/env python3
"""
omr-evidence Implementation
Extracts research questions, claims, evidence, gaps from collected materials
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

def extract_evidence(workspace_root: Path, materials_dir: Path = None) -> Dict:
    """
    Extract evidence from collected materials

    Args:
        workspace_root: Project workspace root
        materials_dir: Path to raw materials (default: workspace_root/raw)

    Returns:
        Dict with brief and evidence map
    """
    if materials_dir is None:
        materials_dir = workspace_root / 'raw'

    # Read collected materials
    materials = read_materials(materials_dir)

    if not materials:
        return {
            'status': 'failed',
            'error': 'No materials found in raw/'
        }

    # Extract research questions (from titles, abstracts if available)
    research_questions = extract_questions(materials)

    # Extract evidence claims (simplified - would use LLM in real implementation)
    evidence_claims = extract_claims(materials)

    # Identify gaps
    gaps = identify_gaps(materials, research_questions)

    # Generate research brief
    brief = generate_brief(research_questions, materials)

    # Generate evidence map
    evidence_map = generate_map(evidence_claims, gaps, materials)

    # Write outputs
    docs_dir = workspace_root / 'docs'

    brief_path = docs_dir / 'research-brief.md'
    brief_path.write_text(brief)

    map_path = docs_dir / 'evidence-map.md'
    map_path.write_text(evidence_map)

    # Update skill tree
    update_tree_state(workspace_root)

    return {
        'status': 'success',
        'brief_path': str(brief_path),
        'map_path': str(map_path),
        'questions_found': len(research_questions),
        'claims_extracted': len(evidence_claims),
        'gaps_identified': len(gaps)
    }

def read_materials(materials_dir: Path) -> List[Dict]:
    """
    Read all markdown materials from raw directories

    Args:
        materials_dir: Path to raw materials

    Returns:
        List of material dicts with content and metadata
    """
    materials = []

    # Check each source type directory
    source_types = ['paper', 'web', 'github', 'dataset']

    for source_type in source_types:
        source_dir = materials_dir / source_type

        if not source_dir.exists():
            continue

        for md_file in source_dir.glob('*.md'):
            content = md_file.read_text()

            # Read metadata from index if available
            index_file = materials_dir.parent / 'docs' / 'index' / f'{source_type}s-index.json'

            metadata = {}
            if index_file.exists():
                index_data = json.loads(index_file.read_text())
                for artifact in index_data.get('artifacts', []):
                    if artifact['file_path'] == str(md_file.relative_to(materials_dir.parent)):
                        metadata = artifact
                        break

            materials.append({
                'content': content,
                'metadata': metadata,
                'source_type': source_type,
                'file_path': str(md_file)
            })

    return materials

def extract_questions(materials: List[Dict]) -> List[Dict]:
    """
    Extract research questions from materials

    Simplified: In real implementation, would use LLM for semantic extraction

    Args:
        materials: List of materials

    Returns:
        List of research question dicts
    """
    questions = []

    for material in materials:
        content = material['content']
        metadata = material['metadata']

        # Extract from title (simplified)
        title = metadata.get('title', 'Unknown')

        # Generate question from title (placeholder logic)
        # Real would use LLM to extract explicit research questions
        question = f"What does {title} contribute?"

        questions.append({
            'question_id': f"Q-{len(questions)+1}",
            'question': question,
            'source': metadata.get('file_path', ''),
            'source_type': material['source_type']
        })

    return questions[:5]  # Limit to top 5

def extract_claims(materials: List[Dict]) -> List[Dict]:
    """
    Extract evidence claims from materials

    Simplified: Placeholder - real would use LLM

    Args:
        materials: List of materials

    Returns:
        List of claim dicts
    """
    claims = []

    for i, material in enumerate(materials[:10]):  # Process first 10
        content = material['content']

        # Placeholder: would use LLM to extract claims
        claim = {
            'claim_id': f"C-{i+1}",
            'claim': f"Key finding from {material['metadata'].get('title', 'source')}",
            'evidence_type': material['source_type'],
            'source': material['file_path'],
            'confidence': 'medium'  # Placeholder
        }

        claims.append(claim)

    return claims

def identify_gaps(materials: List[Dict], questions: List[Dict]) -> List[Dict]:
    """
    Identify research gaps

    Args:
        materials: Collected materials
        questions: Research questions

    Returns:
        List of gap dicts
    """
    gaps = []

    # Placeholder gap identification
    gap = {
        'gap_id': 'G-001',
        'gap': 'Limited coverage of [topic]',
        'related_question': questions[0]['question_id'] if questions else '',
        'priority': 'high'
    }

    gaps.append(gap)

    return gaps

def generate_brief(questions: List[Dict], materials: List[Dict]) -> str:
    """
    Generate research brief markdown

    Args:
        questions: Research questions
        materials: Collected materials

    Returns:
        Markdown brief content
    """
    lines = [
        "# Research Brief",
        "",
        f"**Generated**: {datetime.now().isoformat()}",
        "",
        f"**Materials Collected**: {len(materials)} sources",
        "",
        "---",
        "",
        "## Primary Research Question",
        ""
    ]

    if questions:
        primary_question = questions[0]
        lines.append(f"**Question ID**: {primary_question['question_id']}")
        lines.append("")
        lines.append(f"**Question**: {primary_question['question']}")
        lines.append("")
        lines.append(f"**Scope**: Defined by {len(materials)} collected materials")
        lines.append("")
        lines.append("**Context**: Investigation based on collected evidence")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Supporting Questions")
    lines.append("")

    for question in questions[1:]:
        lines.append(f"- **{question['question_id']}**: {question['question']}")
        lines.append(f"  - Source: {question['source_type']}")
        lines.append("")

    lines.append("")
    lines.append("_Generated by omr-evidence_")

    return "\n".join(lines)

def generate_map(claims: List[Dict], gaps: List[Dict], materials: List[Dict]) -> str:
    """
    Generate evidence map markdown

    Args:
        claims: Evidence claims
        gaps: Research gaps
        materials: Collected materials

    Returns:
        Markdown evidence map content
    """
    lines = [
        "# Evidence Map",
        "",
        f"**Generated**: {datetime.now().isoformat()}",
        "",
        f"**Claims Extracted**: {len(claims)}",
        "",
        f"**Gaps Identified**: {len(gaps)}",
        "",
        "---",
        "",
        "## Primary Evidence",
        ""
    ]

    # Group claims by confidence
    for claim in claims:
        lines.append(f"- **{claim['claim_id']}**: {claim['claim']}")
        lines.append(f"  - Type: {claim['evidence_type']}")
        lines.append(f"  - Confidence: {claim['confidence']}")
        lines.append(f"  - Source: {claim['source']}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Research Gaps")
    lines.append("")

    for gap in gaps:
        lines.append(f"- **{gap['gap_id']}**: {gap['gap']}")
        lines.append(f"  - Related Question: {gap['related_question']}")
        lines.append(f"  - Priority: {gap['priority']}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Coverage Analysis")
    lines.append("")
    lines.append(f"- Materials reviewed: {len(materials)}")
    lines.append(f"- Claims extracted: {len(claims)}")
    lines.append(f"- Questions defined: {len(claims)}")
    lines.append(f"- Gaps identified: {len(gaps)}")
    lines.append("")

    lines.append("")
    lines.append("_Generated by omr-evidence_")

    return "\n".join(lines)

def update_tree_state(workspace_root: Path):
    """
    Update skill tree to unlock downstream skills

    Args:
        workspace_root: Project workspace
    """
    tree_state_path = workspace_root / 'skills' / 'tree-state.json'

    if not tree_state_path.exists():
        return

    state = json.loads(tree_state_path.read_text())

    # Mark omr-evidence as completed
    if 'omr-evidence' in state['ready']:
        state['ready'].remove('omr-evidence')
    elif 'omr-evidence' in state['unlocked']:
        state['unlocked'].remove('omr-evidence')

    state['completed'].append('omr-evidence')

    # Unlock omr-research-plan
    if 'omr-research-plan' in state['locked']:
        state['locked'].remove('omr-research-plan')
        state['ready'].append('omr-research-plan')

    tree_state_path.write_text(json.dumps(state, indent=2))

def main():
    """CLI entry point"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: extract_evidence.py <workspace>")
        print("Example: extract_evidence.py /tmp/test-project")
        sys.exit(1)

    workspace = Path(sys.argv[1])

    print("Extracting evidence from collected materials...")
    result = extract_evidence(workspace)

    if result['status'] == 'success':
        print(f"✓ Evidence extraction complete")
        print(f"  Brief: {result['brief_path']}")
        print(f"  Map: {result['map_path']}")
        print(f"  Questions: {result['questions_found']}")
        print(f"  Claims: {result['claims_extracted']}")
        print(f"  Gaps: {result['gaps_identified']}")

        print(f"\n📊 Skill tree updated")
        print(f"  - omr-research-plan [READY]")

    else:
        print(f"✗ Error: {result['error']}")

if __name__ == "__main__":
    main()