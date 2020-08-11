import unittest
from selenium_generator.factories.tests.base_test import BaseTest
from selenium_generator.base.singleton import singleton
from selenium_generator.handlers.event_handler import EventHandler
from selenium_generator.parsers.config_parser import ConfigParser
import ddt
from selenium_generator.validators.validator import SchemaValidator


@singleton
class TestFactory:
    """Class for generating of test class from test scenario.

    Args:
        config_parser (ConfigParser): Class for parsing of a configuration
        validator (cerberus.validator.Validator): Class used for validation of test scenario
        base_test (BaseTest): Class used as a template for test scenario
        handler (EventHandler): Class used for executing of test scenario steps

    Attributes:
        config_parser (ConfigParser): Instance of a config parser
        validator (cerberus.validator.Validator): Instance of a validator class
        base_test (BaseTest): Instance of a template for test class
        handler (EventHandler): List of a class for executing of test scenario steps
        drivers (dict): Configuration of drivers
    """
    def __init__(self, config_parser=ConfigParser, validator=SchemaValidator, base_test=BaseTest, handler=EventHandler):
        self.validator = validator()
        self.config_parser = config_parser
        self.drivers = self.config_parser().get_drivers_config().keys()
        self.base_test=base_test
        self.handler=handler

    def __call__(self, scenario, driver_name):
        self.scenario = scenario
        self.test_class = type(scenario['name'], (self.base_test,), {
            "scenario": scenario,
            "driver_name": driver_name,
            "handler": self.handler,
            "config_parser": self.config_parser
        })
        self.test_method = self.test_class.base_method
        return self

    def create(self):
        """Main method for generating of test class based on parameters specified in a test scenario.

        Returns:
            BaseTest: Generated test class
        """
        if not self._validate_scenario():
            return self.test_class

        if not self._validate_drivers():
            return self.test_class

        if self._check_skip():
            return self.test_class

        if self._check_data():
            return ddt.ddt(self.test_class)
        return self.test_class

    def _check_data(self):
        """Method checks if any data were specified in test scenario and decorates a test method with needed function
        from `ddt` package.

        Returns:
            bool: True - data were specified, False - data were not specified
        """
        if 'data' not in self.scenario or self.scenario['data'] is None:
            self._create_test_method()
            return False

        if isinstance(self.scenario['data'], str):
            data_path = self.config_parser().get_data_path(self.scenario['data'])
            self._create_test_method(
                ddt.file_data(data_path)(getattr(self.test_class, self.test_method.__name__))
            )
            return True

        ddt._add_tests_from_data(self.test_class, self._generate_test_name(), self.test_method, self.scenario['data'])
        return True

    def _validate_scenario(self):
        """Method validates test scenario structure.

        Returns:
            bool: True - valid, False - invalid
        """
        if not self.validator.validate_scenario(self.scenario):
            setattr(self.test_class, "errors", str(self.validator.get_errors()))
            self._create_test_method()
            return False
        return True

    def _validate_drivers(self):
        """Method validates names of drivers specified in drivers object.

        Returns:
            bool: True - valid, False - invalid
        """
        if 'drivers' in self.scenario:
            if self.scenario['drivers'].__len__() > 0:
                if any(i not in self.drivers for i in self.scenario['drivers']):
                    setattr(self.test_class, "errors", str(self.validator.get_errors()))
                    self._create_test_method()
                    return False
        return True

    def _check_skip(self):
        """Method checks skip object in test scenario and decorates test method with function `unittest.skip`
        if the object has value True.

        Returns:
            bool: True - Test is skipped, False - Test is not skipped
        """
        if "skip" in self.scenario:
            self._create_test_method(
                unittest.skip(self.scenario['skip'])(getattr(self.test_class, self.test_method.__name__))
            )
            return True
        return False

    def _create_test_method(self, fn=None):
        """Method generates test method based on a base method from base test class

        Args:
            fn (type): Parameters used for specifying decorated test method

        Returns:
            BaseTest: Generated test method of a test class
        """
        setattr(self.test_class, self._generate_test_name(), self.test_method if fn is None else fn)
        return self.test_method

    def _generate_test_name(self):
        """Method generates test method name based of a name specified in test scenario.

        Returns:
            str: Generated test method name
        """
        return "test_" + self.scenario['name']

