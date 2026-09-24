.. _guide_algorithms_tree:

===============
Tree Algorithms
===============

.. currentmodule:: sds.algorithms.tree_algorithms

Introduction
============

A traversal visits every node of a tree exactly once, in a defined order.
It is the building block of almost every tree computation: printing,
copying, evaluating an expression tree, checking an invariant. This page
covers the four classic traversals of a binary tree, then the balance of a
binary search tree and how to restore it.

All functions take the tree itself (any ``AbstractBinaryTree``) and walk it
through ``tree.root`` and ``tree.children(node)`` only.

The Four Traversals
===================

.. mermaid::

   graph TD
       A((F)) --> B((B))
       A --> C((G))
       B --> D((A))
       B --> E((D))
       E --> F((C))
       E --> G((E))
       C --> H((" "))
       C --> I((I))
       I --> J((H))

       style H fill:none,stroke:none

.. list-table:: On the tree above
   :header-rows: 1
   :widths: 25 35 40

   * - Traversal
     - Rule
     - Sequence
   * - ``preorder``
     - node, left subtree, right subtree
     - F, B, A, D, C, E, G, I, H
   * - ``inorder``
     - left subtree, node, right subtree
     - A, B, C, D, E, F, G, H, I
   * - ``postorder``
     - left subtree, right subtree, node
     - A, C, E, D, B, H, I, G, F
   * - ``level_order``
     - by depth, left to right
     - F, B, G, A, D, I, C, E, H

The tree is a binary search tree, so ``inorder`` lists its keys in
alphabetical order. This holds for every search tree, by induction: every
key of the left subtree precedes the node, every key of the right subtree
follows it.

From Recursion to an Explicit Stack
-----------------------------------

The depth-first traversals are naturally recursive:

.. code-block:: text

    inorder(node):
        if node is None: return
        inorder(left(node)); emit node; inorder(right(node))

Each recursive call uses a Python stack frame. A binary search tree built
from sorted input is a chain of height :math:`n - 1`, and Python stops at
about a thousand nested calls. The library's implementations manage their
own stack instead:

.. code-block:: text

    inorder(T):
        stack <- []; node <- root(T)
        while stack or node:
            while node:                       # go down the left spine
                push node; node <- left(node)
            node <- pop()
            emit node
            node <- right(node)               # then visit the right subtree

The explicit stack holds exactly the nodes a recursive call chain would
hold, so the order is unchanged, and its size is bounded by the height
:math:`h`.

Cost
----

Each node is pushed and popped once and each edge followed once:

.. math::

   T(n) = \Theta(n), \qquad S(n) = O(h), \quad \log_2 n \le h + 1 \le n

``level_order`` uses a queue instead of a stack; its memory is bounded by
the widest level, up to about :math:`n / 2` for a complete tree.

Choosing a Traversal
--------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Traversal
     - Use it when...
   * - ``preorder``
     - a node must be handled before its descendants: copying a tree,
       serializing it, printing an indented outline.
   * - ``inorder``
     - you need the keys of a search tree in sorted order.
   * - ``postorder``
     - a node needs the results of its descendants: computing sizes or
       heights, freeing memory, evaluating an expression tree.
   * - ``level_order``
     - depth matters: printing level by level, finding the shallowest node
       with a property.

Balance
=======

Definition
----------

A binary tree is **height-balanced** if, at every node, the heights of the
two subtrees differ by at most one (the AVL criterion). With :math:`N(h)`
the minimum number of nodes of a balanced tree of height :math:`h`:

.. math::

   N(h) = N(h-1) + N(h-2) + 1, \qquad N(0) = 1,\ N(1) = 2

which grows like the Fibonacci numbers, :math:`N(h) \ge \varphi^{h}` with
:math:`\varphi = (1 + \sqrt 5)/2`. Hence a balanced tree of :math:`n` nodes
has height :math:`h \le \log_\varphi n \approx 1.44 \log_2 n`: searches stay
logarithmic.

``is_balanced(tree)`` checks the criterion in one postorder pass: a node's
height is known once both children's are, so each node is examined once,
in :math:`O(n)`.

Rebalancing a Search Tree
-------------------------

A plain ``BinarySearchTree`` never repairs its shape. ``rebalance(tree)``
rebuilds it from its sorted content:

.. code-block:: text

    rebalance(T):
        items <- list(inorder(T)); clear T
        queue <- [(0, n - 1)]
        while queue:
            (lo, hi) <- dequeue
            if lo > hi: continue
            mid <- (lo + hi) // 2
            insert items[mid] into T
            enqueue (lo, mid - 1) and (mid + 1, hi)

.. mermaid::

   graph LR
       subgraph "Before"
       A1((1)) --> A2((2)) --> A3((3)) --> A4((4)) --> A5((5)) --> A6((6)) --> A7((7))
       end
       subgraph "After"
       B4((4)) --> B2((2)) & B6((6))
       B2 --> B1((1)) & B3((3))
       B6 --> B5((5)) & B7((7))
       end

**Height.** A range of :math:`m` items becomes a subtree whose root is the
median and whose two sub-ranges have at most :math:`\lceil (m-1)/2 \rceil`
items. With :math:`H(m)` the resulting height:

.. math::

   H(m) = 1 + H\!\left(\left\lceil \frac{m-1}{2} \right\rceil\right),
   \qquad H(1) = 0
   \quad\Longrightarrow\quad H(n) = \lfloor \log_2 n \rfloor

the minimum possible height for :math:`n` nodes. Inserting range by range
in breadth-first order lays each level down before the next, so the
insertion path always follows the final shape.

**Cost.** One traversal, then :math:`n` insertions each of cost
:math:`O(\log n)`: :math:`O(n \log n)` time, :math:`O(n)` memory for the
sorted copy.

.. note::

   ``AVLTree`` and ``RedBlackTree`` are not accepted by ``rebalance()``:
   they keep themselves balanced with rotations performed during every
   insertion and removal. Those rotations are part of the structure's own
   invariant and stay in their classes.

References
==========

* CLRS, chapters 12 (binary search trees, traversals) and 13 (red-black
  trees).
* OpenDSA, *Binary Tree Traversals* and *Balanced Trees* —
  https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/BinaryTreeTraversal.html,
  https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/BalancedTree.html
* R. Sedgewick and K. Wayne, *Algorithms, 4th ed.*, sections 3.2–3.3 —
  https://algs4.cs.princeton.edu/30searching/
