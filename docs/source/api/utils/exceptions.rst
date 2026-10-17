.. _api_utils_exceptions:

==========
Exceptions
==========

.. currentmodule:: sds.utils

The structure modules raise the exceptions of :doc:`../core/exceptions`.
``sds.utils`` adds only the errors of its own tooling, all deriving from
:class:`~sds.core.exceptions.DataStructureError`. Today there is one: the
error raised when a feature needs an extra that is not installed.

Exception Hierarchy
===================

.. mermaid::

   graph TD
       A[Exception] --> B[DataStructureError]
       A --> I[ImportError]
       B --> O[OptionalDependencyError]
       I --> O

       style A fill:#f9f,stroke:#333
       style B fill:#bbf,stroke:#333
       style I fill:#fdd,stroke:#333
       style O fill:#bfb,stroke:#333

``OptionalDependencyError`` has two parents, and each one serves a
different reader:

* as a ``DataStructureError``, it is caught by the same
  ``except DataStructureError`` clause as every other error the library
  reports;
* as an ``ImportError``, it is caught by code that already guards optional
  imports, and its ``name`` attribute holds the missing package, as for any
  failed import.

OptionalDependencyError
=======================

.. autoclass:: OptionalDependencyError
   :members:
   :show-inheritance:

Attributes
----------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Attribute
     - Value
   * - ``package``
     - Importable name of the missing package, such as ``"matplotlib"``
   * - ``extra``
     - Extra of ``pysds-tools`` that installs it, such as ``"image"``
   * - ``name``
     - Same as ``package``; the attribute ``ImportError`` defines
   * - ``message``
     - The full message, ending with the ``pip install`` command

Usage Example
=============

Offer the image only when it can be produced, and fall back on text:

.. code-block:: python

   from sds.tree import AVLTree
   from sds.utils import OptionalDependencyError
   from sds.utils.visualizer import save_image, to_text

   tree = AVLTree()
   for key in (40, 20, 60, 10, 30):
       tree.insert(key)

   try:
       save_image(tree, "tree.png")
   except OptionalDependencyError as err:
       print(f"No image ({err.package} missing), text instead:")
       print(to_text(tree))

The error is raised when the feature is *called*: importing
``sds.utils.visualizer`` always succeeds, with or without matplotlib.

Best Practices
==============

✅ Catch ``OptionalDependencyError`` around the call that needs the extra,
not around the import: the import never fails.

✅ Show ``str(err)`` to the user: it names the command that fixes the
problem.

❌ Do not catch a bare ``ImportError`` to detect a missing extra: a broken
install of the package itself (one of *its* dependencies missing) raises a
plain ``ModuleNotFoundError``, which should not be mistaken for an extra
to install.
