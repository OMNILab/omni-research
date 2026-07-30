#!/usr/bin/env python3
"""
Simple Skill Packager - Creates .skill ZIP files without external dependencies
"""

import fnmatch
import sys
import zipfile
from pathlib import Path

# Patterns to exclude when packaging
EXCLUDE_DIRS = {"__pycache__", "node_modules", "evals"}
EXCLUDE_GLOBS = {"*.pyc"}
EXCLUDE_FILES = {".DS_Store"}

def should_exclude(rel_path: Path, is_root_check: bool = False) -> bool:
    """Check if path should be excluded"""
    parts = rel_path.parts

    # Exclude specific directories
    if any(part in EXCLUDE_DIRS for part in parts):
        return True

    # Exclude root-level evals directory
    if is_root_check and parts and parts[0] == "evals":
        return True

    # Exclude specific file patterns
    if any(fnmatch.fnmatch(rel_path.name, glob) for glob in EXCLUDE_GLOBS):
        return True

    # Exclude specific files
    if rel_path.name in EXCLUDE_FILES:
        return True

    return False

def package_skill(skill_dir: Path, output_dir: Path) -> bool:
    """
    Package a skill directory into a .skill ZIP file

    Args:
        skill_dir: Path to skill directory
        output_dir: Path to output directory

    Returns:
        True if successful, False otherwise
    """
    if not skill_dir.exists():
        print(f"❌ Skill directory not found: {skill_dir}")
        return False

    # Check for SKILL.md
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print(f"❌ SKILL.md not found in: {skill_dir}")
        return False

    skill_name = skill_dir.name
    skill_file = output_dir / f"{skill_name}.skill"

    print(f"📦 Packaging {skill_name}...")

    # Create ZIP archive
    try:
        with zipfile.ZipFile(skill_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk skill directory
            for file_path in skill_dir.rglob('*'):
                if file_path.is_file():
                    # Get relative path from skill directory (NO skill name prefix)
                    rel_path = file_path.relative_to(skill_dir)

                    # Check if should exclude
                    is_root_check = len(rel_path.parts) == 1
                    if should_exclude(rel_path, is_root_check):
                        continue

                    # Add to archive (skill name will be added by unzip process)
                    zipf.write(file_path, rel_path)

        size_kb = skill_file.stat().st_size / 1024
        print(f"  ✓ Created {skill_file.name} ({size_kb:.1f} KB)")
        return True

    except Exception as e:
        print(f"  ❌ Failed: {e}")
        return False

def package_all_skills(skills_dir: Path, output_dir: Path, skills_list: list = None) -> tuple:
    """
    Package all skills

    Args:
        skills_dir: Path to skills directory
        output_dir: Path to output directory
        skills_list: List of skills to package

    Returns:
        Tuple of (success_count, fail_count)
    """
    if skills_list is None:
        # Auto-discover skills
        skills_list = [d.name for d in skills_dir.iterdir()
                       if d.is_dir() and d.name.startswith('omr-')]

    # Sort to ensure omr-core is first
    skills_list = sorted(skills_list, key=lambda s: (0 if s == 'omr-core' else 1, s))

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"PACKAGING OMNIRESEARCH SKILLS")
    print(f"{'='*60}")
    print(f"Skills to package: {len(skills_list)}")
    print(f"Output directory: {output_dir}")

    success_count = 0
    fail_count = 0

    for skill_name in skills_list:
        skill_dir = skills_dir / skill_name
        success = package_skill(skill_dir, output_dir)

        if success:
            success_count += 1
        else:
            fail_count += 1

    # Summary
    print(f"\n{'='*60}")
    print(f"PACKAGING SUMMARY")
    print(f"{'='*60}")
    print(f"✓ Packaged: {success_count}/{len(skills_list)}")
    print(f"❌ Failed: {fail_count}/{len(skills_list)}")

    # List generated files
    if success_count > 0:
        print(f"\nGenerated .skill files:")
        for skill_name in skills_list:
            skill_file = output_dir / f"{skill_name}.skill"
            if skill_file.exists():
                size_kb = skill_file.stat().st_size / 1024
                print(f"  - {skill_file.name} ({size_kb:.1f} KB)")

    return success_count, fail_count

def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python simple_package_skill.py <output-directory> [--skills skill1,skill2,...]")
        print("Example: python simple_package_skill.py ./dist")
        print("         python simple_package_skill.py ./dist --skills omr-core,omr-bootstrap")
        sys.exit(1)

    output_dir = Path(sys.argv[1])
    skills_list = None

    if '--skills' in sys.argv:
        idx = sys.argv.index('--skills')
        if idx + 1 < len(sys.argv):
            skills_list = [s.strip() for s in sys.argv[idx + 1].split(',')]

    skills_dir = Path(__file__).parent.parent

    success, fail = package_all_skills(skills_dir, output_dir, skills_list)

    sys.exit(0 if fail == 0 else 1)

if __name__ == "__main__":
    main()