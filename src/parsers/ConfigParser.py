from src.base.utils import singleton, load_yaml


@singleton
class ConfigParser:

    config = None

    @classmethod
    def load_config(cls, config_path):
        cls.config = load_yaml(config_path)

    def get_pages_path(self):
        return self.config['pages']

    def get_scenarios_path(self):
        return self.config['scenarios']

    def get_report_config(self):
        return self.config['report']

    def get_driver_config(self):
        return self.config['driver']

    def get_data_path(self, path_from_root):
        return self.config['data'] + path_from_root

    def get_tags(self):
        if 'tags' not in self.config or self.config['tags'] is None:
            return None
        return self.config['tags']
