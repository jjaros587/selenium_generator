from selenium import webdriver
from selenium_generator.factories.drivers.base_driver import BaseDriver


class RemoteDriver(BaseDriver):

    REMOTE = False
    """Class attribute signifies that class is for remote driver"""

    def __init__(self, driver_name, params):
        super().__init__(driver_name, params)

    def run(self):
        """Method runs instance of Remote WebDriver.

        Returns:
            Instance of Remote driver."""
        return webdriver.Remote(
            command_executor=self.url,
            desired_capabilities=self.desired_caps,
            options=self.options)
