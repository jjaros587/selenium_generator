.. selenium_generator documentation master file, created by
   sphinx-quickstart on Mon May 25 19:11:29 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

##############################
Welcome to selenium_generator!
##############################

``Selenium_generator`` is a framework for automated generating of automated functional tests of web applications
from test scenarios written in yaml format, based on Selenium WebDriver framework.

Framework provides easy way for writing scenarios in human readable format which is easier to maintain in comparison
with clear code. It also support many of the most used best practices and patterns.

Framework is designed to be easily extensible.

****************
Features
****************

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

*****************
Table of contents
*****************

.. toctree::
   :maxdepth: 3

   installation
   configuration
   starting
   scenario
   keywords
   page_factory
   exceptions
   api
   license
   TODO <todo>

****************
Copyright Notice
****************

Cerberus is an open source project by Jakub Jaros. See the original `LICENSE
<https://github.com/jjaros587/selenium_generator/blob/master/LICENSE>`_ for more
information.
