#!/usr/bin/env python3
"""
Package All OmniResearch Skills for Marketplace Distribution
Creates .skill ZIP archives for all OmniResearch skills using skill-creator's package_skill.py
"""

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

# Skills to package in dependency order (omr-core first)
SKILLS_TO_PACKAGE = [
    'omr-core',           # Foundation infrastructure (must be first)
    'omr-bootstrap',      # Project initializer
    'omr-collection',     # Material collection
    'omr-evidence',       # Evidence extraction
    'omr-research-plan',  # Research planning
    'omr-decision',       # Architecture decisions
    'omr-evaluation',     # Experiment execution
    'omr-synthesis',      # Findings synthesis
    'omr-wiki',           # Wiki generation
    'omr-idea-note',      # Idea capture
    'omr-reconcile',      # Reconciliation
    'omr-research-archive'  # Archiving
]

def find_package_script() -> Path:
    """
    Locate skill-creator's package_skill.py script

    Returns:
        Path to package_skill.py

    Raises:
        FileNotFoundError: If package_skill.py not found
    """
    # Try multiple locations where skill-creator might be installed
    possible_locations = [
        Path.home() / '.claude' / 'skills' / 'skill-creator' / 'scripts' / 'package_skill.py',
        Path.home() / '.claude' / 'plugins' / 'marketplaces' / 'claude-plugins-official' /
            'plugins' / 'skill-creator' / 'skills' / 'skill-creator' / 'scripts' / 'package_skill.py',
        Path('/usr/local/share/claude/skills/skill-creator/scripts/package_skill.py'),
        Path('/opt/claude/skills/skill-creator/scripts/package_skill.py')
    ]

    for location in possible_locations:
        if location.exists():
            return location

    raise FileNotFoundError(
        "package_skill.py not found. Install skill-creator skill first.\n"
        "Tried locations:\n" +
        "\n".join([f"  - {loc}" for loc in possible_locations])
    )

def package_single_skill(skill_name: str,
                         skills_dir: Path,
                         output_dir: Path,
                         package_script: Path) -> Tuple[bool, str]:
    """
    Package a single skill as .skill ZIP archive

    Args:
        skill_name: Skill directory name
        skills_dir: Path to skills/ directory
        output_dir: Path to output directory for .skill files
        package_script: Path to package_skill.py

    Returns:
        Tuple of (success, message)
    """
    skill_path = skills_dir / skill_name

    if not skill_path.exists():
        return False, f"Skill directory not found: {skill_path}"

    print(f"\n📦 Packaging {skill_name}...")

    # Run package_skill.py
    result = subprocess.run(
        [sys.executable, str(package_script), str(skill_path), str(output_dir)],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        skill_file = output_dir / f"{skill_name}.skill"
        if skill_file.exists():
            # Get file size
            size_kb = skill_file.stat().st_size / 1024
            return True, f"✓ Created {skill_file.name} ({size_kb:.1f} KB)"
        else:
            return False, f"Package command succeeded but .skill file not found"
    else:
        error_msg = result.stderr.strip() if result.stderr else result.stdout.strip()
        return False, f"❌ Failed: {error_msg}"

def package_all_skills(skills_dir: Path,
                       output_dir: Path,
                       skills_list: List[str] = None) -> Tuple[List[str], List[str]]:
    """
    Package all OmniResearch skills

    Args:
        skills_dir: Path to skills/ directory
        output_dir: Path to output directory for .skill files
        skills_list: Optional list of skills to package (defaults to SKILLS_TO_PACKAGE)

    Returns:
        Tuple of (packaged_skills, failed_skills)
    """
    if skills_list is None:
        skills_list = SKILLS_TO_PACKAGE

    # Find package_skill.py
    try:
        package_script = find_package_script()
        print(f"✓ Found packaging script: {package_script}")
    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        return [], skills_list

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Output directory: {output_dir}")

    print(f"\n{'='*60}")
    print(f"PACKAGING OMNIRESEARCH SKILLS")
    print(f"{'='*60}")
    print(f"Skills to package: {len(skills_list)}")

    # Package each skill
    packaged = []
    failed = []

    for skill_name in skills_list:
        success, message = package_single_skill(skill_name, skills_dir, output_dir, package_script)
        print(f"  {message}")

        if success:
            packaged.append(skill_name)
        else:
            failed.append(skill_name)

    # Summary
    print(f"\n{'='*60}")
    print(f"PACKAGING SUMMARY")
    print(f"{'='*60}")
    print(f"✓ Packaged: {len(packaged)}/{len(skills_list)} skills")
    print(f"❌ Failed: {len(failed)}/{len(skills_list)} skills")

    if packaged:
        print(f"\nSuccess: {', '.join(packaged)}")

    if failed:
        print(f"\nFailed: {', '.join(failed)}")
        print(f"\n⚠ Some skills failed to package. Check errors above.")

    # List generated files
    if packaged:
        print(f"\nGenerated files in {output_dir}:")
        for skill_name in packaged:
            skill_file = output_dir / f"{skill_name}.skill"
            if skill_file.exists():
                size_kb = skill_file.stat().st_size / 1024
                print(f"  - {skill_file.name} ({size_kb:.1f} KB)")

    return packaged, failed

def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python package_all_skills.py <output-directory>")
        print("Example: python package_all_skills.py ./dist")
        print("\nOptional arguments:")
        print("  --skills <skill1,skill2,...>  Package specific skills only")
        print("\nThis script creates .skill ZIP archives for all OmniResearch skills.")
        print("Requires skill-creator to be installed (provides package_skill.py)")
        sys.exit(1)

    # Parse arguments
    output_dir = Path(sys.argv[1])
    skills_list = None

    if '--skills' in sys.argv:
        skills_arg_index = sys.argv.index('--skills')
        if skills_arg_index + 1 < len(sys.argv):
            skills_arg = sys.argv[skills_arg_index + 1]
            skills_list = [s.strip() for s in skills_arg.split(',')]

    # Determine skills directory
    skills_dir = Path(__file__).parent.parent  # scripts/ -> skills/

    if not skills_dir.exists():
        print(f"Error: Skills directory not found: {skills_dir}")
        sys.exit(1)

    # Package all skills
    packaged, failed = package_all_skills(skills_dir, output_dir, skills_list)

    # Exit with appropriate status
    sys.exit(0 if len(failed) == 0 else 1)

if __name__ == "__main__":
    main()