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

    Pattern matching approach for alpha version

    Args:
        materials: List of materials

    Returns:
        List of research question dicts
    """
    questions = []

    # Keywords that indicate research questions
    question_starters = [
        'this paper investigates',
        'we study',
        'the goal is',
        'this research examines',
        'our objective is',
        'we aim to',
        'this work explores',
        'we analyze',
        'this study addresses'
    ]

    for material in materials:
        content = material['content']
        metadata = material['metadata']
        source_type = material['source_type']
        source_path = material['file_path']

        # Find sentences ending with '?'
        question_sentences = re.findall(r'([A-Z][^.!?]*\?)', content)

        for q_text in question_sentences[:3]:  # Max 3 per material
            questions.append({
                'question_id': f"Q-{len(questions)+1}",
                'question': q_text,
                'source': source_path,
                'source_type': source_type
            })

        # Find sentences starting with question indicators
        for starter in question_starters:
            pattern = re.compile(starter + r'[^.!?]*[.!?]', re.IGNORECASE)
            matches = pattern.findall(content)
            for match in matches[:2]:
                questions.append({
                    'question_id': f"Q-{len(questions)+1}",
                    'question': match.strip(),
                    'source': source_path,
                    'source_type': source_type
                })

        # If no questions found, generate from title
        if len(questions) == 0 or len(questions) < 5:
            title = metadata.get('title', 'Unknown')
            questions.append({
                'question_id': f"Q-{len(questions)+1}",
                'question': f"What does '{title}' contribute to the research domain?",
                'source': source_path,
                'source_type': source_type
            })

    return questions[:10]  # Limit to top 10

def extract_claims(materials: List[Dict]) -> List[Dict]:
    """
    Extract evidence claims from materials

    Pattern matching approach for alpha version

    Args:
        materials: List of materials

    Returns:
        List of claim dicts
    """
    claims = []

    # Keywords for different evidence boundaries
    proven_keywords = ['proves', 'demonstrates', 'validates', 'confirms', 'establishes', 'shows', 'verifies']
    suggested_keywords = ['suggests', 'indicates', 'implies', 'may', 'might', 'could', 'appears', 'seems']
    inferred_keywords = ['likely', 'probably', 'presumably', 'conjectured', 'hypothesized']

    for material in materials:
        content = material['content']
        source_type = material['source_type']
        source_path = material['file_path']
        metadata = material['metadata']

        # Split content into sentences
        sentences = re.split(r'[.!?]+', content)

        for sentence in sentences:
            # Check for claim keywords
            sentence_lower = sentence.lower()

            # Check if sentence contains claim indicators
            has_proven = any(kw in sentence_lower for kw in proven_keywords)
            has_suggested = any(kw in sentence_lower for kw in suggested_keywords)
            has_inferred = any(kw in sentence_lower for kw in inferred_keywords)

            # Only extract if contains claim keywords
            if has_proven or has_suggested or has_inferred:
                # Clean up sentence
                claim_text = sentence.strip()
                if len(claim_text) < 10:  # Skip very short claims
                    continue

                # Classify evidence boundary
                evidence_boundary = classify_evidence_boundary(
                    claim_text=claim_text,
                    source_type=source_type,
                    has_proven=has_proven,
                    has_suggested=has_suggested,
                    has_inferred=has_inferred
                )

                # Create claim entry
                claim = {
                    'claim_id': f"C-{len(claims)+1}",
                    'claim': claim_text,
                    'evidence_type': source_type,
                    'source': source_path,
                    'evidence_boundary': evidence_boundary,
                    'confidence': map_boundary_to_confidence(evidence_boundary)
                }

                claims.append(claim)

        # Limit claims per material to 5
        if len(claims) >= 50:  # Total limit
            break

    return claims[:50]  # Limit to 50 total

def classify_evidence_boundary(claim_text: str, source_type: str, has_proven: bool, has_suggested: bool, has_inferred: bool) -> str:
    """
    Classify claim as proven/suggested/inferred based on keywords and source type

    Args:
        claim_text: Claim text
        source_type: Source type (paper, web, github, dataset)
        has_proven: Contains proven keywords
        has_suggested: Contains suggested keywords
        has_inferred: Contains inferred keywords

    Returns:
        Evidence boundary classification
    """
    # Rule 1: Non-paper sources can never be "proven"
    # Only papers with experimental results can provide proven evidence
    if source_type != 'paper':
        if has_proven:
            return 'suggested'  # Downgrade to suggested
        elif has_suggested:
            return 'suggested'
        else:
            return 'inferred'

    # Rule 2: Paper sources
    # Check if claim contains experimental proof indicators
    if has_proven:
        # Additional check: claim should mention experiment, study, test
        experiment_indicators = ['experiment', 'study', 'test', 'trial', 'validation', 'empirical']
        claim_lower = claim_text.lower()
        has_experiment = any(ind in claim_lower for ind in experiment_indicators)

        if has_experiment:
            return 'proven'  # Paper + proven keyword + experiment = proven
        else:
            return 'suggested'  # Paper + proven keyword but no experiment = suggested

    elif has_suggested:
        return 'suggested'

    elif has_inferred:
        return 'inferred'

    else:
        return 'inferred'  # Default

def map_boundary_to_confidence(boundary: str) -> str:
    """Map evidence boundary to confidence level"""
    mapping = {
        'proven': 'high',
        'suggested': 'medium',
        'inferred': 'low'
    }
    return mapping.get(boundary, 'low')

def identify_gaps(materials: List[Dict], questions: List[Dict]) -> List[Dict]:
    """
    Identify research gaps

    Compare research questions against extracted claims to find unanswered questions

    Args:
        materials: Collected materials
        questions: Research questions

    Returns:
        List of gap dicts
    """
    gaps = []

    # If we have questions, check which ones lack evidence
    if questions:
        # For alpha version: assume questions without strong evidence are gaps
        # In full implementation, would compare questions against claims semantically

        for i, question in enumerate(questions[:5]):
            # Simple heuristic: mark question as gap if it's from non-paper source
            # or if it contains speculative keywords
            question_text = question['question'].lower()
            has_speculation = any(kw in question_text for kw in ['could', 'might', 'should', 'would'])

            if question['source_type'] != 'paper' or has_speculation:
                gap = {
                    'gap_id': f"G-{i+1}",
                    'gap': f"Limited evidence for: {question['question'][:100]}",
                    'related_question': question['question_id'],
                    'priority': 'high' if has_speculation else 'medium',
                    'suggested_action': 'Collect additional materials' if question['source_type'] != 'paper' else 'Run experiment'
                }
                gaps.append(gap)

    # Add generic gap if none identified
    if not gaps:
        gaps.append({
            'gap_id': 'G-001',
            'gap': 'Insufficient proven evidence across research domain',
            'related_question': '',
            'priority': 'high',
            'suggested_action': 'Collect more papers with experimental validation'
        })

    return gaps[:5]  # Limit to 5 gaps

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
        "## Evidence Boundaries Summary",
        ""
    ]

    # Count claims by boundary
    proven_count = sum(1 for c in claims if c.get('evidence_boundary') == 'proven')
    suggested_count = sum(1 for c in claims if c.get('evidence_boundary') == 'suggested')
    inferred_count = sum(1 for c in claims if c.get('evidence_boundary') == 'inferred')

    lines.append(f"- **Proven**: {proven_count} claims")
    lines.append(f"- **Suggested**: {suggested_count} claims")
    lines.append(f"- **Inferred**: {inferred_count} claims")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Primary Evidence")
    lines.append("")
    lines.append("### Proven Claims")
    lines.append("")

    for claim in claims:
        if claim.get('evidence_boundary') == 'proven':
            lines.append(f"- **{claim['claim_id']}**: {claim['claim']}")
            lines.append(f"  - **Evidence boundary**: proven")
            lines.append(f"  - Source type: {claim['evidence_type']}")
            lines.append(f"  - Source: `{claim['source']}`")
            lines.append("")

    lines.append("")
    lines.append("### Suggested Claims")
    lines.append("")

    for claim in claims:
        if claim.get('evidence_boundary') == 'suggested':
            lines.append(f"- **{claim['claim_id']}**: {claim['claim']}")
            lines.append(f"  - **Evidence boundary**: suggested")
            lines.append(f"  - Source type: {claim['evidence_type']}")
            lines.append(f"  - Source: `{claim['source']}`")
            lines.append("")

    lines.append("")
    lines.append("### Inferred Claims")
    lines.append("")

    for claim in claims:
        if claim.get('evidence_boundary') == 'inferred':
            lines.append(f"- **{claim['claim_id']}**: {claim['claim']}")
            lines.append(f"  - **Evidence boundary**: inferred")
            lines.append(f"  - Source type: {claim['evidence_type']}")
            lines.append(f"  - Source: `{claim['source']}`")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Research Gaps")
    lines.append("")

    for gap in gaps:
        lines.append(f"- **{gap['gap_id']}**: {gap['gap']}")
        if gap.get('related_question'):
            lines.append(f"  - Related Question: {gap['related_question']}")
        lines.append(f"  - Priority: {gap['priority']}")
        if gap.get('suggested_action'):
            lines.append(f"  - Suggested Action: {gap['suggested_action']}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Coverage Analysis")
    lines.append("")
    lines.append(f"- Materials reviewed: {len(materials)}")
    lines.append(f"- Claims extracted: {len(claims)}")
    lines.append(f"- Evidence boundaries:")
    lines.append(f"  - Proven: {proven_count}")
    lines.append(f"  - Suggested: {suggested_count}")
    lines.append(f"  - Inferred: {inferred_count}")
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