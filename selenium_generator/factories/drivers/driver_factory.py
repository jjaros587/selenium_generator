from selenium_generator.base.exceptions import MissingDriverConfiguration, UnsupportedDriver
from selenium_generator.base.utils import singleton
from selenium_generator.factories.drivers.local_driver import LocalDriver
from selenium_generator.factories.drivers.remote_driver import RemoteDriver
from selenium_generator.parsers.config_parser import ConfigParser

DEFAULT_BROWSERS = ["chrome", "firefox"]


@singleton
class DriverFactory:

    def __init__(self, allowed_browsers=DEFAULT_BROWSERS):
        self.drivers = ConfigParser().get_drivers_config()
        self.allowed_browsers = allowed_browsers

    def run(self, browser):
        self._verify_browsers(browser)

        params = self.drivers[browser]
        if params['remote']:
            driver = RemoteDriver(params).run()
        else:
            driver = LocalDriver(browser, params).run()
        return driver

    def _verify_browsers(self, browser):
        if browser not in self.allowed_browsers:
            raise UnsupportedDriver(self.allowed_browsers)

        if browser not in self.drivers:
            raise MissingDriverConfiguration(browser)
