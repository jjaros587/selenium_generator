#############
Configuration
#############

Configuration holds everything what is needed for test execution. Bellow are given its first level objects.

.. code-block:: yaml

    scenarios: ""
    pages: ""
    data: ""
    report:
    tags: []
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
**TODO - guide for configuration extension.**

****************
Setting of paths
****************

There are three objects for a specification of paths to directories.
All of them accept string values of relative paths to directories with ``__main__`` as a starting point.

- ``scenarios (string)``
    - defines path to a folder with test scenarios. Scenarios inside the folder can be divided into more complex directory structure of multiple levels. Framework loads scenarios from all folders recursively.

- ``pages (string)``
    - defines path to a folder with created Page Objects. Scenarios inside the folder can be divided into more complex directory structure of multiple levels in a case of a proper configuration of imports in ``__init__`` files. In the other words, it must be possible to load all classes from root folder.

- ``data (string)``
    - defines path to external test data which are loaded from test scenario during the execution. This directory is used only if external files are used for ``DDT``.

*************************
Test report configuration
*************************
``report`` object is used for overriding of the default configuration for a test report.
All if its child objects are not mandatory, only these you want to override has to be specified.

Object consists of several objects which are listed below:

- ``screenshots (boolean)``
    - defines if you want to take screenshots on failure and to attach them in the test report

- ``clean (boolean)``
    - defines if you want to clear the folder where the report and screenshots are being saved before a next text execution

- ``params (dict)``
    - is used for a specification of parameters of the report itself
    - **child objects**:
        - ``output (string)`` defines a directory for generating of the report and saving of the screenshots
        - ``combine_reports (boolean)`` defines whether test classes should be combined into one report or divided into several reports
        - ``report_name (string)`` defines a custom report name (name of the generated file)
        - ``report_title (string)`` defines a custom report title (heading of the generated report)
        - ``template (string)`` defines a path to a custom template instead of the default one.
            - The default template can be seen `here <https://github.com/jjaros587/selenium_generator/blob/dev/selenium_generator/test_runner/template/report_template.html>`_.
            - **TODO - add link to sample report.**

************************
Test suite specification
************************
The only possible option for creating test suites is by marking test scenario with a tag in scenario metadata and specifying tags we want to run in the global configuration.

For more information about adding test to test suite visit this `*page* <scenario.html#adding-test-to-suite>`_.

Tags can be specified as a list of ``String`` values in object ``tags:``, both in scenario and in global configuration.

.. code-block:: yaml

    tags: ["regression", "acceptance"]


The object `tags:` is not mandatory. The effect would be the same as with an empty array ``[]``. The array cannot contain empty ``String``.
This behaviour is applied to both scenario and configuration.

If no tag in configuration is specified, all scenarios will be run.
If array contains at least one tag, the behaviour is as following:

#. List of tags in scenario contains at least one of the tags from global configuration -> test will be run
#. List of tags in scenario doesn't contain any of the tags from global configuration
    #. List of tags in scenario contains String ``*`` -> test will be run
    #. List of tags in scenario doesn't contain String ``*`` -> test won't be run

*********************
Drivers configuration
*********************
``drivers`` object stores information about all drivers which are used for test execution. It can consists of several
objects. Each of the objects represents one driver whose key is a name of the driver. Each driver can have several more
objects which holds its configuration.

.. code-block:: yaml

    drivers:
        chrome:
            remote: true
            version: ""
            options: []
            desired_caps:


The framework allows you to use either local or remote drivers.

- ``remote (boolean)``
    - defines if we want to download and use local driver or to use remote driver
    - only this field is mandatory
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
- ``version (string)`` defines a version of a local driver. If the object isn't specified, the latest version is downloaded.

At this time, the framework provides local drivers only for browsers ``chrome`` adn ``firefox``.

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
- ``url (string)`` defines an URL to a remote driver. If the object isn't specified, the default value ``http://127.0.0.1:4444/wd/hub``  is used.

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

