import unittest
from selenium_generator.factories.tests.base_test import BaseTest
from selenium_generator.base.exceptions import InvalidScenario
from selenium_generator.base.singleton import singleton
from selenium_generator.parsers.config_parser import ConfigParser
import ddt
from selenium_generator.validators.validator import SchemaValidator


@singleton
class TestFactory:

    v = SchemaValidator()

    def __call__(self, scenario):
        self.scenario = scenario
        self.test_class = type(scenario['name'], (BaseTest,), {"scenario": scenario})
        self.test_method = self.test_class.base_method
        return self

    def create(self):
        if not self._validate_scenario():
            return self.test_class

        if self._check_skip():
            return self.test_class

        if self._check_data():
            return ddt.ddt(self.test_class)
        return self.test_class

    def _check_data(self):
        if 'data' not in self.scenario or self.scenario['data'] is None:
            self._create_test_method()
            return False

        if isinstance(self.scenario['data'], str):
            data_path = ConfigParser().get_data_path(self.scenario['data'])
            self._create_test_method(
                ddt.file_data(data_path)(getattr(self.test_class, self.test_method.__name__))
            )
            return True

        ddt._add_tests_from_data(self.test_class, self._generate_test_name(), self.test_method, self.scenario['data'])
        return True

    def _validate_scenario(self):
        try:
            self.v.validate_scenario(self.scenario)
        except InvalidScenario as e:
            setattr(self.test_class, "errors", str(self.v.get_errors()))
            self._create_test_method()
            return False
        else:
            return True

    def _check_skip(self):
        if "skip" in self.scenario:
            self._create_test_method(
                unittest.skip(self.scenario['skip'])(getattr(self.test_class, self.test_method.__name__))
            )
            return True
        return False

    def _create_test_method(self, fn=None):
        setattr(self.test_class, self._generate_test_name(), self.test_method if fn is None else fn)
        return self.test_method

    def _generate_test_name(self):
        return "test_" + self.scenario['name']

