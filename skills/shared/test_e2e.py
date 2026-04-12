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
        raw_paper = workspace / 'raw' / 'paper'
        raw_paper.mkdir(parents=True, exist_ok=True)
        mock_paper = raw_paper / 'mock-paper.md'
        mock_paper.write_text("# Mock Paper\n\nContent about agent memory...\n")
        print("✓ Mock materials created")

        # Step 3: Evidence extraction
        print("\n[3] Extract evidence...")
        result = run_skill(
            'skills/omr-evidence/extract_evidence.py',
            str(workspace)
        )
        assert result['success'], "Evidence extraction failed"
        print("✓ Evidence extracted")

        # Step 4: Research planning (Gate A)
        print("\n[4] Research planning...")
        result = run_skill(
            'skills/omr-research-plan/plan_research.py',
            str(workspace)
        )
        assert result['success'], "Research planning failed"
        print("✓ Research plan complete (Gate A passed)")

        # Step 5: Decision (Gate B)
        print("\n[5] Make decision...")
        result = run_skill(
            'skills/omr-decision/make_decision.py',
            str(workspace)
        )
        assert result['success'], "Decision failed"
        print("✓ Decision made (Gate B passed)")

        # Step 6: Evaluation (Gate C)
        print("\n[6] Run evaluation...")
        result = run_skill(
            'skills/omr-evaluation/run_evaluation.py',
            str(workspace)
        )
        assert result['success'], "Evaluation failed"
        print("✓ Evaluation complete (Gate C passed)")

        # Step 7: Synthesis (Gate D)
        print("\n[7] Synthesize findings...")
        result = run_skill(
            'skills/omr-synthesis/synthesize_findings.py',
            str(workspace) + ' brief'
        )
        assert result['success'], "Synthesis failed"
        print("✓ Synthesis complete (Gate D passed)")

        # Step 8: Wiki generation
        print("\n[8] Generate wiki...")
        result = run_skill(
            'skills/omr-wiki/generate_wiki.py',
            str(workspace)
        )
        assert result['success'], "Wiki generation failed"
        print("✓ Wiki generated")

        # Verify all artifacts exist
        print("\n[9] Verify artifacts...")
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
        print("\n[10] Verify skill tree...")
        tree_state_path = workspace / 'skills' / 'tree-state.json'
        assert tree_state_path.exists(), "Tree state missing"

        import json
        state = json.loads(tree_state_path.read_text())
        completed = state.get('completed', [])

        expected_skills = [
            'omr-bootstrap',
            'omr-collection',
            'omr-evidence',
            'omr-research-plan',
            'omr-decision',
            'omr-evaluation',
            'omr-synthesis',
            'omr-wiki'
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