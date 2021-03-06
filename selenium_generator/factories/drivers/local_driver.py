"""
    Module contains class for running local WebDriver.
"""

from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from selenium_generator.factories.drivers.base_driver import BaseDriver


class LocalDriver(BaseDriver):
    """Class used for initialization of local WebDriver"""

    REMOTE = False
    """Class attribute signifies that class is for local driver"""

    def run(self):
        """Method calls individual method for running specific driver based on driver name.

        Returns:
            Instance of required driver."""
        return getattr(self, "_run_" + self.driver_name)()

    def _run_chrome(self):
        """Method runs instance of driver for Chrome.

        Returns:
            Instance of driver for Chrome.
        """
        chrome_options = self._add_option(ChromeOptions())
        return webdriver.Chrome(
            chrome_options=chrome_options,
            desired_capabilities=self.desired_caps,
            executable_path=ChromeDriverManager(version=self.version).install())

    def _run_firefox(self):
        """Method runs instance of driver for Firefox.

        Returns:
            Instance of driver for Firefox."""
        self.desired_caps["marionette"] = True
        firefox_options = self._add_option(FirefoxOptions())
        return webdriver.Firefox(
            options=firefox_options,
            desired_capabilities=self.desired_caps,
            executable_path=GeckoDriverManager(version=self.version).install())

    def _add_option(self, options):
        """Method adds items to instance of Options for the required driver from configuration.

        Args:
            options: Instance of Options class for required browser
        """
        for item in self.options:
            options.add_argument(item)
        return options
