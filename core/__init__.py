"""
Core package for Resmind library. It contains the main functionality of the library,
including all the utils and services that are necessary to perform a research.

authors = [
    "@paudefuente",
]
"""

__version__ = "0.1.1"

from .search.query_generator import QueryGenerator
from .search.scrapper_googlescholar import ScrapperService

__all__ = ["QueryGenerator", "ScrapperService"]