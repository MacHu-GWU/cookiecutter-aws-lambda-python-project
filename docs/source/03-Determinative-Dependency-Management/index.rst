Determinative Dependency Management
==============================================================================
"Determinative dependency" is a principle in software development for production projects. This means that if the code is not changed, building the project at any time will result in exactly the same bytes-by-bytes. For a production-ready project, this is a must-have feature to ensure software integrity and consistent delivery.

However, the popular pip install method does not provide determinative dependencies and has several drawbacks:

- If specific versions of dependencies are not defined, pip install may install the latest version, which is constantly changing over time.
- Even if specific versions of dependencies are defined, it is not practical to specify the version for all of the dependencies that they rely on.
- If there is a conflict between dependencies at either the root or child dependency level, pip cannot resolve it.
- Even when using the pip freeze command to export specific versions of all dependencies, it does not provide integrity checks. Hackers may compromise the public PyPI repository and replace a version with malicious code, which has already happened many times in the industry.

`Poetry <https://python-poetry.org/>`_ is one of the tools that can ensure determinative dependencies. Other alternatives include `PDM <https://pdm.fming.dev/latest/>`_, which is more powerful and adopts the latest Python standards, but is a younger project. And `pipenv <https://pipenv.pypa.io/en/latest/>`_, an older tool with worse performance that may not always work correctly and is not recommended. For a comprehensive comparison of these tools, please see this `blog post <https://dev.to/frostming/a-review-pipenv-vs-poetry-vs-pdm-39b4>`_. In this project, I choose poetry to manage the Python dependencies.

From June 2020, `Python community start using pyproject.toml file for project dependencies definition <https://peps.python.org/pep-0621/>`_. In this project, I define four groups of dependencies:

- main: core dependencies to run the application
- dev: optional dependencies to speed up the development
- test: dependencies for testing
- automation: dependencies for DevOps automation scripts

Everytime you changed the ``pyproject.toml``, you should run ``poetry lock`` or ``make poetry-lock`` to resolve the dependencies tree, and store the determinative results in the ``poetry.lock`` file and committed it to Git as a record. This allows us to rollback to a historical version of the dependencies if needed.

.. code-block:: bash

    make poetry-lock

For local development, I usually run the ``make install-all`` command to install all dependencies at once. In the best practice, you should put dependencies for different purpose in different groups, and only install the dependencies you need:

.. code-block:: bash

    make install-all

The following "workflow action" are related to dependency management. For local development, the most useful commands are ``make poetry-lock`` and ``make install-all``::

    install                                  ** Install main dependencies and Package itself
    install-dev                              Install Development Dependencies
    install-test                             Install Test Dependencies
    install-doc                              Install Document Dependencies
    install-automation                       Install Automation Dependencies
    install-all                              Install All Dependencies
    poetry-export                            Export requirements-*.txt from poetry.lock file
    poetry-lock                              Resolve dependencies using poetry, update poetry.lock file
