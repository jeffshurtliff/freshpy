##########
Change Log
##########
This page documents the additions, changes, fixes, deprecations and removals made in each release.

***********
v3.0.0.dev0
***********
**Release Date: TBD**

Added
=====

Core Object
-----------
Additions to the :doc:`core-object-methods`.

* Added the :py:meth:`freshpy.core.FreshPy.Tickets.get_ticket_fields` method
* Added the :py:class:`freshpy.core.FreshPy.Workspaces` inner class with the following methods:
    * :py:meth:`freshpy.core.FreshPy.Workspaces.get_workspace`
    * :py:meth:`freshpy.core.FreshPy.Workspaces.get_all_workspaces`
* Added the :py:meth:`freshpy.core.FreshPy._import_workspaces_class` method

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:func:`freshpy.tickets.get_ticket_fields` function
* Added the :py:mod:`freshpy.workspaces` module with the following functions:
    * :py:func:`freshpy.workspaces.get_workspace`
    * :py:func:`freshpy.workspaces.get_all_workspaces`

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>` are listed below.

* Added the following new test modules:
    * :py:mod:`freshpy.utils.tests.test_log_utils`
    * :py:mod:`freshpy.utils.tests.test_version_utils`
* Added the new :py:exc:`freshpy.errors.exceptions.InvalidDataTypeError` exception

General
-------
* Added the new ``.github/workflows/ci.yml`` CI workflow to follow best practices and improve deployments
* Added the ``.readthedocs.yaml`` file to manage the integration with the ReadTheDocs documentation
* Added the ``AGENTS.md`` file to define agent guidelines with the package

Changed
=======

Core Object
-----------
Changes to the :doc:`core-object-methods`.

* Improved and standardized the handling of SSL verification when performing API calls
    * Added the ``verify_ssl`` parameter to the object instantiation method (which defaults to ``True`` if not defined)
      which allows SSL verification to be enabled or disabled at the object-level
    * Added the :py:meth:`freshpy.core.FreshPy._determine_ssl_verification` method and called it in relevant
      core object methods to determine the appropriate SSL verification setting
    * Changed the default value of the ``verify_ssl`` parameter in core methods to be ``None`` rather than ``True``
* Introduced the ability to utilize environment variables instead of passing in settings with parameters
    * Added the :py:meth:`freshpy.core.FreshPy._get_env_variable_names` method to get the environment variable names
    * Added...

Supporting Modules
------------------
Changes to the :doc:`supporting modules <supporting-modules>` are listed below.

* Completely refactored the :py:mod:`freshpy.utils.version` module to retrieve the version
  from the package metadata and using it to define the ``__version__`` special variable
* Updated the :py:mod:`freshpy.utils.log_utils` module to always define a default logging level
* Updated the :py:exc:`freshpy.errors.exceptions.MissingRequiredDataError` exception to allow a specific missing
  argument to be specified for the init message when applicable

General
-------
* Updated the ``pyproject.toml`` file to follow best practices and to include the following changes:
    * Changed the minimum supported Python version to be 3.9
    * Added hyperlinks to available resources and documentation
    * Added Trove classifiers for PyPI
    * Switched from ``setuptools`` to ``poetry``
    * Moved ``pytest`` to a dev dependency group
    * Removed ``setuptools`` and ``urllib3`` from runtime dependencies
    * Updated dependency versions to mitigate known vulnerabilities found in earlier versions
    * Added ``bandit`` with SARIF support to the dev dependencies
* Updated the ``requirements.txt`` file to be runtime-only and mirror the ``pyproject.toml`` file
* Moved the ``tests/`` directory from the root level to under ``src/freshpy/utils/`` instead
* Updated the Sphinx configuration (``docs/conf.py``) to follow recommendations and best practices

Removed
=======

General
-------
* Removed the ``setup.py`` file as it is no longer needed for this package
* Removed ``.github/workflows/codeql-analysis.yml`` (replaced by ``.github/workflows/ci.yml``)
* Removed the ``.readthedocs.yml`` file (replaced by ``.readthedocs.yaml``)

|

-----

******
v2.0.0
******
**Release Date: 2025-01-29**

Added
=====

Core Object
-----------
Additions to the :doc:`core-object-methods`.

* Added the :py:class:`freshpy.core.FreshPy.Agents` class with the following methods:
    * :py:meth:`freshpy.core.FreshPy.Agents.get_user_info`
    * :py:meth:`freshpy.core.FreshPy.Agents.get_all_agents`
    * :py:meth:`freshpy.core.FreshPy.Agents.get_agent_id`
    * :py:meth:`freshpy.core.FreshPy.Agents.get_assignment_history`

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:mod:`freshpy.agents` with the following functions:
    * :py:func:`freshpy.agents.get_user_info`
    * :py:func:`freshpy.agents.get_all_agents`
    * :py:func:`freshpy.agents.get_agent_id`
    * :py:func:`freshpy.agents.get_assignment_history`
    * :py:func:`freshpy.agents._get_user_info_by_email`

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:exc:`freshpy.errors.exceptions.InvalidFilterError` exception.

Changed
=======

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Added error handling to the :py:func:`freshpy.api.get_request_with_retries` function.
* Replaced a generic py:exc:`Exception` with a py:exc:`RuntimeError` exception in the
  py:func:`freshpy.api._report_failed_attempt` function.
* Removed an unnecessary ``return`` statement from the
  :py:func:`freshpy.api._report_failed_attempt` function.

|

-----

******
v1.1.1
******
**Release Date: 2023-05-08**

Changed
=======

General
-------
* Updated the required packages in the ``requirements.txt`` file.
* Adjusted the required install packages in the ``setup.py`` script.

|

-----

******
v1.1.0
******
**Release Date: 2021-01-05**

Added
=====

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:func:`freshpy.utils.version.get_major_minor_version` function.

Documentation
-------------
The documentation was fully created and hosted.

Changed
=======

Core Object
-----------
Changes to the :doc:`core-object-methods`.

* Added the ability to disable SSL verification on API calls in the following methods:
    * :py:meth:`freshpy.core.FreshPy.get`
    * :py:meth:`freshpy.core.FreshPy.Tickets.get_ticket`
    * :py:meth:`freshpy.core.FreshPy.Tickets.get_tickets`

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Added the ability to disable SSL verification on API calls in the following functions:
    * :py:func:`freshpy.api.get_request_with_retries`
    * :py:func:`freshpy.tickets.get_ticket`
    * :py:func:`freshpy.tickets.get_tickets`
