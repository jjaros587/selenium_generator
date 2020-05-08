import os
from cerberus import Validator
from selenium_generator.base.exceptions import InvalidConfiguration
from selenium_generator.base.utils import singleton, load_json

DEFAULT_CONFIG_SCHEMA = os.path.join(os.path.dirname(__file__), "schemas", "config_schema.json")
DEFAULT_DRIVER_SCHEMA = os.path.join(os.path.dirname(__file__), "schemas", "driver_schema.json")
DEFAULT_SCENARIO_SCHEMA = os.path.join(os.path.dirname(__file__), "schemas", "scenario_schema.json")


class ExtendedValidator(Validator):

    def validate_presence_if_value(self, document, field, value, required_field):
        if document[field] is value and required_field not in document:
            self._error(required_field, "Required when field [%s] is [%s]" % (field, str(value)))
            return False
        return True


@singleton
class SchemaValidator:

    def __init__(self, config_schema=DEFAULT_CONFIG_SCHEMA, scenario_schema=DEFAULT_SCENARIO_SCHEMA,
                 driver_schema=DEFAULT_DRIVER_SCHEMA):
        self.v = ExtendedValidator()
        self.config_schema = self._load_file(config_schema)
        self.scenario_schema = self._load_file(scenario_schema)
        self.local_driver_schema = self._load_file(driver_schema)

    def validate(self, document, schema):
        return self.v.validate(document, schema)

    def validate_config(self, document):
        if self.validate(document, self.config_schema):
            for item in document['drivers'].values():
                if not self.validate(item, self.local_driver_schema):
                    raise InvalidConfiguration(self.v.errors)
                if not self.v.validate_presence_if_value(item, "remote", True, "desired_caps"):
                    raise InvalidConfiguration(self.v.errors)
            return True
        else:
            raise InvalidConfiguration(self.v.errors)

    def validate_scenario(self, document):
        return self.validate(document,  self.scenario_schema)

    def get_errors(self):
        return self.v.errors

    @staticmethod
    def _load_file(file):
        if not isinstance(file, dict):
            return load_json(file)
