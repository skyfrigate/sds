.. _api_tree_binary:

============
Binary Trees
============

.. currentmodule:: sds.tree.binary

Overview
========

This module provides implementations of binary tree structures, where each node has at most two children
(left and right). Includes both unordered binary trees and ordered binary search trees (BST).

.. mermaid::

   graph TB
       subgraph "Binary Tree"
       A[10] --> B[5]
       A --> C[15]
       B --> D[3]
       B --> E[7]
       end
       
       subgraph "Binary Search Tree"
       F[10] --> G[5]
       F --> H[15]
       G --> I[3]
       G --> J[7]
       H --> K[12]
       H --> L[20]
       end
       
       style A fill:#3498db
       style F fill:#e74c3c

Classes
=======

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   BinaryTree
   BinarySearchTree

Detailed Documentation
======================

BinaryTree
----------

.. autoclass:: BinaryTree
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

   .. automethod:: insert
   .. automethod:: remove
   .. automethod:: search
   .. automethod:: height

   .. rubric:: Traversal Methods

   .. automethod:: inorder_traversal
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

BinarySearchTree
----------------

.. autoclass:: BinarySearchTree
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

   .. automethod:: insert
   .. automethod:: remove
   .. automethod:: search
   .. automethod:: height
   .. automethod:: find_min
   .. automethod:: find_max

   .. rubric:: Traversal Methods

   .. automethod:: inorder_traversal
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

BinaryTree Examples
-------------------

Basic Operations
^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.tree import BinaryTree

   # Create and populate
   tree = BinaryTree()
   tree.insert(10)
   tree.insert(5)
   tree.insert(15)
   tree.insert(3)
   
   print(len(tree))      # Output: 4
   print(tree.height())  # Output: 2

Traversals
^^^^^^^^^^

.. code-block:: python

   tree = BinaryTree()
   for val in [10, 5, 15, 3, 7]:
       tree.insert(val)
   
   # Different traversal orders
   print(list(tree.inorder_traversal()))
   # Output: [3, 5, 7, 10, 15]
   
   print(list(tree.preorder_traversal()))
   # Output: [10, 5, 3, 7, 15]
   
   print(list(tree.level_order_traversal()))
   # Output: [10, 5, 15, 3, 7]

BinarySearchTree Examples
--------------------------

Ordered Insertion
^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.tree import BinarySearchTree

   bst = BinarySearchTree()
   
   # Insert maintains BST property
   for val in [50, 30, 70, 20, 40, 60, 80]:
       bst.insert(val)
   
   # Inorder gives sorted sequence
   print(list(bst.inorder_traversal()))
   # Output: [20, 30, 40, 50, 60, 70, 80]

Efficient Search
^^^^^^^^^^^^^^^^

.. code-block:: python

   bst = BinarySearchTree()
   for val in range(1, 100, 2):  # 1, 3, 5, ..., 99
       bst.insert(val)
   
   # O(log n) search in balanced tree
   print(bst.search(45))  # Output: True
   print(45 in bst)       # Output: True
   print(46 in bst)       # Output: False

Min/Max Operations
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   bst = BinarySearchTree()
   for val in [50, 30, 70, 20, 40, 60, 80]:
       bst.insert(val)
   
   print(bst.find_min())  # Output: 20
   print(bst.find_max())  # Output: 80

Removal
^^^^^^^

.. code-block:: python

   bst = BinarySearchTree()
   for val in [50, 30, 70, 20, 40, 60, 80]:
       bst.insert(val)
   
   # Remove maintains BST property
   bst.remove(30)
   print(list(bst.inorder_traversal()))
   # Output: [20, 40, 50, 60, 70, 80]

Real-World Applications
=======================

Application 1: Expression Tree
-------------------------------

Evaluating mathematical expressions:

.. code-block:: python

   from sds.tree import BinaryTree
   from sds.tree.node import BinaryNode

   class ExpressionTree(BinaryTree):
       """Binary tree for expression evaluation."""
       
       def build_from_postfix(self, postfix):
           """Build tree from postfix expression."""
           from sds.linear import Stack
           
           stack = Stack()
           operators = {'+', '-', '*', '/', '^'}
           
           for token in postfix.split():
               if token not in operators:
                   # Operand
                   node = BinaryNode(float(token))
                   stack.push(node)
               else:
                   # Operator
                   node = BinaryNode(token)
                   node.right = stack.pop()
                   node.left = stack.pop()
                   stack.push(node)
           
           self._root = stack.pop()
           self._size = self._count_nodes(self._root)
       
       def _count_nodes(self, node):
           """Count nodes in subtree."""
           if node is None:
               return 0
           return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)
       
       def evaluate(self):
           """Evaluate the expression tree."""
           return self._evaluate_recursive(self._root)
       
       def _evaluate_recursive(self, node):
           """Recursively evaluate expression."""
           if node is None:
               return 0
           
           # Leaf node (operand)
           if node.is_leaf():
               return node.data
           
           # Internal node (operator)
           left_val = self._evaluate_recursive(node.left)
           right_val = self._evaluate_recursive(node.right)
           
           if node.data == '+':
               return left_val + right_val
           elif node.data == '-':
               return left_val - right_val
           elif node.data == '*':
               return left_val * right_val
           elif node.data == '/':
               return left_val / right_val
           elif node.data == '^':
               return left_val ** right_val
   
   # Usage
   expr = ExpressionTree()
   expr.build_from_postfix("3 4 + 2 * 7 /")  # ((3+4)*2)/7
   result = expr.evaluate()
   print(f"Result: {result}")  # Output: 2.0

Application 2: File System Structure
-------------------------------------

Representing directory hierarchies:

.. code-block:: python

   from sds.tree import BinaryTree
   from sds.tree.node import BinaryNode

   class FileNode:
       """Represent a file or directory."""
       def __init__(self, name, is_dir=False, size=0):
           self.name = name
           self.is_dir = is_dir
           self.size = size  # bytes
       
       def __repr__(self):
           type_str = "DIR" if self.is_dir else "FILE"
           if self.is_dir:
               return f"{type_str}: {self.name}"
           return f"{type_str}: {self.name} ({self.size} bytes)"
   
   class FileSystem:
       """Simple file system using binary tree."""
       
       def __init__(self):
           self.tree = BinaryTree()
           # Root directory
           root = FileNode("root", is_dir=True)
           self.tree.insert(root)
       
       def calculate_total_size(self):
           """Calculate total size of all files."""
           total = 0
           
           def sum_sizes(node):
               nonlocal total
               if node and not node.data.is_dir:
                   total += node.data.size
           
           for node_data in self.tree.inorder_traversal():
               if not node_data.is_dir:
                   total += node_data.size
           
           return total
       
       def list_files(self, extension=None):
           """List all files, optionally filtered by extension."""
           files = []
           
           for node_data in self.tree.inorder_traversal():
               if not node_data.is_dir:
                   if extension is None or node_data.name.endswith(extension):
                       files.append(node_data)
           
           return files
   
   # Usage
   fs = FileSystem()
   fs.tree.insert(FileNode("document.txt", size=1024))
   fs.tree.insert(FileNode("image.png", size=2048))
   fs.tree.insert(FileNode("video.mp4", size=5120))
   
   print(f"Total size: {fs.calculate_total_size()} bytes")
   print(f"Text files: {len(fs.list_files('.txt'))}")

Application 3: Binary Decision Tree
------------------------------------

Decision-making with binary choices:

.. code-block:: python

   from sds.tree.node import BinaryNode

   class DecisionNode:
       """Node for decision tree."""
       def __init__(self, question=None, yes_outcome=None, no_outcome=None):
           self.question = question
           self.yes_outcome = yes_outcome
           self.no_outcome = no_outcome
           self.is_leaf = yes_outcome is None and no_outcome is None
       
       def __repr__(self):
           if self.is_leaf:
               return f"Outcome: {self.question}"
           return f"Question: {self.question}"
   
   class DecisionTree:
       """Binary decision tree for diagnostics/classification."""
       
       def __init__(self):
           self.root = None
       
       def build_sample_tree(self):
           """Build a sample troubleshooting tree."""
           # Build tree for computer troubleshooting
           self.root = BinaryNode(
               DecisionNode("Does the computer turn on?")
           )
           
           # Left branch (No)
           self.root.left = BinaryNode(
               DecisionNode("Is it plugged in?")
           )
           self.root.left.left = BinaryNode(
               DecisionNode("Plug it in!")
           )
           self.root.left.right = BinaryNode(
               DecisionNode("Check power supply")
           )
           
           # Right branch (Yes)
           self.root.right = BinaryNode(
               DecisionNode("Does it boot to OS?")
           )
           self.root.right.left = BinaryNode(
               DecisionNode("Check boot drive")
           )
           self.root.right.right = BinaryNode(
               DecisionNode("System is working!")
           )
       
       def diagnose(self):
           """Interactive diagnosis session."""
           current = self.root
           
           while current and not current.data.is_leaf:
               print(f"\n{current.data.question}")
               answer = input("(yes/no): ").strip().lower()
               
               if answer == 'yes':
                   current = current.right
               elif answer == 'no':
                   current = current.left
               else:
                   print("Please answer yes or no")
                   continue
           
           if current:
               print(f"\n{current.data.question}")
   
   # Usage
   tree = DecisionTree()
   tree.build_sample_tree()
   # tree.diagnose()  # Interactive session

Performance Characteristics
===========================

Time Complexity
---------------

BinaryTree (Unordered)
^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 20 20 20 30

   * - Operation
     - Best
     - Average
     - Worst
     - Notes
   * - ``insert()``
     - O(1)
     - O(n)
     - O(n)
     - Level-order insertion
   * - ``remove()``
     - O(1)
     - O(n)
     - O(n)
     - Must find node
   * - ``search()``
     - O(1)
     - O(n)
     - O(n)
     - Linear search
   * - ``height()``
     - O(n)
     - O(n)
     - O(n)
     - Must traverse
   * - Traversals
     - O(n)
     - O(n)
     - O(n)
     - Visit all nodes

BinarySearchTree (Ordered)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 20 20 20 30

   * - Operation
     - Best
     - Average
     - Worst
     - Notes
   * - ``insert()``
     - O(1)
     - O(log n)
     - O(n)
     - Degenerate tree
   * - ``remove()``
     - O(1)
     - O(log n)
     - O(n)
     - Degenerate tree
   * - ``search()``
     - O(1)
     - O(log n)
     - O(n)
     - Degenerate tree
   * - ``find_min/max()``
     - O(1)
     - O(log n)
     - O(n)
     - Leftmost/rightmost
   * - ``height()``
     - O(n)
     - O(n)
     - O(n)
     - Must traverse
   * - Inorder
     - O(n)
     - O(n)
     - O(n)
     - Sorted output

Space Complexity
----------------

* **Tree storage**: O(n) for n nodes
* **Recursion stack**: O(h) where h is height
  * Balanced: O(log n)
  * Degenerate: O(n)

Best Practices
==============

Do's
----

✅ **Use BST when order matters**

.. code-block:: python

   # Need sorted data → use BST
   bst = BinarySearchTree()
   for val in [50, 30, 70, 20, 40]:
       bst.insert(val)
   
   sorted_data = list(bst.inorder_traversal())

✅ **Check tree state before operations**

.. code-block:: python

   if not tree.is_empty():
       min_val = bst.find_min()

✅ **Use appropriate traversal**

.. code-block:: python

   # Copy tree structure → preorder
   # Get sorted data from BST → inorder
   # Delete tree → postorder
   # Level-by-level processing → level-order

Don'ts
------

❌ **Don't expect BST performance from unordered tree**

.. code-block:: python

   # Bad: BinaryTree has O(n) search
   tree = BinaryTree()
   tree.insert(50)
   tree.search(50)  # O(n), not O(log n)!
   
   # Good: Use BST for fast search
   bst = BinarySearchTree()
   bst.insert(50)
   bst.search(50)  # O(log n) average

❌ **Don't assume balanced tree**

.. code-block:: python

   # Worst case: insert sorted data into BST
   bst = BinarySearchTree()
   for i in range(1000):
       bst.insert(i)  # Creates degenerate tree!
   
   # Better: shuffle or use balanced tree
   import random
   data = list(range(1000))
   random.shuffle(data)
   for val in data:
       bst.insert(val)

See Also
========

* :doc:`balanced` - AVL and Red-Black trees (always balanced)
* :doc:`general` - Trees with more than 2 children
* :doc:`../../guide/tree_structures/binary` - Detailed guide

References
==========

.. [1] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Ed., Chapter 12
.. [2] Knuth, D. E. "The Art of Computer Programming, Vol. 1", Section 2.3
.. [3] Sedgewick, R., Wayne, K. "Algorithms", 4th Ed., Section 3.2
