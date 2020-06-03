import os
import unittest
from datetime import datetime
from selenium_generator.base.exceptions import InvalidScenario
from selenium_generator.base.file_manager import FileManager
from selenium_generator.handlers.event_handler import EventHandler
from selenium_generator.parsers.config_parser import ConfigParser


class BaseTest(unittest.TestCase):

    errors = None
    scenario = None
    handler = None
    driver = None
    screen_shot_path = None

    @classmethod
    def setUpClass(cls):
        cls.handler = EventHandler()
        if "before_all" in cls.scenario:
            cls.handler.execute(cls, cls.scenario['before_all'])

    def setUp(self):
        if self.errors is not None:
            raise InvalidScenario(self.errors)
        self.screen_shot_path = None
        if "before_each" in self.scenario:
            self.handler.execute(self, self.scenario['before_each'])

    def base_method(self, **data):
        if "steps" in self.scenario:
            self.handler.execute(self, self.scenario['steps'], data)

    def tearDown(self):
        if ConfigParser().get_report_config()['screenshots']:
            self._screen_shot_on_error()
        if "after_each" in self.scenario:
            self.handler.execute(self, self.scenario['after_each'])

    @classmethod
    def tearDownClass(cls):
        if "after_all" in cls.scenario:
            cls.handler.execute(cls, cls.scenario['after_all'])

    def _screen_shot_on_error(self):
        """Take a Screen-shot of the drive homepage, when it Failed."""
        for method, error in self._outcome.errors:
            if error:
                filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + self.id() + ".png"
                path = ConfigParser().get_report_config()['output'] + "\\screenshots\\" + filename
                FileManager.mkdir(os.path.dirname(path))
                self.driver.get_screenshot_as_file(path)
                self.screen_shot_path = "screenshots\\" + filename


def factory(class_name, scenario):
    return type(class_name, (BaseTest,), {"scenario": scenario})
