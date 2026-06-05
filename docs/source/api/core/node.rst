.. _api_core_node:

====
Node
====

.. currentmodule:: sds.core.node

Abstract base class for all node types in SDS-Tools.

Class Definition
================

.. autoclass:: Node
   :members:
   :inherited-members:
   :special-members: __init__, __repr__, __str__
   :member-order: bysource

Overview
========

The ``Node`` class serves as the foundation for all node types used throughout
the library. It provides a unified interface and uses a flexible ``_refs`` list
to store references to other nodes.

Key Concepts
============

Generic Reference Storage
-------------------------

The ``_refs`` list allows different node types to store varying numbers of
references while maintaining a consistent interface:

.. code-block:: python

   # SimpleNode stores 1 reference
   simple_node._refs = [next_node]

   # DoublyNode stores 2 references
   doubly_node._refs = [next_node, prev_node]

   # TreeNode stores N children
   tree_node._refs = [child1, child2, child3, ...]

Memory Efficiency
-----------------

The class uses ``__slots__`` to minimize memory overhead:

.. code-block:: python

   class Node(ABC):
       __slots__ = ("_data", "_refs", "_parent")

This restricts the attributes that can be dynamically added to instances,
reducing memory usage per node.

Attributes
==========

.. attribute:: _data
   :type: Any

   The value stored in the node. Accessible via the :attr:`data` property.

.. attribute:: _refs
   :type: List[Optional[Node]]

   List of references to other nodes. The interpretation depends on the
   concrete subclass.

.. attribute:: _parent
   :type: Optional[Node]

   Reference to the parent node. Accessible via the :attr:`parent` property.

Properties
==========

data
----

.. autoattribute:: data
   :annotation:

Get or set the data stored in the node.

**Example:**

.. code-block:: python

   from sds.linear.node import SimpleNode

   node = SimpleNode(42)
   print(node.data)  # 42

   node.data = 100
   print(node.data)  # 100

parent
------

.. autoattribute:: parent
   :annotation:

Get or set the parent node reference.

**Example:**

.. code-block:: python

   from sds.tree.node import BinaryNode

   root = BinaryNode(10)
   child = BinaryNode(5)
   root.left = child

   print(child.parent is root)  # True

Abstract Methods
================

Concrete subclasses must implement these methods:

__repr__()
----------

.. automethod:: __repr__

Return a detailed string representation of the node.

**Implementation example:**

.. code-block:: python

   def __repr__(self) -> str:
       return f"SimpleNode({self._data!r})"

__str__()
---------

.. automethod:: __str__

Return a simple string representation of the node's data.

**Implementation example:**

.. code-block:: python

   def __str__(self) -> str:
       return str(self._data)

Subclass Implementation Guide
==============================

Creating a Custom Node Type
----------------------------

To create a new node type, inherit from ``Node`` and:

1. Call ``super().__init__(data)`` in your ``__init__``
2. Initialize ``_refs`` according to your needs
3. Implement ``__repr__`` and ``__str__``
4. Optionally create properties for accessing ``_refs`` elements

**Example - Binary Node:**

.. code-block:: python

   from typing import Optional
   from sds.core.node import Node

   class BinaryNode(Node):
       __slots__ = ()  # Inherits slots from Node

       def __init__(self, data, left=None, right=None):
           super().__init__(data)
           self._refs = [left, right]  # [left, right]

       @property
       def left(self) -> Optional['BinaryNode']:
           return self._refs[0]

       @left.setter
       def left(self, node: Optional['BinaryNode']):
           self._refs[0] = node
           if node is not None:
               node._parent = self

       @property
       def right(self) -> Optional['BinaryNode']:
           return self._refs[1]

       @right.setter
       def right(self, node: Optional['BinaryNode']):
           self._refs[1] = node
           if node is not None:
               node._parent = self

       def __repr__(self) -> str:
           return f"BinaryNode({self._data!r})"

       def __str__(self) -> str:
           return str(self._data)

Usage Patterns
==============

Basic Node Creation
-------------------

Nodes cannot be instantiated directly (abstract class):

.. code-block:: python

   from sds.core.node import Node

   # This will raise TypeError
   try:
       node = Node(42)
   except TypeError as e:
       print(e)  # Can't instantiate abstract class

Use concrete implementations instead:

.. code-block:: python

   from sds.linear.node import SimpleNode, DoublyNode

   # Create nodes
   simple = SimpleNode(42)
   doubly = DoublyNode(42)

Traversing Node Chains
----------------------

Example with singly linked nodes:

.. code-block:: python

   from sds.linear.node import SimpleNode

   # Build a chain
   node3 = SimpleNode(3)
   node2 = SimpleNode(2, node3)
   node1 = SimpleNode(1, node2)

   # Traverse
   current = node1
   while current is not None:
       print(current.data)
       current = current.next

Working with Parent References
-------------------------------

Example with tree nodes:

.. code-block:: python

   from sds.tree.node import BinaryNode

   root = BinaryNode(10)
   left_child = BinaryNode(5)
   right_child = BinaryNode(15)

   root.left = left_child    # Sets left_child.parent = root
   root.right = right_child  # Sets right_child.parent = root

   # Navigate up the tree
   print(left_child.parent.data)  # 10

Design Rationale
================

Why Abstract?
-------------

The ``Node`` class is abstract because:

1. **Interface Definition** - Ensures all node types provide ``__repr__`` and ``__str__``
2. **Flexibility** - Different structures need different reference patterns
3. **Type Safety** - Abstract methods enforce implementation in subclasses

Why _refs List?
---------------

Using a list for references provides:

1. **Uniformity** - All nodes use the same storage mechanism
2. **Flexibility** - Easy to extend to any number of references
3. **Memory Efficiency** - Single allocation for all references
4. **Simplicity** - Subclasses just define property accessors

Why __slots__?
--------------

Memory optimization is crucial for data structures:

.. code-block:: python

   # Without __slots__: ~152 bytes per instance
   # With __slots__:    ~56 bytes per instance

   # For 1,000,000 nodes: ~96 MB savings!

Performance Considerations
==========================

.. list-table:: Node Operations Complexity
   :header-rows: 1
   :widths: 40 30 30

   * - Operation
     - Time Complexity
     - Space Complexity
   * - Create node
     - O(1)
     - O(1)
   * - Access data
     - O(1)
     - O(1)
   * - Access reference
     - O(1)
     - O(1)
   * - Set reference
     - O(1)
     - O(1)

See Also
========

* :doc:`interfaces` - Abstract collection interfaces
* :doc:`../linear/node` - Concrete linear node implementations
* :doc:`../tree/node` - Concrete tree node implementations
* :doc:`../graphs/node` - Concrete graph node implementations

.. note::

   The ``Node`` class is designed to be extended, not used directly.
   Always use concrete implementations like ``SimpleNode``, ``DoublyNode``,
   or create your own subclass.