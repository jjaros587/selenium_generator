##############################
Welcome to selenium_generator!
##############################

``Selenium_generator`` is a framework for automated generating of automated functional tests of web applications
from test scenarios written in yaml format, based on Selenium WebDriver framework.

Framework provides easy way for writing scenarios in human readable format which is easier to maintain in comparison
with clear code. It also support many of the most used best practices and patterns.

Framework is designed to be easily extensible.

`Link to an oficial documentation <https://selenium-generator.readthedocs.io/>`_.

`Link to a sample project <https://github.com/jjaros587/selenium_generator_sample_project>`_.

***********
Instalation
***********
You can easily install the latest version with

.. code-block:: console

    pip install selenium_generator

********
Features
********

- Automated generation of Tests based on Scenarios in yaml format
- Configuration of everything needed in one file
- Validation of a configuration and test scenarios against schema
- Data Driven Testing (DDT)
- Page Factory design pattern
- Specification of Test suites using tags
- WebDriver manager - with support of either local or remote WebDrivers
- Genarating of a configurable test report
- Taking screenshots on failure
- Including screenshots in a test report

******************
Easy configuration
******************
Configure everything what is needed for test execution from one place.

.. code-block:: yaml

    scenarios: "scenarios"
    data: "data"
    pages: "pages"

    report:
      screenshots: true
      clean: true
      params:
        output: "reports"
        report_name: "TestReport"
        report_title: "My Report"

    tags: ["acceptance", "regression"]

    drivers:
      chrome:
        remote: false

      firefox:
        remote: false

******************************
Simple test scenario structure
******************************

Write a test scenario easily in yaml format with using of predefined keywords which can be extended.

.. code-block:: yaml

    name: "search_positive_inline_data"
    data:
      - search_text: "text1"
      - search_text: "text2"
    tags: []
    drivers: ["chrome"]
    steps:
      - run_driver:
      - maximize:
      - page_object:
          class: "GoogleSearchPage"
          method: "search_positive"
      - close_driver:



****************
Copyright Notice
****************

Cerberus is an open source project by Jakub Jaros. See the original `LICENSE
<https://github.com/jjaros587/selenium_generator/blob/master/LICENSE>`_ for more
information.
