from functools import wraps

__instances = {}
"""List of class instances created with singleton decorator."""


def singleton(cls):
    """Decorator for singleton design pattern. Function decorates a class and stores its instance to a list of instances
    from which is later returned if the class is called again.

    Args:
        cls: Decorated class

    Returns:
        Instance of a decorated class
    """
    @wraps(cls)
    def get_instance(*args, **kwargs):
        instance = __instances.get(cls, None)
        if not instance:
            instance = cls(*args, **kwargs)
            __instances[cls] = instance
        return instance
    return get_instance
