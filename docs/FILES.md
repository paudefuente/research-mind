"""
Functionality created to clean all the files created by the LaTeX compiler. This function is called by the main function
in the main.py file, in which the user can choose to clean the files or not.

The function will take all the file extensions that defined in .gitignore file and ignored by the git, and will remove them
from the directory. 
"""

import subprocess
import os
import fnmatch
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


# Constants
GIT_IGNORE_FILE_PATH = "./src/docs/paper/.gitignore"


# Functions
def clean_ignored_files(project_path: str, git_ignore_path: str):
    """
    This function will remove all the files that are defined in the .gitignore file. 

    :param project_path: The path of the project.
    :param git_ignore_path: The path of the .gitignore file.
    :return: None
    """

    try:

        # Verify that the project path exists
        if not os.path.exists(project_path):
            raise FileNotFoundError(f"No se encontró el directorio {project_path}")
        if not os.path.exists(git_ignore_path):
            raise FileNotFoundError(f"No se encontró el archivo .gitignore en {git_ignore_path}")
        
        # Get the patterns that are defined in the .gitignore file
        patterns = get_gitignore_patterns(git_ignore_path)

        # Iterate over the folder / files structure and remove the files that match the patterns
        for root, dirs, files in os.walk(project_path):
            for file in files:

                file_path = os.path.join(root, file)
                
                if any(fnmatch.fnmatch(file_path, os.path.join(project_path, pattern)) for pattern in patterns):

                    try:
                        os.remove(file_path)
                        print(f"File Deleted: {file_path}")
                    except Exception as e:
                        print(f"Not possible to delete the file {file_path}")
                        print(e)
        
    except subprocess.CalledProcessError as e:
        print(e)
    except Exception as e:
        print("Took place an unexpected error:")
        print(e)
        print("Took place an unexpected error:")
        print(e)


def get_gitignore_patterns(gitignore_path: str):
        
        """
        This function will read the .gitignore file and return the patterns that are defined in the file.

        :param git_repo_path: The path of the git repository.
        :return: The patterns that are defined in the .gitignore file.
        """
        
        with open(gitignore_path, "r") as file:
            patterns = [line.strip() for line in file if line.strip() and not line.startswith("#")]
        
        return patterns


def get_current_directory():
    """
    This function will return the current directory where the script is running.

    :return: The current directory.
    """
    return os.path.dirname(os.path.abspath(__file__))


def get_project_path():
    """
    This function will return the path of the project.

    :return: The path of the project.
    """
    path = get_current_directory()
    return os.path.join(get_current_directory(), "../../")


def main():
    """
    Main function which will clean the files that are defined in the .gitignore file
    searching in the project path.
    """
    print("Cleaning the files that are defined in the .gitignore file.")
    clean_ignored_files(get_project_path(), GIT_IGNORE_FILE_PATH)


# Execute the main function
if __name__ == "__main__":
    main()
