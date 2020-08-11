#############
Configuration
#############

Configuration holds everything what is needed for test execution. Bellow are given its first level objects.

.. code-block:: yaml

    scenarios:
    pages:
    data:
    report:
    tags:
    drivers:


None of the objects is mandatory. If any of the objects is not specified a value from the default configuration would be used.
In other words, an object has to be specified if there is a need for overriding the default value.

.. toggle-header::
    :header: **Show the default config**

        .. literalinclude:: _static/default_config.yaml
            :language: yaml


.. note:: The default configuration use only local drivers of the latest versions.

Configuration is validated against schema using `Cerberus <https://docs.python-cerberus.org/en/stable/index.html>`_.
If the configuration doesn't meet the requirements, ``InvalidConfiguration`` exception is thrown.

Configuration can be extended with custom objects. Consequently, the validation schema would have to be extended as well.

****************
Setting of paths
****************

There are three objects for a specification of paths to directories.
All of them accept string values of relative paths to directories with ``__main__`` as a starting point.

- ``scenarios (str)``
    - defines path to a folder with test scenarios. Scenarios inside the folder can be divided into more complex directory structure of multiple levels. Framework loads scenarios from all folders recursively.

- ``pages (str)``
    - defines path to a folder with created Page Objects. Scenarios inside the folder can be divided into more complex directory structure of multiple levels in a case of a proper configuration of imports in ``__init__`` files. In the other words, it must be possible to load all classes from root folder.

- ``data (str)``
    - defines path to external test data which are loaded from test scenario during the execution. This directory is used only if external files are used for ``DDT``.

*************************
Test report configuration
*************************
``report`` object is used for overriding of the default configuration for a test report.
The report is based on the extension for unittest framework `html-testRunner <https://pypi.org/project/html-testRunner/>`_.
It supports functionality for generating test reports in html format based on given template.
Also screenshots taken when a executed test failed is included in test report.
All if its child objects are not mandatory, only these you want to override has to be specified.

The main object consists of several objects which are listed below:

- ``screenshots (bool)``
    - defines if you want to take screenshots on failure and to attach them in the test report

- ``clean (bool)``
    - defines if you want to clear the folder where the report and screenshots are being saved before a next text execution

- ``params (dict)``
    - is used for a specification of parameters of the report itself
    - **child objects**:
        - ``output (str)`` defines a directory for generating of the report and saving of the screenshots
        - ``report_name (str)`` defines a custom report name (name of the generated file)
        - ``report_title (str)`` defines a custom report title (heading of the generated report)
        - ``template (str)`` defines a path to a custom template instead of the default one.
            - The default template can be seen `here <https://github.com/jjaros587/selenium_generator/blob/dev/selenium_generator/test_runner/template/report_template.html>`_.

************************
Test suite specification
************************
The only possible way for creating test suites is by marking test scenario with a tag in scenario metadata and specifying tags we want to run in the global configuration.

For more information about adding test to test suite visit this `*page* <scenario.html#adding-test-to-suite>`_.

Tags can be specified as a list of ``String`` values in object ``tags:``, both in scenario and in configuration.

.. code-block:: yaml

    tags: ["regression", "acceptance"]


The object is not mandatory. An effect would be the same as with an empty array ``[]``. The array cannot contain empty ``String``.
This behaviour is applied to both scenario and configuration.

If no tag in configuration is specified, all scenarios will be run.
If array contains at least one tag, the behaviour is as following:

#. List of tags in scenario contains at least one of the tags from  configuration -> test will be run
#. List of tags in scenario doesn't contain any of the tags from global configuration
    #. List of tags in scenario contains String ``*`` -> test will be run
    #. List of tags in scenario doesn't contain String ``*`` -> test won't be run

For better understanding, below is given a table with logic of the loading.

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - Configuration
     - Scenario
     - Result

   * - []
     - no effect
     - All scenarios will be load

   * - [“tag1”, “tag2”]
     - []
     - Won't be load

   * - [“tag1”, “tag2”]
     - [“tag1”, “tag3”]
     - Will be load

   * - [“tag1”, “tag2”]
     - [“tag3”]
     - Won't be load

   * - no effect
     - [“*”]
     - Will be load always


*********************
Drivers configuration
*********************
``drivers`` object stores information about all drivers which are used for test execution. It can consists of several
objects. Each of the objects represents one driver whose key is a name of the driver. Each driver can have several more
objects which holds its configuration.

The object is also used for specification of drivers which we want to use for test execution.
If we, for some reasons, want to disable any of the drivers, there is no need to delete it from configuration.
There is inner object ``allowed`` for this purpose. More information can be found below.

.. code-block:: yaml

    drivers:
        chrome:
            remote:
            version:
            allowed:
            options:
            desired_caps:


The framework allows you to use either local or remote drivers.

- ``remote (bool)``
    - defines if we want to download and use local driver or to use remote driver
    - only this field is mandatory
- ``allowed (bool)``
    - defines whether a driver is allowed or not
    - if it's set on true driver isn't be included in the drivers which will be used for test execution
    - field is not mandatore and by default is set on ``True``
- ``options (list)``
    - defines a list of needed Options
- ``desired_caps (dict)``
    - defines objects with Desired Capabilities

There are two more objects which can be specified, ``version`` and ``url``.
These depends on a type of a driver and they are explained bellow.
Its specification with a wrong type of a driver doesn't throw any error. They are simply ignored.

Invalid driver configuration can throw several of exceptions. `*See the detailed information* <exceptions.html>`_

Local WebDriver
===============
- ``version (str)`` defines a version of a local driver. If the object isn't specified, the latest version is used.

At this time, the framework provides local drivers only for browsers ``chrome`` and ``firefox``.
In the need of using other WebDrivers,

.. code-block:: yaml

    drivers:
        chrome:
            remote: false
            version: "80.0.3987.106"

        firefox:
            remote: false
            options:
                - "--width=150"
                - "--height=100"


Remote WebDriver
================
- ``url (str)`` defines an URL to a remote driver. If the object isn't specified, the default value ``http://127.0.0.1:4444/wd/hub``  is used.

The usage of remote drivers for different browsers are limited only with your own configuration of a ``hub`` and ``nodes`` or with an external service which you are using.

.. code-block:: yaml

    drivers:
        chrome:
            remote: true
            options:
                - "--headless"
            desired_caps:
                os: "Windows"
                os_version: "10"
                browser: "Firefox"
                browser_version: "74"
                name: "First Test"

        firefox:
            remote: true
            url: "http://example.com:4444/wd/hub"
            options:
                - "--width=150"
                - "--height=100"

