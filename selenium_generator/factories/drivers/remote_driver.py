from selenium import webdriver
from selenium_generator.factories.drivers.base_driver import BaseDriver

DEFAULT_EXECUTOR = 'http://127.0.0.1:4444/wd/hub'


class RemoteDriver(BaseDriver):
    __doc__ = BaseDriver.__doc__

    REMOTE = False

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
