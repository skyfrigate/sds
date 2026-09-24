.. _api_algorithms:

=================================
Algorithms (sds.algorithms)
=================================

.. currentmodule:: sds.algorithms

This module gathers the algorithmic logic of the library: sorting,
traversing, searching and optimizing. None of it lives inside the structure
classes. Every algorithm is a free function that receives the structure it
works on as a parameter.

Overview
========

.. important::

   **Structures and algorithms are kept apart.** A structure models a
   container and its relations; an algorithm computes something *from* a
   structure. Keeping them in separate modules means an algorithm can be
   read, tested and replaced without touching the structure, and one
   algorithm serves every structure that offers what it needs.

Each function types its structure parameter against the **broadest
abstract interface** that provides the capabilities the algorithm requires,
and only narrows it when no interface does. For instance, a graph traversal
accepts any ``AbstractGraph``, whatever its internal representation.

.. mermaid::

   graph LR
       subgraph "Structures"
       L[sds.linear]
       T[sds.tree]
       G[sds.graph]
       end

       subgraph "sds.algorithms"
       S[sorting]
       TA[tree_algorithms]
       GA[graph_algorithms]
       end

       L -- "to_list() / from_list()" --> S
       T -- "root, children()" --> TA
       G -- "neighbors(), outgoing_edges()" --> GA

       style S fill:#3498db,color:#fff
       style TA fill:#3498db,color:#fff
       style GA fill:#3498db,color:#fff

Module Contents
===============

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Subpackage
     - Contents
     - Operates on
   * - :doc:`sorting`
     - ``merge_sort``, ``quick_sort``
     - Python ``list``
   * - :doc:`tree_algorithms`
     - ``inorder``, ``preorder``, ``postorder``, ``level_order``
     - any binary tree
   * - :doc:`graph_algorithms`
     - ``bfs``, ``dfs``, ``dijkstra``, ``kruskal``
     - graphs, weighted graphs

Detailed Documentation
======================

.. toctree::
   :maxdepth: 2

   sorting
   tree_algorithms
   graph_algorithms

Related Guides
==============

* :doc:`../linear/convert` - Converting linear structures to and from lists
