.. _api_core:

======================
Core Module (sds.core)
======================

.. currentmodule:: sds.core

The core module provides fundamental abstractions and base classes used throughout
the SDS library. This includes abstract base classes for collections, nodes, and
common exceptions.

Overview
========

The core module establishes the foundational architecture:

* **Abstract base classes** for all data structures
* **Node abstractions** inherited by all specialized nodes
* **Exception hierarchy** for consistent error handling
* **Common interfaces** ensuring API consistency

Module Contents
===============

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   sds.core.node
   sds.core.interfaces
   sds.core.exceptions

Submodules
==========

.. toctree::
   :maxdepth: 2

   node
   interfaces
   exceptions

Related Documentation
=====================

* :doc:`../linear/index` - Linear structures using core abstractions
* :doc:`../tree/index` - Tree structures using core abstractions
* :doc:`../../guide/index` - User guides