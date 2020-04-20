from src.base.BaseTest import factory
from src.base.utils import singleton
from src.parsers.ConfigParser import ConfigParser
import ddt


@singleton
class TestCreator:

    def __call__(self, scenario):
        self.scenario = scenario
        self.test_class = factory(scenario['name'], scenario)
        self.test_method = self.test_class.base_method
        return self

    def create(self):
        self._check_data()
        return ddt.ddt(self.test_class)

    def _check_data(self):
        if 'data' not in self.scenario or self.scenario['data'] is None:
            self._create_test_method(self.test_method)
            return

        if isinstance(self.scenario['data'], str):
            data_path = ConfigParser().get_data_path(self.scenario['data'])
            self._create_test_method(
                ddt.file_data(data_path)(getattr(self.test_class, self.test_method.__name__))
            )
            return

        ddt._add_tests_from_data(self.test_class, self._generate_test_name(), self.test_method, self.scenario['data'])

    def _create_test_method(self, fn):
        setattr(self.test_class, self._generate_test_name(), fn)

    def _generate_test_name(self):
        return "test_" + self.scenario['name']
