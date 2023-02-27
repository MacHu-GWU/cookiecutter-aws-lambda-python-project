Python Development Workflow
==============================================================================


What and Why Development Workflow
------------------------------------------------------------------------------
In a Python project, the development workflow is usually as follows:

1. Create a virtual environment for the project.
2. Install dependencies.
3. Start development.
4. Write test cases.
5. Code Review.

Challenge 1 - Communication Burden without an Internal Standard:

    There are many different ways to do each of these steps. For example, people could use `.venv`, `venv`, `${project_name}_venv` as the virtualenv folder name, people could put the virtualenv folder at ``${project_root_dir}/.venv``, ``${project_root_dir}/venv``, ``${HOME}/venvs/${project_name}_venv``, ``${HOME}/apps/venvs/...``, ``${HOME}/apps/poetry/venvs/${project_name}-${random_hash}``. And the CLI command for those options are different. In enterprise projects, having too many options can increase the communication burden for collaboration.

Challenges 2 - Steep Learning Curve for New Team Members:

    Each step in the development workflow requires the developer to enter many CLI commands, some of which may have very long arguments that can be difficult to enter accurately. In addition, it is often necessary for developers to navigate to a specific directory in order to run the commands. This can be time-consuming, particularly for new team members who are onboarding the project, and it can also increase the risk of errors.

Having an internal standard for development workflow can reduce communication burden, improve productivity and reduce the risk of errors. The development workflow introduced in this tutorial is primarily based on my career experiences. I have been doing Python development since 2008 and actively maintaining around 20+ open source Python projects with total two millions monthly downloads, delivered 10+ commercial projects to production with around 5k ~ 10k line of code in average. This development workflow is primarily focus on AWS + Lambda + Python styled microservice project, and I cannot say that it is the best practice. But, I am pretty sure this is not the worst workflow.


THE recommended Development Workflow
------------------------------------------------------------------------------
First, let's install some dependencies for automation scripts. You need to install the following dependencies to your "User Python".

.. code-block:: bash

    pip3.8 install -r requirements-automation.txt

Now you can use ``make`` (MacOS and Linux has `GNU make <https://www.gnu.org/software/make/>`_ installed by default) command to show list of available action in this development workflow.

.. image:: ./images/make-command.png


Setup Python Virtual Environment
------------------------------------------------------------------------------
`Doing your development work in a virtual environment <https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment>`_ is must-have best practice.

First, you need to install


pip3.8 install "poetry>=1.2.0"
pip3.8 install -r requirements-automation.txt

make info
make venv-create
make install-all
source ./.venv/bin/activate
