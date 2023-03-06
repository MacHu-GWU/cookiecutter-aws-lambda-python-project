Infrastructure as Code
==============================================================================
Infrastructure as Code (IAC) is the managing and provisioning of infrastructure through code instead of through manual processes. It is a critical piece for building applications on cloud. There are lots of IAC tools, such as `terraform <https://www.terraform.io/>`_, `pulumi <https://www.pulumi.com/>`_, `CloudFormation <https://aws.amazon.com/cloudformation/>`_, etc ... You can use any of them that you feel most comfortable with. In this project, for demonstration purpose, we will use CloudFormation. But the concepts and best practices are the same for all of them.


Break down the infrastructure into modules
------------------------------------------------------------------------------
In this example, we have an ``iac`` module that implements the IAC. It has three sub-modules. ``define`` module declared all the infrastructure in code, and break down the IAC definition into modules when it is large. ``output.py`` module declared the adaptor to access the IAC output. And the ``deploy.py`` module implements the IAC deployment script::

    .../iac
    .../iac/define/
    .../iac/define/main.py
    .../iac/define/iam.py
    .../iac/output.py
    .../iac/deploy.py

The ``main.py`` is a module to choose what IAC module you want to includes. It just import other IAC modules.

.. literalinclude:: ../../../aws_lambda_python_example-project/iac/define/main.py
   :language: python

The ``iam.py`` is a IAC module that includes the AWS IAM related resources. Of course you can have more IAC modules like this. I personally use `cottonformation <https://pypi.org/project/cottonformation/>`_, a Pythonic IAC tools. Please feel free to use any other tools.

.. literalinclude:: ../../../aws_lambda_python_example-project/iac/define/iam.py
   :language: python

The ``output.py`` module provides a simple and straightforward way to programmatically access the CloudFormation stack output values.

.. literalinclude:: ../../../aws_lambda_python_example-project/iac/output.py
   :language: python

The ``deploy.py`` module is a wrapper of the native deployment API. It implements the core logic that can be reused by the CI/CD shell scripts

.. literalinclude:: ../../../aws_lambda_python_example-project/iac/deploy.py
   :language: python

Again, I use ``cottonformation``, this is the example deployment logs from my CI build::

    +----- ⏱ 🚀 🐑 Deploy CloudFormation Stack ------------------------------------+
    🐑
    open cloudformation console for status: https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks?filteringStatus=active&filteringText=aws_lambda_python_example-dev&viewNested=true&hideStacks=false&stackId=
    ============== Deploy stack: aws_lambda_python_example-dev ==============
      preview stack in AWS CloudFormation console: https://console.aws.amazon.com/cloudformation/home?#/stacks?filteringStatus=active&filteringText=aws_lambda_python_example-dev&viewNested=true&hideStacks=false
      upload template to s3://111122223333-us-east-1-artifacts/projects/aws_lambda_python_example/cloudformation/templates/a8992bbc770b11edc09a6a406b45385e.json ...
        preview at https://console.aws.amazon.com/s3/object/111122223333-us-east-1-artifacts?prefix=projects/aws_lambda_python_example/cloudformation/templates/a8992bbc770b11edc09a6a406b45385e.json
      preview change set details at: https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/changesets/changes?stackId=arn:aws:cloudformation:us-east-1:111122223333:stack/aws_lambda_python_example-dev/1f97ce30-b6bd-11ed-8c9e-0ac70d5d88bf&changeSetId=arn:aws:cloudformation:us-east-1:111122223333:changeSet/aws_lambda_python_example-dev-2023-02-27-16-38-11-129/b3bb8c3e-e0ee-467e-a6e8-a5f253e47a4e
      wait for change set creation to finish ...
    
        on 1 th attempt, elapsed 5 seconds, remain 115 seconds ...
        reached status CREATE_COMPLETE
                    >>> Change for stack aws_lambda_python_example-dev <<<
    stack id = arn:aws:cloudformation:us-east-1:111122223333:stack/aws_lambda_python_example-dev/1f97ce30-b6bd-11ed-8c9e-0ac70d5d88bf
    change set id = arn:aws:cloudformation:us-east-1:111122223333:changeSet/aws_lambda_python_example-dev-2023-02-27-16-38-11-129/b3bb8c3e-e0ee-467e-a6e8-a5f253e47a4e
    +---------------------------- Change Set Statistics -----------------------------
    | 🟢 Add        2 Resources
    |
    +--------------------------------------------------------------------------------
    +----------------------------------- Changes ------------------------------------
    | 🟢 📦 Add Resource:        IamInlinePolicyForLambda                 AWS::IAM::Policy
    | 🟢 📦 Add Resource:        IamRoleForLambda                         AWS::IAM::Role
    |
    +--------------------------------------------------------------------------------
        need to execute the change set to apply those changes.
      preview create stack progress at: https://us-east-1.console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/stackinfo?filteringText=aws_lambda_python_example-dev&viewNested=true&hideStacks=false&stackId=arn:aws:cloudformation:us-east-1:111122223333:stack/aws_lambda_python_example-dev/1f97ce30-b6bd-11ed-8c9e-0ac70d5d88bf&filteringStatus=active
     wait for deploy to finish ...
    
        on 1 th attempt, elapsed 5 seconds, remain 115 seconds ...
        on 2 th attempt, elapsed 10 seconds, remain 110 seconds ...
        on 3 th attempt, elapsed 15 seconds, remain 105 seconds ...
        on 4 th attempt, elapsed 20 seconds, remain 100 seconds ...
        reached status 🟢 'CREATE_COMPLETE'
      done
    🐑 ✅ Deploy CloudFormation stack succeeded!
    🐑 
    +----- ⏰ 🚀 🐑 End 'Deploy CloudFormation Stack', elapsed = 56.83 sec ---------+

If you are interested in how to use this framework to work with other IAC tools, please submit an `issue <https://github.com/MacHu-GWU/cookiecutter-aws-lambda-python-project/issues>`_ to ask the `Author <https://github.com/MacHu-GWU>`_.
