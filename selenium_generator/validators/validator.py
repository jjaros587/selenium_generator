"""
    Module contains classes and constants which are used for validation of dictionaries against schema.
"""

import os
from collections import namedtuple

from cerberus import Validator, errors
from cerberus.errors import ErrorDefinition, ValidationError
from selenium_generator.base.exceptions import InvalidConfiguration
from selenium_generator.base.file_manager import FileManager
from selenium_generator.base.singleton import singleton

DEFAULT_CONFIG_SCHEMA = os.path.join(os.path.dirname(__file__), "schemas", "config_schema.json")
"""Path to a file with a default schema for configuration`"""

DEFAULT_DRIVER_SCHEMA = os.path.join(os.path.dirname(__file__), "schemas", "driver_schema.json")
"""Path to a file with a default schema for configuration of drivers`"""

DEFAULT_SCENARIO_SCHEMA = os.path.join(os.path.dirname(__file__), "schemas", "scenario_schema.json")
"""Path to a file with a default schema for test scenario`"""


class ExtendedValidator(Validator):
    """Class extends Validator class from Cerberus framework :class:`cerberus.validator.Validator`"""

    def validate_presence_if_value(self, document, field, value, required_field):
        """Method checks presence of key based on another field and its value.

        Args:
            document (dict): Dictionary to check
            field (str): Dependent field for required field
            value: Value of a dependent field
            required_field (str): Field which should be present

        Returns:
            bool: True - valid (required field is in document), False - invalid (required field is not in document)
        """
        if document[field] is value and required_field not in document:
            return False
        return True


@singleton
class SchemaValidator:
    """Class validates Python dictionaries based on schema in json format.
    It is used for validation of the configuration and test scenarios structure.

    Args:
        validator (:class:`cerberus.validator.Validator`): Class used for validation.
        file_manager (FileManager): Class used for file management.
        config_schema (dict/str): Schema for configuration in dict format/Path to schema for configuration.
        scenario_schema (dict/str): Schema for test scenario in dict format/Path to schema for test scenario.
        driver_schema (dict/str): Schema for configuration of drivers in dict format/Path to schema for configuration of drivers.

    Attributes:
        validator (:class:`cerberus.validator.Validator`): Instance of class used for validation.
        file_manager (FileManager): Class used for file management.
        config_schema (dict): Loaded schema for configuration.
        scenario_schema (dict): Loaded schema for test scenario.
        driver_schema (dict): Loaded schema for configuration of drivers.
    """

    def __init__(self, config_schema=DEFAULT_CONFIG_SCHEMA, scenario_schema=DEFAULT_SCENARIO_SCHEMA,
                 driver_schema=DEFAULT_DRIVER_SCHEMA, validator=ExtendedValidator, file_manager=FileManager):
        self.validator = validator()
        self.file_manager = file_manager
        self.config_schema = self._load_file(config_schema)
        self.scenario_schema = self._load_file(scenario_schema)
        self.local_driver_schema = self._load_file(driver_schema)

    def validate(self, document, schema):
        """Base method for dict validation against schema.

        Args:
            document (dict): Document to validate loaded as dictionary
            schema (dict): Schema loaded as dictionary

        Returns:
            bool: True - valid, False - invalid
        """
        return self.validator.validate(document, schema)

    def validate_config(self, document):
        """Method for validation of configuration.

        Args:
            document (dict): Document to validate loaded as dictionary

        Returns:
            bool: True - Valid configuration

        Raises:
              InvalidConfiguration: If the configuration is invalid
        """
        if self.validate(document, self.config_schema):
            for item in document['drivers'].values():
                if not self.validate(item, self.local_driver_schema):
                    raise InvalidConfiguration(self.validator.errors)
                if not self.validator.validate_presence_if_value(item, "remote", True, "desired_caps"):
                    raise InvalidConfiguration("Field [%s] is required when field [%s] is [%s]" % ("desired_caps", "remote", True))
            return True
        else:
            raise InvalidConfiguration(self.validator.errors)

    def validate_scenario(self, document):
        """Method for validation of test scenario.

        Args:
            document (dict): Document to validate loaded as dictionary

        Returns:
            bool: True - valid, False - invalid
        """
        if not self.validate(document,  self.scenario_schema):
            return False
        return True

    def get_errors(self):
        """Method returns list of validation errors

        Returns:
            dict: All errors present in checked document against schema
        """
        return self.validator.errors

    def _load_file(self, schema):
        """Method checks if the given schema is file path or dict. If the schema is file path, it loads the the schema
        from file and return dict. If the schema is already in dict format, it is only returned.

        Args:
            schema (dict/str): Schema in dict format/Path to the schema

        Returns:
            dict: Loaded schema in dict format

        Raises:
            ValueError: Invalid extension for schema
        """
        if isinstance(schema, dict):
            return schema
        else:
            extensions = [".json", ".yaml"]
            for extension in extensions:
                if FileManager.check_extension(schema, extension):
                    extension = extension[1:]
                    if extension == "json":
                        return self.file_manager.load_json(schema)
                    if extension == "yaml":
                        return self.file_manager.load_yaml(schema)
            raise ValueError("Incorrect extension of a file with schema. It has to be %s" % extensions)
