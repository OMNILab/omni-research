#!/usr/bin/env python3
"""
Input Router for omr-collection
Detects input type (URL, DOI, Arxiv ID, Search Query) and routes to appropriate handler
"""

import re
from typing import Tuple, Optional
from enum import Enum

class InputType(Enum):
    """Input type classification"""
    URL_HTTP = "url_http"
    URL_HTTPS = "url_https"
    DOI = "doi"
    ARXIV_ID = "arxiv_id"
    GITHUB_URL = "github_url"
    HUGGINGFACE_URL = "huggingface_url"
    SEARCH_QUERY = "search_query"
    LOCAL_PATH = "local_path"
    UNKNOWN = "unknown"

class InputRouter:
    """
    Routes inputs to appropriate handlers based on pattern matching
    """

    # Pattern definitions
    DOI_PATTERN = re.compile(r'^10\.\d{4,9}/[-._;()/:A-Z0-9]+$', re.IGNORECASE)
    ARXIV_ID_PATTERN = re.compile(r'^(\d{4}\.\d{4,5}|[a-z-]+/\d{7})$', re.IGNORECASE)
    ARXIV_URL_PATTERN = re.compile(r'arxiv\.org/(abs|pdf)/(\d{4}\.\d{4,5})', re.IGNORECASE)
    GITHUB_URL_PATTERN = re.compile(r'github\.com/([\w-]+)/([\w-]+)', re.IGNORECASE)
    HUGGINGFACE_URL_PATTERN = re.compile(r'huggingface\.co/(datasets|models)/([\w-]+)/([\w-]+)', re.IGNORECASE)
    PDF_URL_PATTERN = re.compile(r'https?://.*\.pdf$', re.IGNORECASE)
    URL_PATTERN = re.compile(r'^https?://', re.IGNORECASE)
    LOCAL_PATH_PATTERN = re.compile(r'^[./]|^[A-Za-z]:\\')  # Unix or Windows paths

    def classify_input(self, input_str: str) -> Tuple[InputType, Optional[str]]:
        """
        Classify input and extract relevant identifier

        Args:
            input_str: User input (URL, DOI, ID, query, path)

        Returns:
            (input_type, extracted_id)
        """
        input_str = input_str.strip()

        # Check for quoted string (explicit search marker)
        if input_str.startswith('"') and input_str.endswith('"'):
            return InputType.SEARCH_QUERY, input_str[1:-1]

        # Check for PDF URL first (route to paper handler)
        pdf_url_match = self.PDF_URL_PATTERN.search(input_str)
        if pdf_url_match:
            # Treat as paper for PDF conversion
            return InputType.URL_HTTPS, input_str  # Will be routed to paper handler based on .pdf extension

        # Check for arXiv URL first (extract ID)
        arxiv_match = self.ARXIV_URL_PATTERN.search(input_str)
        if arxiv_match:
            arxiv_id = arxiv_match.group(2)
            return InputType.ARXIV_ID, arxiv_id

        # Check for GitHub URL (extract repo)
        github_match = self.GITHUB_URL_PATTERN.search(input_str)
        if github_match:
            repo = f"{github_match.group(1)}/{github_match.group(2)}"
            return InputType.GITHUB_URL, repo

        # Check for HuggingFace URL (extract resource)
        hf_match = self.HUGGINGFACE_URL_PATTERN.search(input_str)
        if hf_match:
            resource_type = hf_match.group(1)  # datasets or models
            resource_name = f"{hf_match.group(2)}/{hf_match.group(3)}"
            return InputType.HUGGINGFACE_URL, f"{resource_type}/{resource_name}"

        # Check for DOI
        doi_match = self.DOI_PATTERN.match(input_str)
        if doi_match:
            return InputType.DOI, input_str

        # Check for bare arXiv ID
        arxiv_id_match = self.ARXIV_ID_PATTERN.match(input_str)
        if arxiv_id_match:
            return InputType.ARXIV_ID, input_str

        # Check for URL (HTTP/HTTPS)
        url_match = self.URL_PATTERN.match(input_str)
        if url_match:
            if input_str.startswith('https://'):
                return InputType.URL_HTTPS, input_str
            else:
                return InputType.URL_HTTP, input_str

        # Check for local path
        path_match = self.LOCAL_PATH_PATTERN.match(input_str)
        if path_match:
            return InputType.LOCAL_PATH, input_str

        # Fallback: treat as search query
        # (No URL pattern detected, assume user wants to search)
        return InputType.SEARCH_QUERY, input_str

    def get_handler_name(self, input_type: InputType, extracted_id: str = None) -> str:
        """
        Get handler name for input type

        Args:
            input_type: Classified input type
            extracted_id: Optional extracted ID to check for PDF extension

        Returns:
            Handler name ('generic_web', 'paper', 'github', 'huggingface')
        """
        # Check if URL ends with .pdf, route to paper handler
        if extracted_id and extracted_id.endswith('.pdf'):
            return 'paper'

        handler_map = {
            InputType.URL_HTTP: 'generic_web',
            InputType.URL_HTTPS: 'generic_web',
            InputType.DOI: 'paper',
            InputType.ARXIV_ID: 'paper',
            InputType.GITHUB_URL: 'github',
            InputType.HUGGINGFACE_URL: 'huggingface',
            InputType.LOCAL_PATH: 'generic_web',  # Will need special handling
            InputType.SEARCH_QUERY: 'search',  # Special mode
            InputType.UNKNOWN: 'generic_web'
        }

        return handler_map.get(input_type, 'generic_web')

    def is_search_mode(self, input_type: InputType) -> bool:
        """
        Check if input should trigger search mode

        Args:
            input_type: Classified input type

        Returns:
            True if search mode
        """
        return input_type == InputType.SEARCH_QUERY

    def route_inputs(self, inputs: list[str]) -> list[dict]:
        """
        Route multiple inputs to handlers

        Args:
            inputs: List of user inputs

        Returns:
            List of routing decisions with input_type, handler, extracted_id
        """
        routed = []

        for input_str in inputs:
            input_type, extracted_id = self.classify_input(input_str)
            handler = self.get_handler_name(input_type, extracted_id)

            routed.append({
                'input': input_str,
                'input_type': input_type.value,
                'handler': handler,
                'extracted_id': extracted_id,
                'is_search': self.is_search_mode(input_type)
            })

        return routed

def route_inputs(inputs: list[str]) -> list[dict]:
    """
    Route multiple inputs to handlers

    Args:
        inputs: List of user inputs

    Returns:
        List of routing decisions with input_type, handler, extracted_id
    """
    router = InputRouter()
    routed = []

    for input_str in inputs:
        input_type, extracted_id = router.classify_input(input_str)
        handler = router.get_handler_name(input_type, extracted_id)

        routed.append({
            'input': input_str,
            'input_type': input_type.value,
            'handler': handler,
            'extracted_id': extracted_id,
            'is_search': router.is_search_mode(input_type)
        })

    return routed

def main():
    """CLI test for input router"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: input_router.py <inputs>")
        print("Example: input_router.py 'https://arxiv.org/abs/2402.12345' '10.1234/paper' 'agent memory'")
        sys.exit(1)

    inputs = sys.argv[1:]
    routed = route_inputs(inputs)

    print("Input routing results:")
    print("-" * 80)
    for item in routed:
        print(f"Input: {item['input']}")
        print(f"  Type: {item['input_type']}")
        print(f"  Handler: {item['handler']}")
        print(f"  Extracted ID: {item['extracted_id']}")
        print(f"  Is Search: {item['is_search']}")
        print()

if __name__ == "__main__":
    main()