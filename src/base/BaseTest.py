import unittest
from datetime import datetime

from src.handlers.EventHandler import EventHandler
from src.parsers.ConfigParser import ConfigParser


class BaseTest(unittest.TestCase):

    scenario = None
    handler = None
    driver = None
    screen_shot_path = None

    @classmethod
    def setUpClass(cls):
        cls.handler = EventHandler()
        if "setupclass" in cls.scenario:
            cls.handler.execute(cls, cls.scenario['setup_class'])

    def setUp(self):
        self.screen_shot_path = None
        if "setup" in self.scenario:
            self.handler.execute(self, self.scenario['setup'])

    def base_method(self, **data):
        if "steps" in self.scenario:
            self.handler.execute(self, self.scenario['steps'], data)

    def tearDown(self):
        if ConfigParser().get_report_config()['screenshots']:
            self._screen_shot_on_error()
        if "teardown" in self.scenario:
            self.handler.execute(self, self.scenario['teardown'])

    @classmethod
    def tearDownClass(cls):
        if "teardown_class" in cls.scenario:
            cls.handler.execute(cls, cls.scenario['teardown_class'])

    def _screen_shot_on_error(self):
        """Take a Screen-shot of the drive homepage, when it Failed."""
        for method, error in self._outcome.errors:
            if error:
                filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + self.id() + ".png"
                path = ConfigParser().get_report_config()['output'] + "\\screenshots\\" + filename
                self.driver.get_screenshot_as_file(path)
                self.screen_shot_path = "screenshots\\" + filename


def factory(class_name, scenario):
    return type(class_name, (BaseTest,), {"scenario": scenario})
