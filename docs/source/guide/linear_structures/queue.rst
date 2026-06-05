.. _guide_linear_queue:

===========
Queue Guide
===========

.. currentmodule:: sds.linear

Introduction
============

A **queue** is a fundamental linear data structure that follows the 
**First-In-First-Out (FIFO)** principle. Think of it like a line at a store:
the first person in line is the first to be served.

.. mermaid::

   graph LR
       A[Front] --> B[Element 1<br/>First In]
       B --> C[Element 2]
       C --> D[Element 3<br/>Most Recent]
       D --> E[Rear]
       
       F[dequeue] -.->|Remove from front| A
       E -.->|Add to rear| G[enqueue]
       
       style A fill:#e74c3c,stroke:#c0392b,color:#fff
       style E fill:#3498db,stroke:#2980b9,color:#fff
       style B fill:#f39c12
       style F fill:#e74c3c,stroke:#c0392b,color:#fff
       style G fill:#27ae60,stroke:#229954,color:#fff

.. note::
   
   This guide covers queues, deques (double-ended queues), and priority queues.

Mathematical Model
==================

Formal Definition
-----------------

A queue :math:`Q` is an ordered collection:

.. math::

   Q = \langle e_1, e_2, \ldots, e_n \rangle

where :math:`e_1` is the **front** element (oldest, will be removed next) and :math:`e_n` is the **rear** element (newest, just added).

Operations
----------

Enqueue Operation
^^^^^^^^^^^^^^^^^

Adds an element to the rear:

.. math::

   enqueue(Q, x) = \langle e_1, e_2, \ldots, e_n, x \rangle

**Properties:**
   * :math:`|Q'| = |Q| + 1`
   * :math:`rear(Q') = x`
   * :math:`front(Q') = front(Q)` if :math:`|Q| > 0`

Dequeue Operation
^^^^^^^^^^^^^^^^^

Removes and returns the front element:

.. math::

   dequeue(\langle e_1, e_2, \ldots, e_n \rangle) = (e_1, \langle e_2, \ldots, e_n \rangle)

**Properties:**
   * :math:`|Q'| = |Q| - 1`
   * Undefined for empty queue

Queue Invariants
----------------

1. **FIFO ordering**: :math:`enqueue_i` before :math:`enqueue_j \implies dequeue_i` before :math:`dequeue_j`
2. **Size**: :math:`|Q| \geq 0`
3. **Front accessibility**: If :math:`|Q| > 0`, :math:`front(Q)` is defined

Deque Extensions
----------------

A **deque** (double-ended queue) allows operations at both ends:

.. math::

   \begin{align*}
   add\_front(Q, x) &= \langle x, e_1, e_2, \ldots, e_n \rangle \\
   add\_rear(Q, x) &= \langle e_1, e_2, \ldots, e_n, x \rangle \\
   remove\_front(Q) &= (e_1, \langle e_2, \ldots, e_n \rangle) \\
   remove\_rear(Q) &= (e_n, \langle e_1, \ldots, e_{n-1} \rangle)
   \end{align*}

Priority Queue Model
--------------------

A priority queue dequeues by priority rather than insertion order:

.. math::

   dequeue(PQ) = (e_i, PQ \setminus \{e_i\}) \text{ where } priority(e_i) = \max_{e \in PQ} priority(e)

Algorithmic Model
=================

Queue ADT
---------

.. code-block:: text

   ADT Queue:
       Data:
           - elements: sequence
           - front: reference to first element
           - rear: reference to last element
           - size: number of elements
       
       Operations:
           - Queue(): create empty queue
           - enqueue(item): add to rear
           - dequeue(): remove from front
           - front(): peek at front element
           - is_empty(): check if empty

Implementation Strategies
--------------------------

Array-Based (Circular Buffer)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. mermaid::

   graph TD
       A["Array [0,1,2,3,4]"]
       B[front = 2]
       C[rear = 4]
       D["[-, -, A, B, C]"]
       
       style A fill:#3498db
       style D fill:#f39c12

**Advantages:**
   * O(1) enqueue and dequeue
   * Good cache locality
   * Fixed memory usage

**Disadvantages:**
   * Fixed size (without reallocation)
   * Complexity in handling wrap-around

Linked List Implementation
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. mermaid::

   graph LR
       F[Front] --> A[Node 1]
       A --> B[Node 2]
       B --> C[Node 3]
       C --> N[None]
       R[Rear] -.-> C
       
       style F fill:#e74c3c
       style R fill:#3498db

**Advantages:**
   * Dynamic size
   * Simple logic
   * O(1) operations (with tail pointer)

**Disadvantages:**
   * Extra memory for pointers
   * Less cache-friendly

Algorithm Pseudocode
--------------------

Queue Operations
^^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: ENQUEUE(Q, item)
   Input: Queue Q, element item
   Output: Modified queue Q
   
   1. Create new_node with data = item
   2. if Q.rear ≠ null then
   3.     Q.rear.next ← new_node
   4. else
   5.     Q.front ← new_node
   6. end if
   7. Q.rear ← new_node
   8. Q.size ← Q.size + 1

.. code-block:: text

   Algorithm: DEQUEUE(Q)
   Input: Queue Q
   Output: Front element
   Precondition: Q is not empty
   
   1. if Q.front = null then
   2.     raise EmptyStructureError
   3. end if
   4. item ← Q.front.data
   5. Q.front ← Q.front.next
   6. if Q.front = null then
   7.     Q.rear ← null
   8. end if
   9. Q.size ← Q.size - 1
   10. return item

Deque Operations
^^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: ADD_FRONT(D, item)
   // Add to front of deque
   1. new_node ← Node(item, next=D.head)
   2. if D.is_empty() then
   3.     D.tail ← new_node
   4. else
   5.     D.head.prev ← new_node
   6. end if
   7. D.head ← new_node
   8. D.size ← D.size + 1

Priority Queue Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: ENQUEUE_PRIORITY(PQ, item, priority)
   // Insert maintaining priority order
   1. new_node ← Node(item, priority)
   2. if PQ.head = null or priority > PQ.head.priority then
   3.     new_node.next ← PQ.head
   4.     PQ.head ← new_node
   5. else
   6.     current ← PQ.head
   7.     while current.next ≠ null and current.next.priority ≥ priority do
   8.         current ← current.next
   9.     end while
   10.     new_node.next ← current.next
   11.     current.next ← new_node
   12. end if
   13. PQ.size ← PQ.size + 1

Complexity Analysis
-------------------

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 20 15

   * - Operation
     - Queue
     - Deque
     - Priority Queue
     - Notes
   * - **Enqueue/Add**
     - O(n)*
     - O(1)
     - O(n)
     - * Without tail pointer
   * - **Dequeue/Remove**
     - O(1)
     - O(1)
     - O(1)
     - Always from front
   * - **Peek**
     - O(1)
     - O(1)
     - O(1)
     - Just read, no modify
   * - **Search**
     - O(n)
     - O(n)
     - O(n)
     - Linear scan
   * - **Space**
     - O(n)
     - O(n)
     - O(n)
     - Proportional to size

Practical Usage
===============

Basic Queue Usage
-----------------

.. code-block:: python

   from sds.linear import Queue
   
   # Create queue
   queue = Queue()
   
   # Enqueue elements
   queue.enqueue("Task 1")
   queue.enqueue("Task 2")
   queue.enqueue("Task 3")
   
   # Dequeue (FIFO order)
   print(queue.dequeue())  # Output: Task 1
   print(queue.front())    # Output: Task 2
   
   # Check state
   print(len(queue))       # Output: 2
   print(queue.is_empty()) # Output: False

Deque Usage
-----------

.. code-block:: python

   from sds.linear import Deque
   
   deque = Deque()
   
   # Add to both ends
   deque.add_rear(2)
   deque.add_front(1)
   deque.add_rear(3)
   
   print(list(deque))  # Output: [1, 2, 3]
   
   # Remove from both ends
   print(deque.remove_front())  # Output: 1
   print(deque.remove_rear())   # Output: 3

Priority Queue Usage
--------------------

.. code-block:: python

   from sds.linear import PriorityQueue
   
   pq = PriorityQueue()
   
   # Lower number = higher priority
   pq.enqueue(5)
   pq.enqueue(1)
   pq.enqueue(3)
   
   print(pq.dequeue())  # Output: 1 (highest priority)
   print(pq.dequeue())  # Output: 3
   print(pq.dequeue())  # Output: 5 (lowest priority)

Real-World Applications
=======================

Application 1: Task Scheduler
------------------------------

.. code-block:: python

   from sds.linear import Queue
   import time
   
   class TaskScheduler:
       def __init__(self):
           self.queue = Queue()
       
       def schedule(self, task, callback):
           """Schedule a task."""
           self.queue.enqueue((task, callback))
       
       def run(self):
           """Process all scheduled tasks."""
           while not self.queue.is_empty():
               task, callback = self.queue.dequeue()
               print(f"Processing: {task}")
               callback()
               time.sleep(0.1)
   
   # Usage
   scheduler = TaskScheduler()
   scheduler.schedule("Send email", lambda: print("  Email sent"))
   scheduler.schedule("Update DB", lambda: print("  DB updated"))
   scheduler.schedule("Generate report", lambda: print("  Report ready"))
   
   scheduler.run()

Application 2: BFS Algorithm
-----------------------------

.. code-block:: python

   from sds.linear import Queue
   
   def bfs(graph, start):
       """Breadth-First Search using queue."""
       visited = set()
       queue = Queue()
       result = []
       
       queue.enqueue(start)
       visited.add(start)
       
       while not queue.is_empty():
           vertex = queue.dequeue()
           result.append(vertex)
           
           for neighbor in graph.get(vertex, []):
               if neighbor not in visited:
                   visited.add(neighbor)
                   queue.enqueue(neighbor)
       
       return result
   
   # Test
   graph = {
       'A': ['B', 'C'],
       'B': ['A', 'D', 'E'],
       'C': ['A', 'F'],
       'D': ['B'],
       'E': ['B', 'F'],
       'F': ['C', 'E']
   }
   
   print(bfs(graph, 'A'))
   # Output: ['A', 'B', 'C', 'D', 'E', 'F']

Application 3: Sliding Window (Deque)
--------------------------------------

.. code-block:: python

   from sds.linear import Deque
   
   def sliding_window_max(nums, k):
       """Maximum in sliding window using deque."""
       if not nums or k <= 0:
           return []
       
       deque = Deque()
       result = []
       
       for i, num in enumerate(nums):
           # Remove out-of-window indices
           while (not deque.is_empty() and 
                  deque.peek_front() <= i - k):
               deque.remove_front()
           
           # Remove smaller elements
           while (not deque.is_empty() and 
                  nums[deque.peek_rear()] < num):
               deque.remove_rear()
           
           deque.add_rear(i)
           
           if i >= k - 1:
               result.append(nums[deque.peek_front()])
       
       return result
   
   # Test
   nums = [1, 3, -1, -3, 5, 3, 6, 7]
   print(sliding_window_max(nums, 3))
   # Output: [3, 3, 5, 5, 6, 7]

Application 4: Event Simulator (Priority Queue)
------------------------------------------------

.. code-block:: python

   from sds.linear import PriorityQueue, PriorityItem
   
   class Simulation:
       def __init__(self):
           self.queue = PriorityQueue(key=lambda x: x.priority)
           self.current_time = 0
       
       def schedule_event(self, name, time, action):
           """Schedule an event."""
           event = PriorityItem((name, action), time)
           self.queue.enqueue(event)
       
       def run(self):
           """Run simulation."""
           while not self.queue.is_empty():
               event = self.queue.dequeue()
               self.current_time = event.priority
               name, action = event.data
               
               print(f"Time {self.current_time}: {name}")
               action()
   
   # Usage
   sim = Simulation()
   sim.schedule_event("Start", 0, lambda: print("  System starting"))
   sim.schedule_event("User login", 5, lambda: print("  User authenticated"))
   sim.schedule_event("Process data", 3, lambda: print("  Data processed"))
   sim.schedule_event("Shutdown", 10, lambda: print("  System shutdown"))
   
   sim.run()

Best Practices
==============

Queue
-----

✅ Use for FIFO, task scheduling, BFS

.. code-block:: python

   # Good: Sequential processing
   queue = Queue()
   for task in tasks:
       queue.enqueue(task)
   
   while not queue.is_empty():
       process(queue.dequeue())

Deque
-----

✅ Use for operations at both ends

.. code-block:: python

   # Good: Efficient at both ends
   deque = Deque()
   deque.add_front(1)  # O(1)
   deque.add_rear(2)   # O(1)

Priority Queue
--------------

✅ Use for priority-based processing

.. code-block:: python

   # Good: Process by priority
   pq = PriorityQueue()
   pq.enqueue(PriorityItem("urgent", 1))
   pq.enqueue(PriorityItem("normal", 5))

Common Pitfalls
===============

1. **Queue vs Stack confusion**
2. **Forgetting FIFO order**
3. **Priority queue direction** (low number = high priority by default)

See Also
========

* :doc:`/api/linear/queue` - API reference
* :doc:`stack` - LIFO alternative
* :doc:`linked_list` - Implementation details
