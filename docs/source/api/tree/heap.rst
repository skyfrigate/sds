.. _api_tree_heap:

====
Heap
====

.. currentmodule:: sds.tree.heap

Overview
========

This module provides heap data structures for efficient priority queue operations.
Heaps maintain a complete binary tree where each parent is less than (min-heap) or
greater than (max-heap) its children, enabling O(1) access to the minimum or maximum
element and O(log n) insertions and deletions.

.. mermaid::

   graph TB
       subgraph "Min-Heap"
       A1[1] --> B1[3]
       A1 --> C1[2]
       B1 --> D1[7]
       B1 --> E1[8]
       C1 --> F1[5]
       C1 --> G1[4]
       end
       
       subgraph "Max-Heap"
       A2[100] --> B2[70]
       A2 --> C2[80]
       B2 --> D2[50]
       B2 --> E2[60]
       C2 --> F2[75]
       C2 --> G2[65]
       end
       
       style A1 fill:#e74c3c,color:#fff
       style A2 fill:#e74c3c,color:#fff

Classes
=======

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   MinHeap
   MaxHeap
   HeapPriorityQueue

Detailed Documentation
======================

MinHeap
-------

.. autoclass:: MinHeap
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __len__, __iter__, __contains__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: size

   .. rubric:: Core Operations

   .. automethod:: insert
   .. automethod:: extract
   .. automethod:: peek

   .. rubric:: Utility Methods

   .. automethod:: is_empty
   .. automethod:: clear

   .. rubric:: Special Methods

   .. automethod:: __len__
   .. automethod:: __iter__
   .. automethod:: __contains__
   .. automethod:: __repr__
   .. automethod:: __str__

MaxHeap
-------

.. autoclass:: MaxHeap
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __len__, __iter__, __contains__, __repr__, __str__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: size

   .. rubric:: Core Operations

   .. automethod:: insert
   .. automethod:: extract
   .. automethod:: peek

   .. rubric:: Utility Methods

   .. automethod:: is_empty
   .. automethod:: clear

   .. rubric:: Special Methods

   .. automethod:: __len__
   .. automethod:: __iter__
   .. automethod:: __contains__
   .. automethod:: __repr__
   .. automethod:: __str__

HeapPriorityQueue
-----------------

.. autoclass:: HeapPriorityQueue
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __len__, __iter__, __repr__, __str__

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

   .. rubric:: Special Methods

   .. automethod:: __len__
   .. automethod:: __iter__
   .. automethod:: __repr__
   .. automethod:: __str__

Usage Examples
==============

Min-Heap Operations
-------------------

Basic Usage
^^^^^^^^^^^

.. code-block:: python

   from sds.tree import MinHeap

   # Create min-heap
   heap = MinHeap()
   
   # Insert elements
   heap.insert(5)
   heap.insert(3)
   heap.insert(7)
   heap.insert(1)
   
   # Peek minimum - O(1)
   print(heap.peek())  # Output: 1
   
   # Extract minimum - O(log n)
   print(heap.extract())  # Output: 1
   print(heap.extract())  # Output: 3
   print(heap.extract())  # Output: 5

Build from Array
^^^^^^^^^^^^^^^^

.. code-block:: python

   # Build heap from existing array - O(n)
   data = [5, 3, 7, 1, 9, 2, 8]
   heap = MinHeap(data)
   
   # Already heapified!
   print(heap.peek())  # Output: 1
   
   # Get sorted output
   sorted_data = []
   while not heap.is_empty():
       sorted_data.append(heap.extract())
   print(sorted_data)
   # Output: [1, 2, 3, 5, 7, 8, 9]

Max-Heap Operations
-------------------

Basic Usage
^^^^^^^^^^^

.. code-block:: python

   from sds.tree import MaxHeap

   # Create max-heap
   heap = MaxHeap()
   
   # Insert elements
   for val in [5, 3, 7, 1, 9]:
       heap.insert(val)
   
   # Peek maximum - O(1)
   print(heap.peek())  # Output: 9
   
   # Extract in descending order
   while not heap.is_empty():
       print(heap.extract(), end=' ')
   # Output: 9 7 5 3 1

Priority Queue
--------------

Basic Usage
^^^^^^^^^^^

.. code-block:: python

   from sds.tree import HeapPriorityQueue

   # Create priority queue
   pq = HeapPriorityQueue()
   
   # Enqueue with priorities (lower = higher priority)
   pq.enqueue("urgent task", priority=1)
   pq.enqueue("normal task", priority=5)
   pq.enqueue("low priority", priority=10)
   pq.enqueue("high priority", priority=2)
   
   # Dequeue in priority order
   while not pq.is_empty():
       item, priority = pq.dequeue()
       print(f"[{priority}] {item}")
   # Output:
   # [1] urgent task
   # [2] high priority
   # [5] normal task
   # [10] low priority

Real-World Examples
===================

Example 1: Task Scheduler
--------------------------

Real-time task scheduling with priorities:

.. code-block:: python

   from sds.tree import HeapPriorityQueue
   from datetime import datetime, timedelta
   import time

   class TaskScheduler:
       """Schedule and execute tasks by priority and deadline."""
       
       def __init__(self):
           self.tasks = HeapPriorityQueue()
           self.task_count = 0
       
       def schedule(self, name, priority, deadline=None, callback=None):
           """Schedule a task."""
           task_id = self.task_count
           self.task_count += 1
           
           task = {
               'id': task_id,
               'name': name,
               'scheduled': datetime.now(),
               'deadline': deadline,
               'callback': callback
           }
           
           # Priority: (priority, deadline_timestamp, task_id)
           # Lower values = higher priority
           priority_key = (
               priority,
               deadline.timestamp() if deadline else float('inf'),
               task_id
           )
           
           self.tasks.enqueue(task, priority_key)
           return task_id
       
       def run(self, max_tasks=None):
           """Execute tasks in priority order."""
           executed = 0
           
           while not self.tasks.is_empty():
               if max_tasks and executed >= max_tasks:
                   break
               
               task, priority = self.tasks.dequeue()
               
               print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                     f"Executing: {task['name']}")
               
               # Execute callback
               if task['callback']:
                   task['callback']()
               
               executed += 1
           
           return executed
   
   # Usage
   scheduler = TaskScheduler()
   
   # Schedule tasks with different priorities
   scheduler.schedule("Database backup", priority=1,
                     deadline=datetime.now() + timedelta(hours=1))
   scheduler.schedule("Send emails", priority=5)
   scheduler.schedule("Clean logs", priority=10)
   scheduler.schedule("Critical alert", priority=0)
   
   # Execute tasks
   scheduler.run()

Example 2: Dijkstra's Algorithm
--------------------------------

Shortest path using min-heap:

.. code-block:: python

   from sds.tree import HeapPriorityQueue

   class Graph:
       """Weighted graph for shortest path."""
       
       def __init__(self):
           self.edges = {}
       
       def add_edge(self, from_node, to_node, weight):
           """Add weighted edge."""
           if from_node not in self.edges:
               self.edges[from_node] = []
           self.edges[from_node].append((to_node, weight))
       
       def dijkstra(self, start, end):
           """Find shortest path using heap."""
           # Min-heap: (distance, node, path)
           heap = HeapPriorityQueue()
           heap.enqueue((start, [start]), 0)
           
           visited = set()
           distances = {start: 0}
           
           while not heap.is_empty():
               (current, path), dist = heap.dequeue()
               
               if current in visited:
                   continue
               
               visited.add(current)
               
               # Found destination
               if current == end:
                   return path, dist
               
               # Explore neighbors
               if current in self.edges:
                   for neighbor, weight in self.edges[current]:
                       if neighbor not in visited:
                           new_dist = dist + weight
                           
                           if (neighbor not in distances or 
                               new_dist < distances[neighbor]):
                               distances[neighbor] = new_dist
                               new_path = path + [neighbor]
                               heap.enqueue((neighbor, new_path), new_dist)
           
           return None, float('inf')  # No path found
   
   # Usage
   graph = Graph()
   graph.add_edge('A', 'B', 4)
   graph.add_edge('A', 'C', 2)
   graph.add_edge('B', 'D', 5)
   graph.add_edge('C', 'D', 8)
   
   path, distance = graph.dijkstra('A', 'D')
   print(f"Shortest path: {' -> '.join(path)}")
   print(f"Total distance: {distance}")

Example 3: Median Tracker
--------------------------

Track running median using two heaps:

.. code-block:: python

   from sds.tree import MinHeap, MaxHeap

   class MedianTracker:
       """Maintain running median using two heaps."""
       
       def __init__(self):
           # Max-heap for smaller half
           self.low = MaxHeap()
           # Min-heap for larger half
           self.high = MinHeap()
       
       def add_number(self, num):
           """Add number and maintain median."""
           # Add to appropriate heap
           if self.low.is_empty() or num <= self.low.peek():
               self.low.insert(num)
           else:
               self.high.insert(num)
           
           # Balance heaps (keep sizes within 1)
           if len(self.low) > len(self.high) + 1:
               self.high.insert(self.low.extract())
           elif len(self.high) > len(self.low):
               self.low.insert(self.high.extract())
       
       def get_median(self):
           """Get current median - O(1)."""
           if self.low.is_empty():
               return None
           
           if len(self.low) > len(self.high):
               return self.low.peek()
           else:
               return (self.low.peek() + self.high.peek()) / 2
   
   # Usage
   tracker = MedianTracker()
   
   numbers = [5, 15, 1, 3, 8, 7, 9, 10, 20]
   
   for num in numbers:
       tracker.add_number(num)
       median = tracker.get_median()
       print(f"After adding {num}: median = {median}")

Example 4: Top-K Frequent Elements
-----------------------------------

Find most frequent elements efficiently:

.. code-block:: python

   from sds.tree import MinHeap
   from collections import Counter

   class TopKTracker:
       """Track top-K most frequent items."""
       
       def __init__(self, k):
           self.k = k
           self.frequencies = Counter()
           self.heap = MinHeap()
       
       def add(self, item):
           """Add item occurrence."""
           self.frequencies[item] += 1
       
       def get_top_k(self):
           """Get top-K most frequent items."""
           # Build heap of (frequency, item) pairs
           heap = MinHeap()
           
           for item, freq in self.frequencies.items():
               heap.insert((freq, item))
               if len(heap) > self.k:
                   heap.extract()  # Remove smallest
           
           # Extract all and return in descending order
           result = []
           while not heap.is_empty():
               freq, item = heap.extract()
               result.append((item, freq))
           
           return list(reversed(result))
   
   # Usage
   tracker = TopKTracker(k=3)
   
   # Add items
   items = ['apple', 'banana', 'apple', 'orange', 
            'banana', 'apple', 'grape', 'banana']
   for item in items:
       tracker.add(item)
   
   # Get top 3
   top_3 = tracker.get_top_k()
   for item, freq in top_3:
       print(f"{item}: {freq}")

Performance Characteristics
===========================

Time Complexity
---------------

.. list-table::
   :header-rows: 1
   :widths: 35 20 40

   * - Operation
     - Complexity
     - Notes
   * - **Insert**
     - O(log n)
     - Sift up from bottom
   * - **Extract Min/Max**
     - O(log n)
     - Sift down from top
   * - **Peek Min/Max**
     - O(1)
     - Just read root
   * - **Heapify (build)**
     - O(n)
     - Bottom-up construction
   * - **Delete arbitrary**
     - O(log n)
     - Find + extract
   * - **Increase/Decrease key**
     - O(log n)
     - Sift up or down
   * - **Search**
     - O(n)
     - No ordering within levels

Space Complexity
----------------

* **Heap storage**: O(n)
* **No pointers needed**: Array-based, just store values
* **Auxiliary space**: O(1) for all operations (iterative)

Heap Sort Algorithm
===================

.. code-block:: python

   from sds.tree import MinHeap

   def heap_sort(array):
       """Sort array using heap - O(n log n)."""
       # Build heap - O(n)
       heap = MinHeap(array)
       
       # Extract elements in order - O(n log n)
       sorted_array = []
       while not heap.is_empty():
           sorted_array.append(heap.extract())
       
       return sorted_array

   # Usage
   data = [5, 2, 8, 1, 9, 3, 7]
   sorted_data = heap_sort(data)
   print(sorted_data)
   # Output: [1, 2, 3, 5, 7, 8, 9]

**Time complexity**: O(n log n)
**Space complexity**: O(n)

Best Practices
==============

Do's
----

✅ **Use heaps for priority management**

.. code-block:: python

   # Perfect for:
   # - Priority queues
   # - Task scheduling
   # - Top-K problems
   # - Median tracking

✅ **Build heap from array when possible**

.. code-block:: python

   # O(n) construction vs O(n log n) insertions
   heap = MinHeap([5, 3, 7, 1, 9])  # Fast!

✅ **Use for streaming algorithms**

.. code-block:: python

   # Find top-K in stream
   heap = MinHeap()
   K = 10
   
   for item in stream:
       if len(heap) < K:
           heap.insert(item)
       elif item > heap.peek():
           heap.extract()
           heap.insert(item)

Don'ts
------

❌ **Don't use for general searches**

.. code-block:: python

   # Bad: O(n) search time
   # Use hash table or BST instead

❌ **Don't expect sorting within heap**

.. code-block:: python

   # Heap only guarantees root is min/max
   # Children are not sorted

❌ **Don't use for range queries**

.. code-block:: python

   # Heaps don't support efficient range queries
   # Use segment tree or B-tree instead

Common Pitfalls
===============

1. **Confusing min and max heaps**

.. code-block:: python

   # MinHeap.extract() returns smallest
   # MaxHeap.extract() returns largest
   # Choose based on your need!

2. **Not using heapify for initialization**

.. code-block:: python

   # Slow: O(n log n)
   heap = MinHeap()
   for x in data:
       heap.insert(x)
   
   # Fast: O(n)
   heap = MinHeap(data)

3. **Using heap when BST is better**

.. code-block:: python

   # Heaps don't maintain full sorted order
   # Use BST if you need range queries

See Also
========

* :doc:`binary` - Binary tree fundamentals
* :doc:`balanced` - Balanced search trees
* :doc:`../../guide/tree_structures/heap` - Heap theory and guide

References
==========

.. [1] Williams, J. W. J. "Algorithm 232: Heapsort", 1964
.. [2] Floyd, R. W. "Algorithm 245: Treesort 3", 1964
.. [3] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Chapter 6
.. [4] Knuth, D. E. "The Art of Computer Programming, Volume 3"
