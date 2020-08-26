"""
    Module contains base test class which serves as template for test class generating.
"""

import os
import unittest
from datetime import datetime
from typing import Callable
from selenium_generator.base.exceptions import InvalidScenario
from selenium_generator.base.file_manager import FileManager
from selenium_generator.handlers.event_handler import EventHandler


class BaseTest(unittest.TestCase):
    """Base class which serves as a template for generating of a test class from test scenario.

    Attributes:
        errors (dict): Errors which are present in a test scenario
        scenario (dict): Loaded test scenario in dictionary format
        handler (EventHandler): Instance of a class for executing of steps from test scenario
        driver (:class:`selenium.webdriver.remote.webdriver.WebDriver`): Instance of a WebDriver
        screen_shot_path (str): Path to a screenshot taken on fail
        driver_name (str): Name of a driver to be used
        config_parser (ConfigParser): Class for parsing of a configuration
    """
    errors = None
    scenario = None
    handler = None
    driver = None
    screen_shot_path = None
    driver_name = None
    config_parser: Callable = None

    @classmethod
    def setUpClass(cls):
        """Method is executed before all test methods in the class"""
        if cls.errors is None:
            cls.handler = EventHandler()
            if "before_all" in cls.scenario:
                cls.handler.execute(cls, cls.scenario['before_all'])

    def setUp(self):
        """Method is executed before each test methods in the class.

        Raises:
            InvalidScenario: It is raised when a test scenario is invalid
        """
        if self.errors is not None:
            raise InvalidScenario(self.errors)
        if "before_each" in self.scenario:
            self.handler.execute(self, self.scenario['before_each'])

    def base_method(self, **data):
        """Base method which serves as a template for generation of a test method from test scenario."""
        if "steps" in self.scenario:
            self.handler.execute(self, self.scenario['steps'], data)

    def tearDown(self):
        """Method is executed after each test methods in the class"""
        if self.config_parser().get_report_config()['screenshots']:
            self._screen_shot_on_error()
        if "after_each" in self.scenario:
            self.handler.execute(self, self.scenario['after_each'])

    @classmethod
    def tearDownClass(cls):
        """Method is executed after all test methods in the class"""
        if "after_all" in cls.scenario:
            cls.handler.execute(cls, cls.scenario['after_all'])

    def _screen_shot_on_error(self):
        """Method takes and saves a screen shot of a driver page on fail."""
        for method, error in self._outcome.errors:  # pylint: disable=unused-variable
            if error:
                filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + self.id() + ".png"
                path = self.config_parser().get_report_config()['output'] + "\\screenshots\\" + filename
                FileManager.mkdir(os.path.dirname(path))
                self.driver.get_screenshot_as_file(path)
                self.screen_shot_path = "screenshots\\" + filename
