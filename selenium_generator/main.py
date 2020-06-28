from selenium_generator.test_runner import loader
from selenium_generator.test_runner.runner import Runner
from selenium_generator.parsers.config_parser import ConfigParser
from selenium_generator.base.file_manager import FileManager


def main():
    """The MAIN method of the framework.
    The method calls classes for loading configuration according to which the tests are executed.
    Based to loaded allowed drivers for configuration, the scenarios are run for all specified drivers.
    """
    report_config = ConfigParser().get_report_config()
    if report_config['clean']:
        FileManager.remove_tree(report_config['output'])

    for driver in ConfigParser().get_allowed_drivers():
        print("\n Running driver %s..." % driver)
        runner = Runner(driver, **ConfigParser().get_report_params())
        runner.run(loader.Loader().load_scenarios(driver))


if __name__ == "__main__":
    main()
