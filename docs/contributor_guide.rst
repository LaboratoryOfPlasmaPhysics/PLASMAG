Contributor Guide
=================

It is possible to contribute to PLASMAG at different levels: whether you have to report a bug, help
fixing it, improve the documentation or add a new feature, it will still be a useful
contribution.

If reporting a bug is easily done through our Github issue page [#issuePage]_, it still required
some context elements like:

- your version of PLASMAG
- your operating system (type and version)
- your python installation (from one of the \*_environment.yml file or manually installed)
- what where you trying to do (steps)
- what happened that was not expected

For the other ways to contribute, please read the section
:ref:`Contributor Workflow <Contributor Workflow>` before reading the one that concerns the
contribution itself.

.. rubric:: Footnotes

.. [#issuePage] https://github.com/LaboratoryOfPlasmaPhysics/PLASMAG/issues


Contributor Workflow
--------------------

The contributing workflow is intended to be:

0. Check in the online documentation and the the GitHub repository if what you want isn't already
   implemented (see *Reviewing existing assets* sub-section to learn where to search)
#. Fork the github repository
#. Clone your fork
#. Create a development virtual environment using contributor_environment.yml prerequisites file
#. Create a new branch for your contribution (see *Git guidelines* sub-section)
#. Fix, add or whatever you wanted to do
#. Check the code quality and compliance to the project standards (see *linting* sub-section)
#. Update the documentation according to your changes (see *Documentation* sub-section)
#. Commit your changes in your fork (see *Git guidelines* sub-section)
#. Create a pull request

Please try to:

- keep your pull requests small and focused on a single feature or bug fix to facilitate the review
  process.
- ensure your contributions follow the project’s coding standards and guidelines.
- regularly update your fork to keep it in sync with the main project. This helps in minimizing
  merge conflicts.

By following these guidelines, you contribute to the efficiency and
clarity of the project, making it easier for others to review your
contributions and maintain the project’s health.


Reviewing existing assets
^^^^^^^^^^^^^^^^^^^^^^^^^

1. Review Existing Strategies: Inspect all the calculation strategies in
   the calculation_strategies folder to ensure your strategy hasn’t
   already been implemented. All the strategies are located in the
   ``src/model/strategies/strategy_lib/`` folder.
2. Review Parameters: Examine the parameters defined in
   ``/data/default.json``. Determine if new parameters are needed for
   your strategy.

Linting
^^^^^^^

We use pylint to ensure compliance with PEP8 guidelines. Lint your code
with:

.. code:: bash

    pylint --rcfile pylintrc src/folder/file.py

Replace ``src/folder/file.py`` with the path to the file you want to
lint. Check the return of the command to see if there are any errors or
warnings in the code. Adapt and correct the code according to the pylint
output.

You can read the `pylint
documentation <https://pylint.pycqa.org/en/latest/>`__ for more
information on how to use pylint.

Documentation
^^^^^^^^^^^^^

Depending on what you modified in the code, you may need to:

- update docstrings (changes in parameters, behaviour...) in the python files
- update the description of a feature in the user guide
- add a new module in the API reference guide
- ...

Once you have made all your modification in the documentation, make sure that it compiles well and
that your changes render as expected.

To test the compilation on your computer go to the *docs* folder and run ::

   make html

then open in a webbrowser the file *_build/html/index.html* and check the result.

Don't forget to commit your changes to documentation

Git Guidelines
^^^^^^^^^^^^^^

To maintain the repository’s integrity and streamline development
processes, we adhere to a GitFlow-inspired workflow and specific naming
conventions for branches and commit messages. Below is a comprehensive
guide on how to contribute code to this project effectively.

Branching Strategy
~~~~~~~~~~~~~~~~~~

We use a branching strategy that categorizes work based on the nature of
changes, ensuring that our repository remains organized and manageable.
When starting work on a new feature, bug fix, or other tasks, you must
create a new branch following these conventions:

- **Feature Branches**: ``engine/branch-name``, ``UI/branch-name``,
   ``controller/branch-name``
- **Module Branches**: ``model/physical-quantity-name``, ``SPICE/branch-name``, ``OPTI/branch-name``
- **Refactoring**: ``refactor/branch-name``

**Important**: Direct commits to the ``dev`` branch are not recommended.
Try to create a new branch for your work, branching off from the latest
``dev`` branch.

Commit Message Format
~~~~~~~~~~~~~~~~~~~~~

Commit messages should be clear, concise, and follow a formal structure
to simplify the repository’s history. Use the following format:

::

   TYPE[TAG] - DESCRIPTION

   [optional body]

   [optional footer(s)]

**Tags**: Include ``#issue_id`` if your work addresses a specific open
issue.

The recommended types are:

- ``FEAT``: Introduces a new feature.
- ``FIX``: Fixes a bug.
- ``CORE``: Changes that don’t affect the source or test files, like
  updating dependencies.
- ``REFACTOR``: Code changes that neither fix a bug nor add a feature.
- ``DOC``: Documentation updates.
- ``QUAL``: General code quality improvements.
- ``TEST``: Adds or updates tests.
- ``PERF``: Performance improvements.
- ``REVERT``: Reverts a previous commit.

For more detailed examples and best practices on commit messages, refer
to `this
article <https://www.freecodecamp.org/news/how-to-write-better-git-commit-messages/>`__.

Fixing bugs
-----------

Improving documentation
-----------------------

.. .. _contributing new code:

Contributing new code
---------------------

Improving the analytical model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _adding new physical quantity:

adding a new physical quantity as input of the model (no computing strategy)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The parameters asked to the user are listed in the *default.json* file.
Each parameter must be added to a section like this::

   { "<section_name>":
     {
       "<param_name>": {
         "default": <default numerical value>,
         "min": <minimum numerical value>,
         "max": <maximum numerical value>,
         "description": "<Short description, displayed in tooltip>",
         "input_unit": "<unit used in the user interface>",
         "target_unit": "<unit used in equations>"
       }
     }
   }

where:

- section_name and param_name are the names used in the user interface
- default, min and max numerical values are given in the unit described in “input_unit”.

Note that PLASMAG is using the `Pint library <https://pint.readthedocs.io/en/stable/index.html>`__
to deal with unit conversion. So don't hesitate to
choose the most readable unit for "input_unit".
For dimensionless parameters, you can either let the units to "" or set it to "dimensionless".

.. _adding new strategy:

adding a new strategy to an existing physical quantity (Node)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each strategy of a node is a class in a python module. To add a new strategy to an existing node,
you just have to add a new class to it's module and add the name of the new class to the list of
strategies of this node in ``scm_model.py``.

Here is an example of a strategy class::

   class MyNewFooCalculationStrategy(CalculationStrategy):
       """ Analytical model for Foo

       .. math::

           Foo(f) = dep_1 . param_1

       With:
           - :math:`dep_1` : <short description of the variable>
           - :math:`param_1` : <short description of the parameter>

       """
       def calculate(self, dependencies, parameters):
           # retrieve user's parameters
           param1 = parameters.data["param1"]

           # retrieve values from other nodes
           frequency_vector = dependencies["frequency_vector"]["data"]
           dep1 = dependencies["dependency1"]["data"][:, 1]

           # Custom calculation logic here
           result = dep1 * param1

           # results must be returned as a tensor if the quantity depends on another one
           results = column_stack((frequency_vector, result))

           # the return format is a dictionary with the numerical results stored in "data", the
           # labels and units used for plot legend.
           return {
               "data": results,
               "labels": ["Frequency", "myFoo"],
               "units": ["Hz", "<Foo unit>"]
           }

       @staticmethod
       def get_dependencies():
           # this methode must return the list of user parameters and node values used as input to
           # the strategy calculation
           return ["dependency1", "frequency_vector", "param1"]

In this example, the calculation uses the user parameter *param1* and the result of the calculation
of the node *dependency1* along with the *frequency_vector*. The three inputs of this calculation
need to be listed in the *get_dependencies* return list.

The calculate method must return a dictionary containing the values of the physical quantity in
"data" (it must be a tensor if your physical quantity varies with time or frequency),
the plot labels and the units in the "labels" and "units" lists (even if your physical quantity
is static).

.. note:: Don't forget to document your new strategy and to add it to ``user_guide.rst`` and to the API reference.

Once your strategy is written, you have to add it to the model (``scm_model.py``). First import it::

   from src.model.strategies.strategy_lib.MyFoo import MyFooCalculationStrategy, MyNewFooCalculationStrategy

Then add it to the strategy list for Foo (and decide if it should become the new default or not)::

       "myFoo": {
          "default": MyFooCalculationStrategy,
          "strategies": [MyFooCalculationStrategy, MyNewFooCalculationStrategy]
       },


adding a new computable physical quantity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you understand the steps of :ref:`adding new physical quantity` and of
:ref:`adding new strategy`, adding a new computable physical quantity is quite easy:

#. create a new module in *src/model/strategies/strategy_lib* for your new node
#. implement one or more strategies for it
#. add new user parameters if needed
#. add your new node and its strategies to the model (``scm_model.py``)


Improving the SPICE feature
^^^^^^^^^^^^^^^^^^^^^^^^^^^

adding a new strategy to an existing circuit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

adding a new circuit
~~~~~~~~~~~~~~~~~~~~
