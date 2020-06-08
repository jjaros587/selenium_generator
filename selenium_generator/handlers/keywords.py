from selenium_generator.factories.drivers.driver_factory import DriverFactory
from selenium_generator.parsers.config_parser import ConfigParser
import importlib
import inspect
import sys


class Keywords:
    """Class stores all keywords which can be used in test scenario and its implementation.

    Attributes:
        pages (module): Module with all Page Objects loaded from directory specified in configuration
        test (BaseTest): Instance of BaseTest class
        data (dict): Test data
    """

    def __init__(self):
        sys.path.append(ConfigParser().get_pages_path())
        self.pages = importlib.import_module("pages")

    def __call__(self, test, data):
        self.test = test
        self.data = data

    def _run_driver(self, command):
        """Method initializes instance of required driver.

        Args:
            command (str): Name of a driver to be used
        """
        self.test.driver = DriverFactory().run(command)

    def _maximize(self, *args, **kwargs):
        """Method maximizes window of a driver"""
        self.test.driver.maximize_window()

    def _close_driver(self, *args, **kwargs):
        """Method close instance of a driver"""
        self.test.driver.close()

    def _page_object(self, command):
        """Method executes required method of a given Page Object and parse data in it.

        Args:
            command (dict): Parameters for Page Object to be used based of configuration structure
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
    def execute_method(cls, class_instance, method, params, data):
        """The main method of a class. Gets arguments of a method to be run and calls method for calling itself
        with the right parameters.

        Args:
            class_instance:
            method:
            params (dict): Data from params in scenario step
            data (dict): Data from DDT
        """
        arguments = inspect.signature(getattr(class_instance, method)).parameters
        if arguments.__len__() == 0:
            cls._call_method(class_instance, method)
        elif params is not None:
            cls._call_method(class_instance, method, arguments, params)
        else:
            cls._call_method(class_instance, method, arguments, data)

    @classmethod
    def _call_method(cls, class_instance, method, arguments=None, data=None):
        """Method for calling given method based on the given parameters.

        Args:
            class_instance:
            method:
            arguments (dict): Arguments of a method to be called
            data (dict): Test data
        """
        if not arguments:
            getattr(class_instance, method)()
        else:
            getattr(class_instance, method)(**cls._feed_params(arguments, data))

    @classmethod
    def _feed_params(cls, arguments, data):
        """Method feeds method with given data based on method arguments.

        Args:
            arguments (dict): Arguments of a method to be called
            data (dict): Test data
        """
        values = dict()
        for argument in arguments:
            if argument in data:
                values.update({argument: data[argument]})
        return values
