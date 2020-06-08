def cacheable_decorator(lookup):
    def func(self):
        if not hasattr(self, '_elements_cache'):
            self._elements_cache = {}  # {callable_id: element(s)}
        cache = self._elements_cache

        key = id(lookup)
        if key not in cache:
            cache[key] = lookup(self)
        return cache[key]

    return func


_strategy_kwargs = ['id_', 'xpath', 'link_text', 'partial_link_text',
                    'name', 'tag_name', 'class_name', 'css_selector']


def _find_by(how, using, multiple, cacheable, context, driver_attr, **kwargs):
    def func(self):
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
    return _find_by(how, using, multiple, cacheable, context, driver_attr, **kwargs)
