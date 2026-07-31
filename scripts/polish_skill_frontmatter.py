#!/usr/bin/env python3
"""
Polish SKILL.md frontmatter according to agent skill specification
"""

import re
from pathlib import Path


def yaml_scalar(value) -> str:
    """Render a frontmatter value, quoting it when a plain scalar would be ambiguous.

    A plain YAML scalar cannot contain ": " or " #", and cannot end with ":", because
    those read as a mapping separator or a comment. Values that are already quoted or
    are flow collections ([...] / {...}) are passed through untouched.
    """
    text = str(value)
    if not text or text[0] in "'\"[{":
        return text
    if ": " not in text and " #" not in text and not text.endswith(":"):
        return text
    return "'" + text.replace("'", "''") + "'"


def polish_frontmatter(skill_dir: Path):
    """Polish SKILL.md frontmatter to match agent skill spec"""

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print(f"No SKILL.md in {skill_dir}")
        return

    content = skill_md.read_text()

    # Extract frontmatter
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if not match:
        print(f"No frontmatter in {skill_md}")
        return

    frontmatter_lines = match.group(1).split("\n")
    body = match.group(2)

    # Parse frontmatter into dict
    frontmatter = {}
    in_metadata = False
    metadata_values = {}

    for line in frontmatter_lines:
        if not line.strip():
            continue

        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            if key == "metadata":
                in_metadata = True
                frontmatter["metadata"] = {}
            elif in_metadata:
                if key in [
                    "requires_skills",
                    "provides",
                    "required_for",
                    "enhancements",
                ]:
                    # Convert arrays to space-separated strings
                    if value.startswith("["):
                        value = (
                            value.replace("[", "")
                            .replace("]", "")
                            .replace(",", " ")
                            .replace('"', "")
                            .strip()
                        )
                    metadata_values[key] = value
                else:
                    metadata_values[key] = value
            else:
                # Move version and author to metadata
                if key in ["version", "author"]:
                    metadata_values[key] = value
                else:
                    frontmatter[key] = value

    # Ensure metadata has version and author
    if "metadata" not in frontmatter:
        frontmatter["metadata"] = {}

    for key, value in metadata_values.items():
        frontmatter["metadata"][key] = value

    # Build polished frontmatter
    polished_lines = ["---"]

    # Required fields first
    polished_lines.append(f"name: {yaml_scalar(frontmatter.get('name', skill_dir.name))}")

    # Description (ensure <1024 chars)
    desc = frontmatter.get("description", "")
    if len(desc) > 1024:
        desc = desc[:1020] + "..."
    polished_lines.append(f"description: {yaml_scalar(desc)}")

    # Optional: license
    if "license" in frontmatter:
        polished_lines.append(f"license: {yaml_scalar(frontmatter['license'])}")

    # Optional: compatibility
    if "compatibility" in frontmatter:
        polished_lines.append(f"compatibility: {yaml_scalar(frontmatter['compatibility'])}")

    # Optional: metadata
    if "metadata" in frontmatter and frontmatter["metadata"]:
        polished_lines.append("metadata:")
        for key, value in sorted(frontmatter["metadata"].items()):
            polished_lines.append(f"  {key}: {yaml_scalar(value)}")

    polished_lines.append("---")

    # Write polished content
    polished_content = "\n".join(polished_lines) + "\n\n" + body

    skill_md.write_text(polished_content)
    print(f"Polished: {skill_dir.name}")


def main():
    skills_dir = Path(__file__).parent.parent

    for skill in skills_dir.glob("omr-*"):
        if skill.is_dir():
            polish_frontmatter(skill)


if __name__ == "__main__":
    main()
