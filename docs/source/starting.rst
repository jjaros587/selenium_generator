################
Starting the app
################

Tests can be easily run with main module of the framework.

.. code-block:: python

    from selenium_generator import main

    if __name__ == "__main__":
        main.main()

The framework needs loaded configuration for test execution.
The main module loads configuration and run tests with test runner according to loaded configuration.
If no configuration is specified, framework will use default configuration.

.. toggle-header::
    :header: **Show default config**

        .. code-block:: yaml

            scenarios: "scenarios"
            data: "data"
            pages: "pages"

            report:
              screenshots: true
              clean: true

            tags: []

            drivers:
              chrome:
                remote: false

              firefox:
                remote: false

.. note::
    Default configuration can be used only for local drivers of the latest versions.

If the default config isn't sufficient there are two ways of setting custom configuration.

#. To place file ``config.yaml`` with the custom configuration in the root directory of the project
#. To load the config file from any other directory and to specify the path to it with CLI argument

.. code-block:: console

    python main.py -c custom_dir/custom_config.yaml

The framework tries to load config in following order:

#. Path from CLI argument
#. ``config.yaml`` file from the root folder of the project
#. Default config

************
Custom start
************
You may find the main module insufficient for running the tests, especially if the framework is being extended.
In this case you can create your own workflow and override the default behaviour by calling the needed methods individually.
Just be aware that the configuration might need to be extended as well as its schema for validation.
