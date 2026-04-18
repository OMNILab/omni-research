#!/usr/bin/env python3
"""
Organize skill directory structures per agent skill specification
"""

import shutil
from pathlib import Path

def organize_skill(skill_dir: Path):
    """Organize skill directory to match spec"""

    skill_name = skill_dir.name
    print(f"\n=== Organizing {skill_name} ===")

    # Create scripts directory
    scripts_dir = skill_dir / 'scripts'
    scripts_dir.mkdir(exist_ok=True)

    # Move all .py files from root to scripts
    py_files = list(skill_dir.glob('*.py'))

    if py_files:
        print(f"Found {len(py_files)} Python files in root")
        for py_file in py_files:
            dest = scripts_dir / py_file.name
            if not dest.exists():
                shutil.move(str(py_file), str(dest))
                print(f"  Moved: {py_file.name}")
            else:
                print(f"  Already exists: {py_file.name}")
    else:
        print("No Python files in root")

    # Rename templates to assets (if exists)
    templates_dir = skill_dir / 'templates'
    assets_dir = skill_dir / 'assets'

    if templates_dir.exists() and not assets_dir.exists():
        shutil.move(str(templates_dir), str(assets_dir))
        print(f"Renamed: templates -> assets")
    elif assets_dir.exists():
        print(f"assets directory already exists")

    # Verify structure
    print(f"\nFinal structure for {skill_name}:")
    print(f"  Root files: {[f.name for f in skill_dir.iterdir() if f.is_file()]}")
    print(f"  Root dirs: {[d.name for d in skill_dir.iterdir() if d.is_dir() and d.name != '__pycache__']}")

def main():
    skills_dir = Path(__file__).parent.parent

    print("Organizing all skills per agent skill specification...")

    for skill in sorted(skills_dir.glob('omr-*')):
        if skill.is_dir():
            organize_skill(skill)

    print("\n" + "="*60)
    print("Organization complete!")
    print("="*60)

if __name__ == "__main__":
    main()