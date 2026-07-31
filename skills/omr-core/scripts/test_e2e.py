#!/usr/bin/env python3
"""
End-to-End Test Workflow
Tests complete Evidence-First pattern workflow
"""

import subprocess
import sys
from pathlib import Path
import tempfile
import shutil
from typing import Dict

def test_evidence_first_workflow():
    """
    Test complete Evidence-First pattern workflow

    Returns:
        Dict with test results
    """
    print("=" * 80)
    print("TEST: Evidence-First Pattern Workflow")
    print("=" * 80)

    # Create temporary workspace
    temp_dir = Path(tempfile.mkdtemp())
    workspace = temp_dir / 'test-project'

    try:
        # Step 1: Bootstrap
        print("\n[1] Bootstrap workspace...")
        result = run_skill(
            'skills/omr-bootstrap/scripts/bootstrap_workspace.py',
            'test-project "Agent memory mechanisms"',
            cwd=temp_dir
        )
        assert result['success'], "Bootstrap failed"
        print("✓ Bootstrap complete")

        # Step 2: Collection (mock data for testing)
        print("\n[2] Create mock materials...")
        raw_paper = workspace / 'materials' / 'paper'
        raw_paper.mkdir(parents=True, exist_ok=True)
        mock_paper = raw_paper / 'mock-paper.md'
        mock_paper.write_text("# Mock Paper\n\nContent about agent memory...\n")
        print("✓ Mock materials created")

        # Step 3: Analyze (evidence extraction + research planning, Gate A)
        print("\n[3] Analyze materials...")
        result = run_skill(
            'skills/omr-analyze/scripts/analyze.py',
            str(workspace)
        )
        assert result['success'], "Analysis failed"
        print("✓ Analysis complete (Gate A passed)")

        # Step 4: Decision (Gate B)
        print("\n[4] Make decision...")
        result = run_skill(
            'skills/omr-decision/make_decision.py',
            str(workspace)
        )
        assert result['success'], "Decision failed"
        print("✓ Decision made (Gate B passed)")

        # Step 5: Evaluation (Gate C)
        print("\n[5] Run evaluation...")
        result = run_skill(
            'skills/omr-evaluation/run_evaluation.py',
            str(workspace)
        )
        assert result['success'], "Evaluation failed"
        print("✓ Evaluation complete (Gate C passed)")

        # Step 6: Synthesis (Gate D, includes wiki generation)
        print("\n[6] Synthesize findings...")
        result = run_skill(
            'skills/omr-synthesis/synthesize_findings.py',
            str(workspace) + ' brief'
        )
        assert result['success'], "Synthesis failed"
        print("✓ Synthesis complete (Gate D passed, wiki auto-generated)")

        # Verify all artifacts exist
        print("\n[7] Verify artifacts...")
        docs_dir = workspace / 'docs'
        expected_artifacts = [
            'research-brief.md',
            'evidence-map.md',
            'judgment-summary.md',
            'research-plan.md',
            'architecture-decision.md',
            'experiment-spec.md',
            'evaluation-report.md',
            'brief/summary.md'
        ]

        for artifact in expected_artifacts:
            artifact_path = docs_dir / artifact
            assert artifact_path.exists(), f"Missing artifact: {artifact}"
            print(f"  ✓ {artifact}")

        # Verify skill tree state
        print("\n[8] Verify skill tree...")
        tree_state_path = workspace / '.omr' / 'tree-state.json'
        assert tree_state_path.exists(), "Tree state missing"

        import json
        state = json.loads(tree_state_path.read_text())
        completed = state.get('completed', [])

        expected_skills = [
            'omr-bootstrap',
            'omr-collection',
            'omr-analyze',
            'omr-decision',
            'omr-evaluation',
            'omr-synthesis',
        ]

        for skill in expected_skills:
            assert skill in completed, f"Skill not marked completed: {skill}"
            print(f"  ✓ {skill}")

        print("\n" + "=" * 80)
        print("TEST RESULT: ✓ ALL TESTS PASSED")
        print("=" * 80)

        return {
            'status': 'passed',
            'workspace': str(workspace),
            'artifacts_verified': len(expected_artifacts),
            'skills_completed': len(expected_skills)
        }

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {str(e)}")
        return {
            'status': 'failed',
            'error': str(e)
        }

    except Exception as e:
        print(f"\n✗ TEST ERROR: {str(e)}")
        return {
            'status': 'error',
            'error': str(e)
        }

    finally:
        # Cleanup
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
            print("\nCleaned up temporary workspace")

def run_skill(script_path: str, args: str, cwd: Path = None) -> Dict:
    """
    Run skill script

    Args:
        script_path: Path to skill script
        args: Arguments string
        cwd: Working directory

    Returns:
        Dict with success, output
    """
    try:
        cmd = f'python3 {script_path} {args}'
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=60
        )

        success = result.returncode == 0

        return {
            'success': success,
            'output': result.stdout,
            'error': result.stderr if not success else None
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def test_experiment_first_workflow():
    """
    Test Experiment-First pattern workflow (pattern override)

    Returns:
        Dict with test results
    """
    print("=" * 80)
    print("TEST: Experiment-First Pattern Workflow (Pattern Override)")
    print("=" * 80)

    # Similar structure but with pattern override
    temp_dir = Path(tempfile.mkdtemp())
    workspace = temp_dir / 'test-project'

    try:
        # Bootstrap + evaluation with pattern override
        print("\n[1] Bootstrap...")
        run_skill(
            'skills/omr-bootstrap/scripts/bootstrap_workspace.py',
            'test-project "Test"',
            cwd=temp_dir
        )
        print("✓ Bootstrap complete")

        # Evaluation with pattern override
        print("\n[2] Run evaluation (pattern override)...")
        result = run_skill(
            'skills/omr-evaluation/run_evaluation.py',
            str(workspace) + ' --pattern-override'
        )
        assert result['success'], "Evaluation with override failed"
        print("✓ Evaluation complete (pattern override working)")

        print("\n" + "=" * 80)
        print("TEST RESULT: ✓ EXPERIMENT-FIRST WORKING")
        print("=" * 80)

        return {
            'status': 'passed',
            'pattern_override': True
        }

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {str(e)}")
        return {
            'status': 'failed',
            'error': str(e)
        }

    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)


def test_loop_pattern_smoke():
    """
    Smoke test: Loop pattern loads, gate_l validates, loop_state + detect work.

    Returns:
        Dict with test results
    """
    print("=" * 80)
    print("TEST: Loop Pattern + Gate L Smoke")
    print("=" * 80)

    core_dir = Path(__file__).parent.parent
    temp_dir = Path(tempfile.mkdtemp())
    workspace = temp_dir / 'loop-workspace'

    try:
        import json
        import importlib.util

        # Load Loop pattern
        print("\n[1] Load patterns/loop.json...")
        loop_path = core_dir / 'patterns' / 'loop.json'
        assert loop_path.exists(), "Missing patterns/loop.json"
        loop = json.loads(loop_path.read_text())
        assert loop['name'] == 'Loop'
        assert 'cycles' in loop['graph']
        assert set(loop.get('loop_modes', [])) == {'idea-dev', 'deep-analyze'}
        assert loop['skill_gates'].get('omr-analyze') == 'gate_l'
        print("✓ Loop pattern loaded")

        # Validate contracts including gate_l
        print("\n[2] Validate contracts (gate_l)...")
        vc_spec = importlib.util.spec_from_file_location(
            'validate_contract', core_dir / 'scripts' / 'validate_contract.py'
        )
        vc_mod = importlib.util.module_from_spec(vc_spec)
        vc_spec.loader.exec_module(vc_mod)

        schema_path = core_dir / 'schemas' / 'contract.schema.json'
        for name in ('omr-analyze.json', 'omr-idea-note.json'):
            ok, err = vc_mod.validate_contract(core_dir / 'contracts' / name, schema_path)
            assert ok, f"{name}: {err}"
            contract = json.loads((core_dir / 'contracts' / name).read_text())
            gate_ids = [g['id'] for g in contract['gates']]
            assert 'gate_l' in gate_ids, f"{name} missing gate_l"
            print(f"  ✓ {name}")

        # loop_state helper
        print("\n[3] Exercise loop_state.py...")
        spec = importlib.util.spec_from_file_location(
            'loop_state', core_dir / 'scripts' / 'loop_state.py'
        )
        loop_state = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loop_state)

        workspace.mkdir(parents=True)
        (workspace / '.omr').mkdir()
        state = loop_state.activate_loop(
            workspace, mode='deep-analyze', focus_question='lifecycle gaps'
        )
        assert state['active'] is True
        assert loop_state.is_loop_active(workspace) is True
        state = loop_state.record_iteration(
            workspace, last_delta='filled gap G1', gaps=['G2']
        )
        assert state['iteration'] == 1
        assert loop_state.get_gaps(workspace) == ['G2']
        state = loop_state.advance_loop(workspace)
        assert state['active'] is False
        print("✓ loop_state activate / iterate / advance")

        # Pattern detection boost for cyclic sequence
        print("\n[4] Detect Loop from cyclic sequence...")
        tree_state = {
            'completed': [
                'omr-collection',
                'omr-analyze',
                'omr-collection',
                'omr-analyze',
            ]
        }
        (workspace / '.omr' / 'tree-state.json').write_text(
            json.dumps(tree_state, indent=2)
        )

        detect_spec = importlib.util.spec_from_file_location(
            'detect_pattern', core_dir / 'scripts' / 'detect_pattern.py'
        )
        detect_mod = importlib.util.module_from_spec(detect_spec)
        detect_spec.loader.exec_module(detect_mod)
        result = detect_mod.detect_pattern(workspace)
        assert result['status'] == 'detected', result
        assert result['pattern_name'] == 'Loop', result
        print(f"✓ Detected Loop (score={result['match_score']:.2f})")

        print("\n" + "=" * 80)
        print("TEST RESULT: ✓ LOOP SMOKE PASSED")
        print("=" * 80)

        return {'status': 'passed', 'pattern': 'Loop'}

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {str(e)}")
        return {'status': 'failed', 'error': str(e)}

    except Exception as e:
        print(f"\n✗ TEST ERROR: {str(e)}")
        return {'status': 'error', 'error': str(e)}

    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)


def main():
    """Run all end-to-end tests"""
    print("\nRunning all end-to-end tests...\n")

    results = []

    # Test 1: Evidence-First
    result1 = test_evidence_first_workflow()
    results.append(('Evidence-First', result1))

    # Test 2: Experiment-First (pattern override)
    result2 = test_experiment_first_workflow()
    results.append(('Experiment-First', result2))

    # Test 3: Loop pattern + Gate L smoke
    result3 = test_loop_pattern_smoke()
    results.append(('Loop', result3))

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    passed = sum(1 for _, r in results if r['status'] == 'passed')
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result['status'] == 'passed' else "✗ FAIL"
        print(f"{name}: {status}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n✓ ALL TESTS PASSED")
        sys.exit(0)
    else:
        print("\n✗ SOME TESTS FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()