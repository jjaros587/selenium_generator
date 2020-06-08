class InvalidConfiguration(Exception):
    """Exception is raised when configuration doesn't match its schema.

    Args:
        errors (:class:`cerberus.errors.ErrorList`): List of allowed drivers
    """

    def __init__(self, errors):
        super().__init__("Failed due to invalid configuration: %s" % errors)


class InvalidScenario(Exception):
    """Exception is raised when scenario doesn't match its schema.

    Args:
        errors (:class:`cerberus.errors.ErrorList`): List of allowed drivers
    """

    def __init__(self, errors):
        super().__init__("Invalid scenario structure: %s" % errors)


class MissingDriverConfiguration(Exception):
    """Exception is raised when in test scenario there is specified driver which is not configured in configuration.

    Args:
        driver (str): Name of a driver whose configuration is missing
    """

    def __init__(self, driver):
        super().__init__("Missing configuration for driver [%s]" % driver)


class UnsupportedDriver(ValueError):
    """Exception is raised when in configuration there is configured local driver which is not supported.

    Args:
        allowed_drivers (list(str)): List of allowed drivers
    """

    def __init__(self, allowed_drivers):
        super().__init__("Unsupported driver. Allowed drivers are: %s" % allowed_drivers)
