import os
from cerberus import Validator

from src.base.Exceptions import InvalidConfiguration
from src.base.utils import singleton, load_json

DEFAULT_CONFIG_SCHEMA = os.path.join(os.path.dirname(__file__), "schemas", "globalConfigSchema.json")
DEFAULT_SCENARIO_SCHEMA = os.path.join(os.path.dirname(__file__), "schemas", "scenarioSchema.json")


@singleton
class SchemaValidator:

    def __init__(self, config_schema=DEFAULT_CONFIG_SCHEMA, scenario_schema=DEFAULT_SCENARIO_SCHEMA):
        self.v = Validator()
        self.config_schema = self._load_file(config_schema)
        self.scenario_schema = self._load_file(scenario_schema)

    def validate(self, document, schema):
        return self.v.validate(document, schema)

    def validate_config(self, document):
        if self.validate(document, self.config_schema):
            return True
        else:
            raise InvalidConfiguration(self.v.errors)

    def validate_scenario(self, document):
        return self.validate(document,  self.scenario_schema)

    @staticmethod
    def _load_file(file):
        if not isinstance(file, dict):
            return load_json(file)

