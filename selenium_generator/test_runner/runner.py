"""
    Module contains classes needed for running the tests and storing the result in the test report.
"""

from HtmlTestRunner.runner import HTMLTestRunner, HtmlTestResult
from HtmlTestRunner.result import _TestInfo
from unittest.result import failfast
import os

DEFAULT_TEMPLATE = os.path.join(os.path.dirname(__file__), "template", "report_template.html")
"""Path to a default template for test report"""
DEFAULT_OUTPUT = "./reports/"
"""Default directory where test report should be generated."""


class TestInfo(_TestInfo):
    """Class which stores information about executed test.

    Args:
        test_result (Result): Test result class
        test_method (type): Executed test method
        outcome (int): Index which takes test correct value for test result type from _TestInfo class
        err (tuple): Holds detailed information about occurred error
        sub_test:
        screen_shot (str): Path to screen shot of a failed test

    Attributes:
        screen_shot (str): Path to screen shot of a failed test
    """
    def __init__(self, test_result, test_method, outcome=_TestInfo.SUCCESS, err=None, sub_test=None, screen_shot=None):
        _TestInfo.__init__(self, test_result, test_method, outcome=outcome, err=err, subTest=sub_test)
        self.screen_shot = screen_shot


class Result(HtmlTestResult):
    """Class which is used for generating of test result.

    Args:
        stream (:class:`unittest.runner._WritelnDecorator`):
        descriptions (bool):
        verbosity (int): Arg specify how detailed information we want to write in the console

    Attributes:
        infoclass (TestInfo): Class for storing information about test execution
    """
    def __init__(self, stream, descriptions, verbosity):
        HtmlTestResult.__init__(self, stream, descriptions, verbosity)
        self.infoclass = TestInfo

    @failfast
    def addFailure(self, test, err):
        """Method which create information about failed tests on fail.

        Args:
            test_method (type): Executed test method
            err (tuple): Holds detailed information about occurred error
        """
        self._save_output_data()
        test_info = self._create_test_info(test, err)
        self._prepare_callback(test_info, self.failures, "FAIL", "F")

    @failfast
    def addError(self, test, err):
        """Method which create information about failed tests on error.

        Args:
            test_method (type): Executed test method
            err (tuple): Holds detailed information about occurred error
        """
        self._save_output_data()
        test_info = self._create_test_info(test, err)
        self._prepare_callback(test_info, self.errors, 'ERROR', 'E')

    def _create_test_info(self, test, err):
        """Base method for creating of instance of _TestInfo class based on given parameters.

        Args:
            test_method (type): Executed test method
            err (tuple): Holds detailed information about occurred error

        Returns:
            TestInfo: Instance of a _TestInfo class which holds information about execution of a test
        """
        screen_shot = test.screen_shot_path if hasattr(test, 'screen_shot_path') else None
        return self.infoclass(self, test, outcome=self.infoclass.FAILURE, err=err, screen_shot=screen_shot)


class Runner(HTMLTestRunner):
    """Class for running test scenarios.

    Args:
        driver_name (str): Name of a driver
        output (str): Path to folder for storing test report
        report_title (str): Title of a generated test report
        report_name (str): Name of a html file with test report
        template (str): Path to file with test report template
        resultclass (Result): Test result class

    Attributes:
        driver_name (str): Name of a driver
        output (str): Path to folder for storing test report
        report_title (str): Title of a generated test report
        report_name (str): Name of a html file with test report
        template (str): Path to file with test report template
        resultclass (Result): Test result class
    """

    def __init__(self, driver_name="", output=DEFAULT_OUTPUT, report_title="Test results", report_name="TestReport",
                 template=DEFAULT_TEMPLATE, resultclass=Result):

        print("\n Running driver %s..." % driver_name)

        report_name = report_name + "_" + driver_name + "_"

        HTMLTestRunner.__init__(self, output=output, report_title=report_title, report_name=report_name,
                                template=template, resultclass=resultclass, combine_reports=True)
