from HtmlTestRunner.runner import HTMLTestRunner, HtmlTestResult
from HtmlTestRunner.result import _TestInfo
from unittest.result import failfast
import os

DEFAULT_TEMPLATE = os.path.join(os.path.dirname(__file__), "template", "report_template.html")
DEFAULT_OUTPUT = "./reports/"


class TestInfo(_TestInfo):

    def __init__(self, test_result, test_method, outcome=_TestInfo.SUCCESS, err=None, sub_test=None, screen_shot=None):
        _TestInfo.__init__(self, test_result, test_method, outcome=outcome, err=err, subTest=sub_test)
        self.screen_shot = screen_shot


class Result(HtmlTestResult):

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
        """" Called when a test method raises an error. """
        self._save_output_data()
        test_info = self._create_test_info(test, err)
        self._prepare_callback(test_info, self.errors, 'ERROR', 'E')

    def _create_test_info(self, test, err):
        screen_shot = test.screen_shot_path if test.screen_shot_path else None
        return self.infoclass(self, test, outcome=self.infoclass.FAILURE, err=err, screen_shot=screen_shot)


class Runner(HTMLTestRunner):
    def __init__(self, output=DEFAULT_OUTPUT, report_title=None, report_name=None, template=DEFAULT_TEMPLATE,
                 resultclass=Result, add_timestamp=True, combine_reports=False, template_args=None):

        HTMLTestRunner.__init__(self, output=output, report_title=report_title, report_name=report_name,
                                template=template, resultclass=resultclass, add_timestamp=add_timestamp,
                                combine_reports=combine_reports, template_args=template_args)
