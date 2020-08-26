"""
    Module contains class which stores implementation of keywords and related class for calling methods of classes.
"""

import sys
import pathlib
import inspect
import importlib
from selenium_generator.factories.drivers.driver_factory import DriverFactory
from selenium_generator.parsers.config_parser import ConfigParser


class Keywords:
    """Class stores all keywords which can be used in test scenario and its implementation.

    Attributes:
        pages (module): Module with all Page Objects loaded from directory specified in configuration
        test (:class:`unittest.TestCase`): Instance of BaseTest class
        data (dict): Test data
    """

    def __init__(self):
        path = ConfigParser().get_pages_path()
        sys.path.append(path)
        self.pages = importlib.import_module(pathlib.PurePath(path).name)

    def __call__(self, test, data):
        self.test = test
        self.data = data

    def run_driver(self, *args, **kwargs):    # pylint: disable=unused-argument
        """Method initializes instance of required driver."""
        self.test.driver = DriverFactory().run(self.test.driver_name)

    def maximize(self, *args, **kwargs):    # pylint: disable=unused-argument
        """Method maximizes window of a driver"""
        self.test.driver.maximize_window()

    def close_driver(self, *args, **kwargs):    # pylint: disable=unused-argument
        """Method close instance of a driver"""
        self.test.driver.close()

    def page_object(self, command):
        """Method executes required method of a given Page Object and parse data in it.

        Args:
            command (dict): Object with specification of a keyword for Page Object
        """
        my_class = getattr(getattr(self.pages, command['class']), command['class'])
        instance = my_class(self.test.driver)
        MethodExecutor.execute_method(
            instance,
            command['method'],
            command['params'] if 'params' in command and command['params'] is not None else None,
            self.data
        )


class MethodExecutor:
    """Class executes method of a required class with given data based on a type of data specification"""

    @classmethod
    def execute_method(cls, instance, method, params, data):
        """The main method of a class. Gets arguments of a method to be run and calls method for calling itself
        with the right parameters.

        Args:
            instance: Instance of the class whose method we want to execute
            method (str): Name of a class method to execute.
            params (dict): Data from params in scenario step
            data (dict): Data from DDT
        """
        arguments = inspect.signature(getattr(instance, method)).parameters
        if arguments.__len__() == 0:
            cls._call_method(instance, method)
        elif params is not None:
            cls._call_method(instance, method, arguments, params)
        else:
            cls._call_method(instance, method, arguments, data)

    @classmethod
    def _call_method(cls, instance, method, arguments=None, data=None):
        """Method for calling given method based on the given parameters.

        Args:
            instance: Instance of the class whose method we want to execute
            method (str): Name of a class method to execute.
            arguments (dict): Arguments of a method to be called
            data (dict): Test data
        """
        if not arguments:
            getattr(instance, method)()
        else:
            getattr(instance, method)(**cls._feed_params(arguments, data))

    @classmethod
    def _feed_params(cls, arguments, data):
        """Method feeds method with given data based on method arguments.

        Args:
            arguments (dict): Arguments of a method to be called with
            data (dict): Test data

        Returns:
            dict: Parameters to be parsed in a given method
        """
        values = dict()
        for argument in arguments:
            if argument in data:
                values.update({argument: data[argument]})
        return values
