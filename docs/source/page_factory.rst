############
Page Factory
############

The framework supports functionality for Page Factory design pattern. It extends basic Page Object Model (POM) by two things.

#. lazy loading of web elements
    - Elements are searched only when we ask for them and not when the POM class is initialized **->** no more ``NoSuchElementExceptions`` for elements which are rendered after some operation and not on the page load.

#. caching of elements
    - Avoiding of re-searching of web elements when we need to use them again. They are stored in a cache during the first search and with other search requests returned from it.


You can implement POM classes as you are used to. Only needed change is to use function ``find_by()`` from ``page_factory`` module instead of function
``find_element()`` from **selenium framework**. You can also used the same strategy for searching for web elements. It's possible to search them by these parameters:

**['id\_', 'xpath', 'link_text', 'partial_link_text', 'name', 'tag_name', 'class_name', 'css_selector']**

For usage just store the function with necessary parameters in the class attributes which represents web elements of the page.
In the need of use of the element just call the attribute as a function, as it's shown in the example below.

.. code-block:: python

    from selenium_generator.factories.page_factory import find_by
    from selenium.webdriver.common.by import By


    class GoogleSearchPage:

        _field_search = find_by(By.NAME, "q", cacheable=True)
        _button_search = find_by(name="btnK", cacheable=True)

        def __init__(self, driver):
            self._driver = driver
            self._driver.get("https://www.google.com/")

        def search_positive(self, search_text):
            self._field_search().send_keys(search_text)
            self._button_search().click()
            assert "search" in self._driver.current_url

Function accepts several parameters:

- ``how (str)`` - Name of a attribute by which we want to search for a web element

- ``using (str)`` - Value of a attribute by which we want to search for a web element

- ``multiple (bool)`` - for searching for multiple elements (eg. list of columns in table)

- ``cacheable (bool)`` - for storing element in cache

- ``context (WebElement)`` - for searching for an element in another element and not in driver

- ``driver_attr (str)`` - By default the function search for instance of a WebDriver in attribute ``_driver`` but you can change the default name with this parameter.


As you can see in the given example, there are two possible ways of specifying parameters of a web element we want to search for.

#. using of parameters ``how`` and ``using``

#. using ``kwargs`` parameters - If you prefere using kwargs argumets for specifying strategy and value for searching for web elements you can use ``key-pair values`` where ``key`` is strategy parameter and ``value`` is a needed value








