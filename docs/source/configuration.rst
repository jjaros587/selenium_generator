#############
Configuration
#############

Global configuration holds everything what is needed for running the tests. Bellow are given its objects.

.. code-block:: yaml

    scenarios: ""
    pages: ""
    data: ""
    report:
    tags: []
    drivers:

****************
Setting of paths
****************
There are three objects for specification of paths to directories.
All of them accept string values of relative paths to directories with ``__main__`` as starting point.

**Scenarios** defines path to the folder with test scenarios. This value is mandatory.
Scenarios inside the folder can be divided into more complex directory structure of multiple levels.
Framework loads scenarios from all folders recursively.

**Pages** defines path to the folder with  created Page Objects. This value is mandatory.
Scenarios inside the folder can be divided into more complex directory structure of multiple levels in case of proper
configuration of imports in ``__init__`` files. In the other words, it must be possible to load all classes from root folder.

**Data** defines path to test data which are loaded from test scenario during the execution. This field is not mandatory,
unless you are using data from external files for scenarios. Otherwise ``UnspecifiedDataFolder`` exception would be raised and the test would fail.

*************************
Test report configuration
*************************
Report object is used for overriding of a default configuration for a test report.
All if its child objects are not mandatory, only these you want to override may be specified.

**Screenshots** object defines if you want to take screenshots on failure and to attache them in the test report. By default is set on ``true``.

**Clean** object defines if you want to clear the folder where report and screenshots are being saved before the next text execution. By default is set on ``true``.

**Params** object is used for a specification of parameters of the report itself.

- **output** defines the directory for generating of the report and saving of the screenshots. By default it's ``/report`` in the root directory of the project
- **combine_reports** defines whether test classes should be combined into one report or divided into several reports. By default is set on ``true``
- **report_name** defines custom report name (name of the generated file). By default it is ``"TestReport"``
- **report_title** defines custom report title (heading of the generated report). By default it is ``"Test results"``
- **template** is used for using custom template instead of the default one. The value is path to the custom template

.. code-block:: yaml

    report:
        screenshots: [true/false]
        clean: [true/false]
        params:
            output: "[folder for storing test report]"
            combine_reports: [true/false]
            report_name: "[test report file name]"
            report_title: "[test report title]"
            template: "[path to template]"

************************
Test suite specification
************************
The only possible option for creating test suites is by marking test scenario with a tag in scenario metadata and specifying tags we want to run in the global configuration.

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

.. note::
    As you can see, there is an option to specify string with character ``*``. It simply means a scenario would be run all the times, no matter what tag was specified in global configuration.

*********************
Drivers configuration
*********************

.. code-block:: yaml

    drivers:
        chrome:
            version: "80.0.3987.106"

        firefox:
            options:
                - "--width=150"
                - "--height=100"

Local WebDriver
===============


Remote WebDriver
================
