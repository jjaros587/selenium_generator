import unittest
from src.handlers.EventHandler import EventHandler


class BaseTest(unittest.TestCase):

    scenario = None
    handler = None

    @classmethod
    def setUpClass(cls):
        cls.handler = EventHandler()
        if "setupclass" in cls.scenario:
            cls.handler.execute(cls, cls.scenario['setup_class'])

    def setUp(self):
        if "setup" in self.scenario:
            self.handler.execute(self, self.scenario['setup'])

    def base_method(self, **data):
        if "steps" in self.scenario:
            self.handler.execute(self, self.scenario['steps'], data)

    def tearDown(self):
        if "teardown" in self.scenario:
            self.handler.execute(self, self.scenario['teardown'])

    @classmethod
    def tearDownClass(cls):
        if "teardown_class" in cls.scenario:
            cls.handler.execute(cls, cls.scenario['teardown_class'])


def factory(class_name, scenario):
    return type(class_name, (BaseTest,), {"scenario": scenario})
