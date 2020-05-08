from selenium import webdriver

DEFAULT_EXECUTOR = 'http://127.0.0.1:4444/wd/hub'


class RemoteDriver:

    def __init__(self, params):
        self.url = params['url'] if 'url' in params else DEFAULT_EXECUTOR
        self.desired_caps = params['desired_caps']
        self.options = params['options'] if 'options' in params else []

    def run(self):
        return webdriver.Remote(
            command_executor=self.url,
            desired_capabilities=self.desired_caps,
            options=self.options)
