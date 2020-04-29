from src.base.utils import load_yaml, singleton
from src.testRunner import Runner
from src.validators.Validator import SchemaValidator


@singleton
class ConfigParser:

    config = None

    @classmethod
    def load_config(cls, config_path):
        cls.config = load_yaml(config_path)
        SchemaValidator().validate_config(cls.config)
        ConfigUpdater(cls).update_config()

    def get_pages_path(self):
        return self.config['pages']

    def get_scenarios_path(self):
        return self.config['scenarios']

    def get_report_config(self):
        return self.config['report']

    def get_report_params(self):
        if 'params' in self.config['report']:
            return self.config['report']['params']
        else:
            return {}

    def get_driver_config(self):
        return self.config['driver']

    def get_data_path(self, data_path):
        return self.config['data'] + data_path

    def get_tags(self):
        return self.config['tags']


@singleton
class ConfigUpdater:

    def __init__(self, parser):
        self.parser = parser
        self.config = parser.config

    def update_config(self):
        self._verify_tags()
        self._verify_report()

    def _verify_tags(self):
        if 'tags' not in self.config or self.config['tags'] is None:
            self.config.update({'tags': []})

    def _verify_report(self):
        if 'report' not in self.config:
            self.config.update({'report': None})
        report = self.parser().get_report_config()
        if 'screenshots' not in report:
            report.update({'screenshots': False})
        if 'clean' not in report:
            report.update({'clean': True})
        self._verify_output_folder()

    def _verify_output_folder(self):
        report = self.parser().get_report_config()
        if 'params' in report:
            if 'output' in report['params']:
                report.update({'output':  report['params']['output']})
                return
        report.update({'output': Runner.DEFAULT_OUTPUT})

