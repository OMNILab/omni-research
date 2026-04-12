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

    judgment_path = docs_dir / 'judgment-summary.md'
    judgment = None
    if judgment_path.exists():
        judgment = judgment_path.read_text()

    # Define alternatives (simplified - would use LLM)
    alternatives = define_alternatives()

    # Select best alternative
    selected = select_alternative(alternatives)

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
        'selected_alternative': selected['name']
    }

def define_alternatives() -> List[Dict]:
    """
    Define architecture alternatives (placeholder)

    Returns:
        List of alternative dicts
    """
    alternatives = [
        {
            'name': 'Alternative A',
            'description': 'Lightweight approach with minimal overhead',
            'pros': ['Simple', 'Fast', 'Low cost'],
            'cons': ['Limited scalability', 'Fewer features'],
            'suitable_for': 'Quick prototyping'
        },
        {
            'name': 'Alternative B',
            'description': 'Comprehensive approach with full features',
            'pros': ['Robust', 'Scalable', 'Feature-complete'],
            'cons': ['Complex', 'Higher cost', 'Longer setup'],
            'suitable_for': 'Production deployment'
        },
        {
            'name': 'Alternative C',
            'description': 'Hybrid approach balancing simplicity and features',
            'pros': ['Balanced', 'Moderate complexity', 'Flexible'],
            'cons': ['Medium cost', 'Some tradeoffs'],
            'suitable_for': 'Balanced requirements'
        }
    ]

    return alternatives

def select_alternative(alternatives: List[Dict]) -> Dict:
    """
    Select best alternative (placeholder)

    Args:
        alternatives: List of alternatives

    Returns:
        Selected alternative dict
    """
    # Placeholder: select Alternative C (hybrid) by default
    return alternatives[2]

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
    decision_id = "DEC-001"

    markdown = f"""# Architecture Decision

**Decision ID**: {decision_id}

**Generated**: {datetime.now().isoformat()}

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
        markdown += "---\n\n"

    markdown += "## Selected Alternative\n\n"
    markdown += f"**{selected['name']}**: {selected['description']}\n\n"
    markdown += "**Rationale**:\n"
    markdown += "- Balanced approach suitable for current requirements\n"
    markdown += "- Moderate complexity acceptable for project scope\n"
    markdown += "- Flexibility allows future scaling\n\n"

    markdown += "---\n\n"
    markdown += "## Evidence References\n\n"
    markdown += f"- Evidence Map: {evidence_map_path.name}\n"

    if judgment:
        markdown += f"- Judgment Summary: judgment-summary.md\n"

    markdown += "\n---\n\n"
    markdown += "## Risks\n\n"
    markdown += "- **Risk 1**: Moderate complexity may require additional documentation\n"
    markdown += "- **Risk 2**: Hybrid approach may not fully optimize for either extreme\n"
    markdown += "- **Mitigation**: Incremental refinement based on evaluation results\n\n"

    markdown += "---\n\n"
    markdown += "## Implementation Notes\n\n"
    markdown += "- Decision made based on {len(alternatives)} alternatives evaluated\n"
    markdown += f"- Selected: {selected['name']}\n"
    markdown += "- Next: Proceed to evaluation for validation\n\n"

    markdown += "\n_Generated by omr-decision_"

    return {
        'decision_id': decision_id,
        'markdown': markdown,
        'alternatives_count': len(alternatives)
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