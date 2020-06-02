########
Keywords
########

``run_driver (string)``

Create an instance of a required driver.
Its parameter is a name of a required driver which has to correspond with one of the keys in configuration of drivers.
If a key is not found in configuration ``MissingConfiguration`` is thrown.
For more information about configuration of drivers visit this `*page* <configuration.html#drivers-configuration>`_.

.. code-block:: yaml

    steps:
        - run_driver: "chrome"


----

``maximize``

Maximizes a windows of an instance of a driver.

.. code-block:: yaml

    steps:
        - run_driver: "chrome"
        - maximize:


----

``close_driver``

Closes an instance of a driver which were run before.

.. code-block:: yaml

    steps:
        - run_driver: "chrome"
        - close_driver:


----

``page_object``

It instantiates the Page Object and calls its requested method, including parsing of method's parameters.

.. code-block:: yaml

    steps:
        - page_object:
            class: "GoogleSearchPage"
            method: "search_negative"
            params:
                searchText: "any text"

- ``class (string)``
    - defines a class name of a required Page Object
- ``method (string)``
    - defines a class method of a required Page Object
- ``params (string)``
    - defines parameters and its values of a requested method
    - parameters represent ``**kwargs`` parameters of a method
    - this object is not required - for more information about parsing parsing method parameters visit this `*page* <scenario.html#test-data>`_


