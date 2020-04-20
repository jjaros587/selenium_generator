from unittest import TestLoader, TestSuite
from src.base.utils import get_list_of_files, load_yaml
from src.factories.TestCreator import TestCreator
from src.parsers.ConfigParser import ConfigParser


class Loader:

    def __init__(self):
        self.tests = []
        self.scenarios = get_list_of_files(ConfigParser().get_scenarios_path())
        self.tags = ConfigParser().get_tags()
        self.test_creator = TestCreator()

    def load_scenarios(self):
        for item in self.scenarios:
            scenario = load_yaml(item)
            if not self._verify_tags(scenario):
                continue
            test_class = self.test_creator(load_yaml(item)).create()
            self.tests.append(TestLoader().loadTestsFromTestCase(test_class))

        return TestSuite(self.tests)

    def _verify_tags(self, scenario):
        if self.tags is not None:
            if 'tags' not in scenario:
                return False
            if scenario['tags'] is None:
                return False
            if scenario['tags'].__len__() == 0:
                return False
            if "*" not in scenario['tags'] and not any(i in self.tags for i in scenario['tags']):
                return False
        return True
