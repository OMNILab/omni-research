#!/usr/bin/env python3
"""
Pattern Emergence Detection
Detects pattern from skill sequence after 3+ invocations
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

def detect_pattern(workspace_root: Path) -> Dict:
    """
    Detect emerging pattern from skill invocation sequence

    Args:
        workspace_root: Project workspace

    Returns:
        Dict with detected pattern name, confidence, save recommendation
    """
    tree_state_path = workspace_root / 'skills' / 'tree-state.json'

    if not tree_state_path.exists():
        return {
            'status': 'no_state',
            'message': 'No skill tree state found'
        }

    state = json.loads(tree_state_path.read_text())

    completed_skills = state.get('completed', [])

    # Need at least 3 skills to detect pattern
    if len(completed_skills) < 3:
        return {
            'status': 'insufficient_data',
            'message': f'Need 3+ skill invocations (current: {len(completed_skills)})'
        }

    # Match against known patterns
    patterns_dir = workspace_root / 'skills' / 'patterns'

    if not patterns_dir.exists():
        # Load from implementation directory
        patterns_dir = Path(__file__).parent.parent / 'patterns'

    pattern_matches = []

    for pattern_file in patterns_dir.glob('*.json'):
        pattern = json.loads(pattern_file.read_text())

        # Calculate match score
        match_score = calculate_pattern_match(completed_skills, pattern)

        if match_score > 0:
            pattern_matches.append({
                'pattern_name': pattern['name'],
                'match_score': match_score,
                'pattern_file': str(pattern_file)
            })

    # Sort by match score
    pattern_matches.sort(key=lambda x: x['match_score'], reverse=True)

    if not pattern_matches:
        return {
            'status': 'no_match',
            'message': 'No known pattern detected from sequence'
        }

    best_match = pattern_matches[0]

    return {
        'status': 'detected',
        'pattern_name': best_match['pattern_name'],
        'match_score': best_match['match_score'],
        'confidence': 'high' if best_match['match_score'] >= 0.7 else 'medium',
        'pattern_file': best_match['pattern_file'],
        'completed_sequence': completed_skills,
        'recommendation': f'Pattern emerging: {best_match["pattern_name"]}. Save pattern?'
    }

def calculate_pattern_match(completed_skills: List[str], pattern: Dict) -> float:
    """
    Calculate how well completed sequence matches pattern

    Args:
        completed_skills: List of completed skill names
        pattern: Pattern definition dict

    Returns:
        Match score (0-1)
    """
    # Check if sequence matches pattern entry point
    graph = pattern['graph']
    entry_points = graph['entry_points']

    if not completed_skills:
        return 0.0

    # First skill should be entry point
    if completed_skills[0] not in entry_points:
        return 0.0

    # Calculate overlap with pattern nodes
    pattern_nodes = set(graph['nodes'])

    completed_set = set(completed_skills)

    overlap = len(pattern_nodes & completed_set)

    total_pattern_nodes = len(pattern_nodes)

    overlap_score = overlap / total_pattern_nodes if total_pattern_nodes > 0 else 0.0

    # Check sequence order (simplified)
    sequence_score = 1.0 if len(completed_skills) >= 3 else 0.5

    # Combined score
    match_score = (overlap_score * 0.6 + sequence_score * 0.4)

    return match_score

def save_pattern(workspace_root: Path, pattern_name: str, custom_sequence: List[str] = None) -> Dict:
    """
    Save pattern as reusable template

    Args:
        workspace_root: Project workspace
        pattern_name: Name for saved pattern
        custom_sequence: Optional custom skill sequence

    Returns:
        Dict with saved pattern path
    """
    patterns_dir = workspace_root / 'skills' / 'patterns'
    patterns_dir.mkdir(parents=True, exist_ok=True)

    tree_state_path = workspace_root / 'skills' / 'tree-state.json'

    if not tree_state_path.exists():
        return {
            'status': 'failed',
            'error': 'No skill tree state to save'
        }

    state = json.loads(tree_state_path.read_text())

    completed_skills = custom_sequence or state.get('completed', [])

    # Create pattern definition
    pattern_def = {
        'name': pattern_name,
        'description': f'User-defined pattern: {pattern_name}',
        'graph': {
            'entry_points': [completed_skills[0]] if completed_skills else [],
            'nodes': completed_skills,
            'edges': generate_edges(completed_skills)
        },
        'skill_gates': {},
        'contract_overrides': {},
        'recommendations': {
            'agency': 'semi-automated',
            'estimated_time': 'variable',
            'synthesis_mode': 'brief',
            'description': 'Custom pattern saved from user workflow'
        },
        'saved_at': datetime.now().isoformat(),
        'user_defined': True
    }

    # Save pattern
    pattern_file = patterns_dir / f'{pattern_name.lower().replace(" ", "-")}.json'
    pattern_file.write_text(json.dumps(pattern_def, indent=2))

    return {
        'status': 'success',
        'pattern_file': str(pattern_file),
        'pattern_name': pattern_name,
        'sequence': completed_skills
    }

def generate_edges(skill_sequence: List[str]) -> List[str]:
    """
    Generate edges from skill sequence

    Args:
        skill_sequence: List of skill names in order

    Returns:
        List of edge strings "skill_a → skill_b"
    """
    edges = []

    for i in range(len(skill_sequence) - 1):
        edges.append(f"{skill_sequence[i]} → {skill_sequence[i+1]}")

    return edges

def main():
    """CLI entry point"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: detect_pattern.py <workspace> [--save <name>]")
        print("Example: detect_pattern.py /tmp/test-project")
        print("         detect_pattern.py /tmp/test-project --save my-custom-pattern")
        sys.exit(1)

    workspace = Path(sys.argv[1])

    save_mode = '--save' in sys.argv

    if save_mode:
        # Get pattern name
        pattern_name_idx = sys.argv.index('--save') + 1
        pattern_name = sys.argv[pattern_name_idx] if pattern_name_idx < len(sys.argv) else 'custom-pattern'

        print(f"Saving pattern: {pattern_name}...")
        result = save_pattern(workspace, pattern_name)

        if result['status'] == 'success':
            print(f"✓ Pattern saved")
            print(f"  File: {result['pattern_file']}")
            print(f"  Name: {result['pattern_name']}")
            print(f"  Sequence: {result['sequence']}")

        else:
            print(f"✗ Error: {result['error']}")

    else:
        # Detect pattern
        print("Detecting pattern from skill sequence...")
        result = detect_pattern(workspace)

        if result['status'] == 'detected':
            print(f"\n✓ Pattern detected")
            print(f"  Pattern: {result['pattern_name']}")
            print(f"  Confidence: {result['confidence']}")
            print(f"  Match score: {result['match_score']:.2f}")
            print(f"\n  {result['recommendation']}")

        elif result['status'] == 'insufficient_data':
            print(f"\n  {result['message']}")

        else:
            print(f"\n  {result['message']}")

if __name__ == "__main__":
    main()