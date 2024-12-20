"""
This script will create request to a LM Studio API to get search queries based on key-terms passed 
as arguments. 
"""

# Packages to import
import os
import sys

import json
import logging
import pandas as pd
from collections import Counter 
from itertools import product


# Classes
class QueryGenerator:
    """
    This class is created to create the requests to the LM Studio API, for different
    purposes.

    Library utilised: pandas, json, logging, collections, itertools
    """
    KEY_CONCEPTS_FILE_PATH = "./files/json/key-concepts.json" # "./files/json/key-concepts.json" 
    KEY_TERMS_FILE_PATH = "./files/json/key-terms.json" # "./files/json/key-terms.json"
    SEP_KEY_TERMS_FILE_PATH = "./files/json/separated_keyterms.json" # "./files/json/separated_keyterms.json"
    THESAURUS_FILE_PATH = "./files/json/thesaurus.json" # "./files/json/thesaurus.json"
    SOURCE_INFO_FILE_PATH = "./files/json/source-information.json" # "./files/json/source-information.json"
    SEARCH_RULES_FILE_PATH = "./files/json/search-rules.json"   # "./files/json/search-rules.json"
    TRIAL_SEARCHES_QUERIES_FOLDER = "./files/json/trial-search-queries/" # "./files/json/trial-search-queries/"
    JSON_FOLDER_PATH = "./files/json/"

    def __init__(self):
        """
        Init functions to set the API URL and the logging level.
        """
        logging.basicConfig(level=logging.INFO)     
        self.log = logging.getLogger(__name__)

    @staticmethod
    def get_concepts(file_path: str) -> pd.Series:
        """
        Gets the context provided to init the model and understand the field of the search.

        :param context: The context of the search.
        :return: The context of the search.
        """
        df = pd.DataFrame(pd.read_json(file_path))
        context = df["key-concepts"]
        return context

    @staticmethod
    def get_keyterms(file_path: str) -> tuple[pd.Series, set[str], list[dict[str, set[str]]], set[str]]:
        """
        Gets all the keyterms defined from a file.
        
        :param keyterms_path: The path of the file that contains the keyterms.
        :return: The keyterms and thesaurus, in different lists.
        """
        # Gets keyterms
        df = pd.DataFrame(pd.read_json(file_path))
        keyterms = df["keyterms"].copy()

        all_keyterms = list()
        for keyterm in keyterms:
            all_keyterms.extend(keyterm["keyterm"])

        # Gets thesaurus
        thesaurus, all_thesaurus_terms = QueryGenerator.create_thesaurus(keyterms)

        return keyterms, set(all_keyterms), thesaurus, all_thesaurus_terms
    

    @staticmethod
    def get_separated_keyterms(file_path: str) -> pd.Series:
        """
        Gets all the separated keyterms according to their importance from a JSON
        file.
        
        :param file_path: The path of the file that contains the separated keyterms.
        :return: The separated keyterms. 
        """
        df = pd.DataFrame(pd.read_json(file_path))
        separated_keyterms = df["data"].copy()
        return separated_keyterms
    

    @staticmethod
    def get_keyterms_by_importance(keyterms: pd.Series, importance: any) -> pd.Series:
        """
        Gets all the keyterms defined in a file according to the importance passed as arguments.
        
        :param keyterms: The keyterms of the search.
        :param importance: The importance of the keyterms.
        """
        keyt = pd.DataFrame(keyterms.tolist().copy())
        return keyt[keyt["importance"] == importance]


    @staticmethod
    def create_thesaurus(keyterms: pd.Series) -> tuple[list[dict[str, str, set[str]]], set[str]]:
        """
        Gets all the thesaurus defined in the keyterms.
        
        :param keyterms: The keyterms of the search.
        :return: The thesaurus of the search.
        """
        thesaurus: list[dict[str, str, set[str]]] = []
        all_thesuari_terms = list()
        for keyterm in keyterms:
            new = {"concept": "", "keyterm": "", "divided": "0", "thesaurus": set()}

            # if "concept" in keyterm and keyterm["keyterm_thesaurus"]:
            #     pass

            new["concept"] = keyterm["concept"]
            if "thesaurus" in keyterm and keyterm["thesaurus"]:
                if "keyterm_thesaurus" in keyterm and keyterm["keyterm_thesaurus"]:
                    new["keyterm"] = keyterm["keyterm_thesaurus"][0]
                    new["divided"] = "1"
                else:
                    new["keyterm"] = keyterm["keyterm"]

                new["thesaurus"].update(set(keyterm["thesaurus"]))
                thesaurus.append(new)

                all_thesuari_terms.extend(keyterm["thesaurus"])
                continue
            
            if "thesaurus_1" in keyterm and keyterm["thesaurus_1"]:
                new["concept"] = keyterm["concept"]
                new["keyterm"] = keyterm["keyterm_thesaurus"][0]
                new["divided"] = "1"
                new["thesaurus"].update(set(keyterm["thesaurus_1"]))
                thesaurus.append(new)

                new_2 = {"concept": "", "keyterm": "", "divided": "1", "thesaurus": set()}
                new_2["concept"] = keyterm["concept"]
                new_2["keyterm"] = keyterm["keyterm_thesaurus"][1]
                new_2["thesaurus"].update(set(keyterm["thesaurus_2"]))
                thesaurus.append(new_2)

                all_thesuari_terms.extend(keyterm["thesaurus_1"])
                all_thesuari_terms.extend(keyterm["thesaurus_2"])
                continue

        # Store the thesaurus in a JSON file
        basic_structure = {
            "_comment": "This file contains the thesaurus of the search.",
            "total_keyterms": len(keyterms),
            "total_thesaurus": len(set(all_thesuari_terms)),
            "data": []
        }
        
        for thes in thesaurus:
            new_thes = {
                "concept": thes["concept"],
                "keyterm": thes["keyterm"],
                "divided": thes["divided"],
                "thesaurus": list(thes["thesaurus"])
            }
            basic_structure["data"].append(new_thes)

        path_file = f"{QueryGenerator.JSON_FOLDER_PATH}/thesaurus.json"
        with open(path_file, "w") as file:
            json.dump(basic_structure, file, indent=4)

        return thesaurus, set(all_thesuari_terms)
    

    @staticmethod
    def get_thesaurus(file_path: any) -> tuple[pd.Series, set[str]]:
        """
        Gets all the thesaurus defined in the keyterms and stored in the specific
        file.
        
        :param file_path: The path of the file that contains the thesaurus.
        :return: The thesaurus of the search + all the thesaurus terms.
        """
        df = pd.DataFrame(pd.read_json(file_path))
        thesaurus = df["data"].copy()

        all_thesaurus_terms = list()
        for thes in thesaurus:
            all_thesaurus_terms.extend(thes["thesaurus"])
        return thesaurus, set(all_thesaurus_terms)


    def check_keyterm_thesaurus(self, keyterm: str, thesaurus: pd.Series) -> bool:
        """
        Check if the keyterm has a thesaurus. 
        
        :param keyterm: The keyterm to check.
        :param thesaurus: The thesaurus of the search.
        :return: True if the keyterm has a thesaurus, False otherwise.
        """
        for thes in thesaurus:
            if thes["keyterm"] == keyterm:
                return True
        return False


    def get_thesaurus_from_keyterm(self, keyterm: str, thesaurus: pd.Series) -> pd.Series: 
        """
        Gets the thesaurus from a keyterm. 

        :param keyterm: The keyterm to get the thesaurus.
        :return: The thesaurus of the keyterm.
        """
        for thes in thesaurus:
            if thes["keyterm"] == keyterm:
                self.log.info(f"Thesaurus: {thes['thesaurus']}")
                return thes["thesaurus"]
        return None
    

    @staticmethod
    def get_sources(file_path: str) -> pd.Series:
        """ 
        Gets all the defined sources of studies from a JSON file
        
        :param file_path: The path of the file that contains the sources.
        :return: The sources of the studies.
        """
        # with open(file_path, "r") as file:
        df = pd.DataFrame(pd.read_json(file_path))
        sources = df["sources"].copy()
        return sources
    

    @staticmethod
    def get_rules(file_path: str) -> pd.Series:
        """
        Gets all the rules defined for each of the sources of information included
        in the search.
        
        :param file_path: The path of the file that contains the rules.
        :return: The rules of the sources of information.
        """
        df = pd.DataFrame(pd.read_json(file_path))
        rules = df["rules_search"].copy()
        return rules


    @staticmethod
    def get_source_rules(information_source: pd.Series, source_name: str) -> set[str]:
        """
        Check the rules of the information source.
        
        :param information_source: The source of information.
        :param rules: The rules of the sources of information.
        :return: The rules of the information source.
        """
        source_rules = set()
        for source in information_source:
            if source["source"].equals(source_name):
                source_rules.update(source["rules"])
                break
        return source_rules
    

    def separate_keyterms(self, concepts: pd.Series, keyterms: pd.Series, 
                          thesaurus: list[dict[str, str, set[str]]]) -> bool:
        """ 
        Based on the keyterms passed as arguments, it will separate the keyterms
        into different categories, according to the concept from which they have 
        been extracted, and therefore, of their importance.
        
        :param keyterms: The keyterms of the search.
        :return: True if the keyterms have been separated & stored successfully,
        false otherwise.
        """
        try:

            conc = pd.DataFrame(concepts.tolist().copy())
            keyt = pd.DataFrame(keyterms.tolist().copy())
            thes = thesaurus.copy()

            total_concepts = str(len(conc))
            total_importance = str(len(set(conc["importance"])) if "importance" in conc else 0)  

            basic_structure = {
                "total_concepts": total_concepts,
                "total_importance": total_importance,
                "data": []
            }

            for _, row1 in conc.iterrows():
                all_keyterms = list()
                all_thesaurus = list()    
                
                for _, row2 in keyt.iterrows():
                    if row1["id"] == row2["concept"]:
                        term = row2["keyterm"]
                        self.log.info(f"Term: {term}")
                        all_keyterms.append(term)
                         
                for thesaur in thes:
                    if thesaur["concept"] == row1["id"]:
                        all_thesaurus.extend(thesaur["thesaurus"])

                self.log.info(f"Keyterms: {all_keyterms}")
                self.log.info(f"The: {all_thesaurus}")

                new_concept = {
                    "concept": row1["id"],
                    "importance": row1["importance"],
                    "keyterms": all_keyterms,
                    "thesaurus": all_thesaurus
                }

                basic_structure["data"].append(new_concept)

            # Create or overwriter JSON file
            path_file = f"{SearchService.JSON_FOLDER_PATH}/separated_keyterms.json"
            with open(path_file, "w") as file:
                json.dump(basic_structure, file, indent=4)

            self.log.info(f" \n Data Succesfully stored in {path_file}")    
            return True
        except Exception as ex:
            self.log.error(f"An error occurred while separating the keyterms: {ex}")
            return False


    @staticmethod
    def generate_search_queries(concepts: pd.Series, separated_keyterms: pd.Series, 
                                thesaurus: pd.Series) -> bool:
        """
        Generates random search queries based on the keyterms, thesaurus, and sources (rules of each). 
        
        :param keyterms: The keyterms of the search.
        :param thesaurus: The thesaurus of the search.
        :param sources: The sources of the search.
        :return: True if the queries have been generated & stored successfully, False otherwise.
        """
        folder_path = QueryGenerator.TRIAL_SEARCHES_QUERIES_FOLDER
        
        try:
            queryGenerator = QueryGenerator()

            # Generate the queries based on the structure
            importance: int = 3  # The importance should be the maximum importance of the concepts and passed as argument
            for x in range(1, importance + 1):
                structure = queryGenerator.create_query_structure(concepts, x)   
                response = queryGenerator.create_query_files(folder_path, structure, x)
                if response:
                    queryGenerator.log.info(f"Created file: {folder_path}")
                else:
                    queryGenerator.log.error(f"An error occurred while creating the queries files.")

            # Generate search queries 
            total_query_files = len(os.listdir(folder_path))
            for x in range(1, total_query_files + 1):
                file_path = f"{folder_path}queries_{x}.json"
                response = queryGenerator.add_terms_to_query_structure(file_path, separated_keyterms, thesaurus, x)
                if response:
                    queryGenerator.log.info(f"Queries have been generated and stored in {file_path}") 
                else:
                    logging.error(f"An error occurred while generating the queries.")
                    

            return True
        except Exception as e:
            logging.error(f"An error occurred while generating the search queries: {e}")
            return False                                                                                                                                                    


    def create_query_structure(self, concepts: pd.Series, target_importance: any) -> str:
        """
        Based on the keyterms, total concepts, and actual concept, this function 
        creates the query structure.
        
        :param concepts: The concepts of the search.
        :param target_importance: The target importance of the search.
        :return: The query structure.

        Example:
        concepts = pd.Series([{"id": 1, "importance": 1}, {"id": 2, "importance": 2}, 
            {"id": 3, "importance": 3}])
        target_importance = 3

        The query structure will be: (concept1_1) AND (concept2_1 OR concept2_2) 
            AND (concept3_1 OR concept3_2 OR concept3_3)
        """
        conc = pd.DataFrame(concepts.tolist().copy())
        total_concepts = conc['importance']

        try:

            # Get the importance counts
            importance_counts = dict(Counter(total_concepts.tolist()))

            # Check if the target importance is in the concepts
            if str(target_importance) not in importance_counts:
                raise ValueError(f"The importance {target_importance} is not in the concepts.")

            # Group the concepts by importance
            grouped_concepts = {}
            counter = 1
            for importance, count in sorted(importance_counts.items(), 
                                            key=lambda x: int(x[0])):
                grouped_concepts[int(importance)] = [f"concept_{counter + i}" for 
                                                     i in range(count)]
                counter += count


            final_structure = ""
            for current_importance in range(1, target_importance + 1):
                structure = ""
                match current_importance:
                    case 1:
                        fields = grouped_concepts.get(1, [])
                        structure = " AND ".join(fields)
                        final_structure = f"({structure})"
                        
                    case 2:
                        fields = grouped_concepts.get(2, [])
                        structure = " OR ".join(fields)
                        final_structure += f" AND ({structure})"

                    case 3:
                        fields = grouped_concepts.get(3, [])
                        structure = " OR ".join(fields)
                        final_structure += f" AND ({structure})"

                    case _:
                        self.log.error("The target importance is not valid.")
                        return ""
            
            return final_structure
        except Exception as e:
            self.log.error(f"An error occurred while creating the query structure: {e}")
            return ""
    

    def create_query_files(self, folder_path: any, structure: str, importance: str) -> bool:
        """
        Creates the files with the query structurem in order to store 
        the queries at a later date.

        :param folder_path: The path of the folder to store the queries.
        :param structure: The structure of the queries.
        :return: True if the files have been created successfully, False otherwise.
        """
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"The folder {folder_path} does not exist.")
        
        if not structure:
            raise ValueError("The structure of the queries is not valid.")
        
        # Check how many files are in the folder
        total_queries_files = len(os.listdir(folder_path))
        if total_queries_files >= 3:
            for file_name in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file_name)
                    os.remove(file_path)

            total_queries_files = 0
        
        try:

            # Create the structure of the JSON file + store it
            basic_structure = {
                "_comment": "This file contains the queries that have been generated based on the corresponding importance.",
                "info": [
                    {
                        "total_concepts": 0,
                        "structure": structure,
                        "importance": importance
                    }
                ],
                "data": []
            }

            self.log.info(f"Total queries files: {total_queries_files}")

            # Write + Save the file
            path_file = f"{folder_path}queries_{total_queries_files + 1}.json"
            self.log.info(f"Path file: {path_file}")
            with open(path_file, "w") as file:
                json.dump(basic_structure, file, indent=4)

            self.log.info(f"Total queries files: {len(os.listdir(folder_path))}") 
            return True
        except Exception as e:
            self.log.error(f"An error occurred while creating the files with the query structure: {e}")
            return False


    # META PROGRAMMING - Interesting to use in the future (create a function which changes
    # its own behavior and structure based on the arguments passed)
    def add_terms_to_query_structure(self, file_path: any, separated_keyterms: pd.Series, 
                                     thesaurus: pd.Series, importance: int) -> bool:
        """
        Adds the terms to the query structure. This function will replace the 
        generic terms in the structure (concept1_1, concept2_1, etc) with the
        actual terms.

        :param separated_keyterms: The separated keyterms.
        :param structure: The structure of the queries.
        :return: True if the terms have been added successfully, False otherwise.
        """
        try:
            separated_keyterms = pd.DataFrame(separated_keyterms.tolist().copy())

            with open(file_path, "r") as file:
                file_data = json.load(file)

            structure = file_data["info"][0]["structure"]
            importance = str(file_data["info"][0]["importance"])
            self.log.info(f"Structure: {importance}")

            match importance:

                case "1":
                    
                    # Extract all keyterms / concepts with same importance
                    imp1_all_key = separated_keyterms[separated_keyterms["importance"] == "1"]
                      
                    # Use of itertools.product to get all possible combinations
                    keyterms = imp1_all_key["keyterms"].tolist().copy()
                    all_combinations = self.generate_combinations(list(keyterms))
                    all_combinations = [list(x) for x in all_combinations]
           
                    all_combinations_copy = all_combinations.copy()

                    # Execute logic
                    response = self.generate_combinations_thesaurus(file_path, all_combinations, all_combinations_copy,
                                                                    thesaurus, structure)
                    return response

            
                case "2":
                    
                    # Extract all keyterms / concepts with same importance
                    imp1_all_key = separated_keyterms[separated_keyterms["importance"] == "1"]
                    imp2_all_key = separated_keyterms[separated_keyterms["importance"] == "2"]
                    
                      
                    # Use of itertools.product to get all possible combinations
                    keyterms1 = imp1_all_key["keyterms"].tolist().copy()
                    keyterms2 = imp2_all_key["keyterms"].tolist().copy()
                    all_keyterms = keyterms1 + keyterms2
                    all_combinations = self.generate_combinations(list(all_keyterms))
                    all_combinations = [list(x) for x in all_combinations]

                    all_combinations_copy = all_combinations.copy()

                    # Execute logic
                    response = self.generate_combinations_thesaurus(file_path, all_combinations, all_combinations_copy,
                                                                    thesaurus, structure)
                    return response
                


                case "3":

                     # Extract all keyterms / concepts with same importance
                    imp1_all_key = separated_keyterms[separated_keyterms["importance"] == "1"]
                    imp2_all_key = separated_keyterms[separated_keyterms["importance"] == "2"]
                    imp3_all_key = separated_keyterms[separated_keyterms["importance"] == "3"]
                    
                      
                    # Use of itertools.product to get all possible combinations
                    keyterms1 = imp1_all_key["keyterms"].tolist().copy()
                    keyterms2 = imp2_all_key["keyterms"].tolist().copy()
                    keyterms3 = imp3_all_key["keyterms"].tolist().copy()
                    all_keyterms = keyterms1 + keyterms2 + keyterms3
                    all_combinations = self.generate_combinations(list(all_keyterms))
                    all_combinations = [list(x) for x in all_combinations]

                    all_combinations_copy = all_combinations.copy()

                    # Execute logic
                    response = self.generate_combinations_thesaurus(file_path, all_combinations, all_combinations_copy,
                                                                    thesaurus, structure)
                    return response


                case _: 
                    self.log.error("The importance is not valid.")
                    return False
            
        except Exception as e:
            self.log.error(f"An error occurred while adding the terms to the query structure: {e}")
            return False


    def generate_combinations_thesaurus(self, file_path: any, all_combinations: any,
                                        all_combinations_copy: any, thesaurus: pd.Series,
                                        structure: any) -> bool: 
        """
        Generate all possible combinations adding the thesaurus to the keyterms. 

        :param all_combinations_copy: The copy of all combinations.
        :param all_combinations: The all combinations.

        """           
        # Checkthesaurus f-each keyterm
        try:
            for items in all_combinations_copy:
                combinations = []

                transformed_items = [[item_trans] for item_trans in items] # Mirar esto
                for i, item in enumerate(items):

                    keyterm = item.strip()
                    if self.check_keyterm_thesaurus(keyterm, thesaurus):
                        thes = self.get_thesaurus_from_keyterm(keyterm, thesaurus) 
                        items = list(items)
                        transformed_items[i] = thes if thes else item
                        combinations.extend(self.generate_combinations(transformed_items))
                        continue
                    
                    # Separate the keyterm
                    keyterm = item.split()

                    thes = []
                    if len(keyterm) > 1:
                        # Logic of the thesaurus separated keytem
                        for kt in keyterm:
                            if not self.check_keyterm_thesaurus(kt, thesaurus):
                                thes.append([kt])
                                continue

                            thes.append(self.get_thesaurus_from_keyterm(kt, thesaurus))

                        # All possible combinations of the thesaurus of one keyterm
                        thes = list(self.generate_combinations(thes))
                        thes = [" ".join(x) for x in thes]

                        items = list(items)
                        transformed_items[i] = thes 
                        combinations.extend(self.generate_combinations(transformed_items)) # Check if it is correct 

                if combinations:
                    self.log.info(f"Combinations: {combinations}")
                    for x in combinations:
                        all_combinations.insert(len(all_combinations) + 1, x)

            # Remove duplicates 
            unique_combinations = sorted(set(tuple(x) for x in all_combinations))
            unique_combinations = [list(x) for x in unique_combinations]

            self.log.info(f"Unique combinations: {unique_combinations}")
            self.log.info(f"Structure: {structure}")

             # Replace generic terms with actual terms - Error here
            formatted_combinations = []
            for items in unique_combinations:
                temp = structure
                for i, item in enumerate(items):
                    self.log.info(f"Item: {item}, {i}")
                    temp = temp.replace(f"concept_{i+1}", item)
                formatted_combinations.append(temp)

            # Store the combinations in the JSON file
            with open(file_path, "r") as file:
                data = json.load(file)

            data["data"] = []
            data["data"].extend(formatted_combinations)

            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)

            return True
        except Exception as e:
            self.log.error(f"An error occurred while generating the thesaurus combinations: {e}")
            return False
        

    def generate_combinations(self, keyterms: any) -> any:
        """
        Generates all possible combinations of the keyterms.
        
        :param keyterms: The keyterms to generate the combinations.
        :return: All possible combinations of the keyterms.
        """
        combinations = product(*keyterms)
        return combinations



def main(func): # func: str
    """
    Main function to execute the script. Contains the match statement to execute
    the functions based on the argument passed.
    """
    try:
        match(func):

            case "get_data":
                concepts = QueryGenerator.get_concepts(QueryGenerator.KEY_CONCEPTS_FILE_PATH)
                keyterms, all_keyterms, thesaurus, all_the = QueryGenerator.get_keyterms(QueryGenerator.KEY_TERMS_FILE_PATH)
                sources = QueryGenerator.get_sources(QueryGenerator.SOURCE_INFO_FILE_PATH)
                rules = QueryGenerator.get_rules(QueryGenerator.SEARCH_RULES_FILE_PATH)
                return concepts, keyterms, all_keyterms, thesaurus, all_the, sources, rules

            case "create_files":
                concepts = QueryGenerator.get_concepts(QueryGenerator.KEY_CONCEPTS_FILE_PATH)
                keyterms, _, thesaurus, _ = QueryGenerator.get_keyterms(QueryGenerator.KEY_TERMS_FILE_PATH)
                return QueryGenerator().separate_keyterms(concepts, keyterms, thesaurus)

            case "generate_queries":
                separated_keyterms = QueryGenerator.get_separated_keyterms(QueryGenerator.SEP_KEY_TERMS_FILE_PATH)
                thesaurus, _ = QueryGenerator.get_thesaurus(QueryGenerator.THESAURUS_FILE_PATH)
                concepts = QueryGenerator.get_concepts(QueryGenerator.KEY_CONCEPTS_FILE_PATH)
                response = QueryGenerator.generate_search_queries(concepts, separated_keyterms, thesaurus)
                return response
            
            case _:
                print("Invalid function to execute.")
                return False

    except Exception as e:
        logging.error(f"An error occurred while executing the function: {e}")
        return 1
    
    
# Execute the main function
if __name__ == "__main__":
    # main()
    separated_keyterms = QueryGenerator.get_separated_keyterms(QueryGenerator.SEP_KEY_TERMS_FILE_PATH)
    thesaurus, _ = QueryGenerator.get_thesaurus(QueryGenerator.THESAURUS_FILE_PATH)
    concepts = QueryGenerator.get_concepts(QueryGenerator.KEY_CONCEPTS_FILE_PATH)
    response = QueryGenerator.generate_search_queries(concepts, separated_keyterms, thesaurus)
    pass