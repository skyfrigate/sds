.. _api_linear_queue:

=====
Queue
=====

.. currentmodule:: sds.linear.queue

Overview
========

This module provides queue implementations including FIFO queue, double-ended
queue (deque), and priority queue. Queues are essential for managing ordered
sequences of elements with specific insertion and removal policies.

.. mermaid::

   graph LR
       subgraph "FIFO Queue"
       A1[enqueue] --> B1[1]
       B1 --> C1[2]
       C1 --> D1[3]
       D1 --> E1[dequeue]
       end
       
       subgraph "Deque"
       A2[add_front/rear] <==> B2[1]
       B2 <==> C2[2]
       C2 <==> D2[3]
       D2 <==> E2[remove_front/rear]
       end
       
       subgraph "Priority Queue"
       F1[enqueue] --> G1["1 (high)"]
       F1 --> H1["5 (low)"]
       F1 --> I1["3 (med)"]
       G1 --> J1[dequeue]
       end
       
       style B1 fill:#e74c3c
       style E1 fill:#2ecc71
       style B2 fill:#3498db
       style G1 fill:#f39c12

Classes
=======

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   Queue
   Deque
   PriorityQueue
   PriorityItem

Detailed Documentation
======================

Queue
-----

.. autoclass:: Queue
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __len__, __iter__, __contains__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: size

   .. rubric:: Core Operations

   .. automethod:: enqueue
   .. automethod:: dequeue
   .. automethod:: front
   .. automethod:: rear

   .. rubric:: Utility Methods

   .. automethod:: is_empty
   .. automethod:: clear
   .. automethod:: add
   .. automethod:: remove

   .. rubric:: Special Methods

   .. automethod:: __len__
   .. automethod:: __iter__
   .. automethod:: __contains__
   .. automethod:: __repr__
   .. automethod:: __str__

Deque
-----

.. autoclass:: Deque
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __len__, __iter__, __reversed__, __contains__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: size

   .. rubric:: Core Operations

   .. automethod:: add_front
   .. automethod:: add_rear
   .. automethod:: remove_front
   .. automethod:: remove_rear
   .. automethod:: peek_front
   .. automethod:: peek_rear

   .. rubric:: Convenience Aliases

   .. automethod:: append
   .. automethod:: appendleft
   .. automethod:: pop
   .. automethod:: popleft

   .. rubric:: Utility Methods

   .. automethod:: is_empty
   .. automethod:: clear
   .. automethod:: add
   .. automethod:: remove

   .. rubric:: Special Methods

   .. automethod:: __len__
   .. automethod:: __iter__
   .. automethod:: __reversed__
   .. automethod:: __contains__
   .. automethod:: __repr__
   .. automethod:: __str__

PriorityQueue
-------------

.. autoclass:: PriorityQueue
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __len__, __iter__, __contains__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: size

   .. rubric:: Core Operations

   .. automethod:: enqueue
   .. automethod:: dequeue
   .. automethod:: peek

   .. rubric:: Utility Methods

   .. automethod:: is_empty
   .. automethod:: clear
   .. automethod:: add
   .. automethod:: remove

   .. rubric:: Special Methods

   .. automethod:: __len__
   .. automethod:: __iter__
   .. automethod:: __contains__
   .. automethod:: __repr__
   .. automethod:: __str__

PriorityItem
------------

.. autoclass:: PriorityItem
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __repr__, __str__, __lt__, __le__, __gt__, __ge__, __eq__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Attributes

   .. attribute:: data
      :type: Any

      The actual data stored in the priority item.

   .. attribute:: priority
      :type: float

      The priority value (lower = higher priority by default).

Usage Examples
==============

Queue Examples
--------------

Basic FIFO Operations
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.linear import Queue

   # Create queue
   queue = Queue()
   
   # Enqueue elements
   queue.enqueue(1)
   queue.enqueue(2)
   queue.enqueue(3)
   
   print(len(queue))  # 3

   # Dequeue in FIFO order
   print(queue.dequeue())  # 1
   print(queue.dequeue())  # 2
   print(queue.dequeue())  # 3

Peek Operations
^^^^^^^^^^^^^^^

.. code-block:: python

   queue = Queue()
   queue.enqueue("first")
   queue.enqueue("second")
   queue.enqueue("third")
   
   # View front without removing
   print(queue.front())  # "first"
   print(len(queue))     # 3 (unchanged)
   
   # View rear without removing
   print(queue.rear())   # "third"

Iteration
^^^^^^^^^

.. code-block:: python

   queue = Queue()
   for i in range(1, 4):
       queue.enqueue(i)
   
   # Iterate from front to rear
   for item in queue:
       print(item, end=' ')
   # Output: 1 2 3

Deque Examples
--------------

Double-Ended Operations
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.linear import Deque

   # Create deque
   deque = Deque()
   
   # Add to both ends
   deque.add_rear(2)    # [2]
   deque.add_front(1)   # [1, 2]
   deque.add_rear(3)    # [1, 2, 3]
   deque.add_front(0)   # [0, 1, 2, 3]
   
   print(list(deque))   # [0, 1, 2, 3]

Remove from Both Ends
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Remove from front
   print(deque.remove_front())  # 0
   
   # Remove from rear
   print(deque.remove_rear())   # 3
   
   print(list(deque))  # [1, 2]

Peek Both Ends
^^^^^^^^^^^^^^

.. code-block:: python

   deque = Deque()
   deque.add_rear(1)
   deque.add_rear(2)
   deque.add_rear(3)
   
   print(deque.peek_front())  # 1
   print(deque.peek_rear())   # 3

Python-Style Aliases
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   deque = Deque()
   
   # Python deque-style methods
   deque.append(1)       # Add to rear
   deque.appendleft(0)   # Add to front
   
   print(deque.pop())         # Remove from rear: 1
   print(deque.popleft())     # Remove from front: 0

Bidirectional Iteration
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   deque = Deque()
   for i in range(1, 4):
       deque.add_rear(i)
   
   # Forward
   print(list(deque))           # [1, 2, 3]
   
   # Backward
   print(list(reversed(deque))) # [3, 2, 1]

PriorityQueue Examples
----------------------

Basic Priority Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.linear import PriorityQueue

   # Create priority queue (min-heap by default)
   pq = PriorityQueue()
   
   # Enqueue with different priorities
   pq.enqueue(5)  # Lower value = higher priority
   pq.enqueue(1)
   pq.enqueue(3)
   pq.enqueue(2)
   
   # Dequeue in priority order
   print(pq.dequeue())  # 1 (highest priority)
   print(pq.dequeue())  # 2
   print(pq.dequeue())  # 3
   print(pq.dequeue())  # 5 (lowest priority)

Max-Heap Behavior
^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Create max-heap (reverse=True)
   pq = PriorityQueue(reverse=True)
   
   pq.enqueue(5)
   pq.enqueue(1)
   pq.enqueue(3)
   
   # Dequeue in descending order
   print(pq.dequeue())  # 5
   print(pq.dequeue())  # 3
   print(pq.dequeue())  # 1

Custom Priority Key
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Custom key function
   pq = PriorityQueue(key=lambda x: x['priority'])
   
   pq.enqueue({'task': 'Important', 'priority': 1})
   pq.enqueue({'task': 'Normal', 'priority': 5})
   pq.enqueue({'task': 'Urgent', 'priority': 0})
   
   # Dequeue by priority field
   task = pq.dequeue()
   print(task)  # {'task': 'Urgent', 'priority': 0}

Using PriorityItem
^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from sds.linear import PriorityItem

   pq = PriorityQueue()
   
   # Create priority items
   pq.enqueue(PriorityItem("Low priority task", priority=10))
   pq.enqueue(PriorityItem("High priority task", priority=1))
   pq.enqueue(PriorityItem("Medium priority task", priority=5))
   
   # Dequeue by priority
   while not pq.is_empty():
       item = pq.dequeue()
       print(f"[{item.priority}] {item.data}")
   
   # Output:
   # [1] High priority task
   # [5] Medium priority task
   # [10] Low priority task

Real-World Examples
===================

Example 1: Task Queue (Queue)
------------------------------

.. code-block:: python

   from sds.linear import Queue
   import time

   class TaskQueue:
       """Simple task queue for background processing."""
       
       def __init__(self):
           self.queue = Queue()
           self.processing = False
       
       def add_task(self, task):
           """Add task to queue."""
           print(f"Adding task: {task}")
           self.queue.enqueue(task)
       
       def process_tasks(self):
           """Process all tasks in queue."""
           self.processing = True
           
           while not self.queue.is_empty():
               task = self.queue.dequeue()
               print(f"Processing: {task}")
               time.sleep(0.5)  # Simulate work
               print(f"Completed: {task}")
           
           self.processing = False
           print("All tasks completed!")
       
       def get_queue_size(self):
           """Get number of pending tasks."""
           return len(self.queue)
   
   # Usage
   task_queue = TaskQueue()
   task_queue.add_task("Send email")
   task_queue.add_task("Generate report")
   task_queue.add_task("Update database")
   
   print(f"Tasks in queue: {task_queue.get_queue_size()}")
   task_queue.process_tasks()

Example 2: Palindrome Checker (Deque)
--------------------------------------

.. code-block:: python

   from sds.linear import Deque

   def is_palindrome(text):
       """Check if text is palindrome using deque."""
       # Remove spaces and convert to lowercase
       text = ''.join(text.split()).lower()
       
       # Build deque
       deque = Deque()
       for char in text:
           deque.add_rear(char)
       
       # Check from both ends
       while len(deque) > 1:
           if deque.remove_front() != deque.remove_rear():
               return False
       
       return True
   
   # Usage
   print(is_palindrome("A man a plan a canal Panama"))  # True
   print(is_palindrome("race car"))                      # True
   print(is_palindrome("hello"))                         # False

Example 3: Sliding Window (Deque)
----------------------------------

.. code-block:: python

   from sds.linear import Deque

   def sliding_window_maximum(nums, k):
       """Find maximum in each sliding window."""
       if not nums or k == 0:
           return []
       
       deque = Deque()
       result = []
       
       for i, num in enumerate(nums):
           # Remove elements outside window
           while (not deque.is_empty() and 
                  deque.peek_front() <= i - k):
               deque.remove_front()
           
           # Remove smaller elements (not useful)
           while (not deque.is_empty() and 
                  nums[deque.peek_rear()] < num):
               deque.remove_rear()
           
           deque.add_rear(i)
           
           # Add to result when window is full
           if i >= k - 1:
               result.append(nums[deque.peek_front()])
       
       return result
   
   # Usage
   nums = [1, 3, -1, -3, 5, 3, 6, 7]
   k = 3
   print(sliding_window_maximum(nums, k))
   # Output: [3, 3, 5, 5, 6, 7]

Example 4: Task Scheduler (PriorityQueue)
------------------------------------------

.. code-block:: python

   from sds.linear import PriorityQueue, PriorityItem
   from datetime import datetime, timedelta

   class TaskScheduler:
       """Schedule tasks by deadline."""
       
       def __init__(self):
           self.tasks = PriorityQueue()
       
       def add_task(self, name, deadline, importance=5):
           """Add task with deadline and importance."""
           # Priority: earlier deadline and higher importance = lower value
           priority = (deadline.timestamp(), -importance)
           
           task = {
               'name': name,
               'deadline': deadline,
               'importance': importance
           }
           
           self.tasks.enqueue(PriorityItem(task, priority))
       
       def get_next_task(self):
           """Get highest priority task."""
           if not self.tasks.is_empty():
               item = self.tasks.dequeue()
               return item.data
           return None
       
       def get_pending_count(self):
           """Get number of pending tasks."""
           return len(self.tasks)
   
   # Usage
   scheduler = TaskScheduler()
   
   now = datetime.now()
   scheduler.add_task("Fix bug", now + timedelta(hours=1), importance=9)
   scheduler.add_task("Write docs", now + timedelta(hours=2), importance=5)
   scheduler.add_task("Review PR", now + timedelta(hours=3), importance=7)
   
   # Process tasks by priority
   while scheduler.get_pending_count() > 0:
       task = scheduler.get_next_task()
       print(f"Next: {task['name']} "
             f"(importance: {task['importance']})")

Example 5: BFS Traversal (Queue)
---------------------------------

.. code-block:: python

   from sds.linear import Queue

   def bfs(graph, start):
       """Breadth-first search using queue."""
       visited = set()
       queue = Queue()
       result = []
       
       queue.enqueue(start)
       visited.add(start)
       
       while not queue.is_empty():
           node = queue.dequeue()
           result.append(node)
           
           # Enqueue unvisited neighbors
           for neighbor in graph.get(node, []):
               if neighbor not in visited:
                   visited.add(neighbor)
                   queue.enqueue(neighbor)
       
       return result
   
   # Usage
   graph = {
       'A': ['B', 'C'],
       'B': ['D', 'E'],
       'C': ['F'],
       'D': [],
       'E': ['F'],
       'F': []
   }
   
   path = bfs(graph, 'A')
   print(f"BFS path: {path}")
   # Output: ['A', 'B', 'C', 'D', 'E', 'F']

Performance Characteristics
===========================

Time Complexity
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 15 15 20

   * - Operation
     - Queue
     - Deque
     - PriorityQueue
   * - ``enqueue/add``
     - O(n)
     - O(1)
     - O(n)
   * - ``dequeue/remove``
     - O(1)
     - O(1)
     - O(1)
   * - ``peek/front/rear``
     - O(1)
     - O(1)
     - O(1)
   * - ``is_empty()``
     - O(1)
     - O(1)
     - O(1)
   * - ``__len__()``
     - O(1)
     - O(1)
     - O(1)
   * - ``__contains__``
     - O(n)
     - O(n)
     - O(n)

Space Complexity
----------------

* **Queue**: O(n)
* **Deque**: O(n) + overhead for doubly linked nodes
* **PriorityQueue**: O(n)

Comparison Summary
==================

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - Feature
     - Queue
     - Deque
     - PriorityQueue
   * - **Order**
     - FIFO
     - Both ends
     - By priority
   * - **Add**
     - One end only
     - Both ends
     - Sorted insert
   * - **Remove**
     - One end only
     - Both ends
     - Highest priority
   * - **Best For**
     - Task queues, BFS
     - Sliding windows
     - Scheduling

Best Practices
==============

Do's
----

✅ **Choose appropriate queue type**

.. code-block:: python

   # FIFO → Queue
   queue = Queue()
   
   # Both-end access → Deque
   deque = Deque()
   
   # Priority-based → PriorityQueue
   pq = PriorityQueue()

✅ **Check emptiness before operations**

.. code-block:: python

   if not queue.is_empty():
       item = queue.dequeue()

✅ **Use for BFS/level-order traversal**

.. code-block:: python

   # Queue is perfect for BFS
   queue = Queue()
   queue.enqueue(root)
   
   while not queue.is_empty():
       node = queue.dequeue()
       # Process node

Don'ts
------

❌ **Don't use Queue if you need LIFO**

.. code-block:: python

   # Wrong: Use Stack for LIFO
   # Queue is for FIFO only

❌ **Don't access middle elements**

.. code-block:: python

   # Queues don't support random access
   # Use list if you need this

❌ **Don't expect sorted iteration from PriorityQueue**

.. code-block:: python

   # PriorityQueue iteration order is not guaranteed
   # Use dequeue() to get items in priority order

Common Pitfalls
===============

1. **Confusing FIFO and LIFO**

.. code-block:: python

   # Queue: First In First Out
   # Stack: Last In First Out
   # Don't mix them up!

2. **Not handling empty queue**

.. code-block:: python

   # Always check before dequeue
   if not queue.is_empty():
       item = queue.dequeue()

3. **Wrong priority direction**

.. code-block:: python

   # By default: lower value = higher priority
   # Use reverse=True for opposite

See Also
========

* :doc:`stack` - LIFO stack structure
* :doc:`list` - Linked list implementations
* :doc:`../../guide/linear_structures/queue` - Queue theory and guide

References
==========

.. [1] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Chapter 10
.. [2] Knuth, D. E. "The Art of Computer Programming, Volume 1", Section 2.2
.. [3] Sedgewick, R., Wayne, K. "Algorithms", 4th Edition, Section 1.3
.. [4] Williams, J. W. J. "Algorithm 232: Heapsort", 1964
