"""
This script defines a scapper service that utilises the `scholarly` library that
enables to search for articles in Google Scholar. The script defines a class
which will locate all the functions that are necessary to search for articles.

authors = [
    "@paudefuente",
]
"""

# Packages to import
import os
import sys

import json
import logging
from pathlib import Path
import pandas as pd
from scholarly import scholarly as scho

from core.search.query_manager import QueryGenerator
from core.librarymanager.structure_manager import StructureManager


class ScrapperService:
    """
    This class is created to define the functions necessary in the systematic review
    search process related with scrapping information from Google Scholar.

    Library utilised: scholarly
    """

    def __init__(self): 
        """
        Constructor of the class.
        """
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger(__name__)

        structureManager = StructureManager()
        self.LIBRARY_FOLDER_PATH = Path(structureManager.ROOT_PATH).joinpath("resmi_folders/json")


    def init_results(self, origin_path: any) -> str | Path:
        """
        Creates a basic file 

        :param folder_path: The path of the folder that will be created.
        :return: bool
        """
        if not isinstance(origin_path, Path):
            origin_path = Path(origin_path)

        with open(origin_path, "r") as file:
            data = json.load(file)

        origin_importance = data.get("info", [])
        if origin_importance:
            origin_importance = origin_importance[0].get("importance")
        else:
            origin_importance = None

        total_combinations = len(data.get("data", []))
        origin_name = os.path.basename(origin_path)

        results = {
                "_comment": "This file contains the total of studies extracted of the corresponding importance.",
                "info": {
                    "importance": origin_importance,
                    "total_combinations":total_combinations,
                },
                "data":[]
            }
        
        results_path = self.LIBRARY_FOLDER_PATH.joinpath(f'trial-searches/que-results/imp{origin_importance}/results_{origin_name}.json')
        with open(results_path, "w") as file:
            json.dump(results, file, indent=4)

        return results_path


    def get_results(self, origin_path: any) -> bool:
        """
        Gets all the files that are in the folder and checks if they have queries
        defined in them. If true, it will extract all the queries and process them,
        saving the total of studies found in another file.

        :param origin_pth: The path of the folder where the queries are stored.
        :param target_pth: The path of the folder where the results will be stored.
        :return: True if the queries are defined correctly
        """
        
        if not isinstance(origin_path, Path):
            origin_path = Path(origin_path)

        if not origin_path.exists():
            self.log.error(f"The folder {origin_path} does not exist.")
            return False

        try: 
            for file in origin_path.iterdir():
                if file.is_file() and file.suffix == ".json":

                    results_path = self.init_results(file.absolute())

                    with open(file, "r") as file:
                        data = json.load(file)
                    
                    queries = pd.Series(data.get("data"))
                    results = self.search_queries(queries)

                    with open(results_path, "r") as file1:
                        data = json.load(file1)
                    
                    data["data"] = []
                    data["data"].extend(results)

                    with open(results_path, "w") as file1:
                        json.dump(data, file1, indent=4)

            return True
        except Exception as e:
            self.log.error(f"Error: {e}")
            return False
        

    def search_queries(self, queries: pd.Series) -> list:
        """
        Gets all the queries defined in a certain .json file, process them in
        order to get all the total results for each query and store them into
        another file.

        :param queries: The queries that will be used to search the studies.
        :return: True if the queries are defined correctly
        """
        try:
            results = []
            for num, query in enumerate(queries):
                search = scho.search_pubs(query)
                results.append({'ind':num, 'query':query, 'num_studies': search.total_results})

            if results:
                return results
            return []
        except Exception as e:
            self.log.error(f"Error: {e}")
            return []








if __name__ == "__main__":
    
    scrapper_service = ScrapperService()

    origin_path = "../../resmi_folders/json/trial-searches/que-gen-combinations/imp1"
    scrapper_service.get_results(origin_path)




                                

# if __name__ == "__main__":
#     """
#     Main function to execute the script
#     """
#     # Create the object of the class
#     scrapper_service = ScrapperService()

#     # Get the total of studies by search
#     for x in range(1, 2):

#         origin_pth = origin_pth.joinpath(f"trial-search-queries-{x}.json")
#         with open(origin_pth) as file:
#             data = json.load(file)

#         queries = pd.Series(data.get("data"))
        

#         response = scrapper_service.check_queries(queries)
#         scrapper_service.log.info(f"The total of studies found by the search query is: {response}")
#         print(f"The total of studies found by the search query is: {response}")
    
#     try:
#         match(func):

#             case "create_results_folder":
#                 origin_pth = Path(target_pth)
#                 importance = "0"
#                 response = scrapper_service.create_results_folder(origin_pth, importance)
#                 scrapper_service.log.info(f'[ScrapperService] The results folder was created successfully: {response}') 


#             case "check_all_queries":

#                 total_query_files = os.listdir(origin_pth)
#                 if total_query_files == 0:
#                     logging.error("There are no queries defined in the queries.csv file.")
#                     exit(1)

#                 response = scrapper_service.check_all_queries(ScrapperService.TRIAL_SEARCHES_QUERIES_FOLDER)
#                 scrapper_service.log.info(f'[ScrapperService] The results folder was created successfully: {response}') 

#             case _:
#                 scrapper_service.log.error("The function that you informed is not valid.")
#                 exit(1)
#     except Exception as e:
#         logging.error(f"Error: {e}")

