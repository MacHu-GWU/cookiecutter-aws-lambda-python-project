Semantic Git Branching
==============================================================================


Summary
------------------------------------------------------------------------------
In this project, we follow the semantic git branching convention. We use different branch name for different purpose, also the CI system will use branch name to identify what to run and what not to run.

- ``main`` branch:
    - usage: for deployment to integration test environment and run integration test
    - name pattern: exactly equal to ``main`` or ``master``
- ``feature`` branch:
    - usage: for feature deployment or bug fix
    - name pattern: starts with ``feat`` or ``feature``
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


Workflow
------------------------------------------------------------------------------
.. contents::
    :class: this-will-duplicate-information-and-it-is-still-useful-here
    :depth: 1
    :local:


Feature development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
I want to develop a new feature, the code change should not break the unit test and maintain decent code coverage.

1. Create a ``feat/${description}`` branch from ``main``.
2. Develop the source code and add unit test cases.
3. Make sure the unit test passed on your local and you have decent code coverage.
4. Push your ``feature`` branch to git, and create a PR from ``feat/${description}`` to ``main``. The CI will test your code in ``dev`` environment.
5. Make sure the unit test passed in the CI before you ask for code review.
6. Ask peers for code review and make changes when necessary.
7. Merge PR and delete the branch. The merge will not trigger any build.


Deploy CloudFormation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
I want to make change to the infrastructure. For example, I want to add a IAM Policy permission to the Lambda Function IAM Role.

1. Create a ``cf/${description}`` branch from ``main``.
2. Develop the infrastructure as code script locally and test your code without deployment.
3. Push your ``cf`` branch to git, and create a PR from ``cf/${description}`` to ``main``. The CI will deploy CloudFormation to ``dev`` environment.
4. Make sure the CloudFormation deployment succeeded in the CI before asking for code review.
5. Ask peers for code review and make changes when necessary.
6. Merge PR and delete the branch. PR merge event from ``cf`` branch to ``main`` branch will trigger a CloudFormation deployment to ``int``.


Deploy Lambda Layer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
I want to publish a new Lambda dependency Layer.

1. Create a ``layer/${description}`` branch from ``main``.
2. Update the ``pyproject.toml`` and run ``make poetry-lock`` to resolve the dependencies tree.
3. Push your ``layer`` branch to git, and create a PR from ``cf/${description}`` to ``main``. The CI will build and publish a new Lambda Layer version.
4. Make sure the Lambda Layer deployment succeeded in the CI before asking for code review.
5. Ask peers for code review and make changes when necessary.
6. Merge PR and delete the branch. The merge will not trigger any build.


Deploy Lambda Function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
I want to test the Lambda Function deployment and do integration test. This work should not make many core logic changes, it should be done in ``feature`` branch already. This work should only focus on the deployment related code.

1. Create a ``lambda/${description}`` branch from ``main``.
2. Update the code in ``{{ cookiecutter.package_name }}/lbd/`` and ``lambda_app/``.
3. Use the ``make deploy-lambda`` command to deploy the lambda to ``dev`` environment.
4. Test the lambda function in integration test locally on ``dev`` environment.
5. Push your ``lambda`` branch to git, and create a PR from ``lambda/${description}`` to ``main``. The CI will deploy Lambda Function to ``dev`` environment and run integration test on ``dev``.
6. Make sure the integration test passed in CI with ``dev`` before asking for code review.
7. Ask peers for code review and make changes when necessary.
8. Merge PR and delete the branch. PR merge event from ``cf`` branch to ``main`` branch will trigger a Lambda Function deployment to ``int`` and run integration test on ``int``.


Release to Prod
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
I want to release a version to production environment.

1. Make sure the current commit of the ``main`` is the merged commit of a ``Deploy Lambda Function`` process. If it is not, repeat ``Deploy Lambda Function`` process to ensure the Lambda Function deployment succeeded and integration test is passed.
2. Create a ``release/${version}`` branch from the ``main`` branch, you should ONLY update the ``chore.txt`` file or the ``config.json`` value on release branch. Don't make any change to the source code. If you really need to change the source code, repeat the ``Deploy Lambda Function`` and cherry pick those changes from the ``main`` branch.
3. Push your ``release`` branch to git, and create a PR from ``release/${version}`` to ``main``. The CI will deploy everything including CloudFormation, Lambda Function to ``prod`` environment.
4. Create a git tag that equals to the ${version} from the current commit.
5. Merge PR and delete the branch.


Rollback to a Historical Version
------------------------------------------------------------------------------
1. Check out based on the git tag, the git tag should be equal to the historical semantic version.
2. Rollback the prod parameter to the historical config data.
3. Create a ``release/${version}`` branch from that git tag commit.
4. Push your ``release`` branch to git, and create a PR from ``release/${version}`` to ``main``. The CI will deploy everything including CloudFormation, Lambda Function to ``prod`` environment.
5. DON't MERGE!!
6. Once the deployment is finished, delete the branch and close the PR.


How to?
------------------------------------------------------------------------------
- Q: How to figure out the release date of a version?
- A: Check the creation time of the commit id for the git tag.

- Q: How to locate a historical config version?
- A: Search AWS Parameter Store using label with ``v${version}``, or you can go to ``config/`` s3 folder and locate the ``prod-v${version}.json`` file.
