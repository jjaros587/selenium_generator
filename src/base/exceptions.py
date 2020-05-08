class InvalidConfiguration(Exception):
    pass


class MissingConfiguration(Exception):
    pass


class UnallowedBrowser(ValueError):
    pass


class UnspecifiedDataFolder(Exception):
    def __init__(self):
        super().__init__("Data folder was not specified in global configuration. "
                         "Specify the folder or use inline data specification.")
