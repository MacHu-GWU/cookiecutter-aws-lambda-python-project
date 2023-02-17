``aws-lambda-python-project``
==============================================================================
This is a sample AWS Lambda Python project template with production ready set up. You can easily generate a project skeleton for your own project.


Usage
------------------------------------------------------------------------------
Enter the following command, it will use the latest template.

.. code-block:: bash

    pip install cookiecutter
    cookiecutter https://github.com/MacHu-GWU/cookiecutter-aws-lambda-python-project

Or, you can use a specific released version, you can find `full list of release at here <https://github.com/MacHu-GWU/cookiecutter-aws-lambda-python-project/releases>`_.

.. code-block:: bash

    # use specific version
    cookiecutter https://github.com/MacHu-GWU/cookiecutter-aws-lambda-python-project --checkout tags/${version}
    # for example (v4 is the latest as of 2023-02-17)
    cookiecutter https://github.com/MacHu-GWU/cookiecutter-aws-lambda-python-project --checkout tags/v4

Then fill in some information::

    package_name [my_package]: ...
    author_name [Firstname Lastname]: ...
    author_email [firstname.lastname@email.com]: ...
    ...

Done.
