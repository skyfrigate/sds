.. SDS-Tools documentation master file

Welcome to SDS-Tools Documentation!
====================================

About This Project
------------------

This package was designed to revisit fundamental algorithms through the implementation
of basic data structures: linear structures, trees, and graphs. The project also serves
as a practical exploration of static code analysis techniques using AI-assisted development.

**SDS-Tools** (Simple Data Structures) is a comprehensive Python library providing
educational and production-ready implementations of advanced data structures not
available in the standard library.

This library implements a wide range of data structures including:

* **Linear structures**: Stack, Queue, Deque, Priority Queue, Linked Lists
* **Tree structures**: Binary Trees, BST, AVL, Red-Black Trees, Heaps, B-Trees, Tries
* **Graph structures**: Directed/Undirected Graphs, Weighted Graphs, Adjacency representations
* **Advanced structures**: Union-Find, Bloom Filters, Skip Lists, Hash Tables

.. note::
   This documentation is available in multiple languages and versions.

   * Current version: |version|
   * Current language: English (also available in French)
   * Project started: 2019
   * Authors: skyfrigate & biface

Quick Start
-----------

Installation
~~~~~~~~~~~~

.. code-block:: bash

    pip install sds-tools

Basic usage example:

.. code-block:: python

    from sds.linear import Stack

    # Create a stack
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)

    # Pop elements
    print(stack.pop())  # Output: 3

Features
--------

✓ **Type-safe implementations** with proper abstractions

✓ **Comprehensive test coverage**

✓ **NumPy-style docstrings** for clear documentation

✓ **Performance-optimized** algorithms

✓ **Educational and production-ready**

✓ **Python 3.10+** support

✓ **AI-assisted development** for code quality analysis

Documentation Structure
-----------------------

This documentation is organized into several sections:

**User Guide**
   Step-by-step guides for using the library, with theoretical background,
   algorithmic descriptions, and practical examples. Includes a comprehensive
   class hierarchy diagram showing the relationships between all data structures.

**API Reference**
   Complete technical documentation auto-generated from source code docstrings.
   Organized by module family (core, linear, tree, graphs, advanced, algorithms).

**Changelog**
   Version history with features, improvements, and deprecations.

.. toctree::
   :maxdepth: 2
   :caption: User Guide
   :name: user-guide

   guide/index
   guide/getting_started
   guide/installation

.. toctree::
   :maxdepth: 2
   :caption: Data Structures
   :name: structures

   guide/linear_structures/index
   guide/tree_structures/index
   guide/graph_structures/index
   guide/advanced_structures/index

.. toctree::
   :maxdepth: 3
   :caption: API Reference
   :name: api-reference

   api/index
   api/core/index
   api/linear/index
   api/tree/index
   api/graph/index
   api/advanced/index
   api/algorithms/index
   api/utils/index

.. toctree::
   :maxdepth: 1
   :caption: Development
   :name: development

   changelog/index
   contributing
   license

.. toctree::
   :maxdepth: 1
   :caption: Documentation tools
   :name: tools

   indices

About the Project
=================

**SDS-Tools** has been developed since 2019 by skyfrigate and biface as an
educational project to explore fundamental data structures and algorithms.
The project emphasizes:

* **Clear, well-documented implementations** following NumPy docstring conventions
* **Comprehensive test coverage** ensuring reliability
* **Modern Python practices** with type hints and proper abstractions
* **AI-assisted development** for exploring static code analysis techniques

The project serves both as a learning resource for understanding data structures
and as a practical library for production use.

Support
=======

* **Documentation**: https://sds-tools.readthedocs.io
* **Source Code**: https://github.com/skyfrigate/sds
* **Issue Tracker**: https://github.com/skyfrigate/sds/issues
* **Discussions**: https://github.com/skyfrigate/sds/discussions

License
=======

This project is licensed under the Apache License 2.0 - see the :doc:`license` file for details.

Copyright 2019-2024 skyfrigate & biface

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.