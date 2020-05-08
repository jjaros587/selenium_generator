from selenium_generator.factories.drivers.driver_factory import DriverFactory
from selenium_generator.parsers.config_parser import ConfigParser
import importlib
import inspect
import sys


class Keywords:

    def __init__(self):
        sys.path.append(ConfigParser().get_pages_path())
        self.pages = importlib.import_module("pages")

    def __call__(self, test, data):
        self.test = test
        self.data = data

    def _run_driver(self, command):
        self.test.driver = DriverFactory().run(command)

    def _maximize(self, *args, **kwargs):
        self.test.driver.maximize_window()

    def _close_driver(self, *args, **kwargs):
        self.test.driver.close()

    def _page_object(self, command):
        my_class = getattr(getattr(self.pages, command['class']), command['class'])
        instance = my_class(self.test.driver)
        MethodExecutor.execute_method(
            instance,
            command['method'],
            command['params'] if 'params' in command and command['params'] is not None else None,
            self.data
        )


class MethodExecutor:

    @classmethod
    def execute_method(cls, class_instance, method, params, data):
        arguments = inspect.signature(getattr(class_instance, method)).parameters
        if arguments.__len__() == 0:
            cls.call_method(class_instance, method)
        elif params is not None:
            cls.call_method(class_instance, method, arguments, params)
        else:
            cls.call_method(class_instance, method, arguments, data)

    @classmethod
    def call_method(cls, class_instance, method, arguments=None, data=None):
        if not arguments:
            getattr(class_instance, method)()
        else:
            getattr(class_instance, method)(**cls.feed_params(arguments, data))

    @classmethod
    def feed_params(cls, arguments, data):
        values = dict()
        for argument in arguments:
            if argument in data:
                values.update({argument: data[argument]})
        return values
