.. _api_algorithms_tree:

========================
Tree Algorithms
========================

.. currentmodule:: sds.algorithms.tree_algorithms

Overview
========

This subpackage provides the four classic traversals of a binary tree,
and two functions about its shape: a balance check and the rebalancing of
a binary search tree. Each traversal takes the tree itself and yields the
data stored in its nodes, one at a time:

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Function
     - Order
     - Typical use
   * - :func:`preorder`
     - node, left, right
     - copying a tree, prefix expressions
   * - :func:`inorder`
     - left, node, right
     - sorted output of a search tree
   * - :func:`postorder`
     - left, right, node
     - freeing a tree, postfix expressions
   * - :func:`level_order`
     - level by level, left to right
     - printing by depth, breadth-first search

They accept any :class:`~sds.tree.interfaces.AbstractBinaryTree`
(``BinaryTree``, ``BinarySearchTree``, ``AVLTree``, ``RedBlackTree``) and
walk it only through ``tree.root`` and ``tree.children(node)``. That
accessor reports absent children as ``None`` whatever the implementation,
so the sentinel leaves of a Red-Black tree never show up in the output.

.. note::

   These functions replace the ``inorder_traversal()``,
   ``preorder_traversal()``, ``postorder_traversal()`` and
   ``level_order_traversal()`` methods, deprecated since 0.7.0 and
   scheduled for removal in 1.0.0:

   .. code-block:: python

      tree.inorder_traversal()     # deprecated
      inorder(tree)                # replacement

   Iterating over a tree directly (``for item in tree``) is unaffected and
   still yields the items in inorder.

The Four Orders
===============

.. mermaid::

   graph TD
       A((10)) --> B((5))
       A --> C((15))
       B --> D((3))
       B --> E((7))
       C --> F((12))
       C --> G((20))

       style A fill:#3498db,color:#fff

.. list-table:: On the binary search tree above
   :header-rows: 1
   :widths: 25 75

   * - Traversal
     - Sequence
   * - ``preorder``
     - 10, 5, 3, 7, 15, 12, 20
   * - ``inorder``
     - 3, 5, 7, 10, 12, 15, 20 (ascending, as for every search tree)
   * - ``postorder``
     - 3, 7, 5, 12, 20, 15, 10
   * - ``level_order``
     - 10, 5, 15, 3, 7, 12, 20

The three depth-first orders can be defined recursively. For a tree
:math:`T` with root :math:`r` and subtrees :math:`L` and :math:`R`:

.. math::

   \mathrm{pre}(T) = r \cdot \mathrm{pre}(L) \cdot \mathrm{pre}(R) \qquad
   \mathrm{in}(T) = \mathrm{in}(L) \cdot r \cdot \mathrm{in}(R) \qquad
   \mathrm{post}(T) = \mathrm{post}(L) \cdot \mathrm{post}(R) \cdot r

The implementations are iterative, with an explicit stack instead of
recursion. The visiting order is the same, but a degenerate tree (for
instance a search tree built from already sorted values, whose height
equals its size) is no longer limited by Python's recursion depth.

Complexity
==========

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Traversal
     - Time
     - Extra space
   * - ``preorder``, ``inorder``, ``postorder``
     - :math:`O(n)`
     - :math:`O(h)`, :math:`h` the height (:math:`\log n` to :math:`n`)
   * - ``level_order``
     - :math:`O(n)`
     - :math:`O(w)`, :math:`w` the widest level (up to about :math:`n/2`)
   * - ``is_balanced``
     - :math:`O(n)`
     - :math:`O(h)`
   * - ``rebalance``
     - :math:`O(n \log n)`
     - :math:`O(n)`

Detailed Documentation
======================

.. autofunction:: inorder

.. autofunction:: preorder

.. autofunction:: postorder

.. autofunction:: level_order

Balance
=======

A binary tree is **height-balanced** when, at every node, the heights of
the two subtrees differ by at most one (the AVL criterion). Its height is
then :math:`O(\log n)`, which keeps searches logarithmic.

A plain ``BinarySearchTree`` does not stay balanced by itself: inserting
sorted values builds a chain. :func:`rebalance` rebuilds such a tree in
place from its sorted content, inserting the median first, then the medians
of each half, level by level:

.. mermaid::

   graph LR
       subgraph "Before: insert 1..7 in order"
       A1((1)) --> A2((2)) --> A3((3)) --> A4((4)) --> A5((5)) --> A6((6)) --> A7((7))
       end

       subgraph "After rebalance()"
       B4((4)) --> B2((2))
       B4 --> B6((6))
       B2 --> B1((1))
       B2 --> B3((3))
       B6 --> B5((5))
       B6 --> B7((7))
       end

       style B4 fill:#2ecc71,color:#fff

The result has the minimum possible height, :math:`\lfloor \log_2 n \rfloor`,
for distinct keys. The self-balancing ``AVLTree`` and ``RedBlackTree`` are
not accepted: they repair their shape with rotations on every update, and
those rotations stay inside their classes as part of their invariant.

.. autofunction:: is_balanced

.. autofunction:: rebalance

Usage Example
=============

.. code-block:: python

   from sds.tree import AVLTree
   from sds.algorithms.tree_algorithms import inorder, level_order

   tree = AVLTree()
   for value in range(1, 8):       # sorted input: the AVL tree rebalances
       tree.insert(value)

   list(inorder(tree))              # [1, 2, 3, 4, 5, 6, 7]
   list(level_order(tree))          # [4, 2, 6, 1, 3, 5, 7]

   # Traversals are lazy: stop as soon as the answer is known
   first_even = next(x for x in inorder(tree) if x % 2 == 0)

References
==========

* OpenDSA, *Binary Tree Traversals* —
  https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/BinaryTreeTraversal.html
* R. Sedgewick and K. Wayne, *Algorithms, 4th Edition*, section 3.2
  (free online companion) — https://algs4.cs.princeton.edu/32bst/
