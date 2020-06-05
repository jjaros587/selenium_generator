##############################
Welcome to selenium_generator!
##############################

``Selenium_generator`` is a framework for automated generating of automated functional tests of web applications
from test scenarios written in yaml format, based on Selenium WebDriver framework.

Framework provides easy way for writing scenarios in human readable format which is easier to maintain in comparison
with clear code. It also support many of the most used best practices and patterns.

Framework is designed to be easily extensible.

`Link to oficial documentation
<https://selenium-generator.readthedocs.io/en/latest/index.html>`_.

********
Features
********

- Automated generation of Tests based on Scenarios in yaml format
- Data Driven Testing (DDT)
- Page Factory design pattern
- Specification of Test suites
- WebDriver manager
- Test report generating
- Taking screenshots on failure
- Including screenshots in test report

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
        combine_reports: true
        report_name: "TestReport"
        report_title: "My Report"

    tags: ["acceptance", "regression"]

    drivers:
      chrome:
        remote: false

      firefox:
        remote: false


****************
Copyright Notice
****************

Cerberus is an open source project by Jakub Jaros. See the original `LICENSE
<https://github.com/jjaros587/selenium_generator/blob/master/LICENSE>`_ for more
information.
