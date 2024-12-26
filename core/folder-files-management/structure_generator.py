"""
StructureGenerator initialises a folder structure formed by a variety of 
folders with different purposes. This structure will be utilised to store different
types of files, accessed and used for other functions within the library.

authors = [
    "paudefuente ",
]
"""

import os 
import sys

import logging
from pathlib import Path


class StructureGenerator:
    """
    StructureGenerator will manage the structure initial which will serve as the
    base for the library. This structure will be used to store the different types
    of files that are necessary for the library to work.
    """

    def __init__(self):
        """
        Init functions to set the API URL and the logging level.
        """
        logging.basicConfig(level=logging.INFO)     
        self.log = logging.getLogger(__name__)

        current_dir = Path(__file__).resolve().parent
        project_root = current_dir
        while not (project_root / ".git").exists() and not (project_root / 'pyproject.toml').exists():
            project_root = project_root.parent

        self.ROOT_PATH = project_root

    def create_structure(self, project_path: Path | str = None) -> bool:
        """
        Creates the basic structure of folders that will be used to store the
        different types of files that are necessary for the library to work.

        :param project_path: The path of the project where the structure will be created.
        :return: boolean indicating if the structure was created successfully.
        """
        
        # Use ROOT_PATH if project_path is not provided
        if project_path is None:
            project_path = self.ROOT_PATH

        # Check if the project_path exists
        if isinstance(project_path, str):
            project_path = Path(project_path)

        if not project_path.exists():
            raise self.log.error(f"[StructureGenerator] Path {project_path} does not exist.")

        # Create the structure
        self.log.info("Creating the structure of folders.")
        response = self.create_folders(project_path)
        return response
    
    def create_folders(self, project_path: Path) -> bool:
        """
        Creates the folders for the basic structure of the library.

        :param project_path: The path of the project where the structure will be created.
        :return: boolean indicating if the structure was created successfully.
        """
        try:
            # Basic Structure (systematic-review)
            structure = [
                'json/def',
                'json/def-processed',
                'json/que-gen-combinations',
                'json/que-results',
                'csv/',
            ]

            # Create the folders
            for folder in structure:
                folder_path = Path(project_path / folder)
                folder_path.mkdir(parents=True, exist_ok=True)

                # .gitkeep file
                gitkeep_path = folder_path / ".gitkeep"
                if not gitkeep_path.exists():
                    gitkeep_path.touch()
                
            self.log.info("[StructureGenerator] Structure of folders created successfully.")
            return True
        except Exception as e:
            self.log.error(f"[StructureGenerator] Error while creating the structure of folders: {e}")
            return False
        
