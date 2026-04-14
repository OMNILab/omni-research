#!/usr/bin/env python3
"""
Standalone test for title slugification (doesn't require handler dependencies)
"""

import re

def slugify_title(title: str) -> str:
    """
    Convert paper title to URL-safe slug

    Args:
        title: Paper title string

    Returns:
        Slug string (lowercase, hyphens, no special chars)
    """
    # Convert to lowercase
    slug = title.lower()

    # Replace spaces and underscores with hyphens
    slug = re.sub(r'[\s_]+', '-', slug)

    # Remove special characters (keep only alphanumeric and hyphens)
    slug = re.sub(r'[^a-z0-9-]', '', slug)

    # Collapse multiple hyphens
    slug = re.sub(r'-{2,}', '-', slug)

    # Trim hyphens from start/end
    slug = slug.strip('-')

    # Limit length (max 100 chars to keep filenames manageable)
    if len(slug) > 100:
        # Truncate to exactly 100 chars, then remove trailing hyphen if present
        slug = slug[:100]
        if slug.endswith('-'):
            slug = slug[:-1]

    return slug

def test_slugify():
    """Test slugification with various title formats"""
    test_cases = [
        # (input_title, expected_slug)
        ("RU-UA Conflict Research Report", "ru-ua-conflict-research-report"),
        ("Neural Networks for Machine Learning", "neural-networks-for-machine-learning"),
        ("A Study on AI & Machine Learning (Part 1)", "a-study-on-ai-machine-learning-part-1"),
        ("Paper  with  multiple   spaces", "paper-with-multiple-spaces"),
        ("Paper_with_underscores", "paper-with-underscores"),
        ("Special@#Characters!$Here", "specialcharactershere"),
        ("123 Numbers in Title", "123-numbers-in-title"),
        ("  Leading and Trailing Spaces  ", "leading-and-trailing-spaces"),
        ("Very Long Title That Should Be Truncated Because It Exceeds The Maximum Length Limit For File Names In The System And Needs To Be Shortened",
         "very-long-title-that-should-be-truncated-because-it-exceeds-the-maximum-length-limit-for-file-names"),
        ("Title---With---Multiple---Hyphens", "title-with-multiple-hyphens"),
    ]

    print("Slugify Title Tests")
    print("=" * 80)

    all_passed = True
    for title, expected in test_cases:
        result = slugify_title(title)
        passed = result == expected

        status = "✓" if passed else "✗"
        print(f"{status} Input:    '{title}'")
        print(f"   Expected: '{expected}'")
        print(f"   Result:   '{result}'")

        if not passed:
            print(f"   ERROR: Mismatch!")
            all_passed = False

        print()

    print("=" * 80)
    if all_passed:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

def main():
    exit_code = test_slugify()
    sys.exit(exit_code)

if __name__ == "__main__":
    import sys
    main()