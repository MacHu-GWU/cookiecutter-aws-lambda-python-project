Centralized Config Management
==============================================================================
POC-style projects often have numerous hardcoded values, with some constant values being used multiple times. This pattern make projects difficult to maintain and prone to errors. In contrast, a production-ready project requires a centralized location to store all configurations. Once configurations are defined, we no longer allow hard-coded values and only reference configurations.

In this project, I implemented a light-weight config management system with the following folder structure::

    /config
    /config/define # config schema definition
    /config/define/main.py # centralized config object
    /config/define/app.py # app related configs, e.g. app name, app artifacts S3 bucket
    /config/define/cloudformation.py # CloudFormation related configs
    /config/define/deploy.py # deployment related configs
    /config/define/lbd_deploy.py # Lambda function deployment related configs
    /config/define/lbd_func.py # per Lambda function name, memory size, timeout configs
    /config/define/name.py # AWS Resource name related configs
    /config/init.py # config value initialization

- The ``define`` module defines the configuration data schema (field and value pairs).
    - To improve maintainability, we break down the long list of configuration fields into sub-modules.
    - There are two types of configuration values: constant values and derived values. Constant values are static values that are hardcoded in the config.json file, typically a string or an integer. Derived values are calculated dynamically based on one or more constant values.
- The ``init`` module defines how to read the configuration data from external storage.
    - On a developer's local laptop, the data is read from a config.json file.
    - During CI build runtime and AWS Lambda function runtime, the data is read from the AWS Parameter Store.

Below is the implementation of the ``init`` module:

.. literalinclude:: ../../../aws_lambda_python_example-project/aws_lambda_python_example/config/init.py
   :language: python
