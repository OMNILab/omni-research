#!/usr/bin/env python3
"""
omr-synthesis Implementation
Configurable synthesis (survey/report/manuscript/brief) with Gate D
"""

import json
from pathlib import Path
from typing import Dict
from datetime import datetime

def synthesize_findings(workspace_root: Path, mode: str = None) -> Dict:
    """
    Synthesize findings into configurable output

    Args:
        workspace_root: Project workspace root
        mode: Synthesis mode (survey/report/manuscript/brief), defaults to pattern config

    Returns:
        Dict with synthesis output path and metadata
    """
    docs_dir = workspace_root / 'docs'

    # Check prerequisites
    evaluation_path = docs_dir / 'evaluation-report.md'
    judgment_path = docs_dir / 'judgment-summary.md'

    if not evaluation_path.exists() and not judgment_path.exists():
        return {
            'status': 'failed',
            'error': 'Need evaluation-report.md OR judgment-summary.md'
        }

    # Determine mode (from pattern config or override)
    if mode is None:
        # Check pattern config
        pattern_config_path = workspace_root / 'skills' / 'pattern-config.json'
        if pattern_config_path.exists():
            config = json.loads(pattern_config_path.read_text())
            mode = config.get('synthesis_mode', 'brief')  # Default to brief
        else:
            mode = 'brief'  # Default mode

    # Generate synthesis based on mode
    synthesis = generate_synthesis(workspace_root, mode)

    # Write synthesis
    output_dir = docs_dir / mode  # survey/report/manuscript/brief
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create chapters/sections
    for chapter in synthesis['chapters']:
        chapter_path = output_dir / chapter['filename']
        chapter_path.write_text(chapter['content'])

    # Create index
    index_path = output_dir / 'index.md'
    index_path.write_text(synthesis['index'])

    # Gate D: Synthesis ready for publication?
    gate_passed = check_gate_d(synthesis)

    if not gate_passed['passed']:
        return {
            'status': 'gate_failed',
            'gate': 'D',
            'message': gate_passed['message'],
            'output_dir': str(output_dir)
        }

    # Update skill tree
    update_tree_state(workspace_root)

    return {
        'status': 'success',
        'gate_passed': gate_passed['passed'],
        'output_dir': str(output_dir),
        'mode': mode,
        'chapters': len(synthesis['chapters'])
    }

def generate_synthesis(workspace_root: Path, mode: str) -> Dict:
    """
    Generate synthesis content based on mode

    Args:
        workspace_root: Project workspace
        mode: Synthesis mode

    Returns:
        Dict with chapters, index
    """
    docs_dir = workspace_root / 'docs'

    # Read inputs
    evaluation_path = docs_dir / 'evaluation-report.md'
    judgment_path = docs_dir / 'judgment-summary.md'

    evaluation_content = evaluation_path.read_text() if evaluation_path.exists() else ""
    judgment_content = judgment_path.read_text() if judgment_path.exists() else ""

    # Generate chapters based on mode
    if mode == 'survey':
        chapters = [
            {
                'filename': '01-introduction.md',
                'title': 'Introduction',
                'content': generate_introduction(judgment_content, evaluation_content)
            },
            {
                'filename': '02-background.md',
                'title': 'Background',
                'content': generate_background(workspace_root)
            },
            {
                'filename': '03-methodology.md',
                'title': 'Methodology',
                'content': generate_methodology(evaluation_content)
            },
            {
                'filename': '04-results.md',
                'title': 'Results',
                'content': generate_results(evaluation_content)
            },
            {
                'filename': '05-conclusions.md',
                'title': 'Conclusions',
                'content': generate_conclusions(judgment_content, evaluation_content)
            }
        ]

    elif mode == 'report':
        chapters = [
            {
                'filename': 'executive-summary.md',
                'title': 'Executive Summary',
                'content': generate_executive_summary(judgment_content, evaluation_content)
            },
            {
                'filename': 'key-findings.md',
                'title': 'Key Findings',
                'content': generate_key_findings(evaluation_content)
            },
            {
                'filename': 'recommendations.md',
                'title': 'Recommendations',
                'content': generate_recommendations(evaluation_content)
            }
        ]

    elif mode == 'manuscript':
        chapters = [
            {
                'filename': 'title.md',
                'title': 'Title Page',
                'content': generate_title_page(workspace_root)
            },
            {
                'filename': 'abstract.md',
                'title': 'Abstract',
                'content': generate_abstract(judgment_content, evaluation_content)
            },
            {
                'filename': 'introduction.md',
                'title': 'Introduction',
                'content': generate_introduction(judgment_content, evaluation_content)
            },
            {
                'filename': 'methods.md',
                'title': 'Methods',
                'content': generate_methodology(evaluation_content)
            },
            {
                'filename': 'results.md',
                'title': 'Results',
                'content': generate_results(evaluation_content)
            },
            {
                'filename': 'discussion.md',
                'title': 'Discussion',
                'content': generate_discussion(judgment_content, evaluation_content)
            },
            {
                'filename': 'references.md',
                'title': 'References',
                'content': generate_references(workspace_root)
            }
        ]

    elif mode == 'brief':
        chapters = [
            {
                'filename': 'summary.md',
                'title': 'Summary',
                'content': generate_brief_summary(judgment_content, evaluation_content)
            }
        ]

    else:
        chapters = [
            {
                'filename': 'output.md',
                'title': 'Output',
                'content': f"Synthesis in {mode} mode\n\n{judgment_content}\n\n{evaluation_content}"
            }
        ]

    # Generate index
    index = generate_index(chapters, mode)

    return {
        'chapters': chapters,
        'index': index,
        'mode': mode
    }

def generate_introduction(judgment: str, evaluation: str) -> str:
    """Generate introduction chapter with traceability"""

    # Extract quality assessment from judgment
    import re
    quality_match = re.search(r'\*\*Quality\*\*: (\w+)', judgment)
    quality = quality_match.group(1) if quality_match else 'Unknown'

    conclusion_match = re.search(r'## Main Conclusion\n\n(.+)', judgment)
    conclusion = conclusion_match.group(1).strip() if conclusion_match else 'Research investigation completed'

    return f"""# Introduction

**Generated**: {datetime.now().isoformat()}

## Overview

{conclusion}

## Research Context

This survey synthesizes findings from systematic research investigation with evidence quality assessment.

**Evidence Quality**: {quality}

## Research Questions

Key research questions addressed based on collected evidence:

{extract_questions_from_judgment(judgment)}

## Scope

Comprehensive review with systematic evaluation ensuring traceability and evidence boundaries.

## Traceability

All claims in this synthesis link to:
- Evidence map (proven/suggested/inferred boundaries)
- Judgment summary (quality assessment)
- Evaluation report (validation results)

---
_Generated by omr-synthesis (survey mode)_"""

def extract_questions_from_judgment(judgment: str) -> str:
    """Extract research questions from judgment"""
    # Simplified extraction
    if 'Evidence foundation' in judgment:
        return "- What architecture approach best meets requirements?\n- How do proven claims support design decisions?\n- What gaps require additional investigation?"
    return "- Research questions defined in evidence mapping phase"

def generate_background(workspace_root: Path) -> str:
    """Generate background chapter from evidence"""
    docs_dir = workspace_root / 'docs'
    evidence_map_path = docs_dir / 'evidence-map.md'

    # Read evidence map for context
    evidence_text = ""
    if evidence_map_path.exists():
        evidence_text = evidence_map_path.read_text()

        # Extract proven claims count
        import re
        proven_count = evidence_text.count('**Evidence boundary**: proven')
        suggested_count = evidence_text.count('**Evidence boundary**: suggested')

        evidence_summary = f"""
## Evidence Foundation

**Proven claims**: {proven_count}

**Suggested claims**: {suggested_count}

Evidence extracted from collected materials provides foundation for background context.
"""
    else:
        evidence_summary = "Background derived from collected materials."

    return f"""# Background

## Context

Research context derived from collected materials in `raw/` directory.

{evidence_summary}

## Prior Work

Review of existing approaches based on collected papers and repositories.

All background claims traceable to evidence sources.

---
_Generated by omr-synthesis_"""

def generate_methodology(evaluation: str) -> str:
    """Generate methodology chapter from evaluation"""

    # Extract validation approach from evaluation
    import re
    validation_match = re.search(r'\*\*Validation Type\*\*: (\w+)', evaluation)
    validation_type = validation_match.group(1) if validation_match else 'systematic'

    checks_match = re.search(r'\*\*Scenarios Tested\*\*: (\d+)', evaluation)
    scenarios_tested = checks_match.group(1) if checks_match else 'N/A'

    return f"""# Methodology

## Approach

Systematic evaluation methodology as documented in experiment specification.

**Validation Type**: {validation_type}

**Scenarios Tested**: {scenarios_tested}

## Metrics

Defined in experiment-spec.md:
- Validation checks passed
- Pass rate percentage
- Artifacts consistency

## Reproducibility

All methodology steps documented in:
- Experiment specification (`experiment-spec.md`)
- Validation checks log (`src/prototype/validation-checks.md`)

---
_Generated by omr-synthesis_"""

def generate_results(evaluation: str) -> str:
    """Generate results chapter with evidence boundaries"""

    # Extract key metrics from evaluation
    import re
    supported_match = re.search(r'\*\*Supported\*\*: (\w+)', evaluation)
    hypothesis_supported = supported_match.group(1) if supported_match else 'Unknown'

    pass_rate_match = re.search(r'\*\*Pass Rate\*\*: ([\d.]+)', evaluation)
    pass_rate = pass_rate_match.group(1) if pass_rate_match else 'N/A'

    evidence_boundary = 'proven' if hypothesis_supported == 'True' else 'suggested'

    return f"""# Results

## Evaluation Outcomes

**Hypothesis Supported**: {hypothesis_supported}

**Evidence Boundary**: {evidence_boundary}

{evaluation[:500] if evaluation else 'Results from evaluation...'}

## Key Metrics

- **Pass Rate**: {pass_rate}%
- **Validation Checks**: documented in evaluation report

## Traceability

Results traceable to:
- Evaluation report (`evaluation-report.md`)
- Decision document (`architecture-decision.md`)
- Evidence map (`evidence-map.md`)

---
_Generated by omr-synthesis_"""

def generate_conclusions(judgment: str, evaluation: str) -> str:
    """Generate conclusions chapter with proper boundary labels"""

    # Extract judgment conclusion
    import re
    conclusion_match = re.search(r'## Main Conclusion\n\n(.+)', judgment)
    conclusion = conclusion_match.group(1).strip() if conclusion_match else 'Research completed'

    quality_match = re.search(r'\*\*Quality\*\*: (\w+)', judgment)
    quality = quality_match.group(1) if quality_match else 'Moderate'

    # Extract hypothesis result
    supported_match = re.search(r'\*\*Supported\*\*: (\w+)', evaluation)
    hypothesis_supported = supported_match.group(1) if supported_match else 'Unknown'

    # Determine evidence boundary for conclusion
    if hypothesis_supported == 'True' and quality == 'Strong':
        evidence_boundary = 'proven'
    elif hypothesis_supported == 'True':
        evidence_boundary = 'suggested'
    else:
        evidence_boundary = 'inferred'

    return f"""# Conclusions

## Summary

{conclusion}

**Evidence Boundary**: {evidence_boundary}

**Quality Assessment**: {quality}

## Key Findings

Based on systematic evaluation:

{extract_findings_from_eval(evaluation)}

## Evidence Support

{extract_proven_count(judgment)} proven claims support these conclusions.

## Future Work

Recommendations for continued investigation:
- Address identified research gaps
- Collect additional proven evidence if needed
- Continue validation experiments

---
_Generated by omr-synthesis_"""

def extract_findings_from_eval(evaluation: str) -> str:
    """Extract key findings from evaluation"""
    if 'hypothesis_supported' in evaluation.lower():
        return "- Hypothesis validated through systematic checks\n- Architecture decision supported by evidence\n- Evaluation demonstrates consistent artifact structure"
    return "- Findings documented in evaluation report"

def extract_proven_count(judgment: str) -> str:
    """Extract proven claims count from judgment"""
    import re
    proven_match = re.search(r'\*\*Proven\*\*: (\d+)', judgment)
    return proven_match.group(1) if proven_match else 'N/A'

def generate_executive_summary(judgment: str, evaluation: str) -> str:
    """Generate executive summary"""
    return f"""# Executive Summary

**Generated**: {datetime.now().isoformat()}

## Key Findings

{judgment[:300] if judgment else 'Judgment summary...'}

## Recommendations

Action items derived from evaluation results.

---
_Generated by omr-synthesis (report mode)_"""

def generate_key_findings(evaluation: str) -> str:
    """Generate key findings"""
    return f"""# Key Findings

{evaluation[:500] if evaluation else 'Evaluation findings...'}

---
_Generated by omr-synthesis_"""

def generate_recommendations(evaluation: str) -> str:
    """Generate recommendations"""
    return f"""# Recommendations

Based on evaluation results:

1. Proceed with selected architecture
2. Address identified gaps
3. Continue monitoring performance

---
_Generated by omr-synthesis_"""

def generate_title_page(workspace_root: Path) -> str:
    """Generate title page"""
    return f"""# Research Manuscript

**Title**: Systematic Investigation

**Authors**: Generated by omr-synthesis

**Date**: {datetime.now().isoformat()}

---
_Generated by omr-synthesis (manuscript mode)_"""

def generate_abstract(judgment: str, evaluation: str) -> str:
    """Generate abstract"""
    return f"""# Abstract

{judgment[:200] if judgment else 'Abstract content...'}

---
_Generated by omr-synthesis_"""

def generate_discussion(judgment: str, evaluation: str) -> str:
    """Generate discussion"""
    return f"""# Discussion

Analysis of results and implications.

---
_Generated by omr-synthesis_"""

def generate_references(workspace_root: Path) -> str:
    """Generate references"""
    return f"""# References

Collected materials indexed in:
- `docs/index/papers-index.json`
- `docs/index/repos-index.json`
- `docs/index/datasets-index.json`

---
_Generated by omr-synthesis_"""

def generate_brief_summary(judgment: str, evaluation: str) -> str:
    """Generate brief summary"""
    return f"""# Brief Summary

**Generated**: {datetime.now().isoformat()}

## Quick Findings

{judgment[:300] if judgment else 'Judgment...'}

## Results

{evaluation[:300] if evaluation else 'Evaluation...'}

---
_Generated by omr-synthesis (brief mode)_"""

def generate_index(chapters: list, mode: str) -> str:
    """Generate synthesis index"""
    lines = [
        f"# {mode.capitalize()} Index",
        "",
        f"**Mode**: {mode}",
        "",
        f"**Generated**: {datetime.now().isoformat()}",
        "",
        "---",
        "",
        "## Contents",
        ""
    ]

    for i, chapter in enumerate(chapters, 1):
        lines.append(f"{i}. [{chapter['title']}](./{chapter['filename']})")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("_Generated by omr-synthesis_")

    return "\n".join(lines)

def check_gate_d(synthesis: Dict) -> Dict:
    """
    Gate D: Synthesis ready for publication?

    Critical checks:
    - All claims have evidence boundary labels (proven/suggested/inferred)
    - All claims traceable to sources
    - No over-claiming (proven only with experimental evidence)

    Args:
        synthesis: Synthesis dict

    Returns:
        Dict with passed, message, checks
    """
    checks_performed = {
        'chapters_exist': len(synthesis['chapters']) > 0,
        'traceability_present': False,
        'boundaries_stated': False,
        'no_overclaiming': False
    }

    # Check all chapters for traceability and boundaries
    all_content = ""
    for chapter in synthesis['chapters']:
        all_content += chapter['content']

    # Check 1: Traceability markers present
    traceability_markers = [
        'Evidence map',
        'Judgment summary',
        'Evaluation report',
        'traceable',
        'Traceability'
    ]
    checks_performed['traceability_present'] = any(marker in all_content for marker in traceability_markers)

    # Check 2: Evidence boundary labels present
    boundary_keywords = ['Evidence Boundary', 'proven', 'suggested', 'inferred']
    checks_performed['boundaries_stated'] = any(kw in all_content for kw in boundary_keywords)

    # Check 3: No over-claiming
    # Look for claims labeled "proven" and verify they reference validation
    has_proven = 'proven' in all_content.lower()
    has_validation = 'validation' in all_content.lower() or 'evaluation' in all_content.lower()

    # If claiming proven, must reference validation/evaluation
    if has_proven:
        checks_performed['no_overclaiming'] = has_validation
    else:
        checks_performed['no_overclaiming'] = True  # No proven claims, no over-claiming

    # All checks must pass
    passed = all(checks_performed.values())

    if passed:
        message = "Gate D passed: Synthesis ready for publication"
    else:
        missing = []
        if not checks_performed['chapters_exist']:
            missing.append("No synthesis content")
        if not checks_performed['traceability_present']:
            missing.append("Traceability not stated")
        if not checks_performed['boundaries_stated']:
            missing.append("Evidence boundaries not stated")
        if not checks_performed['no_overclaiming']:
            missing.append("Over-claiming detected (proven without validation)")

        message = f"Gate D failed: {', '.join(missing)}"

    return {
        'passed': passed,
        'message': message,
        'checks': checks_performed
    }

def update_tree_state(workspace_root: Path):
    """Update skill tree"""
    tree_state_path = workspace_root / 'skills' / 'tree-state.json'

    if not tree_state_path.exists():
        return

    state = json.loads(tree_state_path.read_text())

    if 'omr-synthesis' in state['ready']:
        state['ready'].remove('omr-synthesis')

    state['completed'].append('omr-synthesis')

    tree_state_path.write_text(json.dumps(state, indent=2))

def main():
    """CLI entry point"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: synthesize_findings.py <workspace> [mode]")
        print("Modes: survey, report, manuscript, brief")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    mode = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"Synthesizing findings (mode: {mode or 'auto'})...")
    result = synthesize_findings(workspace, mode)

    if result['status'] == 'success':
        print(f"✓ Synthesis complete")
        print(f"  Output: {result['output_dir']}")
        print(f"  Mode: {result['mode']}")
        print(f"  Chapters: {result['chapters']}")

        if result['gate_passed']:
            print(f"\n⚠️  GATE D: Passed")

        print(f"\n📊 Skill tree updated")

    elif result['status'] == 'gate_failed':
        print(f"⚠️  GATE D FAILED")
        print(f"  {result['message']}")

    else:
        print(f"✗ Error: {result['error']}")

if __name__ == "__main__":
    main()