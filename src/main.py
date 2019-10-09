import os
from HtmlTestRunner import HTMLTestRunner
from src.generator.BaseTest import BaseTest, factory
from unittest import TestLoader, TestSuite
from src.generator.utils import get_list_of_files
from src.generator.utils import load_yaml


def main():
    runner = HTMLTestRunner(combine_reports=True)
    tests = []

    for item in get_list_of_files(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\scenarios"):
        data = load_yaml(item)

        test_class = factory(data['name'], data)
        setattr(test_class, "test_"+data['name'], BaseTest.base_method)

        tests.append(TestLoader().loadTestsFromTestCase(test_class))

    runner.run(TestSuite(tests))


if __name__ == "__main__":
    main()
