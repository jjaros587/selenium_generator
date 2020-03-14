from src.testRunner import Runner, Loader
from src.parsers.ConfigParser import ConfigParser
from src.parsers.ArgParser import ArgParser


def main():
    config_path = ArgParser.parse_args()
    ConfigParser().load_config(config_path)

    runner = Runner.Runner(**ConfigParser().get_report_config())
    runner.run(Loader.Loader().load_scenarios())


if __name__ == "__main__":
    main()
