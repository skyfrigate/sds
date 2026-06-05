.. _guide_tree_heap:

==========
Heap Guide
==========

.. currentmodule:: sds.tree

Introduction
============

A **Heap** is a specialized tree-based data structure that satisfies the **heap property**: in a max-heap, parent nodes are always greater than or equal to their children; in a min-heap, parent nodes are always less than or equal to their children. Heaps are the foundation of efficient priority queues and the heap sort algorithm.

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
       style B1 fill:#3498db,color:#fff
       style C1 fill:#3498db,color:#fff
       style B2 fill:#3498db,color:#fff
       style C2 fill:#3498db,color:#fff

.. note::
   
   Heaps are typically implemented using arrays for memory efficiency and
   cache locality. Despite being trees conceptually, their array representation
   provides O(1) parent/child navigation without storing explicit pointers.

Mathematical Model
==================

Formal Definition
-----------------

Heap Property
^^^^^^^^^^^^^

**Min-Heap Property**:

.. math::

   \forall node \in H: node.value \leq children(node).value

**Max-Heap Property**:

.. math::

   \forall node \in H: node.value \geq children(node).value

Complete Binary Tree
^^^^^^^^^^^^^^^^^^^^

A heap is a **complete binary tree**: all levels are fully filled except possibly the last, which is filled from left to right.

.. math::

   \text{height}(H) = \lfloor \log_2 n \rfloor

where :math:`n` is the number of elements.

Array Representation
^^^^^^^^^^^^^^^^^^^^

For a node at index :math:`i` (0-indexed):

.. math::

   \begin{aligned}
   parent(i) &= \lfloor (i-1)/2 \rfloor \\
   left\_child(i) &= 2i + 1 \\
   right\_child(i) &= 2i + 2
   \end{aligned}

**Example**: Array [1, 3, 2, 7, 8, 5, 4] represents:

.. code-block:: text

         1
       /   \
      3     2
     / \   / \
    7   8 5   4
    
   Index: 0  1  2  3  4  5  6
   Value: 1  3  2  7  8  5  4

Tree Properties
---------------

Height and Size
^^^^^^^^^^^^^^^

For a complete binary tree with :math:`n` nodes:

**Height**:

.. math::

   h = \lfloor \log_2 n \rfloor = O(\log n)

**Minimum nodes for height** :math:`h`:

.. math::

   n_{min} = 2^h

**Maximum nodes for height** :math:`h`:

.. math::

   n_{max} = 2^{h+1} - 1

Level Distribution
^^^^^^^^^^^^^^^^^^

For :math:`n` nodes:

.. math::

   \begin{aligned}
   \text{Level 0 (root)} &: 1 \text{ node} \\
   \text{Level 1} &: 2 \text{ nodes} \\
   \text{Level 2} &: 4 \text{ nodes} \\
   \vdots \\
   \text{Level } h &: \text{up to } 2^h \text{ nodes}
   \end{aligned}

**Leaves**: Approximately :math:`n/2` nodes are leaves.

Heap Invariants
---------------

1. **Shape property**: Complete binary tree

2. **Heap property**: Parent ≤ children (min) or parent ≥ children (max)

3. **Root property**: 

   .. math::

      \begin{aligned}
      \text{Min-heap: } root &= \min(H) \\
      \text{Max-heap: } root &= \max(H)
      \end{aligned}

Algorithmic Model
=================

Abstract Data Type
------------------

.. code-block:: text

   ADT Heap:
       Data:
           - array: list of elements
           - size: number of elements
           - comparator: comparison function (min/max)
       
       Operations:
           - Heap(): create empty heap
           - insert(item): add item maintaining heap property
           - extract(): remove and return root (min/max)
           - peek(): view root without removing
           - heapify(array): build heap from unordered array
           - sift_up(index): restore heap property upward
           - sift_down(index): restore heap property downward
       
       Invariants:
           - Complete binary tree shape
           - Heap property at every node
           - Root contains min/max element

Sift Up Algorithm
-----------------

Used after insertion at the end:

.. code-block:: text

   Algorithm: SIFT_UP(heap, index)
   Input: Heap array, index of newly inserted element
   Output: Heap with property restored
   
   1. while index > 0 do
   2.     parent_idx ← ⌊(index - 1) / 2⌋
   3.     
   4.     // For min-heap: if child < parent, swap
   5.     if heap[index] < heap[parent_idx] then
   6.         swap(heap[index], heap[parent_idx])
   7.         index ← parent_idx
   8.     else
   9.         break  // Heap property satisfied
   10.    end if
   11. end while

**Time complexity**: O(log n) - height of tree
**Space complexity**: O(1)

**Visualization**:

.. code-block:: text

   Insert 1 into min-heap [3, 5, 7]:
   
   Step 1: Add to end        Step 2: Sift up
       3                         1
      / \                       / \
     5   7  →  [3,5,7,1]   →   3   7
    /                          /
   1                          5

Sift Down Algorithm
-------------------

Used after removing the root:

.. code-block:: text

   Algorithm: SIFT_DOWN(heap, index, size)
   Input: Heap array, starting index, heap size
   Output: Heap with property restored
   
   1. while true do
   2.     smallest ← index  // For min-heap
   3.     left ← 2 × index + 1
   4.     right ← 2 × index + 2
   5.     
   6.     // Find smallest among node and children
   7.     if left < size and heap[left] < heap[smallest] then
   8.         smallest ← left
   9.     end if
   10.    
   11.    if right < size and heap[right] < heap[smallest] then
   12.        smallest ← right
   13.    end if
   14.    
   15.    // If smallest is not current node, swap and continue
   16.    if smallest ≠ index then
   17.        swap(heap[index], heap[smallest])
   18.        index ← smallest
   19.    else
   20.        break  // Heap property satisfied
   21.    end if
   22. end while

**Time complexity**: O(log n)
**Space complexity**: O(1)

Insert Operation
----------------

.. code-block:: text

   Algorithm: HEAP_INSERT(heap, item)
   Input: Heap, item to insert
   Output: Updated heap
   
   1. // Add item at end (maintains complete tree)
   2. heap.array.append(item)
   3. heap.size ← heap.size + 1
   4. 
   5. // Restore heap property by sifting up
   6. SIFT_UP(heap, heap.size - 1)

**Time complexity**: O(log n)

Extract Operation
-----------------

.. code-block:: text

   Algorithm: HEAP_EXTRACT(heap)
   Input: Heap
   Output: Root element (min or max)
   
   1. if heap.size = 0 then
   2.     error "Heap is empty"
   3. end if
   4. 
   5. // Save root value
   6. result ← heap.array[0]
   7. 
   8. // Move last element to root
   9. heap.array[0] ← heap.array[heap.size - 1]
   10. heap.array.remove_last()
   11. heap.size ← heap.size - 1
   12. 
   13. // Restore heap property by sifting down
   14. if heap.size > 0 then
   15.    SIFT_DOWN(heap, 0, heap.size)
   16. end if
   17. 
   18. return result

**Time complexity**: O(log n)

Heapify Algorithm
-----------------

Build a heap from an unordered array:

.. code-block:: text

   Algorithm: HEAPIFY(array)
   Input: Unordered array
   Output: Array rearranged as heap
   
   1. size ← length(array)
   2. 
   3. // Start from last non-leaf node and sift down
   4. for i ← ⌊size/2⌋ - 1 down to 0 do
   5.     SIFT_DOWN(array, i, size)
   6. end for

**Time complexity**: O(n) - **not** O(n log n)!

**Proof**: Most nodes are near bottom and need few sifts:
- n/2 leaves: 0 operations
- n/4 nodes at height 1: 1 operation each
- n/8 nodes at height 2: 2 operations each
- ...
- Total: n(1/4 + 2/8 + 3/16 + ...) = O(n)

Complexity Analysis
-------------------

Time Complexity
^^^^^^^^^^^^^^^

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
^^^^^^^^^^^^^^^^

* **Heap storage**: O(n)
* **No pointers needed**: Array-based, just store values
* **Auxiliary space**: O(1) for all operations (iterative)

Practical Usage
===============

Installation and Import
-----------------------

.. code-block:: python

   # Install
   pip install sds-tools
   
   # Import
   from sds.tree import MinHeap, MaxHeap, HeapPriorityQueue

Basic Operations
----------------

Min-Heap
^^^^^^^^

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

Max-Heap
^^^^^^^^

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

Priority Queue
^^^^^^^^^^^^^^

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

Real-World Applications
=======================

Application 1: Task Scheduler
------------------------------

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
               time.sleep(0.1)  # Simulate work
           
           return executed
       
       def pending_count(self):
           """Get number of pending tasks."""
           return len(self.tasks)
   
   # Usage
   scheduler = TaskScheduler()
   
   # Schedule tasks with different priorities
   scheduler.schedule("Database backup", priority=1,
                     deadline=datetime.now() + timedelta(hours=1))
   scheduler.schedule("Send emails", priority=5)
   scheduler.schedule("Clean logs", priority=10)
   scheduler.schedule("Critical alert", priority=0,
                     deadline=datetime.now() + timedelta(minutes=5))
   
   # Execute tasks
   scheduler.run()

Application 2: Dijkstra's Algorithm
------------------------------------

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
   graph.add_edge('B', 'C', 1)
   graph.add_edge('B', 'D', 5)
   graph.add_edge('C', 'D', 8)
   graph.add_edge('C', 'E', 10)
   graph.add_edge('D', 'E', 2)
   
   path, distance = graph.dijkstra('A', 'E')
   print(f"Shortest path: {' -> '.join(path)}")
   print(f"Total distance: {distance}")

Application 3: Event-Driven Simulation
---------------------------------------

Discrete event simulation:

.. code-block:: python

   from sds.tree import HeapPriorityQueue
   from dataclasses import dataclass
   from typing import Callable

   @dataclass
   class Event:
       """Simulation event."""
       time: float
       name: str
       handler: Callable
       data: dict = None

   class EventSimulator:
       """Event-driven simulation using heap."""
       
       def __init__(self):
           self.events = HeapPriorityQueue()
           self.current_time = 0.0
       
       def schedule(self, delay, name, handler, data=None):
           """Schedule an event."""
           event_time = self.current_time + delay
           event = Event(event_time, name, handler, data or {})
           self.events.enqueue(event, event_time)
       
       def run(self, until=None):
           """Run simulation until time or no events."""
           while not self.events.is_empty():
               event, event_time = self.events.dequeue()
               
               # Stop if reached time limit
               if until and event_time > until:
                   break
               
               # Advance time
               self.current_time = event_time
               
               # Execute event handler
               print(f"[t={self.current_time:.2f}] {event.name}")
               event.handler(self, event)
   
   # Example: Server simulation
   def customer_arrival(sim, event):
       """Handle customer arrival."""
       print(f"  Customer {event.data['id']} arrived")
       
       # Schedule service completion
       service_time = 2.5
       sim.schedule(service_time, "Service complete",
                   service_complete,
                   {'id': event.data['id']})
   
   def service_complete(sim, event):
       """Handle service completion."""
       print(f"  Customer {event.data['id']} served")
   
   # Run simulation
   sim = EventSimulator()
   
   # Schedule customer arrivals
   sim.schedule(0.0, "Customer arrival", customer_arrival, {'id': 1})
   sim.schedule(1.5, "Customer arrival", customer_arrival, {'id': 2})
   sim.schedule(3.0, "Customer arrival", customer_arrival, {'id': 3})
   
   sim.run(until=10.0)

Application 4: Median Maintenance
----------------------------------

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
   
   # Output:
   # After adding 5: median = 5
   # After adding 15: median = 10.0
   # After adding 1: median = 5
   # After adding 3: median = 4.0
   # ...

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
**Not in-place**: Requires additional array

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

Further Reading
===============

* :doc:`/api/tree/heap` - Complete API reference
* :doc:`binary` - Binary tree fundamentals
* :doc:`segment_tree` - Range queries

References
==========

.. [WikiHeap] Wikipedia contributors. "Heap (data structure)". Wikipedia.
   https://en.wikipedia.org/wiki/Heap_(data_structure)
   
   Comprehensive overview of heap variants and applications.

.. [CLRS] Cormen, T. H., et al. "Introduction to Algorithms", 3rd Edition, Chapter 6
   
   Detailed heap analysis and heapsort algorithm.

.. [VisuAlgoHeap] Halim, S. "Heap Visualization". VisuAlgo.
   https://visualgo.net/en/heap
   
   Interactive heap visualization tool.

.. [Williams] Williams, J. W. J. "Algorithm 232: Heapsort", 1964
   
   Original heapsort paper.

.. [Floyd] Floyd, R. W. "Algorithm 245: Treesort 3", 1964
   
   Bottom-up heap construction in O(n).
