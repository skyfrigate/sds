.. _api_tree_interfaces:

===============
Tree Interfaces
===============

.. currentmodule:: sds.tree.interfaces

Overview
========

This module defines the abstract base classes (interfaces) for all tree data structures
in the SDS library. These interfaces ensure a consistent API across different tree
implementations and provide a foundation for polymorphic tree operations.

.. mermaid::

   classDiagram
       Collection <|-- AbstractTree
       AbstractTree <|-- AbstractBinaryTree
       AbstractTree <|-- AbstractSegmentTree
       
       class Collection {
           <<abstract>>
           +size: int
           +is_empty()
           +clear()
       }
       
       class AbstractTree {
           <<abstract>>
           +height()
           +insert(item)
           +remove(item)
           +search(item)
       }
       
       class AbstractBinaryTree {
           <<abstract>>
           +root: BinaryNode
           +inorder_traversal()
           +preorder_traversal()
           +postorder_traversal()
           +level_order_traversal()
       }
       
       class AbstractSegmentTree {
           <<abstract>>
           +query(left, right)
           +update(index, value)
           +get(index)
       }

Classes
=======

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   AbstractTree
   AbstractBinaryTree
   AbstractSegmentTree

Detailed Documentation
======================

AbstractTree
------------

.. autoclass:: AbstractTree
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __len__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: size

   .. rubric:: Abstract Methods

   .. automethod:: height
   .. automethod:: insert
   .. automethod:: remove
   .. automethod:: search

   .. rubric:: Concrete Methods

   .. automethod:: __len__
   .. automethod:: is_empty

AbstractBinaryTree
------------------

.. autoclass:: AbstractBinaryTree
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: root

   .. rubric:: Abstract Methods

   .. automethod:: inorder_traversal
   .. automethod:: preorder_traversal
   .. automethod:: postorder_traversal
   .. automethod:: level_order_traversal

AbstractSegmentTree
-------------------

.. autoclass:: AbstractSegmentTree
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __getitem__, __setitem__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: size

   .. rubric:: Abstract Methods

   .. automethod:: query
   .. automethod:: update
   .. automethod:: get
   .. automethod:: to_array

   .. rubric:: Special Methods

   .. automethod:: __getitem__
   .. automethod:: __setitem__

Usage Examples
==============

Implementing Custom Trees
--------------------------

Using AbstractBinaryTree:

.. code-block:: python

   from sds.tree.interfaces import AbstractBinaryTree
   from sds.tree.node import BinaryNode
   from typing import Any, Iterator

   class MyBinaryTree(AbstractBinaryTree):
       """Custom binary tree implementation."""
       
       def __init__(self):
           super().__init__()
           self._root = None
       
       def height(self) -> int:
           """Implement height calculation."""
           return self._height_recursive(self._root)
       
       def _height_recursive(self, node):
           if node is None:
               return -1
           left_h = self._height_recursive(node.left)
           right_h = self._height_recursive(node.right)
           return 1 + max(left_h, right_h)
       
       def insert(self, item: Any) -> None:
           """Implement insertion logic."""
           # Custom insertion implementation
           pass
       
       def remove(self, item: Any) -> Any:
           """Implement removal logic."""
           # Custom removal implementation
           pass
       
       def search(self, item: Any) -> bool:
           """Implement search logic."""
           # Custom search implementation
           pass
       
       def inorder_traversal(self) -> Iterator[Any]:
           """Implement inorder traversal."""
           yield from self._inorder_recursive(self._root)
       
       def _inorder_recursive(self, node):
           if node:
               yield from self._inorder_recursive(node.left)
               yield node.data
               yield from self._inorder_recursive(node.right)
       
       # Implement other abstract methods...

Polymorphic Tree Operations
----------------------------

Working with any tree type:

.. code-block:: python

   from sds.tree.interfaces import AbstractTree
   from typing import List

   def tree_statistics(tree: AbstractTree) -> dict:
       """Get statistics for any tree type."""
       return {
           'size': tree.size,
           'height': tree.height(),
           'is_empty': tree.is_empty()
       }
   
   def contains_all(tree: AbstractTree, items: List[Any]) -> bool:
       """Check if tree contains all items."""
       return all(tree.search(item) for item in items)
   
   def tree_to_sorted_list(tree: AbstractBinaryTree) -> List[Any]:
       """Convert binary tree to sorted list via inorder traversal."""
       return list(tree.inorder_traversal())

Type-Safe Tree Processing
--------------------------

Using type hints with interfaces:

.. code-block:: python

   from sds.tree.interfaces import AbstractBinaryTree
   from typing import TypeVar, Generic

   T = TypeVar('T')

   class TreeProcessor(Generic[T]):
       """Process trees in a type-safe manner."""
       
       def __init__(self, tree: AbstractBinaryTree):
           self.tree = tree
       
       def find_depth(self, item: T) -> int:
           """Find depth of item in tree."""
           def search(node, depth):
               if node is None:
                   return -1
               if node.data == item:
                   return depth
               left = search(node.left, depth + 1)
               if left != -1:
                   return left
               return search(node.right, depth + 1)
           
           return search(self.tree.root, 0)
       
       def collect_leaves(self) -> List[T]:
           """Collect all leaf nodes."""
           leaves = []
           
           def traverse(node):
               if node is None:
                   return
               if node.is_leaf():
                   leaves.append(node.data)
               else:
                   traverse(node.left)
                   traverse(node.right)
           
           traverse(self.tree.root)
           return leaves

Interface Hierarchy
===================

The tree interface hierarchy follows this structure:

.. code-block:: text

   Collection (from core)
       â"‚
       â""â"€â"€ AbstractTree
           â"œâ"€â"€ AbstractBinaryTree
           â"‚   â"œâ"€â"€ BinaryTree
           â"‚   â"œâ"€â"€ BinarySearchTree
           â"‚   â"œâ"€â"€ AVLTree
           â"‚   â""â"€â"€ RedBlackTree
           â"‚
           â"œâ"€â"€ Tree (General)
           â"œâ"€â"€ BTree
           â""â"€â"€ Trie
       
       AbstractSegmentTree
           â""â"€â"€ SegmentTree

Method Requirements
===================

AbstractTree Methods
--------------------

All concrete tree classes must implement:

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Method
     - Required
     - Purpose
   * - ``height()``
     - Yes
     - Return tree height
   * - ``insert(item)``
     - Yes
     - Add item to tree
   * - ``remove(item)``
     - Yes
     - Remove item from tree
   * - ``search(item)``
     - Yes
     - Check if item exists
   * - ``clear()``
     - Yes
     - Remove all items
   * - ``size``
     - No
     - Inherited property
   * - ``is_empty()``
     - No
     - Inherited method

AbstractBinaryTree Methods
---------------------------

Binary tree classes must additionally implement:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Method
     - Purpose
   * - ``inorder_traversal()``
     - Visit left-root-right
   * - ``preorder_traversal()``
     - Visit root-left-right
   * - ``postorder_traversal()``
     - Visit left-right-root
   * - ``level_order_traversal()``
     - Visit level by level (BFS)

Design Patterns
===============

Template Method Pattern
-----------------------

The abstract classes define the template, concrete classes fill in the details:

.. code-block:: python

   # Template (in AbstractTree)
   def __len__(self) -> int:
       """Template method - always works the same way."""
       return self._size
   
   def is_empty(self) -> bool:
       """Template method - built on __len__."""
       return self._size == 0
   
   # Concrete classes only implement specifics
   class BinarySearchTree(AbstractBinaryTree):
       def insert(self, item):
           """Specific to BST: maintains order."""
           # BST-specific insertion logic

Strategy Pattern
----------------

Different traversal strategies for binary trees:

.. code-block:: python

   from enum import Enum

   class TraversalStrategy(Enum):
       INORDER = "inorder"
       PREORDER = "preorder"
       POSTORDER = "postorder"
       LEVELORDER = "levelorder"
   
   def traverse_tree(tree: AbstractBinaryTree, 
                     strategy: TraversalStrategy):
       """Traverse using selected strategy."""
       strategies = {
           TraversalStrategy.INORDER: tree.inorder_traversal,
           TraversalStrategy.PREORDER: tree.preorder_traversal,
           TraversalStrategy.POSTORDER: tree.postorder_traversal,
           TraversalStrategy.LEVELORDER: tree.level_order_traversal
       }
       return list(strategies[strategy]())

Best Practices
==============

Interface Implementation
------------------------

✅ **Always call super().__init__()**

.. code-block:: python

   class MyTree(AbstractTree):
       def __init__(self):
           super().__init__()  # Initialize _size
           # Your initialization

✅ **Update size consistently**

.. code-block:: python

   def insert(self, item):
       # ... insertion logic ...
       self._size += 1
   
   def remove(self, item):
       # ... removal logic ...
       self._size -= 1

✅ **Implement all abstract methods**

.. code-block:: python

   # MyPy will catch missing methods
   class IncompleteTree(AbstractTree):
       # Missing height(), insert(), etc.
       pass  # Type error!

Using Interfaces
----------------

✅ **Program to interfaces, not implementations**

.. code-block:: python

   # Good: Flexible, works with any tree
   def process_tree(tree: AbstractTree):
       if not tree.is_empty():
           # Process...
   
   # Less flexible: Tied to specific type
   def process_bst(tree: BinarySearchTree):
       # Only works with BST

✅ **Use type hints for clarity**

.. code-block:: python

   from typing import Optional
   
   def find_in_tree(tree: AbstractTree, 
                    item: Any) -> bool:
       """Type-safe tree search."""
       return tree.search(item)

Common Patterns
===============

Visitor Pattern for Trees
--------------------------

.. code-block:: python

   from abc import ABC, abstractmethod

   class TreeVisitor(ABC):
       """Abstract visitor for tree nodes."""
       
       @abstractmethod
       def visit(self, node):
           pass
   
   class SumVisitor(TreeVisitor):
       """Sum all numeric values in tree."""
       
       def __init__(self):
           self.total = 0
       
       def visit(self, node):
           if isinstance(node.data, (int, float)):
               self.total += node.data
   
   def accept_visitor(tree: AbstractBinaryTree, 
                      visitor: TreeVisitor):
       """Apply visitor to all nodes."""
       def visit_node(node):
           if node:
               visitor.visit(node)
               visit_node(node.left)
               visit_node(node.right)
       
       visit_node(tree.root)

Iterator Pattern
----------------

.. code-block:: python

   class TreeIterator:
       """Custom iterator for trees."""
       
       def __init__(self, tree: AbstractBinaryTree,
                    traversal_type: str = "inorder"):
           self.tree = tree
           traversals = {
               "inorder": tree.inorder_traversal,
               "preorder": tree.preorder_traversal,
               "postorder": tree.postorder_traversal,
               "levelorder": tree.level_order_traversal
           }
           self._iterator = traversals[traversal_type]()
       
       def __iter__(self):
           return self
       
       def __next__(self):
           return next(self._iterator)

See Also
========

* :doc:`node` - Node implementations
* :doc:`binary` - Binary tree implementations
* :doc:`general` - General tree implementation
* :doc:`../../guide/tree_structures/index` - Tree structures guide

References
==========

.. [1] Gamma, E., et al. "Design Patterns: Elements of Reusable Object-Oriented Software", 1994
.. [2] Martin, R. C. "Clean Architecture", Chapter 11: DIP (Dependency Inversion Principle)
.. [3] Liskov, B. "Data Abstraction and Hierarchy", OOPSLA '87
