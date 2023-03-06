``cookiecutter-aws-lambda-python-project``
==============================================================================
This is an AWS Lambda Python project template with production ready setup. You can easily generate a folder structure as a foundation, then plugin your business code, then go to production.

Best practices and automation features included in this template:

- Multi environments (dev, test, int, preprod, prod, etc ...) config management, host your sensitive config data in AWS SSM Parameter Store.
- Multi AWS Account / multi AWS Region deployment automation.
- Infrastructure as code development, testing and deployment automation.
- Unit test, code coverage test automation.
- Unit test for AWS Lambda without deployment best practice.
- Integration test best practice and automation.
- Lambda layer building automation.
- Add lambda function deployment automation, manage large number of Lambda Function, event source mapping, API Gateway definition at scale.
- Determinative dependencies management to ensure consistency of deployment (same input -> same output, bytes by bytes).
- Versioned build artifacts management in S3, you have the full history of all versioned artifacts you have ever deployed.
- Git branching and Git workflow best practice.
- CI/CD integration with AWS CodeBuild, and you can use any other CI/CD platform (GitHub Actions, Jenkins, CircleCI, GitLab pipeline, BitBucket Pipeline, etc ...)
- Immutable deployment, every deployment is a new version.
- Capability to rollback to any historical release.

Disclaimer:

All the best practice used in this repo is based on my career experience, and my personal opinion. I have done over 50+ AWS microservice projects in dev and 10+ projects in production environments. It is the best practice I am using for years. In average, it took me around months of work to setup a production ready git repo with proper CI/CD strategy. This project template saves me efforts to setup the DevOps automation, and allows me to focus on the business logic, and greatly reduces the releasing cycle. In the three most recent production projects, it took me around 1 week from scratch to production, and fastest releasing cycle is reduced to 1 day. Again, it is my personal best practice, please use it at your own risk.


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

We have an example project generated from this template `aws_lambda_python_example-project <./aws_lambda_python_example-project>`_. Please take a look at it.
