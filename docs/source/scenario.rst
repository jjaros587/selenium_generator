#######################
Test scenario structure
#######################

Test scenario follows the structure of test written by using `unittest <https://docs.python.org/3/library/unittest.html>`_ framework.
Bellow are given its first level objects.

.. code-block:: yaml

    name:
    tags:
    data:
    skip:
    steps:


*********
Test name
*********
``name`` object defines name of a test, which is used for generating of a test class and it's also used in a test report.
It has to follow naming conventions of Python which means it must match a regular expression ``[a-zA-Z0-9_]+``.

********************
Adding test to suite
********************
Test can be added to a test suite by adding tags to a list in ``tags`` object.
The object is not mandatory and can contain only non-empty ``string`` values.

.. code-block:: yaml

    tags: ["regression", "acceptance"]


.. hint::
    There is an option to run a test all the times, no matter what tags are specified in configuration, by adding ``*`` symbol to the array.

    .. code-block:: yaml

        tags: ["*"]

For more information about tags visit `this page <configuration.html#test-suite-specification>`_.

*****
Steps
*****
``steps`` object consists of a list of individual steps of a test scenario.

The list can contain predefined keywords which ensure the execution of the individual steps.

`Click here for more information about keywords <keywords.html>`_.

.. code-block:: yaml

    steps:
        - run_driver: "chrome"
        - page_object:
            class: "GoogleSearchPage"
            method: "search_negative"
            params:
                searchText: "any text"
        - close_driver:


*********
Test data
*********
There are several ways for test data specification. These can be divided into two groups which are as following:

#. Direct specification of method's parameters
#. Using of DDT

We can combine these two approaches, but the direct specification of method's parameters takes priority over second approach.
It means that we can run multiple tests with DDT functionality and in the same time to specify direct parameters for any step in a scenario.
But... these direct parameters would be the same for all of the generated tests with DDT.

Before the data are parsed into class method which is being called, first of all, method's arguments are loaded.
After that the specific data, from params object of data from DDT, are being searched. Only if data with specific key are found, the data are then be parsed into method.
A benefit of this approach is that the option of adding default ``kwargs`` into method, in the ``Python`` way, when the specific value wasn't specified is retained.

Direct specification
====================
For direct specification, object ``params`` is used. This object has ``key-value`` pairs which represent ``**kwargs`` arguments of a method which is being called.
Once the object is specified, it is impossible to use data from the second approach.

See the example:

.. code-block:: yaml

    steps:
      - page_object:
          class: "GoogleSearchPage"
          method: "search"
          params:
            search_text: "searched value"


DDT
===
There are again two possible ways for data specification using DDT approach.

#. Inline specification in scenario with yaml format
#. Load of data from file

Inline specification
--------------------
We can specify data for DDT directly in scenario using object ``data``.
We can specify here array of data objects which would be parsed into methods in the same way how it would be done with external file.
But a format has to follow ``yaml`` format. The example below would generate two tests.

.. code-block:: yaml

    data:
      - search_text: "text1"
      - search_text: "text2"


Data from file
--------------
For using data from file only file path specification, including file format, is needed.
The file path should be relative path from data folder which was specified in configuration.
It's possible to use data in ``json`` or ``yaml`` format.

`Click here for more information about configuration of paths <configuration.html#setting-of-paths>`_.

.. code-block:: yaml

    data: "data.json"

*****************
Skipping scenario
*****************
We might find useful to skip a scenario. This is what object ``skip`` is used for.
If scenario contains this object and its value is set on ``True``, scenario won't be executed and will be added
to a test report as ``Skipped``.
