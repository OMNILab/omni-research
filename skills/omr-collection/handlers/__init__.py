"""
Collection Handlers Package
4 core handlers: Generic Web, Paper, GitHub, HuggingFace
"""

from .base_handler import BaseHandler
from .generic_web_handler import GenericWebHandler
from .paper_handler import PaperHandler
from .github_handler import GitHubHandler
from .huggingface_handler import HuggingFaceHandler

__all__ = [
    'BaseHandler',
    'GenericWebHandler',
    'PaperHandler',
    'GitHubHandler',
    'HuggingFaceHandler'
]