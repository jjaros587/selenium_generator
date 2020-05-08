from src.base.file_manager import FileManager
from src.test_runner import loader
from src.test_runner.runner import Runner
from src.parsers.config_parser import ConfigParser
from src.parsers.arg_parser import ArgParser


def main():
    config_path = ArgParser.parse_args()
    ConfigParser().load_config(config_path)

    report_config = ConfigParser().get_report_config()

    if report_config['clean']:
        FileManager.remove_tree(report_config['output'])

    if report_config['screenshots']:
        FileManager.mkdir(report_config['output'] + "\\screenshots")
    else:
        FileManager.mkdir(report_config['output'])

    runner = Runner(**ConfigParser().get_report_params())
    runner.run(loader.Loader().load_scenarios())


if __name__ == "__main__":
    main()
