import unittest
from src.generator.Handler import Handler


class BaseTest(unittest.TestCase):

    scenario = None
    handler = Handler()

    def setUp(self):
        self.handler.do(self, self.scenario['setUp'])

    def tearDown(self):
        self.handler.do(self, self.scenario['tearDown'])

    def base_method(self, **kwargs):
        self.handler.do(self, self.scenario['steps'], kwargs)


def factory(class_name, scenario):
    return type(class_name, (BaseTest,), {"scenario": scenario})
