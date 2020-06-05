from selenium_generator.base.exceptions import MissingDriverConfiguration, UnsupportedDriver
from selenium_generator.base.utils import singleton
from selenium_generator.factories.drivers.local_driver import LocalDriver
from selenium_generator.factories.drivers.remote_driver import RemoteDriver
from selenium_generator.parsers.config_parser import ConfigParser

DEFAULT_LOCAL_BROWSERS = ["chrome", "firefox", "ie"]
DEFAULT_DRIVER_TYPES = [LocalDriver, RemoteDriver]


@singleton
class DriverFactory:

    def __init__(self,
                 driver_types=DEFAULT_DRIVER_TYPES,
                 allowed_local_browsers=DEFAULT_LOCAL_BROWSERS):

        self.driver_types = driver_types
        self.drivers = ConfigParser().get_drivers_config()
        self.allowed_browsers = allowed_local_browsers

    def run(self, browser):
        self._verify_browser(browser)
        for driver in self.driver_types:
            if driver.check_type(self.drivers[browser]['remote']):
                return driver(browser, self.drivers[browser]).run()

    def _verify_browser(self, browser):
        if browser not in self.allowed_browsers:
            raise UnsupportedDriver(self.allowed_browsers)

        if browser not in self.drivers:
            raise MissingDriverConfiguration(browser)
