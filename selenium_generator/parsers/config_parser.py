import os
import sys
from selenium_generator.base.exceptions import UnspecifiedDataFolder
from selenium_generator.base.file_manager import FileManager
from selenium_generator.base.utils import load_yaml, singleton
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
        'remote': False,
        'version': "80.0.3987.106"
      },
      'firefox': {
        'remote': False
      }
    }
}
@singleton
class ConfigParser:

    def __init__(self, config_path='config.yaml'):
        arg_config = ArgParser.parse_args()
        if arg_config is not None:
            self.config = load_yaml(arg_config)
        elif FileManager.file_exists(config_path):
            self.config = load_yaml(config_path)
        else:
            self.config = DEFAULT_CONFIG

        SchemaValidator().validate_config(self.config)
        ConfigUpdater(self).update_config()

    def get_pages_path(self):
        return self.get_path(self.config['pages'])

    def get_scenarios_path(self):
        return self.get_path(self.config['scenarios'])

    def get_report_config(self):
        return self.config['report']

    def get_report_params(self):
        return self.config['report']['params'] if 'params' in self.config['report'] else {}

    def get_drivers_config(self):
        return self.config['drivers']

    def get_data_path(self, data_path):
        if 'data' not in self.config:
            raise UnspecifiedDataFolder()
        return os.path.join(self.get_path(self.config['data']), data_path)

    def get_tags(self):
        return self.config['tags']

    @staticmethod
    def get_path(folder):
        return os.path.join(os.path.dirname(sys.modules['__main__'].__file__), folder)


@singleton
class ConfigUpdater:

    def __init__(self, parser):
        self.parser = parser
        self.config = parser.config

    def update_config(self):
        self._verify_tags()
        self._verify_report()

    def _verify_tags(self):
        if 'tags' not in self.config:
            self.config.update({'tags': DEFAULT_CONFIG['tags']})

    def _verify_report(self):
        if 'report' not in self.config:
            self.config.update({'report': DEFAULT_CONFIG['report']})
        self._verify_output_folder()

    def _verify_output_folder(self):
        report = self.parser.get_report_config()
        if 'params' in report:
            if 'output' in report['params']:
                updated_path = self.parser.get_path(report['params']['output'])
                report['params']['output'] = updated_path
                report.update({'output':  updated_path})
                return
        report.update({'output': runner.DEFAULT_OUTPUT})

