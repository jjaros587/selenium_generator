from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import IEDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.ie.options import Options as IEOptions
from selenium import webdriver


class LocalDriver:

    def __init__(self, browser, params):
        self.browser = browser
        self.version = params['version'] if 'version' in params else None
        self.options = params['options'] if 'options' in params else []
        self.desired_caps = params['desired_cap'] if 'desired_cap' in params else {}

    def run(self):
        if self.browser == "chrome":
            return self._run_chrome()
        elif self.browser == "firefox":
            return self._run_firefox()
        elif self.browser == "ie":
            return self._run_ie()

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

    def _run_ie(self,):
        ie_options = self._add_option(IEOptions())
        return webdriver.Ie(
            options=ie_options,
            desired_capabilities=self.desired_caps,
            executable_path=IEDriverManager(version=self.version).install())

    def _add_option(self, options):
        for item in self.options:
            options.add_argument(item)
        return options