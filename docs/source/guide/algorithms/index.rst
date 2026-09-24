.. _guide_algorithms:

==========
Algorithms
==========

Introduction
============

The previous parts of this guide describe **data structures**: how to store
items and the relations between them. This part is about **algorithms**:
procedures that compute something *from* a structure, such as a sorted
order, a shortest path or a posterior probability.

In ``sds`` the two are kept strictly apart. Structures live in
``sds.linear``, ``sds.tree``, ``sds.graph``, ``sds.advanced`` and
``sds.probabilistic``; algorithms live in :mod:`sds.algorithms` and receive
the structure they work on as a parameter.

.. mermaid::

   graph LR
       subgraph "Structures (store)"
       L[sds.linear]
       T[sds.tree]
       G[sds.graph]
       P[sds.probabilistic]
       end

       subgraph "sds.algorithms (compute)"
       S[sorting]
       TA[tree_algorithms]
       GA[graph_algorithms]
       PA[probabilistic_algorithms]
       end

       L --> S
       T --> TA
       G --> GA
       P --> PA

       style S fill:#3498db,color:#fff
       style TA fill:#3498db,color:#fff
       style GA fill:#3498db,color:#fff
       style PA fill:#3498db,color:#fff

.. note::

   **Why separate them?** A structure that also implemented every
   algorithm on it would grow without bound, and each algorithm would be
   tied to one representation. As free functions, an algorithm is written
   once against an abstract interface (``AbstractGraph``,
   ``AbstractBinaryTree``, ``AbstractGraphicalModel``) and runs unchanged on
   every structure implementing it: ``dijkstra()`` works on both
   ``WeightedGraph`` and ``WeightedDirectedGraph``.

Measuring Algorithms
====================

Algorithms are compared by how their cost grows with the size :math:`n` of
their input, ignoring constant factors. The three standard notations are:

.. math::

   f(n) = O(g(n)) \iff \exists c > 0,\ n_0,\ \forall n \ge n_0:\
       f(n) \le c \, g(n)

   f(n) = \Omega(g(n)) \iff \exists c > 0,\ n_0,\ \forall n \ge n_0:\
       f(n) \ge c \, g(n)

   f(n) = \Theta(g(n)) \iff f(n) = O(g(n)) \text{ and } f(n) = \Omega(g(n))

:math:`O` is an upper bound, :math:`\Omega` a lower bound, :math:`\Theta` a
tight bound. For graphs, costs are expressed in the number of vertices
:math:`V` and edges :math:`E`; for trees, in the number of nodes :math:`n`
and the height :math:`h`.

.. list-table:: Growth rates met in this guide
   :header-rows: 1
   :widths: 25 35 40

   * - Growth
     - Name
     - Example
   * - :math:`O(\log n)`
     - logarithmic
     - search in a balanced tree
   * - :math:`O(n)`
     - linear
     - tree traversal, BFS, DFS
   * - :math:`O(n \log n)`
     - linearithmic
     - merge sort, Kruskal
   * - :math:`O(n^2)`
     - quadratic
     - quicksort worst case
   * - :math:`O(d^w)`
     - exponential in a parameter
     - variable elimination (:math:`w` = induced width)

Contents
========

.. toctree::
   :maxdepth: 2

   paradigms
   sorting
   tree_algorithms
   graph_algorithms
   probabilistic_algorithms

.. list-table:: Which page for which question
   :header-rows: 1
   :widths: 50 50

   * - Question
     - Page
   * - How are algorithms designed and proved?
     - :doc:`paradigms`
   * - How do I sort, and which sort should I choose?
     - :doc:`sorting`
   * - How do I walk or rebalance a binary tree?
     - :doc:`tree_algorithms`
   * - Shortest paths, spanning trees, reachability?
     - :doc:`graph_algorithms`
   * - Posterior probabilities, likelihoods, decoding?
     - :doc:`probabilistic_algorithms`

For signatures and parameters, see the :doc:`../../api/algorithms/index`.
