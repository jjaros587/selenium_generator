from selenium_generator.base.exceptions import MissingDriverConfiguration, UnsupportedDriver
from selenium_generator.base.utils import singleton
from selenium_generator.parsers.config_parser import ConfigParser

DEFAULT_BROWSERS = ["chrome", "firefox"]
DEFAULT_EXECUTOR = 'http://127.0.0.1:4444/wd/hub'


class BaseDriver:

    REMOTE = None

    def __init__(self, browser, params):
        self.browser = browser
        self.url = params['url'] if 'url' in params else DEFAULT_EXECUTOR
        self.version = params['version'] if 'version' in params else None
        self.options = params['options'] if 'options' in params else []
        self.desired_caps = params['desired_cap'] if 'desired_cap' in params else {}

    @classmethod
    def check_type(cls, driver_type):
        return driver_type == cls.REMOTE
