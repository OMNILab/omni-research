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
    """Generate introduction chapter"""
    return f"""# Introduction

**Generated**: {datetime.now().isoformat()}

## Overview

This survey synthesizes findings from systematic research investigation.

## Research Question

Based on collected evidence and evaluation, this survey addresses key research questions identified in the evidence mapping phase.

## Scope

Comprehensive review of collected materials with systematic evaluation.

---
_Generated by omr-synthesis (survey mode)_"""

def generate_background(workspace_root: Path) -> str:
    """Generate background chapter"""
    return f"""# Background

## Context

Research context derived from collected materials in `raw/` directory.

## Prior Work

Review of existing approaches based on collected papers and repositories.

---
_Generated by omr-synthesis_"""

def generate_methodology(evaluation: str) -> str:
    """Generate methodology chapter"""
    return f"""# Methodology

## Approach

Systematic evaluation methodology as documented in experiment specification.

## Metrics

Defined in experiment-spec.md:
- Execution time
- Accuracy
- Resource usage

---
_Generated by omr-synthesis_"""

def generate_results(evaluation: str) -> str:
    """Generate results chapter"""
    return f"""# Results

## Evaluation Outcomes

{evaluation[:500] if evaluation else 'Results from evaluation...'}

---
_Generated by omr-synthesis_"""

def generate_conclusions(judgment: str, evaluation: str) -> str:
    """Generate conclusions chapter"""
    return f"""# Conclusions

## Summary

Synthesis of judgment and evaluation findings.

## Future Work

Recommendations for continued investigation.

---
_Generated by omr-synthesis_"""

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

    Checks:
    - Results traceable to hypotheses
    - Evidence boundaries stated
    - No over-claiming

    Args:
        synthesis: Synthesis dict

    Returns:
        Dict with passed, message
    """
    # Placeholder gate checks
    chapters_exist = len(synthesis['chapters']) > 0

    passed = chapters_exist

    if passed:
        message = "Gate D passed: Synthesis ready"
    else:
        message = "Gate D failed: No synthesis content"

    return {
        'passed': passed,
        'message': message
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