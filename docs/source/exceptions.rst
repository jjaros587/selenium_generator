##########
Exceptions
##########
There are four exceptions which may be thrown in a case of specific errors.

----

- ``InvalidConfiguration(Exception)``

Exception is thrown when the requirements for a structure of a configuration are not met.
When it's thrown scenarios aren't run and test execution ends.

Bellow are given links for validations schemas.
Schemas had to be divided in two schemas to allow unknown values for driver names.

`Link to alidation schema for configuration <https://github.com/jjaros587/selenium_generator/blob/master/selenium_generator/validators/schemas/config_schema.json>`_.

`Link to validation schema for drivers <https://github.com/jjaros587/selenium_generator/blob/master/selenium_generator/validators/schemas/driver_schema.json>`_.

----

- ``InvalidScenario(Exception)``

Exception is thrown when the requirements for a structure of a scenario are not met.
When it's thrown scenario is skipped and proper messages is added to a test report.
Exception is connected only with specific scenario. It doesn't affect other scenarios.

`Link to validation schema for scenario <https://github.com/jjaros587/selenium_generator/blob/master/selenium_generator/validators/schemas/scenario_schema.json>`_.

----

- ``UnsupportedDriver(ValueError)``

Exception is thrown when a test scenario tries to use driver which is not supported.
This exception is connected with local drivers.
By default the framework supports local drivers for ``chrome`` and ``firefox``.
If any other driver is specified in scenario, exception is thrown.
In the need of using any other driver, ``DriverManager`` has to be extended with the requested driver.

If this error occurs, test scenario is skipped and proper error message is added to test report.

----

- ``MissingDriverConfiguration(Exception)``

Exception is thrown when a test scenario tries to use driver which is supported but its configuration is missing.
