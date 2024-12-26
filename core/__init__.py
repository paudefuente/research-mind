"""
Core package for the application. It contains the main functionality of the library,
including all the utils and services that are necessary to perform a research.
"""

__version__ = "0.1.1"

import cli
from .search.query_generator import QueryGenerator
from .search.scrapper_googlescholar import ScrapperService