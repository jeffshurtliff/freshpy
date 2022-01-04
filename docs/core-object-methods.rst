###################
FreshPy Core Object
###################
This section provides details around the core module and the methods used
within the core object for the **freshpy** package, which are listed below.

* `Init Module (freshpy)`_
* `Core Module (freshpy.core)`_
    * `Core Functionality Subclasses (freshpy.core.FreshPy)`_
        * `Tickets Subclass (freshpy.core.FreshPy.Tickets)`_

|

*********************
Init Module (freshpy)
*********************
This module (being the primary ``__init__.py`` file for the library) provides a
"jumping-off-point" to initialize the primary :py:class:`freshpy.core.FreshPy` object.

.. automodule:: freshpy
   :members: FreshPy
   :special-members: __init__

:doc:`Return to Top <core-object-methods>`

|

**************************
Core Module (freshpy.core)
**************************
This module contains the core object and functions to establish the connection to the API
and leverage it to perform various actions.

.. automodule:: freshpy.core
   :members:
   :special-members: __init__

:doc:`Return to Top <core-object-methods>`

|

Core Functionality Subclasses (freshpy.core.FreshPy)
====================================================
These classes below are inner/nested classes within the core :py:class:`freshpy.core.FreshPy` class.

.. note:: The classes themselves are *PascalCase* format and singular (e.g. ``Node``, ``Category``, etc.) whereas
          the names used to call the inner class methods are all *lowercase* (or *snake_case*) and plural.
          (e.g. ``core_object.nodes.get_node_id()``, ``core_object.categories.get_category_id()``, etc.)

Tickets Subclass (freshpy.core.FreshPy.Tickets)
-----------------------------------------------
.. autoclass:: freshpy.core::FreshPy.Tickets
   :members:
   :noindex:

:doc:`Return to Top <core-object-methods>`

|
