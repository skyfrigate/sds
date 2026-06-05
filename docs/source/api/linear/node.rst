.. _api_linear_node:

===================
Linear Node Classes
===================

.. currentmodule:: sds.linear.node

Overview
========

This module provides node implementations for linear data structures such as linked lists,
stacks, and queues. Each node type is optimized for its specific structure.

.. mermaid::

   classDiagram
       Node <|-- SimpleNode
       Node <|-- DoublyNode
       
       class Node {
           <<abstract>>
           +data: Any
           +parent: Node
           +_refs: List
       }
       
       class SimpleNode {
           +next: SimpleNode
           __init__(data, next_node)
       }
       
       class DoublyNode {
           +next: DoublyNode
           +prev: DoublyNode
           __init__(data, next_node, prev_node)
       }

Classes
=======

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   SimpleNode
   DoublyNode

Detailed Documentation
======================

SimpleNode
----------

.. autoclass:: SimpleNode
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: next
   .. autoproperty:: data

   .. rubric:: Inherited Properties

   .. attribute:: parent
      :type: Node | None

      Reference to parent node (inherited from Node).

   .. rubric:: Methods

   .. automethod:: __repr__
   .. automethod:: __str__

DoublyNode
----------

.. autoclass:: DoublyNode
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: next
   .. autoproperty:: prev
   .. autoproperty:: data

   .. rubric:: Inherited Properties

   .. attribute:: parent
      :type: Node | None

      Reference to parent node (inherited from Node).

   .. rubric:: Methods

   .. automethod:: __repr__
   .. automethod:: __str__

Usage Examples
==============

SimpleNode Examples
-------------------

Basic Usage
^^^^^^^^^^^

.. code-block:: python

   from sds.linear.node import SimpleNode

   # Create a simple node
   node = SimpleNode(42)
   print(node.data)      # 42
   print(node.next)      # None

   # Create a chain of nodes
   node3 = SimpleNode(3)
   node2 = SimpleNode(2, node3)
   node1 = SimpleNode(1, node2)

   # Traverse the chain
   current = node1
   while current is not None:
       print(current.data, end=' -> ')
       current = current.next
   # Output: 1 -> 2 -> 3 ->

Modifying Node Data
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Modify node data
   node = SimpleNode(42)
   node.data = 100
   print(node.data)  # 100

   # Modify next reference
   node.next = SimpleNode(200)
   print(node.next.data)  # 200

Building a Linked List
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Build a simple linked list
   head = SimpleNode(1)
   head.next = SimpleNode(2)
   head.next.next = SimpleNode(3)

   # Traverse and print
   current = head
   while current:
       print(current.data)
       current = current.next
   # Output:
   # 1
   # 2
   # 3

Inserting Nodes
^^^^^^^^^^^^^^^

.. code-block:: python

   # Insert at beginning
   new_head = SimpleNode(0, head)
   head = new_head

   # Insert in middle
   node1 = SimpleNode(1)
   node3 = SimpleNode(3)
   node1.next = node3

   # Insert node2 between node1 and node3
   node2 = SimpleNode(2, node3)
   node1.next = node2

   # Result: 1 -> 2 -> 3

DoublyNode Examples
-------------------

Basic Usage
^^^^^^^^^^^

.. code-block:: python

   from sds.linear.node import DoublyNode

   # Create a doubly linked node
   node = DoublyNode(42)
   print(node.data)      # 42
   print(node.next)      # None
   print(node.prev)      # None

Creating Bidirectional Chain
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Create nodes
   node1 = DoublyNode(1)
   node2 = DoublyNode(2)
   node3 = DoublyNode(3)

   # Link forward
   node1.next = node2
   node2.next = node3

   # Link backward
   node2.prev = node1
   node3.prev = node2

   # Traverse forward
   current = node1
   while current:
       print(current.data, end=' -> ')
       current = current.next
   # Output: 1 -> 2 -> 3 ->

   # Traverse backward
   current = node3
   while current:
       print(current.data, end=' <- ')
       current = current.prev
   # Output: 3 <- 2 <- 1 <-

Convenient Initialization
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Create with next and prev in one step
   node2 = DoublyNode(2)
   node1 = DoublyNode(1, next_node=node2)
   node3 = DoublyNode(3, prev_node=node2)

   # Set remaining links
   node2.prev = node1
   node2.next = node3

   # Now bidirectionally linked: 1 <-> 2 <-> 3

Inserting Nodes
^^^^^^^^^^^^^^^

.. code-block:: python

   # Insert in middle
   node1 = DoublyNode(1)
   node3 = DoublyNode(3)
   
   # Link 1 and 3
   node1.next = node3
   node3.prev = node1

   # Insert node2 between them
   node2 = DoublyNode(2)
   
   # Update links
   node2.next = node3
   node2.prev = node1
   node1.next = node2
   node3.prev = node2

   # Result: 1 <-> 2 <-> 3

Removing Nodes
^^^^^^^^^^^^^^

.. code-block:: python

   # Remove node2 from: 1 <-> 2 <-> 3
   node1.next = node3
   node3.prev = node1

   # node2 is now disconnected
   # Result: 1 <-> 3

Memory Layout
=============

SimpleNode Memory Structure
----------------------------

.. code-block:: text

   SimpleNode with next reference:

   ┌─────────────────┐
   │  SimpleNode     │
   ├─────────────────┤
   │ data: 42        │
   │ next:  ────────┼─> ┌─────────────────┐
   └─────────────────┘   │  SimpleNode     │
                         ├─────────────────┤
                         │ data: 100       │
                         │ next:  ────────┼─> None
                         └─────────────────┘

   Memory per SimpleNode:
   - data: 8 bytes (pointer to object)
   - next: 8 bytes (pointer to next node)
   - Total: ~16 bytes + object overhead

DoublyNode Memory Structure
----------------------------

.. code-block:: text

   DoublyNode with bidirectional links:

   ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
   │  DoublyNode     │    │  DoublyNode     │    │  DoublyNode     │
   ├─────────────────┤    ├─────────────────┤    ├─────────────────┤
   │ data: 1         │    │ data: 2         │    │ data: 3         │
   │ prev: None      │    │ prev: ◄─────────┼────┤ prev: ◄─────────┼──┐
   │ next:  ────────┼───>│ next:  ────────┼───>│ next: None      │  │
   └─────────────────┘    └────────┬────────┘    └─────────────────┘  │
          │                        │                      ▲            │
          └────────────────────────┘                      └────────────┘

   Memory per DoublyNode:
   - data: 8 bytes (pointer to object)
   - next: 8 bytes (pointer to next node)
   - prev: 8 bytes (pointer to previous node)
   - Total: ~24 bytes + object overhead

Comparison
==========

SimpleNode vs DoublyNode
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - Aspect
     - SimpleNode
     - DoublyNode
   * - **Memory**
     - 16 bytes per node
     - 24 bytes per node
   * - **Traversal**
     - Forward only
     - Both directions
   * - **Insertion**
     - O(1) if have prev node
     - O(1) always
   * - **Deletion**
     - O(1) if have prev node
     - O(1) always
   * - **Use Case**
     - Simple lists, stacks
     - Deques, LRU cache
   * - **Complexity**
     - Simpler to implement
     - More bookkeeping

When to Use Each
----------------

**Use SimpleNode when:**
   - Only forward traversal needed
   - Memory is constrained
   - Implementing stacks or queues
   - Building simple linked lists
   - Don't need backward references

**Use DoublyNode when:**
   - Need backward traversal
   - Implementing deques
   - Building LRU caches
   - Need O(1) insertion/deletion anywhere
   - Extra memory acceptable

Best Practices
==============

Do's
----

✅ **Use appropriate node type**

.. code-block:: python

   # Forward-only traversal → SimpleNode
   node = SimpleNode(data)
   
   # Bidirectional traversal → DoublyNode
   node = DoublyNode(data)

✅ **Maintain link consistency**

.. code-block:: python

   # Good: Update both directions for DoublyNode
   node1.next = node2
   node2.prev = node1
   
   # Bad: Only update one direction
   node1.next = node2  # node2.prev still None!

✅ **Check for None before traversal**

.. code-block:: python

   # Good: Safe traversal
   current = head
   while current is not None:
       print(current.data)
       current = current.next
   
   # Also good: Python idiom
   while current:
       print(current.data)
       current = current.next

Don'ts
------

❌ **Don't create circular references accidentally**

.. code-block:: python

   # Bad: Creates infinite loop
   node1 = SimpleNode(1)
   node2 = SimpleNode(2)
   node1.next = node2
   node2.next = node1  # Circular!
   
   # Traversal will loop forever
   current = node1
   while current:  # Never ends!
       current = current.next

❌ **Don't forget to update both links in DoublyNode**

.. code-block:: python

   # Bad: Inconsistent state
   node1.next = node2
   # Forgot: node2.prev = node1
   
   # Now backward traversal from node2 won't reach node1

❌ **Don't modify data during iteration**

.. code-block:: python

   # Dangerous: Modifying structure during traversal
   current = head
   while current:
       next_node = current.next
       # Delete current node somehow
       current = next_node

Common Patterns
===============

Stack Pattern (SimpleNode)
---------------------------

.. code-block:: python

   class SimpleStack:
       """Stack using SimpleNode."""
       
       def __init__(self):
           self.top = None
       
       def push(self, item):
           """Push item onto stack."""
           new_node = SimpleNode(item, self.top)
           self.top = new_node
       
       def pop(self):
           """Pop item from stack."""
           if self.top is None:
               raise IndexError("Pop from empty stack")
           
           data = self.top.data
           self.top = self.top.next
           return data
       
       def peek(self):
           """View top item."""
           if self.top is None:
               raise IndexError("Peek at empty stack")
           return self.top.data

   # Usage
   stack = SimpleStack()
   stack.push(1)
   stack.push(2)
   print(stack.pop())   # 2
   print(stack.peek())  # 1

Queue Pattern (SimpleNode)
---------------------------

.. code-block:: python

   class SimpleQueue:
       """Queue using SimpleNode."""
       
       def __init__(self):
           self.front = None
           self.rear = None
       
       def enqueue(self, item):
           """Add item to rear."""
           new_node = SimpleNode(item)
           
           if self.rear is None:
               self.front = self.rear = new_node
           else:
               self.rear.next = new_node
               self.rear = new_node
       
       def dequeue(self):
           """Remove item from front."""
           if self.front is None:
               raise IndexError("Dequeue from empty queue")
           
           data = self.front.data
           self.front = self.front.next
           
           if self.front is None:
               self.rear = None
           
           return data

   # Usage
   queue = SimpleQueue()
   queue.enqueue(1)
   queue.enqueue(2)
   print(queue.dequeue())  # 1

Deque Pattern (DoublyNode)
---------------------------

.. code-block:: python

   class SimpleDeque:
       """Deque using DoublyNode."""
       
       def __init__(self):
           self.front = None
           self.rear = None
       
       def add_front(self, item):
           """Add item to front."""
           new_node = DoublyNode(item)
           
           if self.front is None:
               self.front = self.rear = new_node
           else:
               new_node.next = self.front
               self.front.prev = new_node
               self.front = new_node
       
       def add_rear(self, item):
           """Add item to rear."""
           new_node = DoublyNode(item)
           
           if self.rear is None:
               self.front = self.rear = new_node
           else:
               new_node.prev = self.rear
               self.rear.next = new_node
               self.rear = new_node
       
       def remove_front(self):
           """Remove item from front."""
           if self.front is None:
               raise IndexError("Remove from empty deque")
           
           data = self.front.data
           self.front = self.front.next
           
           if self.front is None:
               self.rear = None
           else:
               self.front.prev = None
           
           return data
       
       def remove_rear(self):
           """Remove item from rear."""
           if self.rear is None:
               raise IndexError("Remove from empty deque")
           
           data = self.rear.data
           self.rear = self.rear.prev
           
           if self.rear is None:
               self.front = None
           else:
               self.rear.next = None
           
           return data

   # Usage
   deque = SimpleDeque()
   deque.add_front(2)
   deque.add_front(1)
   deque.add_rear(3)
   print(deque.remove_front())  # 1
   print(deque.remove_rear())   # 3

Common Pitfalls
===============

1. **Forgetting to update both links**

.. code-block:: python

   # Wrong: Only forward link
   node1.next = node2
   
   # Correct: Both links for DoublyNode
   node1.next = node2
   node2.prev = node1

2. **Creating memory leaks**

.. code-block:: python

   # In languages with manual memory management,
   # remember to clean up references
   # Python handles this with garbage collection

3. **Not handling empty cases**

.. code-block:: python

   # Always check for None
   if head is not None:
       # Safe to access head.next

See Also
========

* :doc:`interfaces` - Abstract linked list interface
* :doc:`list` - Concrete linked list implementations
* :doc:`../../guide/linear_structures/linked_list` - Linked list guide

References
==========

.. [1] Knuth, D. E. "The Art of Computer Programming, Volume 1", Section 2.2
.. [2] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Chapter 10
.. [3] Sedgewick, R., Wayne, K. "Algorithms", 4th Edition, Section 1.3
