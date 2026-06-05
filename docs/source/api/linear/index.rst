.. _api_linear:

==============================
Linear Structures (sds.linear)
==============================

.. currentmodule:: sds.linear

Linear data structures organize elements in a sequential manner, where each element 
(except the first and last) has exactly one predecessor and one successor.

Overview
========

The linear module provides implementations of fundamental sequential data structures:

* **Linked Lists** - Singly, doubly, and circular linked lists
* **Stacks** - LIFO (Last In First Out) structures
* **Queues** - FIFO (First In First Out) structures
* **Deques** - Double-ended queues
* **Priority Queues** - Queues with priority-based ordering

Key Features
============

✓ **Flexible insertion/deletion** - O(1) at beginning/end for most structures
✓ **Dynamic size** - No pre-allocation needed
✓ **Iterator support** - Pythonic iteration over elements
✓ **Type hints** - Full type annotation support
✓ **Consistent API** - Uniform interface across all linear structures

Module Contents
===============

Node Classes
------------

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   SimpleNode
   DoublyNode

Linked List Structures
-----------------------

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   LinkedList
   DoublyLinkedList
   CircularLinkedList

Stack and Queue Structures
---------------------------

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   Stack
   Queue
   Deque
   PriorityQueue

Detailed Documentation
======================

.. toctree::
   :maxdepth: 2

   interfaces
   node
   list
   stack
   queue

Structure Comparison
====================

.. list-table:: Linear Structure Comparison
   :header-rows: 1
   :widths: 20 15 15 15 35

   * - Structure
     - Insert (front)
     - Insert (back)
     - Access
     - Best Use Case
   * - **LinkedList**
     - O(1)
     - O(n)
     - O(n)
     - Frequent front insertions
   * - **DoublyLinkedList**
     - O(1)
     - O(1)
     - O(n)
     - Bidirectional traversal
   * - **CircularLinkedList**
     - O(1)
     - O(1)
     - O(n)
     - Round-robin scheduling
   * - **Stack**
     - O(1)
     - N/A
     - O(1) top
     - LIFO operations
   * - **Queue**
     - N/A
     - O(n)
     - O(1) front
     - FIFO operations
   * - **Deque**
     - O(1)
     - O(1)
     - O(1) ends
     - Both-end operations
   * - **PriorityQueue**
     - O(n)
     - O(n)
     - O(1) min
     - Priority-based processing

Quick Start Examples
====================

Linked Lists
------------

.. code-block:: python

   from sds.linear import LinkedList, DoublyLinkedList, CircularLinkedList

   # Singly linked list
   lst = LinkedList()
   lst.append(1)
   lst.append(2)
   lst.prepend(0)
   print(list(lst))  # [0, 1, 2]

   # Doubly linked list (bidirectional)
   dll = DoublyLinkedList()
   dll.append(1)
   dll.append(2)
   print(list(reversed(dll)))  # [2, 1]

   # Circular linked list (with rotation)
   cll = CircularLinkedList()
   cll.append(1)
   cll.append(2)
   cll.append(3)
   cll.rotate(1)
   print(list(cll))  # [2, 3, 1]

Stacks
------

.. code-block:: python

   from sds.linear import Stack

   # LIFO stack
   stack = Stack()
   stack.push(1)
   stack.push(2)
   stack.push(3)
   
   print(stack.pop())   # 3
   print(stack.peek())  # 2
   print(len(stack))    # 2

Queues
------

.. code-block:: python

   from sds.linear import Queue, Deque, PriorityQueue

   # FIFO queue
   queue = Queue()
   queue.enqueue(1)
   queue.enqueue(2)
   print(queue.dequeue())  # 1

   # Double-ended queue
   deque = Deque()
   deque.add_front(1)
   deque.add_rear(2)
   print(deque.remove_front())  # 1

   # Priority queue (min-heap)
   pq = PriorityQueue()
   pq.enqueue(5)
   pq.enqueue(1)
   pq.enqueue(3)
   print(pq.dequeue())  # 1

Visual Representation
=====================

.. mermaid::

   graph LR
       subgraph "Singly Linked List"
       A1[1] --> B1[2]
       B1 --> C1[3]
       C1 --> D1[None]
       end

       subgraph "Doubly Linked List"
       A2[1] <--> B2[2]
       B2 <--> C2[3]
       end

       subgraph "Circular Linked List"
       A3[1] --> B3[2]
       B3 --> C3[3]
       C3 --> A3
       end

       style A1 fill:#e74c3c
       style A2 fill:#3498db
       style A3 fill:#2ecc71

Common Operations
=================

Insertion
---------

.. code-block:: python

   # At beginning (prepend)
   lst.prepend(0)  # O(1) for all list types
   
   # At end (append)
   lst.append(4)   # O(n) for LinkedList, O(1) for others
   
   # At index
   lst.insert_at(2, 99)  # O(n)

Removal
-------

.. code-block:: python

   # From beginning
   lst.remove_first()  # O(1)
   
   # From end
   lst.remove_last()   # O(n) for LinkedList, O(1) for DoublyLinkedList
   
   # By value
   lst.remove(99)      # O(n)
   
   # By index
   lst.remove_at(2)    # O(n)

Access
------

.. code-block:: python

   # By index (read/write)
   value = lst[2]      # O(n)
   lst[2] = 100        # O(n)
   
   # Search
   index = lst.find(99)  # O(n), returns -1 if not found
   
   # Contains
   if 99 in lst:       # O(n)
       print("Found!")

Traversal
---------

.. code-block:: python

   # Forward iteration
   for item in lst:
       print(item)
   
   # Backward iteration (DoublyLinkedList only)
   for item in reversed(dll):
       print(item)

When to Use Each Structure
===========================

Decision Guide
--------------

.. mermaid::

   graph TD
       A{What operation is most frequent?}
       
       A -->|Insert/delete at ends| B{Need both ends?}
       B -->|Yes| C[Deque]
       B -->|No| D{Which end?}
       D -->|Front only| E[Stack]
       D -->|Back only| F[Queue]
       
       A -->|Insert/delete anywhere| G{Need backward traversal?}
       G -->|Yes| H[DoublyLinkedList]
       G -->|No| I[LinkedList]
       
       A -->|Circular operations| J[CircularLinkedList]
       A -->|Priority-based| K[PriorityQueue]

       style C fill:#e74c3c
       style E fill:#3498db
       style F fill:#f39c12
       style H fill:#9b59b6
       style I fill:#27ae60
       style J fill:#e67e22
       style K fill:#1abc9c

Use Cases
---------

**LinkedList**: Browser history, undo functionality, music playlists

**DoublyLinkedList**: LRU cache, text editors, navigation systems

**CircularLinkedList**: Round-robin scheduling, buffer management

**Stack**: Expression evaluation, backtracking, function calls

**Queue**: Task scheduling, breadth-first search, print spooler

**Deque**: Palindrome checking, sliding window problems

**PriorityQueue**: Dijkstra's algorithm, event simulation, A* search

Performance Guidelines
======================

Time Complexity Summary
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 25 15 15 15 30

   * - Operation
     - LinkedList
     - DoublyLinkedList
     - CircularLinkedList
     - Notes
   * - ``prepend()``
     - O(1)
     - O(1)
     - O(1)
     - Always fast
   * - ``append()``
     - O(n)
     - O(1)
     - O(1)
     - LinkedList has no tail
   * - ``remove_first()``
     - O(1)
     - O(1)
     - O(1)
     - Always fast
   * - ``remove_last()``
     - O(n)
     - O(1)
     - O(n)
     - Need to traverse
   * - ``insert_at(i)``
     - O(n)
     - O(n)
     - O(n)
     - Must reach index
   * - ``remove_at(i)``
     - O(n)
     - O(n)
     - O(n)
     - Must reach index
   * - ``find(item)``
     - O(n)
     - O(n)
     - O(n)
     - Linear search
   * - ``__getitem__[i]``
     - O(n)
     - O(n/2)
     - O(n)
     - DoublyLinkedList optimized

Space Complexity
----------------

All linear structures have:

* **Storage**: O(n) for n elements
* **Per-node overhead**:
  - SimpleNode: 1 reference (next)
  - DoublyNode: 2 references (next, prev)
* **No contiguous memory**: Unlike arrays

Best Practices
==============

Do's
----

✅ **Choose the right structure for your access pattern**

.. code-block:: python

   # Frequent insertions at both ends → Deque
   deque = Deque()
   
   # Only LIFO operations → Stack
   stack = Stack()
   
   # Need backward traversal → DoublyLinkedList
   dll = DoublyLinkedList()

✅ **Use appropriate methods**

.. code-block:: python

   # Good: Use specialized methods
   stack.push(item)
   queue.enqueue(item)
   
   # Less clear: Generic add()
   stack.add(item)  # Works but less clear

✅ **Check emptiness before operations**

.. code-block:: python

   if not stack.is_empty():
       item = stack.pop()

Don'ts
------

❌ **Don't use linked lists for random access**

.. code-block:: python

   # Bad: O(n) for each access
   for i in range(len(lst)):
       print(lst[i])
   
   # Good: O(n) total
   for item in lst:
       print(item)

❌ **Don't forget about space overhead**

.. code-block:: python

   # Linked lists use more memory than arrays
   # Each node has overhead for references

❌ **Don't mix LIFO/FIFO operations**

.. code-block:: python

   # Bad: Confusing semantics
   stack.push(1)
   stack.remove(1)  # Not LIFO!
   
   # Good: Stick to stack operations
   stack.push(1)
   stack.pop()

Common Pitfalls
===============

1. **Using wrong list type**

.. code-block:: python

   # If you need O(1) append, don't use LinkedList
   # Use DoublyLinkedList or CircularLinkedList instead

2. **Not considering traversal cost**

.. code-block:: python

   # Multiple index accesses are expensive
   # Cache results or use iteration instead

3. **Ignoring iterator performance**

.. code-block:: python

   # Good: Single pass
   for item in lst:
       process(item)
   
   # Bad: Multiple passes
   for i in range(len(lst)):
       process(lst[i])

Related Guides
==============

* :doc:`../../guide/linear_structures/index` - User guide for linear structures
* :doc:`../core/index` - Core abstractions
* :doc:`../tree/index` - Tree structures

See Also
========

External Resources
------------------

* `Wikipedia: Linked List <https://en.wikipedia.org/wiki/Linked_list>`_
* `VisuAlgo: Linked List <https://visualgo.net/en/list>`_
* `Python Data Structures <https://docs.python.org/3/tutorial/datastructures.html>`_

Academic References
-------------------

.. [1] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Chapter 10
.. [2] Knuth, D. E. "The Art of Computer Programming, Volume 1", Section 2.2
.. [3] Sedgewick, R., Wayne, K. "Algorithms", 4th Edition, Section 1.3
.. [4] Weiss, M. A. "Data Structures and Algorithm Analysis", Chapter 3
