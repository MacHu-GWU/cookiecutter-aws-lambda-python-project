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
    # for example (v5 is the latest as of 2023-02-18)
    cookiecutter https://github.com/MacHu-GWU/cookiecutter-aws-lambda-python-project --checkout tags/v5

Then fill in some information::

    package_name [my_package]: ...
    author_name [Firstname Lastname]: ...
    author_email [firstname.lastname@email.com]: ...
    ...

Then it will generate a Git repo folder structures like this:

- ``/bin/*.py``: binary executable scripts for automation, devops, CI/CD
- ``/config/...``: non-sensitive multi-env config management
- ``/${package_name}/...`` your python project source code
- ``/lambda_app/...``: AWS Lambda microservices management and deployment
- ``/tests/...``: unit test
- ``/tests_int/..``: integration test
- ``/.coveragerc``: code coverage test config
- ``/Makefile``: the automation script CLI tools for local development
- ``/pyproject.toml`` and ``/poetry.lock``: determinative dependency management
- (Optional) ``/codebuild-config.json`` and ``/buildspec.yml``: the CI/CD integration with AWS CodeBuild, but you can use any other CI/CD platform (GitHub Actions, Jenkins, CircleCI, GitLab pipeline, BitBucket, Pipeline, etc ...), and just copy and paste the following shell scripts to your CI workflow definition file::

.. code-block:: bash

    pip install poetry==1.2.2 --quiet --disable-pip-version-check
    pip install -r requirements-automation.txt --quiet --disable-pip-version-check
    python ./bin/s99_1_install_phase.py
    ./.venv/bin/python ./bin/s99_2_pre_build_phase.py
    ./.venv/bin/python ./bin/s99_3_build_phase.py
    ./.venv/bin/python ./bin/s99_4_post_build_phase.py
