from unittest import TestLoader, TestSuite
from src.base.utils import get_list_of_files, load_yaml
from src.factories.TestCreator import TestCreator
from src.parsers.ConfigParser import ConfigParser


class Loader:

    tests = []

    def load_scenarios(self):
        for item in get_list_of_files(ConfigParser().get_scenarios_path()):
            test_class = TestCreator(load_yaml(item)).create()
            self.tests.append(TestLoader().loadTestsFromTestCase(test_class))

        return TestSuite(self.tests)
