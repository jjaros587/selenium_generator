"""
    This module implements classes needed for test execution.
"""

from HtmlTestRunner.runner import HTMLTestRunner, HtmlTestResult
from HtmlTestRunner.result import _TestInfo
from unittest.result import failfast
import os
from selenium_generator.base.file_manager import FileManager
from selenium_generator.parsers import config_parser

DEFAULT_TEMPLATE = os.path.join(os.path.dirname(__file__), "template", "report_template.html")
DEFAULT_OUTPUT = "./reports/"


class TestInfo(_TestInfo):
    """ TestInfo class.

    Args:
        test_result (Result): Test result class
        test_method:
        outcome:
        err:
        sub_test:
        screen_shot: Path to screen shot of a failed test
    """
    def __init__(self, test_result, test_method, outcome=_TestInfo.SUCCESS, err=None, sub_test=None, screen_shot=None):
        _TestInfo.__init__(self, test_result, test_method, outcome=outcome, err=err, subTest=sub_test)
        self.screen_shot = screen_shot


class Result(HtmlTestResult):
    """ Result class.

    Args:
        stream:
        descriptions:
        verbosity:
    """
    def __init__(self, stream, descriptions, verbosity):
        HtmlTestResult.__init__(self, stream, descriptions, verbosity)
        self.infoclass = TestInfo

    @failfast
    def addFailure(self, test, err):
        """ Called when a test method fails.

        Args:
            test:
            err:
        """
        self._save_output_data()
        test_info = self._create_test_info(test, err)
        self._prepare_callback(test_info, self.failures, "FAIL", "F")

    @failfast
    def addError(self, test, err):
        """ Called when a test method raises an error.

        Args:
            test:
            err:
        """
        self._save_output_data()
        test_info = self._create_test_info(test, err)
        self._prepare_callback(test_info, self.errors, 'ERROR', 'E')

    def _create_test_info(self, test, err):
        """ Creates test info.

        Args:
            test:
            err:
        """
        screen_shot = test.screen_shot_path if test.screen_shot_path else None
        return self.infoclass(self, test, outcome=self.infoclass.FAILURE, err=err, screen_shot=screen_shot)


class Runner(HTMLTestRunner):
    """Class for running test scenarios.

    Args:
        output (str): Path to folder for storing test report
        report_title (str): Title of a generated test report
        report_name (str): Name of a html file with test report
        template (str): Path to file with test report template
        resultclass (Result): Test result class
        boolean combine_reports (bool): Defines of test report of individual test classes should be combined
    """

    def __init__(self, output=DEFAULT_OUTPUT, report_title="Test results", report_name="TestReport",
                 template=DEFAULT_TEMPLATE, resultclass=Result, combine_reports=True):

        report_config = config_parser.ConfigParser().get_report_config()

        if report_config['clean']:
            FileManager.remove_tree(report_config['output'])

        HTMLTestRunner.__init__(self, output=output, report_title=report_title, report_name=report_name,
                                template=template, resultclass=resultclass, combine_reports=combine_reports)
