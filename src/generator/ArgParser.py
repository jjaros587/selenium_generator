import argparse


class ArgParser:

    def parse_args(self):
        parse = argparse.ArgumentParser()
        parse.add_argument("-c", "--config", type=str, required=True, help="Set path to config file")
        args = parse.parse_args()
        return args.config
    #     return {'parse': parse, 'args': args}
    #
    # @staticmethod
    # def _verify_args(parse, args):
    #     print("Zadejte prosím platný název prostředí")
    #     parse.print_help()
    #     quit(2)
