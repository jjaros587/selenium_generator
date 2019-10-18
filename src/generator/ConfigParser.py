import os
import sys
from src.generator.utils import load_yaml


class ConfigParser:
    ROOT_DIR = os.path.dirname(sys.modules['__main__'].__file__)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
            cls.config = cls._get_config()
        return cls.instance

    def get_pages_path(self):
        return self.config['pages']

    def get_root_dir(self):
        return self.ROOT_DIR

    @classmethod
    def _get_config(cls):
        return load_yaml(cls.ROOT_DIR + "/./config.yaml")
