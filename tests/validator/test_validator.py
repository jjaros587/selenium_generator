import os
import unittest
from ddt import ddt, data, unpack
from selenium_generator.validators.validator import SchemaValidator, ExtendedValidator
import yaml
from selenium_generator.base.exceptions import InvalidConfiguration


@ddt
class ValidatorTest(unittest.TestCase):

    path = os.path.join(os.path.dirname(__file__), "test_data")

    @data(({"aaa": "bbb"}, True), ({"aaa": 1}, False))
    @unpack
    def test_validate(self, document, result):
        self.assertEqual(SchemaValidator().validate(document, {"aaa": {"type": "string"}}), result)

    @data(("scenario_valid.yaml", True), ("scenario_invalid.yaml", False))
    @unpack
    def test_validate_scenario(self, filename, result):
        file = load_file(os.path.join(self.path, filename))
        self.assertTrue(SchemaValidator().validate_scenario(file) == result)

    def test_validate_valid_config(self):
        file = load_file(os.path.join(self.path, "config_valid.yaml"))
        self.assertTrue(SchemaValidator().validate_config(file) is True)

    def test_validate_invalid_config(self):
        self.assertRaises(InvalidConfiguration, SchemaValidator().validate_config, {"aaa": "bbb"})

    @data(({"a": True, "b": None}, True), ({"a": True}, False))
    @unpack
    def test_validate_presence_if_value(self, document, result):
        self.assertEqual(ExtendedValidator().validate_presence_if_value(document, "a", True, "b"), result)

    def test_get_errors(self):
        SchemaValidator().validate({"aaa": 1}, {"aaa": {"type": "string"}})
        self.assertTrue(SchemaValidator().get_errors()['aaa'] is not None)

    @data(os.path.join(path, "test_load.json"), os.path.join(path, "test_load.yaml"), {"aaa": "bbb"})
    def test_load_file_valid(self, test_data):
        file = SchemaValidator()._load_file(test_data)
        self.assertEqual(file['aaa'], "bbb")

    def test_load_file_invalid(self):
        self.assertRaises(ValueError, SchemaValidator()._load_file, os.path.join(self.path, "test_load.txt"))


def load_file(filename):
    with open(filename) as f:
        return yaml.load(f, Loader=yaml.FullLoader)
