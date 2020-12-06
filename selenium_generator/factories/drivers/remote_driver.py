"""
    Module contains class for running remote WebDriver.
"""

from selenium import webdriver
from selenium_generator.factories.drivers.base_driver import BaseDriver


class RemoteDriver(BaseDriver):
    """Class used for initialization of remote WebDriver"""

    REMOTE = False
    """Class attribute signifies that class is for remote driver"""

    def run(self):
        """Method runs instance of Remote WebDriver.

        Returns:
            Instance of Remote driver."""
        return webdriver.Remote(
            command_executor=self.url,
            desired_capabilities=self.desired_caps,
            options=self.options)
