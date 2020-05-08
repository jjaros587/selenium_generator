import os
import shutil
from pathlib import Path


class FileManager:

    @staticmethod
    def remove_tree(path):
        if Path(path).exists():
            shutil.rmtree(path)

    @staticmethod
    def mkdir(path, parents=True, exists_ok=True):
        Path(path).mkdir(parents=parents, exist_ok=exists_ok)

    @staticmethod
    def get_list_of_files(dir_name):
        all_files = list()
        for f in os.listdir(dir_name):
            full_path = os.path.join(dir_name, f)
            if os.path.isdir(full_path):
                all_files += FileManager.get_list_of_files(full_path)
            else:
                all_files.append(full_path)
        return all_files
