Multi AWS Regions and Multi AWS Accounts Deployment
==============================================================================
Initially, a project is developed in one region and in one AWS account. However, we also plan to deploy this solution to other AWS regions and accounts in the future. To enable this, we have created a Python module named ``boto_ses.py``, which defines a variable ``bsm`` (short for "boto session manager") that uses the ``us-east-1`` region and the AWS CLI profile of the POC AWS account. All of the deployment scripts import this module and use ``bsm`` for deployment. This allows us to easily deploy the solution to any new region and account by simply changing the ``profile_name`` and ``region_name`` arguments.

.. literalinclude:: ../../../aws_lambda_python_example-project/aws_lambda_python_example/boto_ses.py
   :language: python
