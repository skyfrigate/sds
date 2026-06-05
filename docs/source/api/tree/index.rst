.. _api_tree:

==========================
Tree Structures (sds.tree)
==========================

.. currentmodule:: sds.tree

Tree data structures organize elements in a hierarchical manner, where each element
(except the root) has exactly one parent and zero or more children.

Overview
========

The tree module provides implementations of fundamental hierarchical data structures:

* **Binary Trees** - Trees with at most two children per node
* **Binary Search Trees** - Ordered binary trees for efficient searching
* **Balanced Trees** - Self-balancing trees (AVL, Red-Black)
* **General Trees** - Trees with arbitrary number of children
* **B-Trees** - Multi-way search trees for disk-based storage
* **Tries** - Prefix trees for string operations
* **Heaps** - Priority queue implementations
* **Segment Trees** - Efficient range query structures

Key Features
============

✓ **Hierarchical organization** - Natural representation of nested data
✓ **Efficient operations** - O(log n) search in balanced trees
✓ **Multiple traversals** - Inorder, preorder, postorder, level-order
✓ **Self-balancing** - AVL and Red-Black trees maintain balance
✓ **Consistent API** - Uniform interface across all tree types

Module Contents
===============

Node Classes
------------

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   BinaryNode
   TreeNode
   BTreeNode
   TrieNode
   AVLNode
   RedBlackNode

Binary Tree Structures
----------------------

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   BinaryTree
   BinarySearchTree

Balanced Trees
--------------

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   AVLTree
   RedBlackTree

General Trees
-------------

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   Tree

Advanced Trees
--------------

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   BTree
   Trie
   MinHeap
   MaxHeap
   HeapPriorityQueue
   SegmentTree

Detailed Documentation
======================

.. toctree::
   :maxdepth: 2

   node
   interfaces
   binary
   balanced
   general
   btree
   trie
   heap
   segment_tree

Tree Type Comparison
====================

.. list-table:: Tree Structure Comparison
   :header-rows: 1
   :widths: 20 15 15 15 35

   * - Structure
     - Insert
     - Search
     - Height
     - Best Use Case
   * - Binary Tree
     - O(n)
     - O(n)
     - O(n)
     - Simple hierarchies
   * - BST
     - O(log n)*
     - O(log n)*
     - O(n)*
     - Ordered data, searching
   * - AVL Tree
     - O(log n)
     - O(log n)
     - O(log n)
     - Frequent searches
   * - Red-Black Tree
     - O(log n)
     - O(log n)
     - O(log n)
     - Frequent insertions
   * - General Tree
     - O(1)
     - O(n)
     - O(n)
     - File systems, DOM
   * - B-Tree
     - O(log n)
     - O(log n)
     - O(log n)
     - Databases, file systems
   * - Trie
     - O(m)
     - O(m)
     - O(m)
     - Autocomplete, dictionaries
   * - Heap
     - O(log n)
     - O(n)
     - O(log n)
     - Priority queues
   * - Segment Tree
     - O(n)
     - O(log n)
     - O(log n)
     - Range queries

\* Average case; O(n) worst case for unbalanced BST
m = length of key for Trie operations

Binary vs General Trees
========================

.. mermaid::

   graph TB
       subgraph "Binary Tree (max 2 children)"
       A1[Root] --> B1[Left]
       A1 --> C1[Right]
       B1 --> D1[LL]
       B1 --> E1[LR]
       end

       subgraph "General Tree (any number)"
       A2[Root] --> B2[Child 1]
       A2 --> C2[Child 2]
       A2 --> D2[Child 3]
       A2 --> E2[Child 4]
       end

       style A1 fill:#e74c3c
       style A2 fill:#3498db

Traversal Methods
=================

All tree structures support multiple traversal methods:

.. code-block:: python

   from sds.tree import BinarySearchTree

   tree = BinarySearchTree()
   for val in [50, 30, 70, 20, 40, 60, 80]:
       tree.insert(val)

   # Inorder (sorted for BST)
   list(tree.inorder_traversal())
   # Output: [20, 30, 40, 50, 60, 70, 80]

   # Preorder (root first)
   list(tree.preorder_traversal())
   # Output: [50, 30, 20, 40, 70, 60, 80]

   # Postorder (root last)
   list(tree.postorder_traversal())
   # Output: [20, 40, 30, 60, 80, 70, 50]

   # Level-order (breadth-first)
   list(tree.level_order_traversal())
   # Output: [50, 30, 70, 20, 40, 60, 80]

Balanced vs Unbalanced Trees
=============================

Impact of Tree Balance
-----------------------

.. code-block:: text

   Balanced BST (height = log n):        Unbalanced BST (height = n):

          50                                    10
         /  \                                     \
       30    70                                   20
      /  \   /  \                                   \
    20  40 60  80                                   30
                                                      \
   Height: 2 (log₂ 7)                                40
   Search: O(log n)                                    \
                                                        50

                                                   Height: 4 (n - 3)
                                                   Search: O(n)

When to Use Each Tree Type
===========================

Decision Guide
--------------

.. mermaid::

   graph TD
       A{What's your priority?}

       A -->|Fast search| B{How often insert?}
       B -->|Frequent| C[Red-Black Tree]
       B -->|Rare| D[AVL Tree]

       A -->|Range queries| E[Segment Tree]
       A -->|String prefix| F[Trie]
       A -->|Priority queue| G[Heap]
       A -->|Disk storage| H[B-Tree]
       A -->|Variable children| I[General Tree]
       A -->|Simple hierarchy| J[Binary Tree]

       style C fill:#e74c3c
       style D fill:#3498db
       style E fill:#f39c12
       style F fill:#9b59b6
       style G fill:#27ae60
       style H fill:#e67e22
       style I fill:#1abc9c
       style J fill:#95a5a6

Common Use Cases
================

Binary Search Trees
-------------------

.. code-block:: python

   from sds.tree import BinarySearchTree

   # Database indexing
   index = BinarySearchTree()
   for record_id in [100, 50, 150, 25, 75, 125, 175]:
       index.insert(record_id)

   # Fast lookup: O(log n)
   if index.search(75):
       print("Record found")

   # Range query (inorder)
   records_50_to_150 = [
       r for r in index.inorder_traversal()
       if 50 <= r <= 150
   ]

AVL Trees
---------

.. code-block:: python

   from sds.tree import AVLTree

   # Dictionary with frequent lookups
   dictionary = AVLTree()
   words = ["apple", "banana", "cherry", "date"]
   for word in words:
       dictionary.insert(word)

   # Always O(log n) search
   print(dictionary.search("banana"))  # True
   print(dictionary.height())  # Guaranteed log n

General Trees
-------------

.. code-block:: python

   from sds.tree import Tree

   # File system representation
   fs = Tree("/")
   fs.add_child("home")
   fs.add_child("usr")
   fs.add_child_to("home", "user1")
   fs.add_child_to("home", "user2")

   # Query structure
   print(fs.degree("/"))  # Number of directories

Tries
-----

.. code-block:: python

   from sds.tree import Trie

   # Autocomplete system
   autocomplete = Trie()
   words = ["hello", "help", "hero", "world"]
   for word in words:
       autocomplete.insert(word)

   # Get suggestions
   suggestions = autocomplete.autocomplete("he")
   print(suggestions)  # ['hello', 'help', 'hero']

Heaps
-----

.. code-block:: python

   from sds.tree import MinHeap

   # Task priority queue
   tasks = MinHeap()
   tasks.insert((1, "Critical bug"))
   tasks.insert((5, "Feature request"))
   tasks.insert((3, "Minor fix"))

   # Process by priority
   while not tasks.is_empty():
       priority, task = tasks.extract()
       print(f"Processing: {task}")

Performance Guidelines
======================

Time Complexity Summary
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 15 15 15 30

   * - Operation
     - Binary Tree
     - Balanced Tree
     - General Tree
     - Notes
   * - Insert
     - O(n)
     - O(log n)
     - O(1)
     - At known position
   * - Search
     - O(n)
     - O(log n)
     - O(n)
     - BST property helps
   * - Delete
     - O(n)
     - O(log n)
     - O(n)
     - Must find node
   * - Height
     - O(n)
     - O(1) or O(n)
     - O(n)
     - Cached in AVL
   * - Min/Max
     - O(n)
     - O(log n)
     - O(n)
     - BST only
   * - Traversal
     - O(n)
     - O(n)
     - O(n)
     - Visit all nodes

Space Complexity
----------------

All tree structures have:

* **Storage**: O(n) for n nodes
* **Recursion**: O(h) where h is height
  * Balanced: O(log n)
  * Unbalanced: O(n)

Related Guides
==============

* :doc:`../../guide/tree_structures/index` - User guide for tree structures
* :doc:`../core/index` - Core abstractions
* :doc:`../linear/index` - Linear structures

See Also
========

External Resources
------------------

* `Wikipedia: Tree (data structure) <https://en.wikipedia.org/wiki/Tree_(data_structure)>`_
* `VisuAlgo: Binary Search Tree <https://visualgo.net/en/bst>`_
* `CLRS Introduction to Algorithms <https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/>`_

Academic References
-------------------

.. [1] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Chapters 10, 12-13
.. [2] Knuth, D. E. "The Art of Computer Programming, Volume 1", Section 2.3
.. [3] Adelson-Velsky, G., Landis, E. M. "An algorithm for the organization of information", 1962
.. [4] Bayer, R., McCreight, E. "Organization and Maintenance of Large Ordered Indices", 1972