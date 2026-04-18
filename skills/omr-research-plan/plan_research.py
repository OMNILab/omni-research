#!/usr/bin/env python3
"""
omr-research-plan Implementation (Merged Skill)
Judges evidence + plans research approach (merged from brainstorming session 1)
"""

import json
from pathlib import Path
from typing import Dict
from datetime import datetime

def plan_research(workspace_root: Path) -> Dict:
    """
    Judge evidence and plan research approach (merged skill)

    Args:
        workspace_root: Project workspace root

    Returns:
        Dict with judgment summary and research plan
    """
    docs_dir = workspace_root / 'docs'

    # Read evidence map
    evidence_map_path = docs_dir / 'evidence-map.md'

    if not evidence_map_path.exists():
        return {
            'status': 'failed',
            'error': 'evidence-map.md not found. Run omr-evidence first.'
        }

    evidence_map = evidence_map_path.read_text()

    # Judge evidence (synthesize main conclusion)
    judgment = synthesize_judgment(evidence_map)

    # Plan research approach
    plan = create_research_plan(evidence_map, judgment)

    # Write outputs
    judgment_path = docs_dir / 'judgment-summary.md'
    judgment_path.write_text(judgment['markdown'])

    plan_path = docs_dir / 'research-plan.md'
    plan_path.write_text(plan['markdown'])

    # Gate A: Evidence sufficient for planning?
    gate_passed = check_gate_a(evidence_map)

    if not gate_passed['passed']:
        return {
            'status': 'gate_failed',
            'gate': 'A',
            'message': gate_passed['message'],
            'judgment_path': str(judgment_path),
            'plan_path': str(plan_path)
        }

    # Update skill tree
    update_tree_state(workspace_root)

    return {
        'status': 'success',
        'gate_passed': gate_passed['passed'],
        'judgment_path': str(judgment_path),
        'plan_path': str(plan_path),
        'main_conclusion': judgment['conclusion'],
        'confidence': judgment['confidence'],
        'priorities': len(plan['priorities'])
    }

def synthesize_judgment(evidence_map: str) -> Dict:
    """
    Synthesize judgment from evidence map

    Calculate coverage and quality based on evidence boundaries

    Args:
        evidence_map: Evidence map markdown content

    Returns:
        Dict with conclusion, confidence, markdown
    """
    # Parse evidence map for claims and boundaries
    import re

    # Count claims by evidence boundary
    proven_count = evidence_map.count('**Evidence boundary**: proven')
    suggested_count = evidence_map.count('**Evidence boundary**: suggested')
    inferred_count = evidence_map.count('**Evidence boundary**: inferred')
    total_claims = proven_count + suggested_count + inferred_count

    # Count gaps
    gaps_count = evidence_map.count('**G-')

    # Calculate coverage percentage
    if total_claims > 0:
        proven_ratio = proven_count / total_claims
        coverage_percentage = round(proven_ratio * 100, 1)
    else:
        coverage_percentage = 0

    # Quality assessment based on proven claims ratio
    if coverage_percentage >= 60:
        quality = "Strong"
        quality_description = "High coverage of proven evidence"
    elif coverage_percentage >= 30:
        quality = "Moderate"
        quality_description = "Moderate coverage, some proven evidence"
    else:
        quality = "Weak"
        quality_description = "Limited proven evidence, mostly suggested/inferred"

    # Confidence based on proven count
    if proven_count >= 10:
        confidence = "high"
    elif proven_count >= 5:
        confidence = "medium"
    else:
        confidence = "low"

    # Main conclusion
    if proven_count >= 5:
        conclusion = "Evidence foundation strong enough for architectural decisions"
    elif proven_count >= 2:
        conclusion = "Evidence foundation adequate, but validation recommended"
    else:
        conclusion = "Evidence foundation weak, collect more proven evidence"

    markdown = f"""# Judgment Summary

**Generated**: {datetime.now().isoformat()}

---

## Main Conclusion

{conclusion}

**Confidence**: {confidence}

---

## Evidence Quality Assessment

**Quality**: {quality}

{quality_description}

---

## Evidence Boundary Distribution

- **Proven**: {proven_count} claims ({coverage_percentage}% of total)
- **Suggested**: {suggested_count} claims
- **Inferred**: {inferred_count} claims
- **Total Claims**: {total_claims}

---

## Research Gaps

- **Gaps Identified**: {gaps_count}

---

## Judgment

Based on {total_claims} extracted claims ({proven_count} proven, {suggested_count} suggested, {inferred_count} inferred) and {gaps_count} identified gaps:

**Evidence Quality**: {quality}

{'Evidence coverage adequate for proceeding with architectural decisions.' if proven_count >= 3 else 'Additional proven evidence needed before architectural decisions.'}

**Recommendation**:
{'Proceed to omr-decision to make architecture choices.' if proven_count >= 3 else 'Consider collecting more papers with experimental validation before proceeding.'}

---

_Generated by omr-research-plan (merged skill: judgment + planning)_"""

    return {
        'conclusion': conclusion,
        'confidence': confidence,
        'quality': quality,
        'proven_count': proven_count,
        'suggested_count': suggested_count,
        'inferred_count': inferred_count,
        'total_claims': total_claims,
        'coverage_percentage': coverage_percentage,
        'markdown': markdown
    }

def create_research_plan(evidence_map: str, judgment: Dict) -> Dict:
    """
    Create research plan from evidence and judgment

    Generate priorities based on gaps and evidence quality

    Args:
        evidence_map: Evidence map content
        judgment: Judgment dict

    Returns:
        Dict with priorities, timeline, markdown
    """
    import re

    # Extract gaps from evidence map
    gap_matches = re.findall(r'\*\*G-(\d+)\*\*: (.+)', evidence_map)
    gaps = [{'id': f"G-{gid}", 'description': desc} for gid, desc in gap_matches]

    # Generate priorities based on judgment and gaps
    priorities = []

    # Priority 1: Address gaps
    if gaps:
        priorities.append({
            'priority': 1,
            'task': f"Address {len(gaps)} identified research gaps",
            'details': [g['description'] for g in gaps[:3]],
            'estimated_time': f"{len(gaps)}-2 weeks" if len(gaps) > 2 else "1-2 days",
            'next_skill': 'omr-collection'
        })
    else:
        priorities.append({
            'priority': 1,
            'task': "Review collected materials comprehensively",
            'details': [],
            'estimated_time': '1-2 days',
            'next_skill': None
        })

    # Priority 2: Validate decisions
    proven_count = judgment.get('proven_count', 0)
    if proven_count < 5:
        priorities.append({
            'priority': 2,
            'task': "Collect additional proven evidence",
            'details': ["Need more papers with experimental validation"],
            'estimated_time': '1 week',
            'next_skill': 'omr-collection'
        })
    else:
        priorities.append({
            'priority': 2,
            'task': "Make architectural decisions based on evidence",
            'details': ["Leverage proven evidence for architecture"],
            'estimated_time': '1-2 days',
            'next_skill': 'omr-decision'
        })

    # Priority 3: Run experiments if decisions made
    priorities.append({
        'priority': 3,
        'task': "Validate architectural decisions through experiments",
        'details': ["Run controlled validation tests"],
        'estimated_time': '2-3 weeks',
        'next_skill': 'omr-evaluation'
    })

    # Calculate timeline
    total_days = sum([int(p['estimated_time'].split()[0]) for p in priorities if p['estimated_time']])
    timeline = f"{total_days}-{total_days+2} days estimated"

    markdown = f"""# Research Plan

**Generated**: {datetime.now().isoformat()}

**Judgment**: {judgment['conclusion']} (Quality: {judgment.get('quality', 'Unknown')}, Confidence: {judgment['confidence']})

---

## Research Priorities

"""

    for priority in priorities:
        markdown += f"### Priority {priority['priority']}: {priority['task']}\n\n"
        if priority['details']:
            for detail in priority['details']:
                markdown += f"- {detail}\n"
        markdown += f"\n**Estimated time**: {priority['estimated_time']}\n"
        if priority['next_skill']:
            markdown += f"\n**Next skill**: `{priority['next_skill']}`\n"
        markdown += "\n"

    markdown += "---\n\n"
    markdown += "## Timeline\n\n"
    markdown += f"**Total Estimated**: {timeline}\n\n"
    markdown += "**Note**: Timeline depends on material availability and experiment complexity.\n\n"

    markdown += "---\n\n"
    markdown += "## Success Criteria\n\n"
    for priority in priorities:
        markdown += f"- [ ] {priority['task']} completed\n"
    markdown += "- [ ] All gates passed (A, B, C, D)\n\n"

    markdown += "---\n\n"
    markdown += "## Next Steps\n\n"

    # Recommend next skill based on priorities
    next_skill = priorities[0]['next_skill'] if priorities[0]['next_skill'] else 'omr-decision'
    markdown += f"**Recommended**: Run `{next_skill}` next.\n\n"

    if next_skill == 'omr-collection':
        markdown += "Additional materials needed to strengthen evidence foundation.\n\n"
    elif next_skill == 'omr-decision':
        markdown += "Evidence foundation sufficient to make architectural decisions.\n\n"
    elif next_skill == 'omr-evaluation':
        markdown += "Ready to validate architectural decisions.\n\n"

    markdown += "\n_Generated by omr-research-plan (merged skill)_"

    return {
        'priorities': priorities,
        'timeline': timeline,
        'markdown': markdown,
        'next_skill': next_skill
    }

def check_gate_a(evidence_map: str) -> Dict:
    """
    Gate A: Evidence sufficient for planning?

    Checks:
    - Evidence coverage adequate
    - Research question clear
    - Scope defined

    Args:
        evidence_map: Evidence map content

    Returns:
        Dict with passed, message
    """
    # Simplified gate checks
    claims_count = evidence_map.count('**C-')

    # Check coverage
    coverage_adequate = claims_count >= 3

    # Check research question present
    question_present = 'Question ID' in evidence_map

    # Check scope defined
    scope_defined = 'Scope' in evidence_map

    passed = coverage_adequate and question_present and scope_defined

    if passed:
        message = "Gate A passed: Evidence sufficient for research planning"
    else:
        missing = []
        if not coverage_adequate:
            missing.append("Evidence coverage insufficient")
        if not question_present:
            missing.append("Research question unclear")
        if not scope_defined:
            missing.append("Scope not defined")

        message = f"Gate A failed: {', '.join(missing)}"

    return {
        'passed': passed,
        'message': message,
        'checks': {
            'coverage_adequate': coverage_adequate,
            'question_present': question_present,
            'scope_defined': scope_defined
        }
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

    # Mark omr-research-plan as completed
    if 'omr-research-plan' in state['ready']:
        state['ready'].remove('omr-research-plan')

    state['completed'].append('omr-research-plan')

    # Unlock omr-decision
    if 'omr-decision' in state['locked']:
        state['locked'].remove('omr-decision')
        state['ready'].append('omr-decision')

    tree_state_path.write_text(json.dumps(state, indent=2))

def main():
    """CLI entry point"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: plan_research.py <workspace>")
        print("Example: plan_research.py /tmp/test-project")
        sys.exit(1)

    workspace = Path(sys.argv[1])

    print("Judging evidence and planning research approach...")
    result = plan_research(workspace)

    if result['status'] == 'success':
        print(f"✓ Research planning complete")
        print(f"  Judgment: {result['judgment_path']}")
        print(f"  Plan: {result['plan_path']}")
        print(f"  Main conclusion: {result['main_conclusion']}")
        print(f"  Confidence: {result['confidence']}")
        print(f"  Priorities: {result['priorities']}")

        if result['gate_passed']:
            print(f"\n⚠️  GATE A: Passed")
            print(f"  Evidence sufficient for planning")

        print(f"\n📊 Skill tree updated")
        print(f"  - omr-decision [READY]")

    elif result['status'] == 'gate_failed':
        print(f"⚠️  GATE A FAILED")
        print(f"  {result['message']}")
        print(f"\n  Review: {result['judgment_path']}")
        print(f"  Plan draft: {result['plan_path']}")

    else:
        print(f"✗ Error: {result['error']}")

if __name__ == "__main__":
    main()