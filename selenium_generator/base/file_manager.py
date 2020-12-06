"""
    Module contains static class which is used for file and folder management.
"""

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
        for file in os.listdir(dir_path):
            full_path = os.path.join(dir_path, file)
            if os.path.isdir(full_path):
                all_files += FileManager.get_list_of_files(full_path)
            else:
                all_files.append(full_path)
        return all_files

    @staticmethod
    def load_yaml(file_path):
        """Method parses yaml file into Python dict

        Returns:
            dict: Parsed yaml file
        """
        with open(file_path) as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    @staticmethod
    def load_json(file_path):
        """Method parses json file into Python dict

        Returns:
            dict: Parsed json file
        """
        with open(file_path) as file:
            return json.load(file)

    @staticmethod
    def check_extension(file_path, extension):
        """Method checks extension of a given file path.

        Returns:
            file_patch (str): Path to a file
            extension (str): Required extension of a file

        Returns:
            bool: True - Correct extension, False - Incorrect extension
        """
        return Path(file_path).suffix == extension
