import os
import shutil
import unittest
from ddt import ddt, data, unpack
from selenium_generator.base.file_manager import FileManager
from pathlib import Path


@ddt
class FileManagerTest(unittest.TestCase):

    path = os.path.join(os.path.dirname(__file__), "test_data")
    path_mkdir = os.path.join(path, "test_mkdir")
    path_rmtree = os.path.join(path, "test_rmtree")

    @classmethod
    def setUpClass(cls):
        os.makedirs(os.path.dirname(os.path.join(cls.path_rmtree, "inner_folder", "test_file.txt")))

    def test_remove_tree(self):
        FileManager.remove_tree(self.path_rmtree)
        self.assertFalse(Path(self.path_rmtree).exists())

    def test_mkdir(self):
        FileManager.mkdir(self.path_mkdir)
        self.assertTrue(Path(self.path_mkdir).exists())

    @data(("test_json.json", True), ("blabla.json", False))
    @unpack
    def test_file_exists(self, filename, result):
        self.assertTrue(FileManager.file_exists(os.path.join(self.path, filename)) == result)

    def test_get_list_of_files(self):
        self.assertEqual(FileManager.get_list_of_files(self.path).__len__(), 3)

    def test_load_yaml(self):
        file = FileManager.load_yaml(os.path.join(self.path, "test_yaml.yaml"))
        self.assertEqual(type(file), dict)
        self.assertEqual(file["test_key"], "test_value")

    def test_load_json(self):
        file = FileManager.load_json(os.path.join(self.path, "test_json.json"))
        self.assertEqual(type(file), dict)
        self.assertEqual(file["test_key"], "test_value")

    @data(("test_json.json", True), ("test_yaml.yaml", False))
    @unpack
    def test_check_extension(self, filename, result):
        self.assertEqual(FileManager.check_extension(os.path.join(self.path, filename), ".json"), result)

    @classmethod
    def tearDownClass(cls):
        if Path(cls.path_mkdir).exists():
            Path(cls.path_mkdir).rmdir()

        if Path(cls.path_rmtree).exists():
            shutil.rmtree(cls.path_rmtree)
