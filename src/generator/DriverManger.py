from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager


class DriverManager:

    allowed_browsers = ["chrome", "firefox"]

    @classmethod
    def run_driver(cls, param):
        if param not in cls.allowed_browsers:
            raise ValueError("Byl zadán neplatný driver! Platné hodnoty jsou %s" % cls.allowed_browsers)
        driver = None
        if param == "chrome":
            driver = DriverManager._run_chrome()
        elif param == "firefox":
            driver = DriverManager._run_firefox()
        driver.maximize_window()
        return driver

    @staticmethod
    def _run_chrome():
        chrome_options = webdriver.chrome.options.Options()
        # if os.environ.get('headless') == "True":
        #     chrome_options.add_argument("--headless")
        #     chrome_options.add_argument("--window-size=1920x1080")
        return webdriver.Chrome(chrome_options=chrome_options, executable_path=ChromeDriverManager().install())

    @staticmethod
    def _run_firefox():
        firefox_options = webdriver.firefox.options.Options()
        # if os.environ.get('headless') == "True":
        #     firefox_options.headless = True
        return webdriver.Firefox(options=firefox_options, executable_path=GeckoDriverManager().install())
