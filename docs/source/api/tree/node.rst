.. _api_tree_node:

=================
Tree Node Classes
=================

.. currentmodule:: sds.tree.node

Overview
========

This module provides node implementations for tree data structures. Each node type
is optimized for its specific tree structure, from simple binary nodes to complex
B-Tree nodes with multiple keys and children.

.. mermaid::

   classDiagram
       Node <|-- BinaryNode
       Node <|-- TreeNode
       Node <|-- TrieNode
       BinaryNode <|-- AVLNode
       BinaryNode <|-- RedBlackNode
       Node <|-- BTreeNode
       
       class Node {
           +data: Any
           +parent: Node
       }
       
       class BinaryNode {
           +left: BinaryNode
           +right: BinaryNode
       }
       
       class TreeNode {
           +children: List[TreeNode]
       }
       
       class AVLNode {
           +height: int
       }
       
       class RedBlackNode {
           +color: str
       }

Classes
=======

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   BinaryNode
   TreeNode
   BTreeNode
   TrieNode
   AVLNode
   RedBlackNode

Detailed Documentation
======================

BinaryNode
----------

.. autoclass:: BinaryNode
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: left
   .. autoproperty:: right

   .. rubric:: Methods

   .. automethod:: is_leaf

TreeNode
--------

.. autoclass:: TreeNode
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: children

   .. rubric:: Methods

   .. automethod:: add_child
   .. automethod:: remove_child
   .. automethod:: is_leaf

BTreeNode
---------

.. autoclass:: BTreeNode
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: keys
   .. autoproperty:: children

   .. rubric:: Methods

   .. automethod:: add_child
   .. automethod:: remove_child
   .. automethod:: is_full
   .. automethod:: is_minimal
   .. automethod:: insert_key
   .. automethod:: remove_key
   .. automethod:: find_key_index

TrieNode
--------

.. autoclass:: TrieNode
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: children

AVLNode
-------

.. autoclass:: AVLNode
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Attributes

   .. attribute:: height
      :type: int

      The height of the subtree rooted at this node.

RedBlackNode
------------

.. autoclass:: RedBlackNode
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Attributes

   .. attribute:: color
      :type: str

      The color of the node ("RED" or "BLACK").

Usage Examples
==============

BinaryNode Examples
-------------------

Basic binary node operations:

.. code-block:: python

   from sds.tree.node import BinaryNode

   # Create a simple binary tree
   root = BinaryNode(10)
   root.left = BinaryNode(5)
   root.right = BinaryNode(15)
   root.left.left = BinaryNode(3)
   root.left.right = BinaryNode(7)

   # Access and modify
   print(root.data)           # Output: 10
   print(root.left.data)      # Output: 5
   print(root.left.is_leaf()) # Output: False

   # Parent references are automatic
   print(root.left.parent is root)  # Output: True

TreeNode Examples
-----------------

General tree with variable children:

.. code-block:: python

   from sds.tree.node import TreeNode

   # Create a tree structure
   root = TreeNode("CEO")
   cto = TreeNode("CTO")
   cfo = TreeNode("CFO")

   root.add_child(cto)
   root.add_child(cfo)

   # Add more levels
   dev_lead = TreeNode("Dev Lead")
   cto.add_child(dev_lead)

   # Check structure
   print(len(root.children))     # Output: 2
   print(cto.parent is root)     # Output: True
   print(dev_lead.is_leaf())     # Output: True

   # Remove child
   root.remove_child(cfo)
   print(len(root.children))     # Output: 1

BTreeNode Examples
------------------

B-Tree node with multiple keys:

.. code-block:: python

   from sds.tree.node import BTreeNode

   # Create a B-Tree node (t=3)
   node = BTreeNode(t=3)

   # Add keys
   node.keys = [10, 20, 30]
   print(node.is_full())      # Output: False (max is 2*3-1 = 5)
   print(node.is_minimal())   # Output: True (min is 3-1 = 2)

   # Find key index
   idx = node.find_key_index(25)
   print(idx)                 # Output: 2 (between 20 and 30)

   # Internal node with children
   parent = BTreeNode(t=3, is_leaf=False)
   parent.keys = [50]
   
   left = BTreeNode(t=3)
   left.keys = [10, 20, 30]
   right = BTreeNode(t=3)
   right.keys = [60, 70, 80]
   
   parent.add_child(left)
   parent.add_child(right)
   
   print(len(parent.children))  # Output: 2

TrieNode Examples
-----------------

Trie node for prefix trees:

.. code-block:: python

   from sds.tree.node import TrieNode

   # Build a simple trie
   root = TrieNode()
   
   # Add "cat"
   root.children['c'] = TrieNode()
   root.children['c'].children['a'] = TrieNode()
   root.children['c'].children['a'].children['t'] = TrieNode()
   root.children['c'].children['a'].children['t'].is_end_of_word = True

   # Check structure
   print('c' in root.children)           # Output: True
   print(len(root.children))             # Output: 1
   
   # Navigate
   node = root.children['c'].children['a'].children['t']
   print(node.is_end_of_word)            # Output: True

AVLNode Examples
----------------

AVL node with height tracking:

.. code-block:: python

   from sds.tree.node import AVLNode

   # Create AVL nodes
   root = AVLNode(10)
   root.left = AVLNode(5)
   root.right = AVLNode(15)

   # Height must be maintained by tree operations
   root.height = 1
   root.left.height = 0
   root.right.height = 0

   print(root.height)        # Output: 1
   print(root.left.height)   # Output: 0

RedBlackNode Examples
---------------------

Red-Black node with color attribute:

.. code-block:: python

   from sds.tree.node import RedBlackNode

   # Create Red-Black nodes
   root = RedBlackNode(10, color="BLACK")
   root.left = RedBlackNode(5, color="RED")
   root.right = RedBlackNode(15, color="RED")

   print(root.color)         # Output: BLACK
   print(root.left.color)    # Output: RED

   # Change color
   root.left.color = "BLACK"
   print(root.left.color)    # Output: BLACK

Memory Layout
=============

BinaryNode Memory Structure
----------------------------

.. code-block:: text

   BinaryNode with left and right children:

   â"Œâ"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"
   â"‚  BinaryNode  â"‚
   â"œâ"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"¤
   â"‚ data: 10     â"‚
   â"‚ parent: None â"‚
   â"‚ left:   â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"> â"Œâ"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"
   â"‚ right:  â"€â"€â"€â"€â"€â"€â"¬â"€â"€â"€â"€â"€> â"‚ data: 5  â"‚
   â""â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"˜    â"‚       â"‚ parent:â"€â"˜
                      â"‚       â""â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"˜
                      â"‚
                      â"‚       â"Œâ"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"
                      â""â"€â"€â"€â"€â"€â"€â"€> â"‚ data: 15 â"‚
                              â"‚ parent:â"€â"˜
                              â""â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"˜

TreeNode Memory Structure
--------------------------

.. code-block:: text

   TreeNode with multiple children:

   â"Œâ"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"
   â"‚    TreeNode      â"‚
   â"œâ"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"¤
   â"‚ data: "Root"     â"‚
   â"‚ children: [...]  â"‚
   â""â"€â"€â"€â"¬â"€â"€â"€â"€â"€â"€â"€â"€â"€â"¬â"€â"€â"€â"€â"€â"€â"˜
        â"‚          â"‚
        â"‚          â""â"€â"€â"€â"€â"€â"€â"€â"€â"€â"> â"Œâ"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"
        â"‚                      â"‚ data: "C"  â"‚
        â"‚                      â""â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"
        â"‚
        â""â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€> â"Œâ"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"
                             â"‚ data: "B"  â"‚
                             â""â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"

BTreeNode Memory Structure
---------------------------

.. code-block:: text

   BTreeNode with multiple keys and children:

   â"Œâ"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"
   â"‚      BTreeNode (t=3)      â"‚
   â"œâ"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"¤
   â"‚ keys: [20, 40, 60]        â"‚
   â"‚ is_leaf: False            â"‚
   â"‚ children: [4 nodes]       â"‚
   â""â"€â"¬â"€â"€â"€â"¬â"€â"€â"€â"¬â"€â"€â"€â"¬â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"˜
      â"‚   â"‚   â"‚   â"‚
      â"‚   â"‚   â"‚   â""â"€â"€â"€> [70, 80, 90]
      â"‚   â"‚   â""â"€â"€â"€â"€â"€â"€> [50, 55]
      â"‚   â""â"€â"€â"€â"€â"€â"€â"€â"€â"€> [25, 30, 35]
      â""â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€â"€> [5, 10, 15]

Best Practices
==============

Do's
----

✅ **Use appropriate node type**

.. code-block:: python

   # Binary structure → BinaryNode
   binary_node = BinaryNode(10)
   
   # Variable children → TreeNode
   tree_node = TreeNode("root")
   
   # Multiple keys → BTreeNode
   btree_node = BTreeNode(t=3)

✅ **Let parent references auto-update**

.. code-block:: python

   # Good: Parent updates automatically
   parent = BinaryNode(10)
   child = BinaryNode(5)
   parent.left = child
   assert child.parent is parent

✅ **Check leaf status before accessing children**

.. code-block:: python

   if not node.is_leaf():
       process_children(node.left, node.right)

Don'ts
------

❌ **Don't create circular references manually**

.. code-block:: python

   # Bad: Causes circular reference
   node1 = BinaryNode(1)
   node2 = BinaryNode(2)
   node1.left = node2
   node2.left = node1  # Circular!

❌ **Don't mix node types**

.. code-block:: python

   # Bad: Type mismatch
   tree_node = TreeNode("root")
   tree_node.add_child(BinaryNode(10))  # Wrong type!

❌ **Don't modify parent references directly**

.. code-block:: python

   # Bad: Breaks consistency
   node._parent = some_other_node
   
   # Good: Use proper assignment
   parent.left = node

See Also
========

* :doc:`interfaces` - Abstract interfaces for trees
* :doc:`binary` - Binary tree implementations
* :doc:`general` - General tree implementation
* :doc:`btree` - B-Tree implementation

References
==========

.. [1] Knuth, D. E. "The Art of Computer Programming, Volume 1", Section 2.3
.. [2] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Chapter 10
.. [3] Bayer, R., McCreight, E. "Organization and Maintenance of Large Ordered Indices", Acta Informatica, 1972
