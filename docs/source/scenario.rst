#######################
Test scenario structure
#######################

Test scenario follows the structure of test written by using unittest framework.

.. code-block:: yaml

    name: ""
    data: ""
    tags: []
    before_all:
    before_each:
    steps:
    after_each:
    after_all:

*************
Tagging tests
*************

********
Keywords
********

- ``run_driver:``

- ``maximize:``

- ``close_driver:``

- ``page_object:``


***********************
Test data specification
***********************
There are several ways for test data specification. These can be divided in two groups which are as following:
#. Direct specification of method's parameters
#. Using of data for DDT

We can combine these two approaches, but the direct specification of method's parameters takes priority over second approach.
It means that we can run multiple tests with DDT functionality and in the same time to specify direct parameters for any step in a scenario.
But... these direct parameters would be the same for all of the tests which were run with DDT.

Before the data are parsed into class method which is being called, first of all, method's arguments are loaded.
After that the specific data, from params object of data from DDT, are being searched. Only if data with specific key was found, the data would be parsed into method.
A benefit of this approach is that the option of adding default ``kwargs`` into method, in the ``Python`` way, when the specific value wasn't specified is retained.

Direct specification
====================
For direct specification, object ``params:`` is used. This object has key-value pairs which represent kwargs arguments of the method which is being called.
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
There are again to possible ways for data specification using DDT approach.

#. Inline specification in scenario with yaml format
#. Load of data from file

Inline specification
--------------------
We can specify data for DDT directly in scenario using object ``data:``.
We can specify here array of data objects which will be parse into methods in the same way how would be done with external file.
But the format has to follow yaml format. The example below would generate two tests.

.. code-block:: yaml

    data:
      - search_text: "text1"
      - search_text: "text2"

Data from file
--------------
For using data from file only file path specification, including file format, is needed.
The file path should be relative path from data folder which was specified in global configuration.
It's possible to use data in ``json`` or ``yaml`` format.

.. code-block:: yaml

    data: "data.json"