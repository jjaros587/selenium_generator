"""
    Module contains class loads required test scenarios and generate test classes based on given parameters.
"""
from typing import Callable
from unittest import TestLoader, TestSuite
from selenium_generator.base.singleton import singleton
from selenium_generator.base.file_manager import FileManager
from selenium_generator.factories.tests.test_factory import TestFactory
from selenium_generator.parsers.config_parser import ConfigParser


@singleton
class Loader:
    """Class for loading scenarios.

    Args:
        config_parser (ConfigParser): Class for parsing of configuration
        test_factory (TestFactory): Class for generating of tests from scenarios in yaml.
        file_manager (FileManager): Class files manipulation

    Attributes:
        test_factory (TestFactory): Instance of class for generating of tests
        file_manager (FileManager): Class for generating of tests from scenarios in yaml.
        scenarios (list(str)):  List of paths of all test scenarios.
        tags (list(str)): List of tags from configuration.
    """
    def __init__(self, config_parser: Callable = ConfigParser, test_factory: Callable = TestFactory, file_manager=FileManager):
        self.file_manager = file_manager
        self.scenarios = self.file_manager.get_list_of_files(config_parser().get_scenarios_path())
        self.tags = config_parser().get_tags()
        self.test_factory = test_factory()

    def load_scenarios(self, driver_name):
        """Methods parses each scenario, checks it and adds them into test suite

        Args:
            driver_name (str): Name of a driver

        Returns:
            unittest.TestSuite: Test suite created for loaded valid scenarios
        """
        tests = []
        for item in self.scenarios:
            scenario = self.file_manager.load_yaml(item)
            if not self._verify_tags(scenario):
                continue
            if not self._verify_drivers(driver_name, scenario):
                continue
            test_class = self.test_factory(scenario, driver_name).create()
            tests.append(TestLoader().loadTestsFromTestCase(test_class))

        return TestSuite(tests)

    def _verify_tags(self, scenario):
        """Method checks if scenario contains any of tags from configuration

        Args:
            scenario (dict): Parsed scenario

        Returns:
            bool: True - scenario contains tag, False - scenario doesn't contain tag
        """
        if self.tags.__len__() > 0 and ('tags' not in scenario or scenario['tags'].__len__() == 0):
            return False
        if self.tags.__len__() == 0 and scenario['tags'].__len__() == 0:
            return True
        if 'tags' in scenario and scenario['tags'] is not None:
            if "*" not in scenario['tags'] and not any(i in self.tags for i in scenario['tags']):
                return False
        return True

    def _verify_drivers(self, driver_name, scenario):
        """Method checks if scenario contains driver we want to run tests for

        Args:
            driver_name (str): Name of a driver
            scenario (dict): Test scenario
        Returns:
            bool: True - scenario contains driver, False - scenario doesn't contain driver
        """
        if 'drivers' not in scenario:
            return True
        if scenario['drivers'].__len__() > 0:
            if driver_name not in scenario['drivers']:
                return False
        return True
