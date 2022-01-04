##########
Change Log
##########
This page documents the additions, changes, fixes, deprecations and removals made in each release.

********
v1.1.0b1
********
**Release Date: TBD**

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


