import os
from HtmlTestRunner import HTMLTestRunner
from unittest import TestLoader, TestSuite
from src.generator.utils import get_list_of_files
from src.generator.utils import load_yaml
from src.generator.TestCreator import TestCreator
from src.generator.ConfigParser import ConfigParser
from src.generator.ArgParser import ArgParser


def main():
    args = ArgParser().parse_args()

    runner = HTMLTestRunner(combine_reports=True)
    tests = []

    for item in get_list_of_files(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__)))) + "\\scenarios"):

        test_class = TestCreator(load_yaml(item)).create()
        tests.append(TestLoader().loadTestsFromTestCase(test_class))

    runner.run(TestSuite(tests))


if __name__ == "__main__":
    main()
