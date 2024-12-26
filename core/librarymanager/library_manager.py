"""

"""

import os 
import sys

import logging
from pathlib import Path

from .structure_manager import StructureManager
from .file_manager import FileManager

class LibraryManager(StructureManager, FileManager):

    def __init__(self):
        super().__init__()

        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger(__name__)

    def create_library(self, project_path: Path | str = None) -> bool:
        """
        Creates the basic structure of folders that will be used to store the
        different types of files that are necessary for the library to work.

        :param project_path: The path of the project where the structure will be created.
        :return: boolean indicating if the structure was created successfully.
        """
        