from selenium_generator.base.exceptions import MissingDriverConfiguration, UnsupportedDriver
from selenium_generator.base.singleton import singleton
from selenium_generator.factories.drivers.local_driver import LocalDriver
from selenium_generator.factories.drivers.remote_driver import RemoteDriver
from selenium_generator.parsers.config_parser import ConfigParser

DEFAULT_LOCAL_DRIVERS = ["chrome", "firefox"]
"""List of names of allowed local drivers. In other words driver which are by default supported with 
:class:`selenium_generator.factories.drivers.local_driver.LocalDriver`"""

DEFAULT_DRIVER_CLASSES = [LocalDriver, RemoteDriver]
"""List of class which :class:`DriverFactory` uses for creating of required driver.

List of default classes:
    :class:`selenium_generator.factories.drivers.local_driver.LocalDriver`
    :class:`selenium_generator.factories.drivers.remote_driver.RemoteDriver`
"""


@singleton
class DriverFactory:
    """Class creates instance of Selenium WebDriver for specified driver.

    Args:
       driver_classes (list(BaseDriver)): List of classes for running individual types of drivers.
       allowed_local_drivers (str): List of names of allowed local drivers.

    Attributes:
       driver_classes (list(BaseDriver)): List of classes for running individual types of drivers.
       allowed_local_drivers (str): List of names of allowed local drivers.
       drivers (dict): Loaded drivers object from configuration.
    """
    def __init__(self,
                 driver_classes=DEFAULT_DRIVER_CLASSES,
                 allowed_local_drivers=DEFAULT_LOCAL_DRIVERS):

        self.driver_classes = driver_classes
        self.drivers = ConfigParser().get_drivers_config()
        self.allowed_local_drivers = allowed_local_drivers

    def run(self, driver_name):
        """Method create instance of required webdriver based on driver_name and its configuration.

        Args:
            driver_name (str): Name of a driver.

        Returns:
            Webdriver: Instance of a required webdriver.
        """
        self._verify_drivers(driver_name)
        for driver in self.driver_classes:
            if driver.check_type(self.drivers[driver_name]['remote']):
                return driver(driver_name, self.drivers[driver_name]).run()

    def _verify_drivers(self, driver_name):
        """Method verify if local driver is allowed in allowed_local_drivers and if any type of driver is configured in
            configuration.

        Args:
            driver_name (str): Name of a driver.

        Raises:
            UnsupportedDriver: If driver_name is not in allowed_local_drivers.
            MissingDriverConfiguration: If configuration of a driver is missing in configuration.
        """
        if driver_name not in self.allowed_local_drivers:
            raise UnsupportedDriver(self.allowed_local_drivers)

        if driver_name not in self.drivers:
            raise MissingDriverConfiguration(driver_name)
