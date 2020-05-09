import argparse


class ArgParser:

    @classmethod
    def parse_args(cls):
        parse = argparse.ArgumentParser()
        parse.add_argument("-c", "--config", type=str, required=False, help="Set path to config file")
        args = parse.parse_args()
        return args.config
