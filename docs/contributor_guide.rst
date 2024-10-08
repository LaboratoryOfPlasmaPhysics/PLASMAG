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

Contributing new code
---------------------

Improving the analytical model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

adding a new physical quantity as input of the model (no computing strategy)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

adding a new strategy to an existing physical quantity (Node)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

adding a new computable physical quantity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Improving the SPICE feature
^^^^^^^^^^^^^^^^^^^^^^^^^^^

adding a new strategy to an existing circuit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

adding a new circuit
~~~~~~~~~~~~~~~~~~~~
