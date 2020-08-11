"""
    Module contains function and constants which are used for implementation of Page Factory design pattern.
"""

_strategy_kwargs = ['id_', 'xpath', 'link_text', 'partial_link_text',
                    'name', 'tag_name', 'class_name', 'css_selector']
"""Constan which stores allowed values by which a web element can be searched."""

def cacheable_decorator(lookup):
    """Decorator used for cacheable elements.

    Args:
        lookup (type): Decorated function

    Returns:
        function: Fuction which search for element in cache
    """
    def func(self):
        """Fuction which search for element in cache

        Args:
            self (cls): Page object class from which the fuction was called.

        Returns:
            :class:`selenium.webdriver.remote.webelement.WebElement`: Fuction which search for element in cache
        """
        if not hasattr(self, '_elements_cache'):
            self._elements_cache = {}  # {callable_id: element(s)}
        cache = self._elements_cache

        key = id(lookup)
        if key not in cache:
            cache[key] = lookup(self)
        return cache[key]

    return func


def _find_by(how, using, multiple, cacheable, context, driver_attr, **kwargs):
    """Decorator used for function which search for web element in used driver.

    Args:
        how (str): Attribute by which we want to search a web element
        using (str): Value of an attribute by which we want to search a web element
        multiple (bool): Specifies if we are searching multiple web elements
        cacheable (bool): Specifies if we want to store found web element in cache
        driver_attr (str): Name of an attribute where instance of driver is stored
        **kwargs (dict): Key-value pair which specify attribute and value by which we want to search for web element

    Returns:
        function: Fuction which search for web element in used driver.
    """
    def func(self):
        """Decorator used for function which search for web element in used driver.

        Args:
            self (cls): Page object class from which the fuction was called.

        Returns:
             :class:`selenium.webdriver.remote.webelement.WebElement`: Found web element
        """
        # context - driver or a certain element
        if context:
            driver = context() if callable(context) else context.__get__(self)  # or property
        else:
            driver = getattr(self, driver_attr)

        # 'how' AND 'using' take precedence over keyword arguments
        if how and using:
            lookup = driver.find_elements if multiple else driver.find_element
            return lookup(how, using)

        [[key, value]] = kwargs.items()
        if len(kwargs) != 1 or key not in _strategy_kwargs:
            raise ValueError(
                "If 'how' AND 'using' are not specified, one and only one of the following "
                "valid keyword arguments should be provided: %s." % _strategy_kwargs)

        suffix = key[:-1] if key.endswith('_') else key  # find_element(s)_by_xxx
        prefix = 'find_elements_by' if multiple else 'find_element_by'
        lookup = getattr(driver, '%s_%s' % (prefix, suffix))
        return lookup(value)

    return cacheable_decorator(func) if cacheable else func


def find_by(how=None, using=None, multiple=False, cacheable=False, context=None, driver_attr='_driver', **kwargs):
    """Public function which returns a correct function for searching for web element.  The base one or chacheable, based on given parameters.

    Args:
        how (str): Attribute by which we want to search a web element
        using (str): Value of an attribute by which we want to search a web element
        multiple (bool): Specifies if we are searching multiple web elements
        cacheable (bool): Specifies if we want to store found web element in cache
        driver_attr (str): Name of an attribute where instance of driver is stored
        **kwargs (dict): Key-value pair which specify attribute and value by which we want to search for web element

    Returns:
        function: Function which is used for searching of web element in driver. The base one or chacheable, based on given parameters.
    """
    return _find_by(how, using, multiple, cacheable, context, driver_attr, **kwargs)
