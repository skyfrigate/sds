.. _guide_linear:

=================
Linear Structures
=================

Introduction
============

Linear data structures organize elements in a sequential manner where each element
(except the first and last) has exactly one predecessor and one successor.

.. mermaid::

   graph LR
       A[Element 1] --> B[Element 2]
       B --> C[Element 3]
       C --> D[Element 4]

       style A fill:#3498db
       style D fill:#e74c3c

This section covers all linear structures provided by SDS-Tools.

Overview
========

Types of Linear Structures
---------------------------

SDS-Tools provides several linear structures, each optimized for specific access patterns:

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Structure
     - Access Pattern
     - Primary Use Cases
   * - **Stack**
     - LIFO (Last-In-First-Out)
     - Function calls, undo operations, expression evaluation
   * - **Queue**
     - FIFO (First-In-First-Out)
     - Task scheduling, BFS, print queues
   * - **Deque**
     - Both ends
     - Sliding window, work stealing
   * - **Priority Queue**
     - By priority
     - Event simulation, Dijkstra's algorithm
   * - **Linked List**
     - Sequential
     - Dynamic insertion/deletion

Choosing the Right Structure
-----------------------------

.. mermaid::

   graph TD
       A{Access Pattern?}
       A -->|Last In First Out| B[Stack]
       A -->|First In First Out| C[Queue]
       A -->|Both Ends| D[Deque]
       A -->|By Priority| E[Priority Queue]
       A -->|Sequential with Insertion| F[Linked List]

       style B fill:#e74c3c
       style C fill:#3498db
       style D fill:#f39c12
       style E fill:#9b59b6
       style F fill:#27ae60

Detailed Guides
===============

.. toctree::
   :maxdepth: 2
   :caption: Stack (LIFO)

   stack

.. toctree::
   :maxdepth: 2
   :caption: Queue (FIFO)

   queue

.. toctree::
   :maxdepth: 2
   :caption: Other Structures

   dequeue
   priority_queue
   linked_list

Common Operations
=================

All linear structures in SDS share a consistent interface:

Basic Operations
----------------

.. code-block:: python

   from sds.linear import Stack, Queue

   # Creating structures
   stack = Stack()
   queue = Queue()

   # Adding elements
   stack.push(item)      # For Stack
   queue.enqueue(item)   # For Queue

   # Removing elements
   stack.pop()           # For Stack
   queue.dequeue()       # For Queue

   # Checking state
   len(structure)        # Get size
   structure.is_empty()  # Check if empty

   # Viewing without removing
   stack.peek()          # For Stack
   queue.front()         # For Queue

Comparison Matrix
=================

Performance Characteristics
---------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 15 15 20

   * - Operation
     - Stack
     - Queue
     - Deque
     - Priority Queue
     - Linked List
   * - Insert at end
     - O(1)
     - O(1)
     - O(1)
     - O(log n)
     - O(1)
   * - Insert at front
     - N/A
     - N/A
     - O(1)
     - N/A
     - O(1)
   * - Remove from end
     - O(1)
     - N/A
     - O(1)
     - N/A
     - O(1)*
   * - Remove from front
     - N/A
     - O(1)
     - O(1)
     - O(log n)
     - O(1)
   * - Access by index
     - N/A
     - N/A
     - N/A
     - N/A
     - O(n)
   * - Space complexity
     - O(n)
     - O(n)
     - O(n)
     - O(n)
     - O(n)

\* With tail pointer

Common Patterns
===============

Pattern 1: Processing in Reverse Order
---------------------------------------

Use a **Stack** when you need to process items in reverse order:

.. code-block:: python

   from sds.linear import Stack

   def reverse_process(items):
       stack = Stack()

       # Push all items
       for item in items:
           stack.push(item)

       # Process in reverse
       results = []
       while not stack.is_empty():
           results.append(process(stack.pop()))

       return results

Pattern 2: First-Come-First-Served
-----------------------------------

Use a **Queue** for fair ordering:

.. code-block:: python

   from sds.linear import Queue

   class TaskScheduler:
       def __init__(self):
           self.queue = Queue()

       def add_task(self, task):
           self.queue.enqueue(task)

       def process_next(self):
           if not self.queue.is_empty():
               task = self.queue.dequeue()
               task.execute()

Pattern 3: Sliding Window
--------------------------

Use a **Deque** for efficient sliding window operations:

.. code-block:: python

   from sds.linear import Deque

   def sliding_window_max(arr, k):
       """Find maximum in each window of size k."""
       deque = Deque()
       result = []

       for i, val in enumerate(arr):
           # Remove elements outside window
           while not deque.is_empty() and deque.front() <= i - k:
               deque.remove_front()

           # Remove smaller elements
           while not deque.is_empty() and arr[deque.back()] < val:
               deque.remove_back()

           deque.add_back(i)

           if i >= k - 1:
               result.append(arr[deque.front()])

       return result

See Also
========

* :doc:`../../api/linear/index` - API reference for linear structures
* :doc:`../tree_structures/index` - Tree structures guide
* :doc:`../graph_structures/index` - Graph structures guide