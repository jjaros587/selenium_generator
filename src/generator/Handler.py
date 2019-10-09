from src.generator.utils import import_submodules
from src.generator.ConfigParser import ConfigParser
from src.generator.DriverManger import DriverManager
import importlib


class Handler:
    pages = import_submodules(
                importlib.import_module(
                    ConfigParser().get_pages_path()
                ))

    def __call__(self, test_instance, data):
        self.test = test_instance
        self.data = data

    def do(self, instance, data):
        self.__call__(instance, data)
        for command in self.data:
            [[key, value]] = command.items()
            self.mapping[key](self, value)

    def _run_driver(self, command):
        self.test.driver = DriverManager.run_driver(command)

    def _close_driver(self, *args, **kwargs):
        self.test.driver.close()

    def _page_object(self, command):
        my_class = getattr(self.pages[command['class']], command['class'])
        instance = my_class(self.test.driver)
        self._call_method(instance, command['method'], command['params'])

    @staticmethod
    def _call_method(class_instance, method, params):
        getattr(class_instance, method)(**params)

    mapping = {
        "runDriver": _run_driver,
        "closeDriver": _close_driver,
        "pageObject": _page_object
    }
