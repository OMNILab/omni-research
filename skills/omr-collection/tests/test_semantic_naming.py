#!/usr/bin/env python3
"""
Test semantic paper naming for PDF URLs
"""

import sys
from pathlib import Path

# Add handlers to path
skill_root = Path(__file__).parent.parent
if str(skill_root) not in sys.path:
    sys.path.insert(0, str(skill_root))

from handlers.paper_handler import PaperHandler

def test_slugify_title():
    """Test title slugification"""
    handler = PaperHandler(Path("/tmp/test"))

    # Test cases
    test_cases = [
        ("RU-UA Conflict Research Report", "ru-ua-conflict-research-report"),
        ("Neural Networks for Machine Learning", "neural-networks-for-machine-learning"),
        ("A Study on AI & Machine Learning (Part 1)", "a-study-on-ai-machine-learning-part-1"),
        ("Paper  with  multiple   spaces", "paper-with-multiple-spaces"),
        ("Paper_with_underscores", "paper-with-underscores"),
        ("Very Long Title That Should Be Truncated Because It Exceeds The Maximum Length Limit For File Names", "very-long-title-that-should-be-truncated-because-it-exceeds-the-maximum-length-limit-for-"),
    ]

    print("Testing slugify_title:")
    print("-" * 80)
    for title, expected in test_cases:
        result = handler._slugify_title(title)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{title}'")
        print(f"  Expected: {expected}")
        print(f"  Result:   {result}")
        if result != expected:
            print(f"  ERROR: Mismatch!")
        print()

    return all(handler._slugify_title(title) == expected for title, expected in test_cases)

def test_output_path_naming():
    """Test output path generation for different source types"""
    handler = PaperHandler(Path("/tmp/test"))

    print("Testing output path naming:")
    print("-" * 80)

    # DOI paper
    doi_path = handler.get_output_path("10.1234/example-paper")
    print(f"DOI paper:")
    print(f"  Source: 10.1234/example-paper")
    print(f"  Path:   {doi_path.name}")
    expected_doi = "doi-10-1234-example-paper.md"
    doi_ok = doi_path.name == expected_doi
    print(f"  {'✓' if doi_ok else '✗'} Expected: {expected_doi}")
    print()

    # arXiv paper
    arxiv_path = handler.get_output_path("2402.12345")
    print(f"arXiv paper:")
    print(f"  Source: 2402.12345")
    print(f"  Path:   {arxiv_path.name}")
    expected_arxiv = "arxiv-2402-12345.md"
    arxiv_ok = arxiv_path.name == expected_arxiv
    print(f"  {'✓' if arxiv_ok else '✗'} Expected: {expected_arxiv}")
    print()

    # PDF URL with title metadata
    pdf_url = "https://example.com/paper.pdf"
    metadata_with_title = {"title": "RU-UA Conflict Research Report"}
    semantic_path = handler.get_output_path(pdf_url, metadata_with_title)
    print(f"PDF URL with title:")
    print(f"  Source: {pdf_url}")
    print(f"  Metadata: {metadata_with_title}")
    print(f"  Path:   {semantic_path.name}")
    expected_semantic = "paper-ru-ua-conflict-research-report.md"
    semantic_ok = semantic_path.name == expected_semantic
    print(f"  {'✓' if semantic_ok else '✗'} Expected: {expected_semantic}")
    print()

    # PDF URL without title metadata (fallback)
    pdf_url_no_title = "https://example.com/another.pdf"
    metadata_no_title = {}
    fallback_path = handler.get_output_path(pdf_url_no_title, metadata_no_title)
    print(f"PDF URL without title (fallback):")
    print(f"  Source: {pdf_url_no_title}")
    print(f"  Metadata: {metadata_no_title}")
    print(f"  Path:   {fallback_path.name}")
    # Should be url-{hash}.md format
    fallback_ok = fallback_path.name.startswith("url-") and fallback_path.name.endswith(".md")
    print(f"  {'✓' if fallback_ok else '✗'} Expected: url-{hash}.md format")
    print()

    return doi_ok and arxiv_ok and semantic_ok and fallback_ok

def main():
    print("=" * 80)
    print("Semantic Paper Naming Tests")
    print("=" * 80)
    print()

    test1_ok = test_slugify_title()
    test2_ok = test_output_path_naming()

    print("=" * 80)
    if test1_ok and test2_ok:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    print("=" * 80)

if __name__ == "__main__":
    main()