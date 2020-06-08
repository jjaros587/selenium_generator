import argparse


class ArgParser:
    """Class for parsing CLI arguments"""

    @classmethod
    def parse_args(cls):
        parse = argparse.ArgumentParser()
        parse.add_argument("-c", "--config", type=str, required=False, help="Set path to config file")
        args = parse.parse_args()
        return args.config
