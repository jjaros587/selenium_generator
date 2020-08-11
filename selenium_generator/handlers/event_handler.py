"""
    Module contains class which executes steps from given objects from test scenario.
"""

from selenium_generator.base.singleton import singleton
from selenium_generator.handlers.keywords import Keywords


@singleton
class EventHandler:
    """Class for execution of steps in scenario.

    Args:
        keywords (Keywords): Class with Keywords.

    Attributes:
        keywords (Keywords): Instance of a Keyword class
    """

    def __init__(self, keywords=Keywords):
        self.keywords = keywords()

    def execute(self, instance, steps, data=None):
        """Method executes the given list of scenario steps.

        Args:
            instance (:class:`unittest.TestCase`): Instance of a TestCase class
            steps (list): List of steps in scenario
            data (dict): Test data
        """
        steps = [] if steps is None else steps
        self.keywords(instance, data)
        for step in steps:
            [[key, value]] = step.items()
            getattr(self.keywords, "_" + key)(value)
