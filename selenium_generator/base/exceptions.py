class InvalidConfiguration(Exception):
    pass


class MissingConfiguration(Exception):
    pass


class UnallowedBrowser(ValueError):
    def __init__(self, allowed_browsers):
        super().__init__("Unallowed browser. Allowed browsers are: %s" % allowed_browsers)
