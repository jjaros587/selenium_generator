import json

import yaml
from functools import wraps

__instances = {}


def singleton(cls):
    @wraps(cls)
    def get_instance(*args, **kwargs):
        instance = __instances.get(cls, None)
        if not instance:
            instance = cls(*args, **kwargs)
            __instances[cls] = instance
        return instance
    return get_instance


def load_yaml(file):
    with open(file) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def load_json(file):
    with open(file) as f:
        return json.load(f)
