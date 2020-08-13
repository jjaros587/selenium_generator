import unittest
from selenium_generator.base.singleton import singleton


@singleton
class TestClass:
    pass


class SingletonTest(unittest.TestCase):

    def test_singleton(self):
        a = TestClass()
        b = TestClass()
        self.assertTrue(a is b)
