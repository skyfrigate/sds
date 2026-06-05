.. _guide_tree:

===============
Tree Structures
===============

Introduction
============

Tree data structures organize elements hierarchically, where each element (except the root)
has exactly one parent and zero or more children. This hierarchical organization makes trees
ideal for representing nested relationships, taxonomies, and structured data.

.. mermaid::

   graph TB
       A[Root] --> B[Child 1]
       A --> C[Child 2]
       A --> D[Child 3]

       B --> E[Grandchild 1]
       B --> F[Grandchild 2]

       C --> G[Grandchild 3]

       style A fill:#e74c3c,stroke:#c0392b,color:#fff
       style B fill:#3498db,stroke:#2980b9,color:#fff
       style C fill:#3498db,stroke:#2980b9,color:#fff
       style D fill:#3498db,stroke:#2980b9,color:#fff
       style E fill:#2ecc71,stroke:#27ae60,color:#fff
       style F fill:#2ecc71,stroke:#27ae60,color:#fff
       style G fill:#2ecc71,stroke:#27ae60,color:#fff

This section covers all tree structures provided by SDS-Tools, from simple binary trees
to advanced structures like B-Trees and Tries.

Overview
========

Types of Tree Structures
-------------------------

SDS-Tools provides a comprehensive collection of tree structures, each optimized for
specific use cases:

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Structure
     - Key Property
     - Primary Use Cases
   * - **Binary Tree**
     - Max 2 children per node
     - Simple hierarchies, expression trees
   * - **Binary Search Tree**
     - Ordered binary tree
     - Searching, sorting, range queries
   * - **AVL Tree**
     - Height-balanced BST
     - Frequent searches, lookups
   * - **Red-Black Tree**
     - Color-balanced BST
     - Frequent insertions, deletions
   * - **General Tree**
     - Variable children
     - File systems, organizations
   * - **B-Tree**
     - Multi-way search tree
     - Databases, file systems
   * - **Trie**
     - Prefix tree
     - Autocomplete, spell checking
   * - **Heap**
     - Complete binary tree
     - Priority queues, sorting
   * - **Segment Tree**
     - Range query tree
     - Range sum/min/max queries

Tree Terminology
----------------

.. mermaid::

   graph TB
       R["Root<br/>(depth 0, height 2)"]
       R --> I1["Internal Node<br/>(depth 1, height 1)"]
       R --> I2["Internal Node<br/>(depth 1, height 0)"]

       I1 --> L1["Leaf<br/>(depth 2, height 0)"]
       I1 --> L2["Leaf<br/>(depth 2, height 0)"]

       style R fill:#e74c3c,stroke:#c0392b,color:#fff
       style I1 fill:#3498db,stroke:#2980b9,color:#fff
       style I2 fill:#3498db,stroke:#2980b9,color:#fff
       style L1 fill:#2ecc71,stroke:#27ae60,color:#fff
       style L2 fill:#2ecc71,stroke:#27ae60,color:#fff

**Key Terms:**

* **Root**: The topmost node (no parent)
* **Leaf**: A node with no children
* **Internal Node**: A node with at least one child
* **Parent**: A node that has children
* **Child**: A node descended from a parent
* **Sibling**: Nodes with the same parent
* **Depth**: Distance from root to node
* **Height**: Distance from node to deepest leaf
* **Degree**: Number of children a node has
* **Subtree**: A node and all its descendants

Choosing the Right Tree
------------------------

.. mermaid::

   graph TD
       A{What's your<br/>requirement?}

       A -->|Need ordering| B{Balance important?}
       B -->|Yes, frequent searches| C[AVL Tree]
       B -->|Yes, frequent updates| D[Red-Black Tree]
       B -->|No| E[Binary Search Tree]

       A -->|Range queries| F[Segment Tree]
       A -->|String prefixes| G[Trie]
       A -->|Priority-based access| H{Min or Max?}
       H -->|Minimum first| I[MinHeap]
       H -->|Maximum first| J[MaxHeap]

       A -->|Large datasets on disk| K[B-Tree]
       A -->|Variable children| L[General Tree]
       A -->|Simple hierarchy| M[Binary Tree]

       style C fill:#e74c3c,color:#fff
       style D fill:#c0392b,color:#fff
       style E fill:#3498db,color:#fff
       style F fill:#f39c12
       style G fill:#9b59b6,color:#fff
       style I fill:#2ecc71,color:#fff
       style J fill:#27ae60,color:#fff
       style K fill:#e67e22,color:#fff
       style L fill:#1abc9c,color:#fff
       style M fill:#95a5a6,color:#fff

Detailed Guides
===============

Basic Trees
-----------

.. toctree::
   :maxdepth: 2
   :caption: Foundation

   binary
   general

Balanced Trees
--------------

.. toctree::
   :maxdepth: 2
   :caption: Self-Balancing

   avl
   red_black

Advanced Trees
--------------

.. toctree::
   :maxdepth: 2
   :caption: Specialized Structures

   btree
   trie
   heap
   segment_tree

Quick Start
===========

Binary Search Tree
------------------

Perfect for maintaining sorted data with efficient search:

.. code-block:: python

   from sds.tree import BinarySearchTree

   # Create and populate
   bst = BinarySearchTree()
   for value in [50, 30, 70, 20, 40, 60, 80]:
       bst.insert(value)

   # Search efficiently: O(log n) average
   print(bst.search(40))  # True
   print(40 in bst)       # True

   # Get sorted data via inorder traversal
   print(list(bst.inorder_traversal()))
   # Output: [20, 30, 40, 50, 60, 70, 80]

   # Find min/max
   print(bst.find_min())  # 20
   print(bst.find_max())  # 80

AVL Tree (Always Balanced)
---------------------------

Guaranteed O(log n) operations with automatic balancing:

.. code-block:: python

   from sds.tree import AVLTree

   # Create AVL tree
   avl = AVLTree()

   # Even inserting sorted data stays balanced!
   for i in range(1, 8):
       avl.insert(i)

   # Height is logarithmic: log₂(7) ≈ 2.8
   print(avl.height())  # 2 (balanced!)

   # Compare to unbalanced BST which would have height 6
   print(list(avl))  # [1, 2, 3, 4, 5, 6, 7]

General Tree
------------

For hierarchies with variable children:

.. code-block:: python

   from sds.tree import Tree

   # Organization chart
   org = Tree("CEO")
   org.add_child("CTO")
   org.add_child("CFO")
   org.add_child("COO")

   # Add sub-departments
   org.add_child_to("CTO", "Engineering")
   org.add_child_to("CTO", "DevOps")
   org.add_child_to("CFO", "Accounting")

   # Query structure
   print(f"Size: {len(org)}")
   print(f"Height: {org.height()}")
   print(f"CTO reports: {org.degree('CTO')}")

Trie for Strings
----------------

Efficient prefix-based operations:

.. code-block:: python

   from sds.tree import Trie

   # Autocomplete system
   trie = Trie()
   words = ["hello", "help", "hero", "world", "word"]
   for word in words:
       trie.insert(word)

   # Get all words with prefix "he"
   suggestions = trie.autocomplete("he")
   print(suggestions)  # ['hello', 'help', 'hero']

   # Check if word exists: O(m) where m is word length
   print("hello" in trie)  # True

Heap for Priorities
-------------------

Efficient priority queue operations:

.. code-block:: python

   from sds.tree import MinHeap

   # Task queue with priorities
   tasks = MinHeap()
   tasks.insert((1, "Critical bug"))
   tasks.insert((3, "Minor fix"))
   tasks.insert((2, "Feature"))

   # Process in priority order
   while not tasks.is_empty():
       priority, task = tasks.extract()
       print(f"[Priority {priority}] {task}")
   # Output:
   # [Priority 1] Critical bug
   # [Priority 2] Feature
   # [Priority 3] Minor fix

Common Patterns
===============

Pattern 1: Tree Traversals
---------------------------

Different traversals serve different purposes:

.. code-block:: python

   from sds.tree import BinarySearchTree

   tree = BinarySearchTree()
   for val in [50, 30, 70, 20, 40, 60, 80]:
       tree.insert(val)

   # Inorder: Get sorted data (for BST)
   sorted_data = list(tree.inorder_traversal())
   # [20, 30, 40, 50, 60, 70, 80]

   # Preorder: Copy tree structure
   def copy_tree(root):
       for value in tree.preorder_traversal():
           new_tree.insert(value)

   # Postorder: Delete tree (children before parent)
   def delete_tree(root):
       for value in tree.postorder_traversal():
           # Process children first
           pass

   # Level-order: Print by levels
   for value in tree.level_order_traversal():
       print(value, end=" ")
   # Output: 50 30 70 20 40 60 80

Pattern 2: Tree Search and Navigation
--------------------------------------

.. code-block:: python

   from sds.tree import BinarySearchTree

   bst = BinarySearchTree()
   values = [50, 30, 70, 20, 40, 60, 80]
   for val in values:
       bst.insert(val)

   # Find a value: O(log n) average
   if bst.search(40):
       print("Found 40")

   # Range query (values between 30 and 70)
   range_values = [
       v for v in bst.inorder_traversal()
       if 30 <= v <= 70
   ]
   print(range_values)  # [30, 40, 50, 60, 70]

   # Find successor (next larger value)
   def find_successor(tree, value):
       larger = [v for v in tree.inorder_traversal() if v > value]
       return larger[0] if larger else None

   print(find_successor(bst, 40))  # 50

Pattern 3: Hierarchical Data Processing
----------------------------------------

.. code-block:: python

   from sds.tree import Tree

   # File system with size calculation
   fs = Tree(("root", 0))
   fs.add_child_to(("root", 0), ("documents", 0))
   fs.add_child_to(("root", 0), ("pictures", 0))
   fs.add_child_to(("documents", 0), ("file1.txt", 100))
   fs.add_child_to(("documents", 0), ("file2.pdf", 500))
   fs.add_child_to(("pictures", 0), ("photo.jpg", 2000))

   def calculate_size(tree, node_data):
       """Calculate total size of directory."""
       node = tree.find_node(node_data)
       if not node:
           return 0

       # Leaf node (file)
       if node.is_leaf():
           return node_data[1]

       # Internal node (directory) - sum children
       total = 0
       for child in node.children:
           total += calculate_size(tree, child.data)

       return total

   print(f"Root size: {calculate_size(fs, ('root', 0))} bytes")

Pattern 4: Priority-Based Processing
-------------------------------------

.. code-block:: python

   from sds.tree import HeapPriorityQueue

   # Event scheduler
   scheduler = HeapPriorityQueue()

   # Add events with timestamps (priority)
   scheduler.enqueue("Wake up", 7)
   scheduler.enqueue("Lunch", 12)
   scheduler.enqueue("Breakfast", 8)
   scheduler.enqueue("Dinner", 19)

   # Process events in chronological order
   print("Today's schedule:")
   while not scheduler.is_empty():
       event, time = scheduler.dequeue()
       print(f"{time}:00 - {event}")

   # Output:
   # 7:00 - Wake up
   # 8:00 - Breakfast
   # 12:00 - Lunch
   # 19:00 - Dinner

Performance Comparison
======================

Operation Complexity
--------------------

.. list-table::
   :header-rows: 1
   :widths: 20 12 12 12 12 12 20

   * - Operation
     - Binary Tree
     - BST
     - AVL
     - Red-Black
     - B-Tree
     - Notes
   * - **Insert**
     - O(n)
     - O(log n)*
     - O(log n)
     - O(log n)
     - O(log n)
     - *avg case
   * - **Search**
     - O(n)
     - O(log n)*
     - O(log n)
     - O(log n)
     - O(log n)
     - *avg case
   * - **Delete**
     - O(n)
     - O(log n)*
     - O(log n)
     - O(log n)
     - O(log n)
     - *avg case
   * - **Min/Max**
     - O(n)
     - O(log n)*
     - O(log n)
     - O(log n)
     - O(log n)
     - BST only
   * - **Height**
     - O(n)
     - O(n)
     - O(1)
     - O(log n)
     - O(log n)
     - Cached in AVL
   * - **Traversal**
     - O(n)
     - O(n)
     - O(n)
     - O(n)
     - O(n)
     - All nodes

Special Structure Complexities
-------------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 35

   * - Structure
     - Insert
     - Search/Query
     - Special Notes
   * - **Trie**
     - O(m)
     - O(m)
     - m = key length
   * - **MinHeap/MaxHeap**
     - O(log n)
     - O(1) peek
     - O(log n) extract
   * - **Segment Tree**
     - O(n) build
     - O(log n)
     - Range queries
   * - **General Tree**
     - O(1) child
     - O(n)
     - Variable degree

Space Complexity
----------------

All tree structures have:

* **Storage**: O(n) where n is number of nodes
* **Recursion Stack**: O(h) where h is height
  * Balanced trees: O(log n)
  * Unbalanced: O(n) worst case

Best Practices
==============

Choosing Operations
-------------------

✅ **Use the right tree for your access pattern**

.. code-block:: python

   # Frequent searches → AVL Tree
   avl = AVLTree()

   # Frequent insertions → Red-Black Tree
   rbt = RedBlackTree()

   # Prefix matching → Trie
   trie = Trie()

   # Priority access → Heap
   heap = MinHeap()

✅ **Consider memory vs speed tradeoffs**

.. code-block:: python

   # BST: Less memory, potentially slower
   bst = BinarySearchTree()

   # AVL: More memory (height storage), always fast
   avl = AVLTree()

✅ **Batch operations when possible**

.. code-block:: python

   # Build tree from sorted array efficiently
   def build_balanced_bst(sorted_array):
       if not sorted_array:
           return None

       mid = len(sorted_array) // 2
       root = BinaryNode(sorted_array[mid])
       root.left = build_balanced_bst(sorted_array[:mid])
       root.right = build_balanced_bst(sorted_array[mid+1:])
       return root

Common Pitfalls
---------------

❌ **Inserting sorted data into unbalanced BST**

.. code-block:: python

   # Bad: Creates degenerate tree
   bst = BinarySearchTree()
   for i in range(1000):
       bst.insert(i)  # Height = 999!

   # Good: Use balanced tree or shuffle
   avl = AVLTree()
   for i in range(1000):
       avl.insert(i)  # Height ≈ 10

❌ **Deep recursion without checking limits**

.. code-block:: python

   import sys

   # Check recursion limit
   print(sys.getrecursionlimit())  # Default: 1000

   # Increase if needed for large trees
   sys.setrecursionlimit(5000)

❌ **Modifying tree during traversal**

.. code-block:: python

   # Bad: Undefined behavior
   for value in tree.inorder_traversal():
       tree.remove(value)  # Don't do this!

   # Good: Collect then modify
   to_remove = list(tree.inorder_traversal())
   for value in to_remove:
       tree.remove(value)

Real-World Applications
=======================

1. **Database Indexing** - B-Trees in databases
2. **File Systems** - General trees for directories
3. **Autocomplete** - Tries for search suggestions
4. **Priority Queues** - Heaps for task scheduling
5. **Expression Evaluation** - Binary trees for parsers
6. **Decision Trees** - Machine learning classification
7. **Game AI** - Minimax trees for game playing
8. **XML/HTML Parsing** - General trees for DOM

See Also
========

* :doc:`../../api/tree/index` - API reference for tree structures
* :doc:`../linear_structures/index` - Linear structures guide
* :doc:`../graph_structures/index` - Graph structures guide

External Resources
------------------

* `VisuAlgo: Binary Search Tree <https://visualgo.net/en/bst>`_ - Interactive visualizations
* `Red-Black Tree Visualization <https://www.cs.usfca.edu/~galles/visualization/RedBlack.html>`_
* `B-Tree Visualization <https://www.cs.usfca.edu/~galles/visualization/BTree.html>`_

References
==========

.. [1] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition
.. [2] Knuth, D. E. "The Art of Computer Programming, Volume 1"
.. [3] Adelson-Velsky, G., Landis, E. M. "An algorithm for the organization of information", 1962
.. [4] Guibas, L. J., Sedgewick, R. "A Dichromatic Framework for Balanced Trees", 1978
.. [5] Bayer, R., McCreight, E. "Organization and Maintenance of Large Ordered Indices", 1972