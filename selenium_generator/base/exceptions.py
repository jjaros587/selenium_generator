class InvalidConfiguration(Exception):
    def __init__(self, errors):
        super().__init__("Failed due to invalid configuration: %s" % errors)


class InvalidScenario(Exception):
    def __init__(self, error):
        super().__init__("Invalid scenario structure: %s" % error)


class MissingDriverConfiguration(Exception):
    def __init__(self, driver):
        super().__init__("Missing configuration for driver [%s]" % driver)


class UnsupportedDriver(ValueError):
    def __init__(self, allowed_browsers):
        super().__init__("Unsupported driver. Allowed drivers are: %s" % allowed_browsers)
