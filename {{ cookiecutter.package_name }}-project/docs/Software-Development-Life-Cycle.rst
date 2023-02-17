Software Development Life Cycle (SDLC)
==============================================================================
.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 2
    :local:


Semantic Git Branching
------------------------------------------------------------------------------
In this project, we follow the semantic git branching convention. We use different branch name for different purpose, also the CI system will use branch name to identify what to run and what not to run.

- ``main`` branch:
    - usage: for deployment to integration test environment and run integration test
    - name pattern: exactly equal to ``main`` or ``master``
- ``feature`` branch:
    - usage: for feature deployment or bug fix
    - name pattern: starts with ``feat`` or ``feature``
- ``int`` branch:
    - usage: for integration test in ``int`` environment
    - name pattern: starts with ``int``
- ``release`` branch:
    - usage: for deployment to prod environment
    - name pattern: starts with ``rls`` or ``release``
- ``cleanup`` branch:
    - usage: delete deployment
    - name pattern: starts with ``clean`` or ``cleanup``
- ``cf`` branch:
    - usage: deploy AWS CloudFormation template
    - name pattern: starts with ``cf`` or ``cloudformation``
- ``layer`` branch:
    - usage: deploy AWS Lambda Layer
    - name pattern: starts with ``layer``
- ``lambda`` branch:
    - usage: deploy AWS Lambda Function
    - name pattern: starts with ``lbd`` or ``lambda``
- ``ecr`` branch:
    - usage: build ECR image
    - name pattern: starts with ``ecr``


**Git Branch vs CI Action**

+--------------------------------+---------+-----+----+-------+--------+-----+---------+---------+
|      Action👇 Git Branch 👉      | feature | fix | cf | layer | lambda | int | release | cleanup |
+--------------------------------+---------+-----+----+-------+--------+-----+---------+---------+
|        Create Virtualenv       |    ✅    |  ✅  |  ✅ |   ✅   |    ✅   |  ✅  |    ✅    |    ✅    |
+--------------------------------+---------+-----+----+-------+--------+-----+---------+---------+
|      Install Dependencies      |    ✅    |  ✅  |  ✅ |   ✅   |    ✅   |  ✅  |    ✅    |    ✅    |
+--------------------------------+---------+-----+----+-------+--------+-----+---------+---------+
|     Run Code Coverage Test     |    ✅    |  ✅  |  ✅ |   ❌   |    ✅   |  ✅  |    ✅    |    ❌    |
+--------------------------------+---------+-----+----+-------+--------+-----+---------+---------+
|      Deploy CloudFormation     |    ❌    |  ❌  |  ✅ |   ❌   |    ❌   |  ✅  |    ✅    |    ❌    |
+--------------------------------+---------+-----+----+-------+--------+-----+---------+---------+
| Build New Lambda Layer Version |    ❌    |  ❌  |  ❌ |   ✅   |    ❌   |  ❌  |    ❌    |    ❌    |
+--------------------------------+---------+-----+----+-------+--------+-----+---------+---------+
|        Deploy Lambda App       |    ❌    |  ❌  |  ❌ |   ❌   |    ✅   |  ✅  |    ✅    |    ❌    |
+--------------------------------+---------+-----+----+-------+--------+-----+---------+---------+
|      Run Integration Test      |    ❌    |  ❌  |  ❌ |   ❌   |    ❌   |  ✅  |    ✅    |    ❌    |
+--------------------------------+---------+-----+----+-------+--------+-----+---------+---------+
|       Backup Prod Config       |    ❌    |  ❌  |  ❌ |   ❌   |    ❌   |  ❌  |    ✅    |    ❌    |
+--------------------------------+---------+-----+----+-------+--------+-----+---------+---------+
|        Delete Lambda App       |    ❌    |  ❌  |  ❌ |   ❌   |    ❌   |  ❌  |    ❌    |    ✅    |
+--------------------------------+---------+-----+----+-------+--------+-----+---------+---------+
|      Delete CloudFormation     |    ❌    |  ❌  |  ❌ |   ❌   |    ❌   |  ❌  |    ❌    |    ✅    |
+--------------------------------+---------+-----+----+-------+--------+-----+---------+---------+

**Git Branch vs Multi-Environment**

+---------------------+-----+-----+---------+
|  Git Branch👇 Env 👉  | dev | int |   prod  |
+---------------------+-----+-----+---------+
|       feature       |  ✅  |     |         |
+---------------------+-----+-----+---------+
|         fix         |  ✅  |     |         |
+---------------------+-----+-----+---------+
|          cf         |  ✅  |     |         |
+---------------------+-----+-----+---------+
|        layer        |  ✅  |     |         |
+---------------------+-----+-----+---------+
|        lambda       |  ✅  |     |         |
+---------------------+-----+-----+---------+
|         int         |     |  ✅  |         |
+---------------------+-----+-----+---------+
|       release       |     |  ✅  |         |
+---------------------+-----+-----+---------+
| cleanup/${env_name} |     |     | depends |
+---------------------+-----+-----+---------+


Software Development Life Cycle (SDLC)
------------------------------------------------------------------------------
.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


1. 📋 Update Project Config (If necessary)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Note: this task should only be done by project ADMIN. **❗ Other develops should not have permission to update parameter store** (prod is using the parameter store).

Development:

1. Create a ``feature/${description}`` or ``feat/${description}`` branch from ``main``.
2. Update the following files according to your business requirement.
    - ``./${python_package_name}/config/define/``: update config object definition.
    - ``./config/config.json``: update non-sensitive config data file.
    - ``${HOME}/.projects/${python_package_name}/config-secret.json``: update sensitive config data file.
3. Run unit test for config definition and initialization ``./tests/config/test_config_init.py``

Code Review:

4. Push your ``feature/${description}`` branch to git, and create a PR from ``feature/${description}`` to ``main``. The CI will test your code in ``dev`` environment.
5. Make sure the unit test passed in the CI before you ask for code review.
6. Ask peers for code review and make changes when necessary.
7. Merge PR and delete the branch. This merge will not trigger any build.
8. Deploy config to AWS Parameter Store from local laptop, run this script ``./config/deploy_parameters.py``.


2. 💻 Implement Feature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Development:

1. Create a ``feature/${description}`` or ``feat/${description}`` branch from ``main``.
2. Develop the source code and add unit test cases.
3. Make sure the unit test passed on your local and you have decent code coverage.

Code Review:

4. Push your ``feature/${description}`` branch to git, and create a PR from ``feature/${description}`` to ``main``. The CI will test your code in ``dev`` environment.
5. Make sure the unit test passed in the CI before you ask for code review.
6. Ask peers for code review and make changes when necessary.
7. Merge PR and delete the branch. This merge will not trigger any build.


3. 🐑 Update Infrastructure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Development:

1. Create a ``cf/${description}`` branch from ``main``.
2. Develop the infrastructure as code script locally. Update the following files according to your business requirement.
    - ``./${python_package_name}/iac/define/``: update CloudFormation stack definition module.
    - ``./${python_package_name}/iac/deploy.py``: update CloudFormation stack deployment module.
    - ``./${python_package_name}/iac/output.py``: update CloudFormation stack output value adaptor.
3. Test your infrastructure-as-code without deployment, run this script ``./tests/iac/test_define.py``.

Code Review:

4. Push your ``cf/${description}`` branch to git, and create a PR from ``cf/${description}`` to ``main``. The CI will deploy CloudFormation to ``dev`` environment.
5. Make sure the CloudFormation deployment succeeded in the CI before asking for code review.
6. Ask peers for code review and make changes when necessary.
7. Merge PR and delete the branch. This merge will not trigger any build.


4. 📦 Publish Lambda Function Dependency Layer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Development:

1. Create a ``layer/${description}`` branch from ``main``.
2. Update the ``[tool.poetry.dependencies]`` in ``pyproject.toml`` and run ``make poetry-lock`` to resolve the dependencies tree.

Code Review:

3. Push your ``layer/${description}`` branch to git, and create a PR from ``cf/${description}`` to ``main``. The CI will build and publish a new Lambda Layer version.
4. Make sure the Lambda Layer deployment succeeded in the CI before asking for code review.
5. Ask peers for code review and make changes when necessary.
6. Merge PR and delete the branch. This merge will not trigger any build.


5. 💻 Lambda Function Application Code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Development:

1. Create a ``lambda/${description}`` branch from ``main``.
2. Update the following files according to your business requirement. Ensure the unit test passed.
    - ``./${python_package_name}/lbd/``: lambda function application logic implementation.
    - ``./tests/lbd/``: lambda function application logic unit test.
3. Prepare for lambda deployment to ``dev``, update the following files, make sure ``update_chalice_config.py`` is working properly:
    - ``./lambda_app/update_chalice_config.py``: lambda function deployment configs, check lambda layer version, function name, environment variables, etc ...
    - ``./lambda_app/app.py``: lambda function handler definition.

Deploy to ``dev`` so you can develop integration test code:

 and run integration test on ``dev``

4. Push your ``lambda/${description}`` branch to git, and create a PR from ``lambda/${description}`` to ``main``. The CI will deploy Lambda Function to ``dev`` environment.
5. Once Lambda Functions are deployed to ``dev``, update the integration test cases in ``./tests_int/lbd/``, make sure it it passed. Copy the console output, you will need this later in code review.

Code Review:

6. Paste the integration test console output to the code review.
7. Ask peers for code review and make changes when necessary.
8. Merge PR and delete the branch. This merge will not trigger any build.


6. 🧪 Integration Test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This should be the final step before the release process. If the integration test failed, don't fix it on ``int/${description}`` branch, repeat the "Lambda Function Application Code" process and fix the integration test in ``dev``.

Development:

1. Create a ``int/${description}`` branch from ``main``.
2. Update the ``./chore.txt`` file, enter any value, so the change can trigger build job in CI.

Code Review:

3. Push your ``int/${description}`` branch to git, and create a PR from ``int/${description}`` to ``main``. The CI will do the following works:
    - run unit test in ``int`` environment.
    - deploy CloudFormation to ``int`` environment.
    - deploy Lambda Function to ``int`` environment.
    - run integration test in ``int`` environment.
4. Ask peers for code review and make changes when necessary.
5. Merge PR and delete the branch. This merge will not trigger any build.


7. 🚀 Release to Production
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Make sure you just did a "Integration Test", and the current ``main`` is the merged commit from the "Integration Test" step.
2. Create a ``release/${version}`` branch from the ``main`` branch.
3. Bump up version in ``./${python_package_name}/._version.py`` and ``./pyproject.toml``, follow the `semantic versioning <https://semver.org/>`_ convention. Usually, if it is a feature release, then bump up minor version; if it is a hot fix release, then bump up micro version.
4. Push your ``release`` branch to git, and create a PR from ``release/${version}`` to ``main``. The CI will deploy everything to ``prod`` environment.
5. When the deployment succeeded, Create a git tag that equals to the ``${version}`` from the current commit.
6. Merge PR and delete the branch.

If the deployment failed:

1. If the deployment failed completely, nothing in ``prod`` got changed, then you should delete this ``release/${description}``, branch and repeat this SDLC, check what went wrong.
2. If the deployment partially succeeded, some resources in ``prod`` got changed changed, follow the "Rollback to a Historical Version" section to rollback.


8. 🔥 Rollback to a Historical Version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Check out the code based on the git tag that equal to the historical version.
2. Rollback the prod parameter to the historical config data.
3. Create a ``release/${version}`` branch from that git tag commit. The ``${version}`` should be equal to the historical version.
4. Push your ``release`` branch to git, and create a PR from ``release/${version}`` to ``main``. The CI will deploy everything to ``prod`` environment.
5. When the deployment succeeded, delete the branch and the PR, and ❗ **DON't MERGE!!**


9. 🗑 Delete Deployment, Clean up AWS Resources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Create a ``cleanup/${env_name}`` branch from the ``main`` branch.
2. Update the ``./chore.txt`` file, enter any value, so the change can trigger build job in CI. Ensure that the commit message following this convention ``cf, lbd: ${description}`` or ``lbd: ${description}``. The branch name tells the CI which environment to delete, and the commit message tells the CI what resources to remove. If the commit message doesn't meet the requirements, then CI build will do nothing.
3. Push your ``cleanup/${env_name}`` branch to git, and create a PR from ``cleanup/${env_name}`` to ``main``. The CI will delete everything from the given ``${env_name}`` environment.
4. When the deletion succeeded, delete the branch and the PR, and ❗ **DON't MERGE!!**
