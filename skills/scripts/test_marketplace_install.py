#!/usr/bin/env python3
"""
Test Marketplace Installation for OmniResearch Skills
Simulates marketplace install workflow and verifies packaged skills work correctly
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Tuple

def test_skill_file_exists(skill_file: Path) -> bool:
    """
    Test that .skill file exists and is valid ZIP

    Args:
        skill_file: Path to .skill file

    Returns:
        True if valid, False otherwise
    """
    if not skill_file.exists():
        print(f"  ❌ File not found: {skill_file}")
        return False

    # Test ZIP structure
    result = subprocess.run(
        ['unzip', '-t', str(skill_file)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"  ❌ Invalid ZIP: {result.stderr}")
        return False

    return True

def install_skill_to_marketplace(skill_file: Path, skills_dir: Path) -> Path:
    """
    Simulate marketplace installation by unzipping .skill to skills directory

    Args:
        skill_file: Path to .skill file
        skills_dir: Path to skills installation directory

    Returns:
        Path to installed skill directory
    """
    skill_name = skill_file.stem
    skill_install_dir = skills_dir / skill_name

    # Clean existing installation
    if skill_install_dir.exists():
        shutil.rmtree(skill_install_dir)

    # Unzip .skill file to skill-specific directory (overwrite mode)
    skill_install_dir.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ['unzip', '-q', '-o', str(skill_file), '-d', str(skill_install_dir)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"Failed to unzip: {result.stderr}")

    return skill_install_dir

def validate_skill_structure(skill_install_dir: Path) -> Tuple[bool, List[str]]:
    """
    Validate installed skill directory structure

    Args:
        skill_install_dir: Path to installed skill

    Returns:
        Tuple of (is_valid, issues)
    """
    issues = []

    # Check SKILL.md exists
    skill_md = skill_install_dir / 'SKILL.md'
    if not skill_md.exists():
        issues.append("SKILL.md missing")

    # Check SKILL.md frontmatter
    if skill_md.exists():
        content = skill_md.read_text()
        if not content.startswith('---'):
            issues.append("SKILL.md missing YAML frontmatter")
        elif 'name:' not in content or 'description:' not in content:
            issues.append("SKILL.md missing required frontmatter fields")
        elif 'version:' not in content:
            issues.append("SKILL.md missing version field (marketplace requirement)")

    # Check for runtime_utils.py in domain skills
    skill_name = skill_install_dir.name
    if skill_name != 'omr-core':
        # Domain skills should have runtime_utils.py
        runtime_utils = None

        # Check in scripts/ directory (omr-bootstrap)
        if (skill_install_dir / 'scripts' / 'runtime_utils.py').exists():
            runtime_utils = skill_install_dir / 'scripts' / 'runtime_utils.py'
        # Check in skill root (other skills)
        elif (skill_install_dir / 'runtime_utils.py').exists():
            runtime_utils = skill_install_dir / 'runtime_utils.py'

        if not runtime_utils:
            issues.append("runtime_utils.py missing (required for infrastructure loading)")

    return len(issues) == 0, issues

def test_skill_installation(skill_file: Path,
                             skills_dir: Path,
                             test_workspace: Path) -> Dict:
    """
    Test complete skill installation and execution

    Args:
        skill_file: Path to .skill file
        skills_dir: Path to skills installation directory
        test_workspace: Path to test workspace

    Returns:
        Dict with test results
    """
    skill_name = skill_file.stem
    results = {
        'skill_name': skill_name,
        'file_valid': False,
        'install_success': False,
        'structure_valid': False,
        'issues': [],
        'details': []
    }

    print(f"\n🧪 Testing {skill_name}...")

    # 1. Test file validity
    results['file_valid'] = test_skill_file_exists(skill_file)
    if results['file_valid']:
        results['details'].append(f"✓ .skill file valid")

    # 2. Install skill
    try:
        skill_install_dir = install_skill_to_marketplace(skill_file, skills_dir)
        results['install_success'] = True
        results['details'].append(f"✓ Installed to {skill_install_dir}")
    except Exception as e:
        results['issues'].append(f"Installation failed: {e}")
        return results

    # 3. Validate structure
    is_valid, issues = validate_skill_structure(skill_install_dir)
    results['structure_valid'] = is_valid
    results['issues'].extend(issues)

    if is_valid:
        results['details'].append(f"✓ Skill structure valid")

    # 4. Skill-specific tests
    if skill_name == 'omr-core':
        # Test infrastructure initialization
        init_script = skill_install_dir / 'scripts' / 'init_workspace.py'
        if init_script.exists():
            # Create test workspace
            test_project = test_workspace / 'test-project'
            test_project.mkdir(parents=True, exist_ok=True)

            result = subprocess.run(
                [sys.executable, str(init_script), str(test_project)],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                results['details'].append(f"✓ Infrastructure initialization successful")

                # Verify infrastructure files
                contracts_dir = test_project / 'skills' / 'contracts'
                if contracts_dir.exists() and len(list(contracts_dir.glob('*.json'))) > 0:
                    results['details'].append(f"✓ Contracts installed in workspace")
                else:
                    results['issues'].append("Contracts not installed in workspace")
            else:
                results['issues'].append(f"Init failed: {result.stderr}")

    elif skill_name == 'omr-bootstrap':
        # Test workspace creation
        bootstrap_script = skill_install_dir / 'scripts' / 'bootstrap_workspace.py'
        if bootstrap_script.exists():
            result = subprocess.run(
                [sys.executable, str(bootstrap_script),
                 'test-project', 'Test research question?'],
                cwd=str(test_workspace),
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                results['details'].append(f"✓ Workspace creation successful")

                # Verify workspace structure
                test_project = test_workspace / 'test-project'
                claude_md = test_project / 'CLAUDE.md'
                if claude_md.exists():
                    results['details'].append(f"✓ CLAUDE.md generated")
                else:
                    results['issues'].append("CLAUDE.md not generated")
            else:
                results['issues'].append(f"Bootstrap failed: {result.stderr}")

    else:
        # Generic skill test - verify SKILL.md and runtime_utils
        if results['structure_valid']:
            results['details'].append(f"✓ Skill structure valid (execution test skipped)")

    return results

def test_marketplace_workflow(dist_dir: Path) -> bool:
    """
    Test complete marketplace workflow:
    1. Verify all .skill files exist
    2. Install skills to marketplace location
    3. Verify infrastructure loading works

    Args:
        dist_dir: Path to dist/ directory containing .skill files

    Returns:
        True if all tests pass, False otherwise
    """
    print(f"\n{'='*70}")
    print(f"MARKETPLACE INSTALLATION TEST")
    print(f"{'='*70}")
    print(f"Testing skills from: {dist_dir}")

    # Find all .skill files
    skill_files = sorted(dist_dir.glob('*.skill'))

    if not skill_files:
        print("❌ No .skill files found in dist/")
        return False

    print(f"\nFound {len(skill_files)} skill files to test")

    # Test skills in isolated environment
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = Path(tmpdir)
        skills_install_dir = test_dir / '.claude' / 'skills'
        test_workspace = test_dir / 'workspace'

        skills_install_dir.mkdir(parents=True, exist_ok=True)
        test_workspace.mkdir(parents=True, exist_ok=True)

        # Test each skill
        all_results = []
        for skill_file in skill_files:
            result = test_skill_installation(skill_file, skills_install_dir, test_workspace)
            all_results.append(result)

        # Print results
        print(f"\n{'='*70}")
        print(f"TEST RESULTS")
        print(f"{'='*70}")

        passed = [r for r in all_results if r['structure_valid'] and len(r['issues']) == 0]
        failed = [r for r in all_results if not r['structure_valid'] or len(r['issues']) > 0]

        print(f"\n✓ Passed: {len(passed)}/{len(all_results)}")
        for r in passed:
            print(f"  {r['skill_name']}: {', '.join(r['details'])}")

        if failed:
            print(f"\n❌ Failed: {len(failed)}/{len(all_results)}")
            for r in failed:
                print(f"  {r['skill_name']}:")
                for issue in r['issues']:
                    print(f"    - {issue}")

        # Print detailed results for failed skills
        if failed:
            print(f"\n{'='*70}")
            print(f"FAILURE DETAILS")
            print(f"{'='*70}")
            for r in failed:
                if r['details']:
                    print(f"\n{r['skill_name']} details:")
                    for detail in r['details']:
                        print(f"  {detail}")

        return len(failed) == 0

def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python test_marketplace_install.py <dist-directory>")
        print("Example: python test_marketplace_install.py ./dist")
        print("\nThis script tests that packaged .skill files can be installed and work correctly.")
        sys.exit(1)

    dist_dir = Path(sys.argv[1])

    if not dist_dir.exists():
        print(f"Error: Dist directory not found: {dist_dir}")
        sys.exit(1)

    success = test_marketplace_workflow(dist_dir)

    if success:
        print(f"\n✅ All tests passed - marketplace installation verified")
        sys.exit(0)
    else:
        print(f"\n❌ Some tests failed - see details above")
        sys.exit(1)

if __name__ == "__main__":
    main()