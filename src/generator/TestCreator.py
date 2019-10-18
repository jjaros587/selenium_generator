from src.generator.BaseTest import factory
import ddt


class TestCreator:

    def __init__(self, scenario):
        self.scenario = scenario
        self.test_class = factory(scenario['name'], scenario)
        self.test_method = self.test_class.base_method

    def create(self):
        self._check_data()
        return ddt.ddt(self.test_class)

    def _check_data(self):
        if ('data' not in self.scenario) or (('data' in self.scenario) and (self.scenario['data'] is None)):
            self._create_test_method(self.test_method)
            return

        if self.scenario['data'] is not None:
            self._create_test_method(
                ddt.file_data
                (self.scenario['data'])
                (getattr(self.test_class, self.test_method.__name__))
            )
            return

    def _create_test_method(self, fn):
        setattr(self.test_class, self._simple_name(), fn)

    def _simple_name(self):
        return "test_" + self.scenario['name']
