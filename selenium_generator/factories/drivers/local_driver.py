from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver

from selenium_generator.factories.drivers.base_driver import BaseDriver


class LocalDriver(BaseDriver):

    REMOTE = False

    def __init__(self, browser, params):
        super().__init__(browser, params)

    def run(self):
        return getattr(self, "_run_" + self.browser)()

    def _run_chrome(self):
        chrome_options = self._add_option(ChromeOptions())
        return webdriver.Chrome(
            chrome_options=chrome_options,
            desired_capabilities=self.desired_caps,
            executable_path=ChromeDriverManager(version=self.version).install())

    def _run_firefox(self):
        firefox_options = self._add_option(FirefoxOptions())
        return webdriver.Firefox(
            options=firefox_options,
            desired_capabilities=self.desired_caps,
            executable_path=GeckoDriverManager(version=self.version).install())

    def _add_option(self, options):
        for item in self.options:
            options.add_argument(item)
        return options
