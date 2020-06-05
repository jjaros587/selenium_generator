from selenium import webdriver
from selenium_generator.factories.drivers.base_driver import BaseDriver

DEFAULT_EXECUTOR = 'http://127.0.0.1:4444/wd/hub'


class RemoteDriver(BaseDriver):

    REMOTE = False

    def __init__(self, browser, params):
        super().__init__(browser, params)

    def run(self):
        return webdriver.Remote(
            command_executor=self.url,
            desired_capabilities=self.desired_caps,
            options=self.options)
