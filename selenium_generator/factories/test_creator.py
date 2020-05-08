import unittest

from selenium_generator.base.base_test import factory
from selenium_generator.base.utils import singleton
from selenium_generator.parsers.config_parser import ConfigParser
import ddt
from selenium_generator.validators.validator import SchemaValidator


@singleton
class TestCreator:

    v = SchemaValidator()

    def __call__(self, scenario):
        self.scenario = scenario
        self.test_class = factory(scenario['name'], scenario)
        self.test_method = self.test_class.base_method
        return self

    def create(self):
        if not self.v.validate_scenario(self.scenario):
            self._create_test_method(
                (unittest.skip("Invalid scenario structure: " + str(self.v.get_errors())))(self.test_method)
            )
            return self.test_class

        self._check_data()
        return ddt.ddt(self.test_class)

    def _check_data(self):
        if 'data' not in self.scenario or self.scenario['data'] is None:
            return

        if isinstance(self.scenario['data'], str):
            data_path = ConfigParser().get_data_path(self.scenario['data'])
            self._create_test_method(
                ddt.file_data(data_path)(getattr(self.test_class, self.test_method.__name__))
            )
            return

        ddt._add_tests_from_data(self.test_class, self._generate_test_name(), self.test_method, self.scenario['data'])

    def _create_test_method(self, fn=None):
        setattr(self.test_class, self._generate_test_name(), self.test_method if fn is None else fn)
        return self.test_method

    def _generate_test_name(self):
        return "test_" + self.scenario['name']
