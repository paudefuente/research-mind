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

from .query_generator import QueryGenerator


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


    def create_results_folder(self, folder_path: Path | str, importance: str) -> str:
        """
        Creates a folder to store the results of the search queries.

        :param folder_path: The path of the folder that will be created.
        :return: bool
        """

        if isinstance(folder_path, Path):
            folder_path.mkdir(parents=True, exist_ok=True) if not folder_path.exists() else None
            folder_path.joinpath(f"results_imp{importance}.json")
        
        if isinstance(folder_path, str):
            folder_path = Path(folder_path)
            folder_path.mkdir(parents=True, exist_ok=True) if not folder_path.exists() else None
            folder_path.joinpath(f"results_imp{importance}.json")

        results = {
                "_comment": "This file contains the total of studies extracted of the corresponding importance.",
                "info": {
                    "importance": importance,
                    "total_studies": sum(results.values())
                },
                "data":[]
            }

        with open(folder_path, "w") as file:
            json.dump(results, file, indent=4)

        return folder_path


    def check_all_queries(self, origin_pth: Path | str , target_pth) -> bool:
        """
        Gets all the files that are in the folder and checks if they have queries
        defined in them. If true, it will extract all the queries and process them,
        saving the total of studies found in another file.
        """
        
        if not isinstance(origin_pth, Path):
            origin_pth = Path(origin_pth)

        if not origin_pth.exists():
            self.log.error(f"The folder {origin_pth} does not exist.")
            return False
        
        try:
            # Create the results folder + add the results file
            for num, file in enumerate(origin_pth.iterdir()):
                results_folder = self.create_results_folder(target_pth, num)

                if file.is_file() and file.suffix == ".json":
                    with open(file) as file:
                        data = json.load(file)
                    
                    queries = pd.Series(data.get("data"))
                    results = self.check_queries(queries)

                    data["data"] = results

                    with open(results_folder, "w") as file:
                        json.dump(data, file, indent=4)
            return True
        except Exception as e:
            self.log.error(f"Error: {e}")
            return False
        

    def check_queries(self, queries: pd.Series) -> dict:
        """
        Gets all the queries defined in a certain .json file, process them in
        order to get all the total results for each query and store them into
        another file.

        :param queries: The queries that will be used to search the studies.
        :return: True if the queries are defined correctly
        """
        try:
            results = {}
            for num, query in enumerate(queries):
                if num >= 3:
                    break
                
                results[num] = self.count_studies_by_search(query)   

            if results:
                return results
            return {}
        except Exception as e:
            self.log.error(f"Error: {e}")

    
    def count_studies_by_search(self, query: any) -> int:
        """
        Gets the total of studies that are found by a specific search query.

        :param query: The query that will be used to search the studies.
        :return: The total of studies that are found by the search query.
        """ 
        search_results = scho.search_pubs(query)
        return search_results.total_results
        
                                

def main(func: str, origin_pth: Path | str, target_pth: Path | str) -> None:
    """
    Main function to execute the script
    """
    # Create the object of the class
    scrapper_service = ScrapperService()

    # Get the total of studies by search
    for x in range(1, 2):

        origin_pth = origin_pth.joinpath(f"trial-search-queries-{x}.json")
        with open(origin_pth) as file:
            data = json.load(file)

        queries = pd.Series(data.get("data"))
        

        response = scrapper_service.check_queries(queries)
        scrapper_service.log.info(f"The total of studies found by the search query is: {response}")
        print(f"The total of studies found by the search query is: {response}")
    
    try:
        match(func):

            case "create_results_folder":
                origin_pth = Path(target_pth)
                importance = "0"
                response = scrapper_service.create_results_folder(origin_pth, importance)
                return response


            case "check_all_queries":

                total_query_files = os.listdir(origin_pth)
                if total_query_files == 0:
                    logging.error("There are no queries defined in the queries.csv file.")
                    exit(1)

                response = scrapper_service.check_all_queries(ScrapperService.TRIAL_SEARCHES_QUERIES_FOLDER)
                return response

            case _:
                logging.error("The function that you informed is not valid.")
                exit(1)
    except Exception as e:
        logging.error(f"Error: {e}")

    



if __name__ == "__main__":
    # main()
    pass