"""
    Module contains class which parses CLI parameters.
"""

import argparse


class ArgParser:
    """Class for parsing CLI arguments

    Attributes:
        args (Namespace): Parsed arguments
    """
    def __init__(self):
        parse = argparse.ArgumentParser()
        parse.add_argument("-c", "--config", type=str, required=False, help="Set path to config file")
        self.args = parse.parse_args()

    def get_config(self):
        """Method for getting argument for configuration.

        Returns:
            str: Path to configuration
        """
        return self.args.config
