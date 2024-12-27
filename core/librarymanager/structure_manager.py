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


class StructureManager:
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

        self.ROOT_PATH = StructureManager.detect_root_path()
        self.basic_structure = [
            'resmi_folders/json/def',
            'resmi_folders/json/def-processed',
            'resmi_folders/json/trial-searches/que-gen-combinations',
            'resmi_folders/json/trial-searches/que-results/imp1',
            'resmi_folders/json/trial-searches/que-results/imp2',
            'resmi_folders/json/trial-searches/que-results/imp3',
            'resmi_folders/csv/',
        ]

    @staticmethod
    def detect_root_path() -> Path:
        """
        Detects the root path of the project where the library is being used.
        
        :return: Path of the root directory of the project.
        """
        possible_root_opt = ['.git', 'pyproject.toml', 'setup.py', 'requirements.txt']
        current_dir = Path(__file__).resolve().parent
        project_root = current_dir
        while not any((project_root / opt).exists() for opt in possible_root_opt):
            if project_root == project_root.parent:
                raise logging.log.error("[StructureManager] Root path of the project could not be detected.")
            project_root = project_root.parent

        return project_root


    def generate_structure(self, project_path: Path | str = None) -> bool:
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
            raise self.log.error(f"[StructureManager] Path {project_path} does not exist.")

        # Generate the structure
        self.log.info("Creating the structure of folders.")
        response = self.generate_folders(project_path)
        return response
    
    def generate_folders(self, project_path: Path) -> bool:
        """
        Creates the folders for the basic structure of the library.

        :param project_path: The path of the project where the structure will be created.
        :return: boolean indicating if the structure was created successfully.
        """
        try:
            
            basic_structure = self.basic_structure if self.basic_structure else []
            for folder in basic_structure:
                folder_path = Path(project_path / folder)
                folder_path.mkdir(parents=True, exist_ok=True)

                # .gitkeep file if the folder is empty
                if not any(folder_path.iterdir()):
                    gitkeep_path = folder_path / ".gitkeep"
                    if not gitkeep_path.exists():
                        gitkeep_path.touch()
                
            self.log.info("[StructureManager] Structure of folders created successfully.")
            return True
        except Exception as e:
            self.log.error(f"[StructureManager] Error while creating the structure of folders: {e}")
            return False
    

    def check_structure(self, project_path: Path | str = None) -> bool:
        """
        Checks if there is any kind of fixed structure in the project_path, 
        enabling the library to work properly.

        :param project_path: The path of the project where the structure will be checked.
        :return: boolean indicating if the structure is correct or exists.
        """


    def total_files(self, project_path: Path | str = None) -> int:
        """
        Returns the total number of files located in a certain path.
        
        :param project_path: The path of the project where the structure will be checked.
        :return: int with the total number of files in the path.
        """
        if project_path is None:
            self.log.error("[StructureManager] Path of the project is not provided.")
            return 0

        if isinstance(project_path, str):
            project_path = Path(project_path)

        if not project_path.exists():
            self.log.error(f"[StructureManager] Path {project_path} does not exist.")
            return 0 
        
        total_files = sum(1 for _ in project_path.iterdir() if _.is_file())
        return total_files