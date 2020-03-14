import os
import sys
import glob
import pkgutil
import importlib
import yaml
from functools import wraps
from functools import partialmethod

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


def screen_shot_on_fail(browser_attr='browser'):
    def decorator(cls):
        def with_screen_shot(self, fn, *args, **kwargs):
            try:
                return fn(self, *args, **kwargs)
            finally:
                if sys.exc_info()[0]:
                    browser = getattr(self, browser_attr)
                    browser.get_screenshot_as_file('screenshot-%s.png' % fn.__name__)

        for attr, fn in cls.__dict__.items():
            if attr[:5] == 'test_' and callable(fn):
                setattr(cls, attr, partialmethod(with_screen_shot, fn))

        return cls
    return decorator


def import_submodules(package, recursive=True):
    def get_subpackages(module):
        folder = os.path.dirname(module.__file__)

        def is_package(d):
            d = os.path.join(folder, d)
            return os.path.isdir(d) and glob.glob(os.path.join(d, '__init__.py*'))

        return filter(is_package, os.listdir(folder))
    """ Import all submodules of a module, recursively, including subpackages

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    results = {}
    for item in get_subpackages(package):

        if isinstance(item, str):
            item = importlib.import_module(package.__name__ + "." + item)

        for loader, name, is_pkg in pkgutil.walk_packages(item.__path__):
            full_name = item.__name__ + '.' + name
            results[name] = importlib.import_module(full_name)
            if recursive and is_pkg:
                results.update(import_submodules(full_name))
    return results


def get_list_of_files(dir_name):
    all_files = list()
    for f in os.listdir(dir_name):
        full_path = os.path.join(dir_name, f)
        if os.path.isdir(full_path):
            all_files += get_list_of_files(full_path)
        else:
            all_files.append(full_path)
    return all_files


def load_yaml(scenario):
    with open(scenario) as f:
        return yaml.load(f, Loader=yaml.FullLoader)
