from unittest import TestLoader, TestSuite
from selenium_generator.base.file_manager import FileManager
from selenium_generator.factories.tests.test_factory import TestFactory
from selenium_generator.parsers.config_parser import ConfigParser


class Loader:
    """Class for loading scenarios.

    Attributes:
        tests (list(:class:`unittest.TestCase`)):
        scenarios (list(str)):
        tags (list(str)):
        test_creator (TestFactory):
    """
    def __init__(self):
        self.tests = []
        self.scenarios = FileManager.get_list_of_files(ConfigParser().get_scenarios_path())
        self.tags = ConfigParser().get_tags()
        self.drivers = ConfigParser().get_allowed_drivers()
        self.test_creator = TestFactory()

    def load_scenarios(self, driver_name):
        """Methods parses each scenario, checks it and adds them into test suite

        Args:
            driver_name (str): Name of a driver

        Returns:
            unittest.TestSuite: Test suite created for loaded valid scenarios
        """
        for item in self.scenarios:
            scenario = FileManager.load_yaml(item)
            if not self._verify_tags(scenario):
                continue
            if not self._verify_drivers(driver_name, scenario):
                continue
            test_class = self.test_creator(scenario, driver_name).create()
            self.tests.append(TestLoader().loadTestsFromTestCase(test_class))

        return TestSuite(self.tests)

    def _verify_tags(self, scenario):
        """Method checks if scenario contains any of tags from configuration

        Args:
            scenario (dict): Parsed scenario

        Returns:
            bool: True - scenario contains tag, False - scenario doesn't contain tag
        """
        if 'tags' not in scenario and self.tags.__len__() > 0:
            return False
        if scenario['tags'].__len__() == 0:
            return False
        if "*" not in scenario['tags'] and not any(i in self.tags for i in scenario['tags']):
            return False
        return True

    def _verify_drivers(self, driver_name, scenario):
        """Method checks if scenario contains driver we want to run tests for

        Args:
            driver_name (str): Name of a driver

        Returns:
            bool: True - scenario contains driver, False - scenario doesn't contain driver
        """
        if scenario['drivers'].__len__() > 0:
            if driver_name not in scenario['drivers']:
                return False
        return True
