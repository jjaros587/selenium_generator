from selenium_generator.handlers.keywords import Keywords


class EventHandler:
    """Class for execution of steps in scenario.

    Attributes:
        keywords (Keywords): Instance of a Keyword class
    """

    def __init__(self):
        self.keywords = Keywords()

    def __call__(self, test_instance, commands, data):
        self.commands = [] if commands is None else commands
        self.keywords(test_instance, data)

    def execute(self, instance, steps, data=None):
        """Method executes the given scenario steps.

        Args:
            instance (BaseTest): Instance of a BaseTest class
            steps (list): List of steps in scenario
            data (dict): Test data
        """
        self.__call__(instance, steps, data)
        for command in self.commands:
            [[key, value]] = command.items()
            getattr(self.keywords, "_" + key)(value)
