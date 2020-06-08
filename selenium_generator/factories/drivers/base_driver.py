DEFAULT_EXECUTOR = 'http://127.0.0.1:4444/wd/hub'
"""URL of a default executor for running tests on remote machine"""


class BaseDriver:
    """Class Base Driver.

    Args:
        driver_name (str): Driver name.
        params (dict): Parameters of a driver from configuration.

    Attributes:
        driver_name (str): Driver name.
        url (str): URL of a remote driver.
        version (str): Version of a local driver.
        options (list(str)): Driver Options from configuration.
        desired_caps (dict): Desired capabilities from configuration.
    """
    REMOTE = None
    """bool: Class attribute for determination of a type of a driver [True - remote, False - local]"""

    def __init__(self, driver_name, params):
        self.driver_name = driver_name
        self.url = params['url'] if 'url' in params else DEFAULT_EXECUTOR
        self.version = params['version'] if 'version' in params else None
        self.options = params['options'] if 'options' in params else []
        self.desired_caps = params['desired_cap'] if 'desired_cap' in params else {}

    @classmethod
    def check_type(cls, driver_type):
        """Method check if type of driver corresponds with a given type in args.

        Args:
            driver_type (str): Type of a driver to check.

        Returns:
            bool: True if corresponds, False otherwise.
        """
        return driver_type == cls.REMOTE
