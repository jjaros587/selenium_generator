"""
    Module contains classes which are used for parsing of configuration and constant with default configuration.
"""

import os
import sys
from selenium_generator.base.file_manager import FileManager
from selenium_generator.base.singleton import singleton
from selenium_generator.parsers.arg_parser import ArgParser
from selenium_generator.test_runner import runner
from selenium_generator.validators.validator import SchemaValidator


DEFAULT_CONFIG = {
    'scenarios': "scenarios",
    'data': "data",
    'pages': "pages",

    'report': {
        'screenshots': True,
        'clean': True,
    },

    'tags': [],

    'drivers': {
        'chrome': {
            'remote': False
        },
        'firefox': {
            'remote': False
        }
    }
}
"""Constant with default configuration"""


@singleton
class ConfigParser:
    """Class for loading and parsing the configuration.

    Args:
        config_path (str): Path to a file with the configuration
        file_manager (FileManager): Class for file manipulation

    Attributes:
        config (dict): Parsed configuration
        allowed_drivers (list(str)): List of allowed drivers from the configuration
    """
    def __init__(self, config_path='config.yaml', file_manager=FileManager):
        arg_config = ArgParser().get_config()
        if arg_config is not None:
            self.config = file_manager.load_yaml(arg_config)
        elif file_manager.file_exists(config_path):
            self.config = file_manager.load_yaml(config_path)
        else:
            self.config = DEFAULT_CONFIG

        SchemaValidator().validate_config(self.config)
        ConfigUpdater(self).update_config()
        self.allowed_drivers = None

    def get_pages_path(self):
        """Method returns a path to a directory with Page Objects.

        Returns:
            str: Path to a directory with Page Objects.
        """
        return self.get_path(self.config['pages'])

    def get_scenarios_path(self):
        """Method returns a path to a directory with scenarios.

        Returns:
            str: Path to a directory with scenarios.
        """
        return self.get_path(self.config['scenarios'])

    def get_report_config(self):
        """Method returns an object with a configuration of test report.

        Returns:
            dict: Object with test report configuration.
        """
        return self.config['report']

    def get_report_params(self):
        """Method returns an object with parameters for generating of file with test report.

        Returns:
            dict: Object with paremeters for test report file.
        """
        return self.config['report']['params'] if 'params' in self.config['report'] else {}

    def get_drivers_config(self):
        """Method returns an object with a configuration of drivers.

        Returns:
            dict: Object with drivers configuration.
        """
        return self.config['drivers']

    def get_allowed_drivers(self):
        """Method returns a list of allowed drivers from configuration.

        Returns:
            list: List of allowed drivers in configuration.
        """
        if self.allowed_drivers is not None:
            return self.allowed_drivers
        drivers = []
        for driver, properties in self.config['drivers'].items():
            if 'allowed' in properties:
                if not properties['allowed']:
                    continue
            drivers.append(driver)
        return drivers

    def get_data_path(self, data_path):
        """Method returns a path to a directory with data for scenarios.

        Returns:
            str: Path to a directory with scenarios data.
        """
        return os.path.join(self.get_path(self.config['data']), data_path)

    def get_tags(self):
        """Method returns a list of tags which we want to run.

        Returns:
            list: List of tags specified in configuration.
        """
        return self.config['tags']

    @staticmethod
    def get_path(folder):
        """Method returns a full path for a given path.

        Returns:
            str: Full path of a given path.
        """
        return os.path.join(os.path.dirname(sys.modules['__main__'].__file__), folder)


@singleton
class ConfigUpdater:
    """Class for updating of the configuration.
    Class checks the loaded configuration and values for missing objects from the default configuration.

    Args:
        parser (ConfigParser): Instance of config parser with the stored configuration.

    Attributes:
        parser (ConfigParser): Instance of config parser with the stored configuration.
        config (dict): Loaded configuration.
    """
    def __init__(self, parser):
        self.parser = parser
        self.config = parser.config

    def update_config(self):
        """The main method of the class which executes methods for verification of specific keys in the configuration."""
        self._verify_scenarios()
        self._verify_pages()
        self._verify_data()
        self._verify_tags()
        self._verify_report()

    def _verify_scenarios(self, key="scenarios"):
        """Method checks configuration for scenarios and add the default value if the related object is not specified.

        Args:
            key (str): Name of an object key of scenarios.
        """
        self._check_object(key)

    def _verify_pages(self, key="pages"):
        """Method checks configuration for Page Objects add the default value if the related object is not specified.

        Args:
            key (str): Name of an object key of Page Objects
        """
        self._check_object(key)

    def _verify_data(self, key="data"):
        """Method checks configuration for data add the default value if the related object is not specified.

        Args:
            key (str): Name of an object key of data.
        """
        self._check_object(key)

    def _verify_tags(self, key="tags"):
        """Method checks configuration for tags add the default value if the related object is not specified.

        Args:
            key (str): Name of an object key of tags.
        """
        self._check_object(key)

    def _verify_report(self, key="report"):
        """Method checks configuration for Test report add the default value if the related object is not specified.

        Args:
            key (str): Name of an object key of Test report.
        """
        self._check_object(key)
        self._verify_output_folder()

    def _verify_output_folder(self, key="params"):
        """Method checks configuration for parameters of file with Test report add the default value if the related object is not specified.

        Args:
            key (str): Name of an object key of parameters for file with Test report.
        """
        report = self.parser.get_report_config()
        if key in report:
            if 'output' in report[key]:
                updated_path = self.parser.get_path(report[key]['output'])
                report[key]['output'] = updated_path
                report.update({'output':  updated_path})
                return
        report.update({'output': runner.DEFAULT_OUTPUT})

    def _check_object(self, key):
        """General method for verifying existence of object key in dictionary and returning an object from the default
        configuration if the key which is being checked is missing.
        This method is used by other methods for verification of specific keys.

        Args:
            key (str): Name of an object key.
        """
        if key not in self.config:
            self.config.update({key: DEFAULT_CONFIG[key]})

