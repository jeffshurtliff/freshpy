##########
Change Log
##########
This page documents the additions, changes, fixes, deprecations and removals made in each release.

******
v2.0.0
******
**Release Date: TBD**

Added
=====

Core Object
-----------
Additions to the :doc:`core-object-methods`.

* Added the :py:class:`freshpy.core.FreshPy.Agents` class with the following methods:
    * :py:meth:`freshpy.core.FreshPy.Agents.get_user_info`
    * :py:meth:`freshpy.core.FreshPy.Agents.get_all_agents`

Primary Modules
---------------
Additions to the :doc:`primary modules <primary-modules>`.

* Added the :py:mod:`freshpy.agents` with the following functions:
    * :py:func:`freshpy.agents.get_user_info`
    * :py:func:`freshpy.agents.get_all_agents`

Supporting Modules
------------------
Additions to the :doc:`supporting modules <supporting-modules>`.

* Added the :py:class:`freshpy.errors.exceptions.InvalidFilterError` exception.

Changed
=======

Primary Modules
---------------
Changes to the :doc:`primary modules <primary-modules>`.

* Added error handling to the :py:func:`freshpy.api.get_request_with_retries` function.
* Replaced a generic py:exc:`Exception` with a py:exc:`RuntimeError` exception in the
  py:func:`freshpy.api._report_failed_attempt` function.

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


