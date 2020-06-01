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

    :param test_result: :func:`~Result`
    :param test_method:
    :param outcome:
    :param err:
    :param sub_test:
    """
    def __init__(self, test_result, test_method, outcome=_TestInfo.SUCCESS, err=None, sub_test=None, screen_shot=None):
        _TestInfo.__init__(self, test_result, test_method, outcome=outcome, err=err, subTest=sub_test)
        self.screen_shot = screen_shot


class Result(HtmlTestResult):
    """ Result class.

    :param stream: :func:`~Result`
    :param descriptions:
    :param verbosity:

    .. automethod:: _create_test_info
    """
    def __init__(self, stream, descriptions, verbosity):
        HtmlTestResult.__init__(self, stream, descriptions, verbosity)
        self.infoclass = TestInfo

    @failfast
    def addFailure(self, test, err):
        """ Called when a test method fails. """
        self._save_output_data()
        test_info = self._create_test_info(test, err)
        self._prepare_callback(test_info, self.failures, "FAIL", "F")

    @failfast
    def addError(self, test, err):
        """ Called when a test method raises an error. """
        self._save_output_data()
        test_info = self._create_test_info(test, err)
        self._prepare_callback(test_info, self.errors, 'ERROR', 'E')

    def _create_test_info(self, test, err):
        """ Creates test info. """
        screen_shot = test.screen_shot_path if test.screen_shot_path else None
        return self.infoclass(self, test, outcome=self.infoclass.FAILURE, err=err, screen_shot=screen_shot)


class Runner(HTMLTestRunner):
    """ Runner class.

    :param string utput:
    :param string report_title:
    :param string report_name:
    :param template:
    :param resultclass:
    :param boolean combine_reports:
    """
    def __init__(self, output=DEFAULT_OUTPUT, report_title="Test results", report_name="TestReport",
                 template=DEFAULT_TEMPLATE, resultclass=Result, combine_reports=True):

        report_config = config_parser.ConfigParser().get_report_config()

        if report_config['clean']:
            FileManager.remove_tree(report_config['output'])

        HTMLTestRunner.__init__(self, output=output, report_title=report_title, report_name=report_name,
                                template=template, resultclass=resultclass, combine_reports=combine_reports)
