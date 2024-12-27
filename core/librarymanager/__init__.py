"""
Init module for the library-manager package.

This module will contain the classes and functions that are necessary to manage the
library of the project.

Authors = [
    "paudefuente",
]
"""

from .structure_manager import StructureManager
from .file_manager import FileManager

__all__ = ['StructureManager', 'FileManager']