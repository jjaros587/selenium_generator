import unittest
from src.generator.Handler import Handler


class BaseTest(unittest.TestCase):

    data = None
    handler = Handler()

    def setUp(self):
        self.handler.do(self, self.data['setUp'])

    def tearDown(self):
        self.handler.do(self, self.data['tearDown'])

    def base_method(self):
        self.handler.do(self, self.data['scenario'])


def factory(class_name, data):
    return type(class_name, (BaseTest,), {"data": data})
