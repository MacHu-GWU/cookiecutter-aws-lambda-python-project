Git Branching Strategy
==============================================================================
A common challenge is that the CI system may not have the capability to run a sequence of build jobs conditionally. For instance, we may not always want to build the Lambda layer, which can be both time-consuming and unnecessary. Similarly, we may not want to run integration tests for small feature improvements made through a simple pull request.

In this project, we follow the semantic git branching convention and used different branch names for different purposes. Additionally, the CI system relies on these branch names to identify what to run and what not to run.

Below is the detailed CI/CD build job workflow that runs only on specific Git branches. The column header is the semantic branch name, it follows the convention ``${semantic_name}/${description}``. For example, ``feature/add-an-awesome-feature`` is a feature branch. The row index is the workflow action.

.. raw:: html

    <style type="text/css">
    .tg  {border-collapse:collapse;border-spacing:0;}
    .tg td{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
      overflow:hidden;padding:10px 5px;word-break:normal;}
    .tg th{border-color:black;border-style:solid;border-width:1px;font-family:Arial, sans-serif;font-size:14px;
      font-weight:normal;overflow:hidden;padding:10px 5px;word-break:normal;}
    .tg .tg-c3ow{border-color:inherit;text-align:center;vertical-align:top}
    </style>
    <table class="tg">
    <thead>
      <tr>
        <th class="tg-c3ow">Action / Git Branch</th>
        <th class="tg-c3ow">feature</th>
        <th class="tg-c3ow">fix</th>
        <th class="tg-c3ow">cf</th>
        <th class="tg-c3ow">layer</th>
        <th class="tg-c3ow">lambda</th>
        <th class="tg-c3ow">int</th>
        <th class="tg-c3ow">release</th>
        <th class="tg-c3ow">cleanup</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="tg-c3ow">Create Virtualenv</td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
      </tr>
      <tr>
        <td class="tg-c3ow">Install Dependencies</td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
      </tr>
      <tr>
        <td class="tg-c3ow">Run Code Coverage Test</td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
      </tr>
      <tr>
        <td class="tg-c3ow">Deploy CloudFormation</td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
      </tr>
      <tr>
        <td class="tg-c3ow">Build New Lambda Layer Version</td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
      </tr>
      <tr>
        <td class="tg-c3ow">Deploy Lambda App</td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
      </tr>
      <tr>
        <td class="tg-c3ow">Run Integration Test</td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
      </tr>
      <tr>
        <td class="tg-c3ow">Backup Prod Config</td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
      </tr>
      <tr>
        <td class="tg-c3ow">Delete Lambda App</td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
      </tr>
      <tr>
        <td class="tg-c3ow">Delete CloudFormation</td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">❌</span></td>
        <td class="tg-c3ow"><span style="font-weight:var(--base-text-weight-normal, 400);font-style:normal">✅</span></td>
      </tr>
    </tbody>
    </table>

This is implemented in our DevOps shell scripts for all workflow actions to determine whether they should be run or not. Below is a sample code that demonstrates how we determine whether to deploy infrastructure via the CloudFormation stack:

.. code-block:: python

    def do_we_deploy_cf_in_ci(
        env_name: str,
        branch_name: str,
        is_cf_branch: bool,
        is_int_branch: bool,
        is_release_branch: bool,
    ) -> bool:
        if is_cf_branch or is_int_branch or is_release_branch:
            return True
        else:
            logger.info(
                f"{Emoji.red_circle} don't deploy CloudFormation. "
                f"in CI runtime, we only deploy CloudFormation from a "
                f"'cf' or 'int' or 'release' branch. "
                f"now it is {env_name!r} env and {branch_name!r} branch."
            )
            return False

Software development life cycles often involve multiple environments. For instance, a ``dev`` environment may be used to experiment with new features, an ``int`` environment may be used to perform end-to-end integration tests, and a ``prod`` environment may be used to deploy the application to production.

Humans are prone to making mistakes, the best practice is to avoid manually entering the environment to which we want to deploy. We have established a relationship between the Git branch and the deployment environment as below. The column header is the environment name, and the row index is the semantic branch name.

+-------------------+-----+-----+------+
| Git Branch👇 Env 👉 | dev | int | prod |
+===================+=====+=====+======+
|      feature      |  ✅  |     |      |
+-------------------+-----+-----+------+
|        fix        |  ✅  |     |      |
+-------------------+-----+-----+------+
|         cf        |  ✅  |     |      |
+-------------------+-----+-----+------+
|       layer       |  ✅  |     |      |
+-------------------+-----+-----+------+
|       lambda      |  ✅  |     |      |
+-------------------+-----+-----+------+
|        int        |     |  ✅  |      |
+-------------------+-----+-----+------+
|      release      |     |     |   ✅  |
+-------------------+-----+-----+------+
|    cleanup/dev    |  ✅  |     |      |
+-------------------+-----+-----+------+
|    cleanup/int    |     |  ✅  |      |
+-------------------+-----+-----+------+
|    cleanup/prod   |     |     |   ✅  |
+-------------------+-----+-----+------+

This is implemented in a Python function that uses a combination of runtime information (in CI or on a developer's laptop) and the Git branch name to automatically determine the appropriate deployment environment. This approach helps to reduce the chance of error. Additionally, the last if/else branch provides flexibility to force deployment to a hardcoded environment when necessary:

.. code-block:: python

    def find_env() -> str:
        if IS_CI: # if in CI runtime
            if (
                IS_FEATURE_BRANCH
                or IS_CF_BRANCH
                or IS_HIL_BRANCH
                or IS_LAYER_BRANCH
                or IS_LAMBDA_BRANCH
            ):
                return EnvEnum.dev.value
            elif IS_INT_BRANCH:
                return EnvEnum.int.value
            elif IS_RELEASE_BRANCH:
                return EnvEnum.prod.value
            elif IS_CLEAN_UP_BRANCH:
                parts = GIT_BRANCH_NAME.lower().split("/") # e.g. "cleanup/${env_name}/..."
                if len(parts) == 1:
                    raise ValueError(
                        f"Invalid cleanup branch name {GIT_BRANCH_NAME!r}! "
                        "Your branch name should be 'cleanup/${env_name}/...'."
                    )
                env_name = parts[1]
                if env_name not in EnvEnum._value2member_map_:
                    raise ValueError(
                        f"Invalid environment name {env_name!r}! "
                        "Your branch name should be 'cleanup/${env_name}/...'."
                    )
                return env_name
            else:
                raise NotImplementedError
        # if it is not in CI (on local laptop), it is always deploy to dev
        else:
            # you can uncomment this line to force to use certain env
            # from your local laptop to run automation, deployment script ...
            # return EnvEnum.dev.value
            return EnvEnum.dev.value
