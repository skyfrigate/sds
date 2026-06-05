.. _api_tree_general:

============
General Tree
============

.. currentmodule:: sds.tree.general

Overview
========

The Tree class implements a general tree (n-ary tree) where each node can have an arbitrary
number of children. This provides maximum flexibility for representing hierarchical data
such as file systems, organizational charts, and XML/HTML documents.

.. mermaid::

   graph TB
       A[Root] --> B[Child 1]
       A --> C[Child 2]
       A --> D[Child 3]
       
       B --> E[Grandchild 1]
       B --> F[Grandchild 2]
       
       C --> G[Grandchild 3]
       C --> H[Grandchild 4]
       C --> I[Grandchild 5]
       
       style A fill:#e74c3c,stroke:#c0392b,color:#fff
       style B fill:#3498db,stroke:#2980b9,color:#fff
       style E fill:#2ecc71,stroke:#27ae60,color:#fff

Classes
=======

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   Tree

Detailed Documentation
======================

Tree Class
----------

.. autoclass:: Tree
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __len__, __iter__, __contains__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: root
   .. autoproperty:: size

   .. rubric:: Core Operations

   .. automethod:: height
   .. automethod:: insert
   .. automethod:: remove
   .. automethod:: search
   .. automethod:: add_child
   .. automethod:: add_child_to
   .. automethod:: remove_node

   .. rubric:: Query Methods

   .. automethod:: find_node
   .. automethod:: get_children
   .. automethod:: get_parent
   .. automethod:: degree
   .. automethod:: is_leaf
   .. automethod:: leaves

   .. rubric:: Traversal Methods

   .. automethod:: preorder_traversal
   .. automethod:: postorder_traversal
   .. automethod:: level_order_traversal

   .. rubric:: Utility Methods

   .. automethod:: is_empty
   .. automethod:: clear

   .. rubric:: Special Methods

   .. automethod:: __len__
   .. automethod:: __iter__
   .. automethod:: __contains__
   .. automethod:: __repr__
   .. automethod:: __str__

Usage Examples
==============

Basic Operations
----------------

Creating a Tree
^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.tree import Tree

   # Create tree with root
   tree = Tree("CEO")
   
   # Check initial state
   print(tree.is_empty())  # Output: False
   print(len(tree))        # Output: 1
   print(tree.height())    # Output: 0

Adding Children
^^^^^^^^^^^^^^^

.. code-block:: python

   # Add children to root
   cto = tree.add_child("CTO")
   cfo = tree.add_child("CFO")
   coo = tree.add_child("COO")
   
   print(f"Tree size: {len(tree)}")  # Output: 4
   
   # Add grandchildren
   tree.add_child_to("CTO", "Dev Manager")
   tree.add_child_to("CTO", "QA Manager")
   tree.add_child_to("CFO", "Accountant")
   
   print(f"Tree size: {len(tree)}")     # Output: 7
   print(f"Tree height: {tree.height()}")  # Output: 2

Working with Nodes
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Find a node
   node = tree.find_node("CTO")
   if node:
       print(f"Found: {node.data}")
       print(f"Is leaf: {node.is_leaf()}")
   
   # Check membership
   print("CFO" in tree)  # Output: True
   print("CEO" in tree)  # Output: True
   
   # Get node's children
   children = tree.get_children("CTO")
   print(f"CTO has {len(children)} direct reports")
   
   # Get node's parent
   parent = tree.get_parent("Dev Manager")
   print(f"Parent: {parent.data}")  # Output: CTO
   
   # Get node degree
   degree = tree.degree("CTO")
   print(f"Degree: {degree}")  # Output: 2

Traversals
^^^^^^^^^^

.. code-block:: python

   tree = Tree("A")
   tree.add_child("B")
   tree.add_child("C")
   tree.add_child_to("B", "D")
   tree.add_child_to("B", "E")
   tree.add_child_to("C", "F")
   
   # Preorder (parent before children)
   print("Preorder:", list(tree.preorder_traversal()))
   # Output: ['A', 'B', 'D', 'E', 'C', 'F']
   
   # Postorder (children before parent)
   print("Postorder:", list(tree.postorder_traversal()))
   # Output: ['D', 'E', 'B', 'F', 'C', 'A']
   
   # Level-order (breadth-first)
   print("Level-order:", list(tree.level_order_traversal()))
   # Output: ['A', 'B', 'C', 'D', 'E', 'F']
   
   # Default iteration uses preorder
   print("Iteration:", list(tree))
   # Output: ['A', 'B', 'D', 'E', 'C', 'F']

Query Operations
^^^^^^^^^^^^^^^^

.. code-block:: python

   # Check if node is leaf
   print(tree.is_leaf("D"))  # Output: True
   print(tree.is_leaf("B"))  # Output: False
   
   # Get all leaf nodes
   leaves = tree.leaves()
   print(f"Leaves: {leaves}")
   # Output: ['D', 'E', 'F']
   
   # Get node degree
   print(f"Degree of B: {tree.degree('B')}")  # Output: 2
   print(f"Degree of A: {tree.degree('A')}")  # Output: 2

Removing Nodes
^^^^^^^^^^^^^^

.. code-block:: python

   # Remove node and its subtree
   tree.remove_node("B")  # Removes B, D, E
   
   print(f"New size: {len(tree)}")  # Output: 3
   print(list(tree))  # Output: ['A', 'C', 'F']
   
   # Clear entire tree
   tree.clear()
   print(tree.is_empty())  # Output: True

String Representation
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   tree = Tree("Root")
   tree.add_child("Child1")
   tree.add_child("Child2")
   tree.add_child_to("Child1", "Grandchild")
   
   print(repr(tree))
   # Output: Tree(size=4)
   
   print(str(tree))
   # Output:
   # Tree: Root
   #   ├─ Child1
   #   │  └─ Grandchild
   #   └─ Child2

Real-World Examples
===================

Example 1: File System
----------------------

Representing a directory structure:

.. code-block:: python

   from sds.tree import Tree

   # Create file system
   fs = Tree("/")
   
   # Add directories
   fs.add_child("home")
   fs.add_child("usr")
   fs.add_child("var")
   
   # Add subdirectories
   fs.add_child_to("home", "user1")
   fs.add_child_to("home", "user2")
   fs.add_child_to("usr", "bin")
   fs.add_child_to("usr", "lib")
   
   # Add files (prefix with .)
   fs.add_child_to("user1", ".bashrc")
   fs.add_child_to("user1", ".profile")
   
   # Query structure
   print(f"Total items: {len(fs)}")
   print(f"Depth: {fs.height()}")
   print(f"home has {fs.degree('home')} items")
   
   # List all files
   files = [item for item in fs if item.startswith('.')]
   print(f"Files: {files}")

Example 2: Organization Chart
------------------------------

Company hierarchy:

.. code-block:: python

   from sds.tree import Tree

   # Build organization
   org = Tree("CEO")
   
   # C-level
   org.add_child("CTO")
   org.add_child("CFO")
   org.add_child("COO")
   
   # Engineering
   org.add_child_to("CTO", "VP Engineering")
   org.add_child_to("VP Engineering", "Dev Manager")
   org.add_child_to("VP Engineering", "QA Manager")
   
   # Finance
   org.add_child_to("CFO", "Controller")
   org.add_child_to("CFO", "Treasurer")
   
   # Operations
   org.add_child_to("COO", "Operations Manager")
   
   # Query org chart
   print(f"Total employees: {len(org)}")
   print(f"Org depth: {org.height()}")
   print(f"CTO reports: {org.degree('CTO')}")
   
   # Find manager
   parent = org.get_parent("Dev Manager")
   print(f"Dev Manager reports to: {parent.data}")
   
   # List all managers (non-leaf nodes)
   managers = [item for item in org if not org.is_leaf(item)]
   print(f"Managers: {managers}")

Example 3: XML/HTML Structure
------------------------------

Document tree:

.. code-block:: python

   from sds.tree import Tree

   # Build HTML structure
   doc = Tree("html")
   
   # Head section
   doc.add_child("head")
   doc.add_child_to("head", "title")
   doc.add_child_to("head", "meta")
   
   # Body section
   doc.add_child("body")
   doc.add_child_to("body", "header")
   doc.add_child_to("body", "main")
   doc.add_child_to("body", "footer")
   
   # Main content
   doc.add_child_to("main", "section")
   doc.add_child_to("section", "h1")
   doc.add_child_to("section", "p")
   doc.add_child_to("section", "ul")
   
   # List items
   doc.add_child_to("ul", "li")
   doc.add_child_to("ul", "li")
   doc.add_child_to("ul", "li")
   
   # Print structure
   print(doc)
   
   # Find all sections
   sections = [node for node in doc if node == "section"]
   
   # Count elements
   print(f"Total elements: {len(doc)}")

Example 4: Game Tree
--------------------

Decision tree for game AI:

.. code-block:: python

   from sds.tree import Tree

   # Build game decision tree
   game = Tree("Initial State")
   
   # Player 1 moves
   game.add_child("Move A")
   game.add_child("Move B")
   game.add_child("Move C")
   
   # Responses to Move A
   game.add_child_to("Move A", "Response A1")
   game.add_child_to("Move A", "Response A2")
   
   # Responses to Move B
   game.add_child_to("Move B", "Response B1")
   game.add_child_to("Move B", "Response B2")
   game.add_child_to("Move B", "Response B3")
   
   # Further moves
   game.add_child_to("Response A1", "Counter A1a")
   game.add_child_to("Response A1", "Counter A1b")
   
   # Analyze game tree
   print(f"Game tree depth: {game.height()}")
   print(f"Total game states: {len(game)}")
   print(f"Move A branches: {game.degree('Move A')}")
   
   # Find all leaf states (terminal positions)
   terminal_states = game.leaves()
   print(f"Terminal positions: {len(terminal_states)}")

Performance Characteristics
===========================

Time Complexity
---------------

.. list-table::
   :header-rows: 1
   :widths: 40 20 40

   * - Operation
     - Complexity
     - Notes
   * - ``add_child(data, parent)``
     - O(1)
     - Direct append to parent's children
   * - ``add_child_to(parent_data, child_data)``
     - O(n)
     - Must find parent node first
   * - ``remove_node(data)``
     - O(n)
     - Must find node
   * - ``find_node(data)``
     - O(n)
     - BFS traversal
   * - ``search(item)``
     - O(n)
     - Linear search
   * - ``height()``
     - O(n)
     - Must visit all nodes
   * - ``get_children(data)``
     - O(n)
     - Find node + O(1) return
   * - ``get_parent(data)``
     - O(n)
     - Find node + O(1) return
   * - ``degree(data)``
     - O(n)
     - Find node + O(1) count
   * - ``is_leaf(data)``
     - O(n)
     - Find node + O(1) check
   * - ``leaves()``
     - O(n)
     - Visit all nodes
   * - ``preorder_traversal()``
     - O(n)
     - Visit each node once
   * - ``postorder_traversal()``
     - O(n)
     - Visit each node once
   * - ``level_order_traversal()``
     - O(n)
     - BFS traversal
   * - ``clear()``
     - O(1)
     - Reset references
   * - ``__len__()``
     - O(1)
     - Cached size
   * - ``__contains__``
     - O(n)
     - Uses search

Space Complexity
----------------

* **Tree storage**: O(n) where n is the number of nodes
* **Each node**: O(1) + O(k) where k is the number of children
* **Total children storage**: O(n) across all nodes
* **Recursion stack**: O(h) where h is the height
  * Balanced tree: O(log n)
  * Unbalanced: O(n)

Implementation Details
======================

Internal Structure
------------------

The Tree uses TreeNode objects internally:

.. code-block:: python

   class Tree:
       def __init__(self, root_data):
           self._root = TreeNode(root_data)
           self._size = 1
       
       def add_child(self, data, parent=None):
           new_node = TreeNode(data)
           if parent is None:
               parent = self._root
           parent.add_child(new_node)
           self._size += 1
           return new_node

Each TreeNode maintains:
   * ``data``: The stored value
   * ``parent``: Reference to parent node
   * ``children``: List of child nodes

Memory Layout
-------------

.. code-block:: text

   Tree with multiple children:

   ┌─────────────────┐
   │  Tree           │
   ├─────────────────┤
   │ _root: ───────────┐
   │ _size: 7        │ │
   └─────────────────┘ │
                       │
                       ▼
   ┌─────────────────────────┐
   │  TreeNode: "Root"       │
   ├─────────────────────────┤
   │ parent: None            │
   │ children: [────┬────┬───]
   └──────────────┼─┼────┼───┘
                  │ │    │
         ┌────────┘ │    └────────┐
         ▼           ▼             ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐
   │ Child 1 │ │ Child 2 │ │ Child 3 │
   └─────────┘ └─────────┘ └─────────┘

Best Practices
==============

Do's
----

✅ **Use descriptive data**

.. code-block:: python

   # Good: Clear, meaningful names
   tree = Tree("Company")
   tree.add_child("Engineering")
   tree.add_child("Sales")

✅ **Check node existence before operations**

.. code-block:: python

   node = tree.find_node("target")
   if node:
       children = tree.get_children("target")
   else:
       print("Node not found")

✅ **Use appropriate traversal**

.. code-block:: python

   # Preorder: Process parent before children
   for item in tree.preorder_traversal():
       process_parent_first(item)
   
   # Postorder: Process children before parent
   for item in tree.postorder_traversal():
       process_children_first(item)
   
   # Level-order: Process by levels
   for item in tree.level_order_traversal():
       process_by_level(item)

Don'ts
------

❌ **Don't create circular references**

.. code-block:: python

   # Bad: Can create cycles
   # Don't manually manipulate node relationships

❌ **Don't modify during iteration**

.. code-block:: python

   # Bad: Modifying while iterating
   for item in tree:
       tree.remove_node(item)  # Dangerous!
   
   # Good: Collect then modify
   to_remove = list(tree)
   for item in to_remove:
       tree.remove_node(item)

❌ **Don't assume child order**

.. code-block:: python

   # Bad: Assuming specific order
   children = tree.get_children("parent")
   first = children[0]  # Order may not be guaranteed
   
   # Good: Search by property
   target = next((c for c in children 
                  if c.data.startswith("A")), None)

Common Pitfalls
===============

1. **Deep recursion on large trees**

.. code-block:: python

   import sys
   
   # Check recursion limit
   print(sys.getrecursionlimit())  # Default: 1000
   
   # Increase if needed
   if tree.height() > 900:
       sys.setrecursionlimit(tree.height() + 100)

2. **Forgetting to handle errors**

.. code-block:: python

   try:
       tree.add_child_to("NonExistent", "NewChild")
   except ValueError as e:
       print(f"Error: {e}")

3. **Memory with large trees**

.. code-block:: python

   # Clear when done
   large_tree.clear()
   large_tree = None

See Also
========

* :doc:`binary` - Binary tree structures
* :doc:`btree` - Multi-way search trees
* :doc:`../../guide/tree_structures/general` - User guide with theory

References
==========

.. [1] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Chapter 10
.. [2] Knuth, D. E. "The Art of Computer Programming, Volume 1", Section 2.3
.. [3] Aho, A. V., et al. "Data Structures and Algorithms", Chapter 4
