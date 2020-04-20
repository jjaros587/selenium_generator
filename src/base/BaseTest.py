import unittest
from src.handlers.EventHandler import EventHandler


class BaseTest(unittest.TestCase):

    scenario = None
    handler = None

    @classmethod
    def setUpClass(cls):
        cls.handler = EventHandler()
        if "set_up_class" in cls.scenario:
            cls.handler.execute(cls, cls.scenario['set_up_class'])

    def setUp(self):
        if "set_up" in self.scenario:
            self.handler.execute(self, self.scenario['set_up'])

    def base_method(self, **data):
        if "steps" in self.scenario:
            self.handler.execute(self, self.scenario['steps'], data)

    def tearDown(self):
        if "tear_down" in self.scenario:
            self.handler.execute(self, self.scenario['tear_down'])

    @classmethod
    def tearDownClass(cls):
        if "tear_down_class" in cls.scenario:
            cls.handler.execute(cls, cls.scenario['tear_down_class'])


def factory(class_name, scenario):
    return type(class_name, (BaseTest,), {"scenario": scenario})
