import os
import shutil
from pathlib import Path
import json
import yaml


class FileManager:
    """Class for file manipulation."""

    @staticmethod
    def remove_tree(path):
        """Methods deletes file/directory and its subdirectories of a given path.

        Args:
            path (str): Path to a file/dir
        """
        if Path(path).exists():
            shutil.rmtree(path)

    @staticmethod
    def mkdir(path, parents=True, exists_ok=True):
        """Method creates dir of a given path

        Args:
            path (str): Path to a dir
            parents (bool): Create all subdirectories recursively
            exists_ok (bool): Firstly checks if dir is already exists
        """
        Path(path).mkdir(parents=parents, exist_ok=exists_ok)

    @staticmethod
    def file_exists(path):
        """Method checks if file of a given path exists.

        Args:
            path (str): Path of a file to check
        Returns:
            Instance of Remote driver.
        """
        return Path(path).is_file()

    @staticmethod
    def get_list_of_files(dir_path):
        """Methods load all files from given directory and its subdirectories recursively.

        Args:
            dir_path (str): Path to a dir to load files from
        Returns:
            list(str): List of all loaded files
        """
        all_files = list()
        for f in os.listdir(dir_path):
            full_path = os.path.join(dir_path, f)
            if os.path.isdir(full_path):
                all_files += FileManager.get_list_of_files(full_path)
            else:
                all_files.append(full_path)
        return all_files

    @staticmethod
    def load_yaml(file):
        """Method parses yaml file into Python dict

        Returns:
            dict: Parsed yaml file
        """
        with open(file) as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    @staticmethod
    def load_json(file):
        """Method parses json file into Python dict

        Returns:
            dict: Parsed json file
        """
        with open(file) as f:
            return json.load(f)
