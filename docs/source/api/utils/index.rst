.. _api_utils:

=========================
Utilities (sds.utils)
=========================

.. currentmodule:: sds.utils

``sds.utils`` gathers the tooling built on top of the data structures:
presentation of a structure as text, diagram or image, and the errors of
that tooling. It holds what is neither algorithmic logic, which belongs to
:doc:`../algorithms/index`, nor part of a domain's own contract, which stays
with the classes of that domain.

Overview
========

.. important::

   **sds.utils is the top layer of the package.** It may import every
   structure module and ``sds.algorithms``; no structure module imports it.
   Each domain therefore loads, and works, without ``sds.utils``.

.. mermaid::

   graph TD
       U[sds.utils] --> A[sds.algorithms]
       U --> L[sds.linear]
       U --> T[sds.tree]
       U --> G[sds.graph]
       A --> L
       A --> T
       A --> G
       L --> C[sds.core]
       T --> C
       G --> C

       style U fill:#3498db,color:#fff
       style C fill:#95a5a6,color:#fff

An arrow reads "imports". The test suite checks the rule: it parses every
module outside ``sds.utils`` and fails if one of them imports it, even
from inside a function.

Optional Dependencies
=====================

The base install of ``pysds-tools`` has no dependency. Features that need a
third-party package get it through an **extra** of the distribution:

.. list-table::
   :header-rows: 1
   :widths: 15 25 60

   * - Extra
     - Installs
     - Needed by
   * - ``image``
     - matplotlib ≥ 3.10
     - :func:`sds.utils.visualizer.save_image`
   * - ``yaml``
     - PyYAML ≥ 6.0
     - reading YAML files with the ``pysds`` command

.. code-block:: bash

   pip install "pysds-tools[image]"        # one extra
   pip install "pysds-tools[image,yaml]"   # both

Importing a module never requires an extra. The package is imported only
when a feature that needs it is called; if it is missing, the call raises
:class:`~sds.utils.OptionalDependencyError`, whose message gives the
command to run.

Module Contents
===============

.. list-table::
   :header-rows: 1
   :widths: 25 45 30

   * - Module
     - Contents
     - Dependency
   * - :doc:`visualizer`
     - ``to_text``, ``to_mermaid``, ``to_dot``, ``render``,
       ``save_image``, ``FORMATS``
     - none (``save_image``: ``image`` extra)
   * - :doc:`exceptions`
     - ``OptionalDependencyError``
     - none

Detailed Documentation
======================

.. toctree::
   :maxdepth: 2

   visualizer
   exceptions

Related Pages
=============

* :doc:`../core/exceptions` - The exception hierarchy of the structures
* :doc:`../linear/convert` - Building linear structures from lists
