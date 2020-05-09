from selenium_generator.test_runner import loader
from selenium_generator.test_runner.runner import Runner
from selenium_generator.parsers.config_parser import ConfigParser
from selenium_generator.parsers.arg_parser import ArgParser


def main():
    config_path = ArgParser.parse_args()
    ConfigParser().load_config(config_path)

    runner = Runner(**ConfigParser().get_report_params())
    runner.run(loader.Loader().load_scenarios())


if __name__ == "__main__":
    main()
