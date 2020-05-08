from src.handlers.keywords import Keywords


class EventHandler:

    def __init__(self):
        self.keywords = Keywords()

    def __call__(self, test_instance, commands, data):
        self.commands = [] if commands is None else commands
        self.keywords(test_instance, data)

    def execute(self, instance, steps, data=None):
        self.__call__(instance, steps, data)
        for command in self.commands:
            [[key, value]] = command.items()
            getattr(self.keywords, "_" + key)(value)
