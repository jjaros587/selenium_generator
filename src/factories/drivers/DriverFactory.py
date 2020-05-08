from src.base.Exceptions import MissingConfiguration, UnallowedBrowser
from src.base.utils import singleton
from src.factories.drivers.LocalDriver import LocalDriver
from src.factories.drivers.RemoteDriver import RemoteDriver
from src.parsers.ConfigParser import ConfigParser

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
            raise UnallowedBrowser("Unallowed browser. Allowed browsers are: %s" % self.allowed_browsers)

        if browser not in self.drivers:
            raise MissingConfiguration("Missing configuration for driver [%s]" % browser)
