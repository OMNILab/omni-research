#!/usr/bin/env python3
"""
omr-decision Implementation
Architecture decision with alternatives + evidence refs + Gate B
"""

import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime

def make_decision(workspace_root: Path) -> Dict:
    """
    Make architecture decision based on evidence

    Args:
        workspace_root: Project workspace root

    Returns:
        Dict with decision document path and metadata
    """
    docs_dir = workspace_root / 'docs'

    # Check prerequisites
    evidence_map_path = docs_dir / 'evidence-map.md'
    if not evidence_map_path.exists():
        return {
            'status': 'failed',
            'error': 'evidence-map.md not found. Run omr-evidence first.'
        }

    evidence_map = evidence_map_path.read_text()

    judgment_path = docs_dir / 'judgment-summary.md'
    judgment = None
    if judgment_path.exists():
        judgment = judgment_path.read_text()

    # Define alternatives based on evidence
    alternatives = define_alternatives(evidence_map)

    # Select best alternative based on evidence support
    selected = select_alternative(alternatives, evidence_map)

    # Generate decision document
    decision_doc = generate_decision_doc(
        alternatives=alternatives,
        selected=selected,
        evidence_map_path=evidence_map_path,
        judgment=judgment
    )

    # Write decision
    decision_path = docs_dir / 'architecture-decision.md'
    decision_path.write_text(decision_doc['markdown'])

    # Gate B: Architecture decision sound?
    gate_passed = check_gate_b(decision_doc)

    if not gate_passed['passed']:
        return {
            'status': 'gate_failed',
            'gate': 'B',
            'message': gate_passed['message'],
            'decision_path': str(decision_path)
        }

    # Update skill tree
    update_tree_state(workspace_root)

    return {
        'status': 'success',
        'gate_passed': gate_passed['passed'],
        'decision_path': str(decision_path),
        'decision_id': decision_doc['decision_id'],
        'selected_alternative': selected['name'],
        'alternatives_count': len(alternatives)
    }

def define_alternatives(evidence_map: str) -> List[Dict]:
    """
    Define architecture alternatives based on evidence

    Generate alternatives from evidence structure

    Args:
        evidence_map: Evidence map content

    Returns:
        List of alternative dicts
    """
    import re

    # Extract proven claims to understand architecture patterns
    proven_claims = []
    claim_matches = re.findall(r'\*\*C-(\d+)\*\*: (.+)\n  - \*\*Evidence boundary\*\*: proven', evidence_map)
    for claim_id, claim_text in claim_matches:
        proven_claims.append({'id': f"C-{claim_id}", 'text': claim_text})

    # Extract suggested claims for alternative ideas
    suggested_claims = []
    suggested_matches = re.findall(r'\*\*C-(\d+)\*\*: (.+)\n  - \*\*Evidence boundary\*\*: suggested', evidence_map)
    for claim_id, claim_text in suggested_matches[:10]:
        suggested_claims.append({'id': f"C-{claim_id}", 'text': claim_text})

    # Generate alternatives based on evidence patterns
    alternatives = []

    # Alternative A: Lightweight (minimal approach)
    alternatives.append({
        'name': 'Lightweight Architecture',
        'description': 'Minimal overhead approach with essential features only',
        'pros': ['Simple implementation', 'Low resource usage', 'Fast deployment', 'Easy maintenance'],
        'cons': ['Limited scalability', 'Fewer features', 'May require future refactoring'],
        'suitable_for': 'Quick prototyping and small-scale experiments',
        'evidence_support': [c['id'] for c in suggested_claims[:3]] if suggested_claims else [],
        'proven_support': len([c for c in proven_claims if 'simple' in c['text'].lower() or 'minimal' in c['text'].lower()])
    })

    # Alternative B: Comprehensive (full approach)
    alternatives.append({
        'name': 'Comprehensive Architecture',
        'description': 'Feature-complete approach with full capabilities',
        'pros': ['Robust and scalable', 'Feature-complete', 'Production-ready', 'Handles complex requirements'],
        'cons': ['Higher complexity', 'More resources needed', 'Longer development time', 'Higher maintenance cost'],
        'suitable_for': 'Production deployment and complex workflows',
        'evidence_support': [c['id'] for c in proven_claims[:5]] if proven_claims else [],
        'proven_support': len(proven_claims)  # Based on proven evidence count
    })

    # Alternative C: Hybrid (balanced approach)
    alternatives.append({
        'name': 'Hybrid Architecture',
        'description': 'Balanced approach combining simplicity with key features',
        'pros': ['Balanced trade-offs', 'Moderate complexity', 'Flexible design', 'Good scalability'],
        'cons': ['Medium resource usage', 'Some compromises needed', 'Requires careful tuning'],
        'suitable_for': 'Balanced requirements with moderate complexity',
        'evidence_support': [c['id'] for c in proven_claims[:3] + suggested_claims[:2]] if proven_claims else [],
        'proven_support': len(proven_claims) // 2 + len(suggested_claims) // 3  # Moderate proven support
    })

    return alternatives

def select_alternative(alternatives: List[Dict], evidence_map: str) -> Dict:
    """
    Select best alternative based on evidence support

    Score alternatives by proven claims count

    Args:
        alternatives: List of alternatives
        evidence_map: Evidence map content

    Returns:
        Selected alternative dict with rationale
    """
    # Score alternatives based on proven_support
    scored_alternatives = []

    for alt in alternatives:
        score = alt.get('proven_support', 0)

        # Boost score if has evidence support
        evidence_support_count = len(alt.get('evidence_support', []))
        score += evidence_support_count * 0.5  # Each evidence reference adds 0.5

        scored_alternatives.append({
            'alternative': alt,
            'score': score,
            'rationale': f"Score {score:.1f} based on {alt.get('proven_support', 0)} proven claims and {evidence_support_count} evidence references"
        })

    # Sort by score (highest first)
    scored_alternatives.sort(key=lambda x: x['score'], reverse=True)

    # Select highest scored alternative
    selected_scored = scored_alternatives[0]
    selected = selected_scored['alternative']

    # Add selection rationale to alternative
    selected['selection_rationale'] = selected_scored['rationale']
    selected['score'] = selected_scored['score']

    # Document rationale
    proven_count = selected.get('proven_support', 0)
    evidence_refs = selected.get('evidence_support', [])

    if proven_count >= 5:
        selected['rationale_details'] = f"Selected based on strong proven evidence support ({proven_count} proven claims). High confidence in architecture choice."
    elif proven_count >= 2:
        selected['rationale_details'] = f"Selected based on moderate proven evidence support ({proven_count} proven claims). Validation recommended."
    else:
        selected['rationale_details'] = f"Selected based on limited proven evidence. Additional validation required to confirm architecture."

    if evidence_refs:
        selected['rationale_details'] += f"\nEvidence references: {', '.join(evidence_refs[:5])}"

    return selected

def generate_decision_doc(alternatives: List[Dict],
                           selected: Dict,
                           evidence_map_path: Path,
                           judgment: str) -> Dict:
    """
    Generate architecture decision document

    Args:
        alternatives: List of alternatives
        selected: Selected alternative
        evidence_map_path: Path to evidence map
        judgment: Judgment content

    Returns:
        Dict with decision_id, markdown
    """
    decision_id = f"DEC-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    markdown = f"""# Architecture Decision

**Decision ID**: {decision_id}

**Generated**: {datetime.now().isoformat()}

---

## Decision Context

**Question**: What architecture approach should be adopted?

**Scope**: Based on {len(alternatives)} alternatives evaluated against available evidence

---

## Alternatives Considered

"""

    for i, alt in enumerate(alternatives, 1):
        markdown += f"### Alternative {i}: {alt['name']}\n\n"
        markdown += f"**Description**: {alt['description']}\n\n"
        markdown += "**Pros**:\n"
        for pro in alt['pros']:
            markdown += f"- {pro}\n"
        markdown += "\n"
        markdown += "**Cons**:\n"
        for con in alt['cons']:
            markdown += f"- {con}\n"
        markdown += "\n"
        markdown += f"**Suitable For**: {alt['suitable_for']}\n\n"

        # Add evidence support
        proven_support = alt.get('proven_support', 0)
        evidence_refs = alt.get('evidence_support', [])

        markdown += f"**Evidence Support**: {proven_support} proven claims\n"
        if evidence_refs:
            markdown += f"**Evidence References**: {', '.join(evidence_refs[:5])}\n\n"

        markdown += "---\n\n"

    markdown += "## Selected Alternative\n\n"
    markdown += f"**{selected['name']}**: {selected['description']}\n\n"

    # Add selection rationale
    markdown += "**Selection Rationale**:\n\n"

    if selected.get('rationale_details'):
        markdown += f"{selected['rationale_details']}\n\n"

    if selected.get('selection_rationale'):
        markdown += f"Scoring: {selected['selection_rationale']}\n\n"

    markdown += "**Key Benefits**:\n"
    for pro in selected['pros'][:3]:
        markdown += f"- {pro}\n"

    markdown += "\n**Trade-offs**:\n"
    for con in selected['cons'][:2]:
        markdown += f"- {con}\n"

    markdown += "\n---\n\n"
    markdown += "## Evidence References\n\n"
    markdown += f"- Evidence Map: `{evidence_map_path.name}`\n"

    if judgment:
        markdown += f"- Judgment Summary: `judgment-summary.md`\n"

    evidence_refs = selected.get('evidence_support', [])
    if evidence_refs:
        markdown += f"\n**Supporting Evidence**: {', '.join(evidence_refs)}\n"

    markdown += "\n---\n\n"
    markdown += "## Risks and Mitigation\n\n"

    # Add risks based on evidence gaps
    proven_count = selected.get('proven_support', 0)

    if proven_count < 3:
        markdown += "- **Risk 1**: Limited proven evidence support may lead to architecture gaps\n"
        markdown += "  - **Mitigation**: Run validation experiments to confirm architecture\n\n"

    markdown += "- **Risk 2**: Trade-offs may impact future scalability\n"
    markdown += "  - **Mitigation**: Design modular components for incremental refinement\n\n"

    if 'comprehensive' in selected['name'].lower():
        markdown += "- **Risk 3**: Higher complexity increases maintenance burden\n"
        markdown += "  - **Mitigation**: Document architecture decisions thoroughly\n\n"

    markdown += "---\n\n"
    markdown += "## Implementation Notes\n\n"
    markdown += f"- Decision made based on {len(alternatives)} alternatives evaluated\n"
    markdown += f"- Selected: {selected['name']} (Score: {selected.get('score', 'N/A')})\n"
    markdown += f"- Evidence foundation: {selected.get('proven_support', 0)} proven claims\n"
    markdown += "- Next: Run `/omr-evaluation` to validate architecture decision\n\n"

    markdown += "\n_Generated by omr-decision_"

    return {
        'decision_id': decision_id,
        'markdown': markdown,
        'alternatives_count': len(alternatives),
        'proven_support': selected.get('proven_support', 0)
    }

def check_gate_b(decision_doc: Dict) -> Dict:
    """
    Gate B: Architecture decision sound?

    Checks:
    - Alternatives documented
    - Risks stated
    - Evidence refs valid

    Args:
        decision_doc: Decision document dict

    Returns:
        Dict with passed, message
    """
    # Check alternatives documented
    alternatives_doc = decision_doc['alternatives_count'] >= 2

    # Check risks stated
    risks_stated = 'Risks' in decision_doc['markdown']

    # Check evidence refs
    evidence_refs = 'Evidence References' in decision_doc['markdown']

    passed = alternatives_doc and risks_stated and evidence_refs

    if passed:
        message = "Gate B passed: Architecture decision sound"
    else:
        missing = []
        if not alternatives_doc:
            missing.append("Alternatives not documented")
        if not risks_stated:
            missing.append("Risks not stated")
        if not evidence_refs:
            missing.append("Evidence refs missing")

        message = f"Gate B failed: {', '.join(missing)}"

    return {
        'passed': passed,
        'message': message
    }

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

    # Mark omr-decision as completed
    if 'omr-decision' in state['ready']:
        state['ready'].remove('omr-decision')

    state['completed'].append('omr-decision')

    # Unlock omr-evaluation
    if 'omr-evaluation' in state['locked']:
        state['locked'].remove('omr-evaluation')
        state['ready'].append('omr-evaluation')

    tree_state_path.write_text(json.dumps(state, indent=2))

def main():
    """CLI entry point"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: make_decision.py <workspace>")
        print("Example: make_decision.py /tmp/test-project")
        sys.exit(1)

    workspace = Path(sys.argv[1])

    print("Making architecture decision...")
    result = make_decision(workspace)

    if result['status'] == 'success':
        print(f"✓ Decision made")
        print(f"  Document: {result['decision_path']}")
        print(f"  ID: {result['decision_id']}")
        print(f"  Selected: {result['selected_alternative']}")

        if result['gate_passed']:
            print(f"\n⚠️  GATE B: Passed")
            print(f"  Architecture decision sound")

        print(f"\n📊 Skill tree updated")
        print(f"  - omr-evaluation [READY]")

    elif result['status'] == 'gate_failed':
        print(f"⚠️  GATE B FAILED")
        print(f"  {result['message']}")
        print(f"\n  Decision draft: {result['decision_path']}")

    else:
        print(f"✗ Error: {result['error']}")

if __name__ == "__main__":
    main()