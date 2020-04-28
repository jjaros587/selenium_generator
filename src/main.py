from src.base.FileManager import FileManager
from src.testRunner import Loader, Runner
from src.parsers.ConfigParser import ConfigParser
from src.parsers.ArgParser import ArgParser


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

    runner = Runner.Runner(**ConfigParser().get_report_params())
    runner.run(Loader.Loader().load_scenarios())


if __name__ == "__main__":
    main()
