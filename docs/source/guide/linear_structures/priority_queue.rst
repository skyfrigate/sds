.. _guide_linear_priority_queue:

====================
Priority Queue Guide
====================

.. currentmodule:: sds.linear

Introduction
============

A **priority queue** is an abstract data structure where each element has an
associated **priority**. Elements are dequeued in priority order rather than
insertion order. Think of it like an emergency room: patients are treated by
urgency, not by arrival time.

.. mermaid::

   graph TB
       A["Priority Queue"]
       B["Element: 'Critical'<br/>Priority: 1"]
       C["Element: 'High'<br/>Priority: 3"]
       D["Element: 'Medium'<br/>Priority: 5"]
       E["Element: 'Low'<br/>Priority: 8"]

       A --> B
       A --> C
       A --> D
       A --> E

       F[dequeue] -.->|Returns highest priority| B

       style A fill:#9b59b6,color:#fff
       style B fill:#e74c3c,color:#fff
       style F fill:#e74c3c,stroke:#c0392b,color:#fff

.. note::

   By convention, **lower numeric values indicate higher priority**
   (priority 1 > priority 5), similar to ranking systems. This can be
   customized based on your needs.

Mathematical Model
==================

Formal Definition
-----------------

A priority queue :math:`PQ` is a collection of elements:

.. math::

   PQ = \{(e_1, p_1), (e_2, p_2), \ldots, (e_n, p_n)\}

where each element :math:`e_i` has an associated priority :math:`p_i \in \mathbb{R}`.

Priority Ordering
-----------------

Elements are ordered by priority, not insertion order:

.. math::

   dequeue(PQ) = (e_i, PQ \setminus \{(e_i, p_i)\})

where :math:`p_i = \min_{(e, p) \in PQ} p` (assuming lower = higher priority)

Operations
----------

Enqueue Operation
^^^^^^^^^^^^^^^^^

Adds element with priority:

.. math::

   enqueue(PQ, e, p) = PQ \cup \{(e, p)\}

**Properties:**
   * :math:`|PQ'| = |PQ| + 1`
   * Position determined by priority, not insertion order
   * Time complexity depends on implementation

Dequeue Operation
^^^^^^^^^^^^^^^^^

Removes and returns highest priority element:

.. math::

   dequeue(PQ) = (e_{min}, PQ \setminus \{(e_{min}, p_{min})\})

where :math:`p_{min} = \min\{p_1, p_2, \ldots, p_n\}`

**Properties:**
   * Returns element with highest priority
   * :math:`|PQ'| = |PQ| - 1`
   * Undefined for empty queue

Peek Operation
^^^^^^^^^^^^^^

Views highest priority element without removing:

.. math::

   peek(PQ) = e_{min} \text{ where } p_{min} = \min\{p_1, \ldots, p_n\}

Priority Queue Invariants
--------------------------

1. **Priority ordering**: :math:`\forall (e_i, p_i) \in PQ : dequeue()` returns element with minimum :math:`p`
2. **Size**: :math:`|PQ| \geq 0`
3. **Uniqueness not required**: Multiple elements can have same priority
4. **FIFO within priority**: Elements with equal priority follow FIFO (optional)

Algorithmic Model
=================

Priority Queue ADT
------------------

.. code-block:: text

   ADT PriorityQueue:
       Data:
           - elements: collection of (element, priority) pairs
           - size: number of elements

       Operations:
           - PriorityQueue(): create empty queue
           - enqueue(item, priority): add with priority
           - dequeue(): remove highest priority item
           - peek(): view highest priority item
           - is_empty(): check if empty
           - size(): get number of elements
           - update_priority(item, new_priority): change priority

Implementation Strategies
-------------------------

1. Unsorted List/Linked List
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Store elements in insertion order.

**Advantages:**
   * Simple implementation
   * :math:`O(1)` enqueue

**Disadvantages:**
   * :math:`O(n)` dequeue (must scan for min)
   * :math:`O(n)` peek

2. Sorted List
^^^^^^^^^^^^^^

Maintain elements sorted by priority.

**Advantages:**
   * :math:`O(1)` dequeue
   * :math:`O(1)` peek

**Disadvantages:**
   * :math:`O(n)` enqueue (must find position)
   * Complex insertion logic

3. Binary Heap (Recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use min-heap or max-heap structure.

.. mermaid::

   graph TD
       A["1<br/>(highest)"]
       B["3"]
       C["5"]
       D["8"]
       E["7"]
       F["9"]
       G["10"]

       A --> B
       A --> C
       B --> D
       B --> E
       C --> F
       C --> G

       style A fill:#e74c3c,color:#fff
       style B fill:#f39c12
       style C fill:#f39c12

**Advantages:**
   * :math:`O(\log n)` enqueue
   * :math:`O(\log n)` dequeue
   * :math:`O(1)` peek
   * Best balance for most use cases

**Disadvantages:**
   * More complex implementation
   * No efficient search for arbitrary element

Algorithm Pseudocode
--------------------

Min-Heap Based Implementation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Enqueue (Insert):**

.. code-block:: text

   Algorithm: ENQUEUE(PQ, item, priority)
   Input: PriorityQueue PQ, element item, priority value
   Output: Modified PQ
   Time: O(log n)

   1. Add (item, priority) to end of heap array
   2. PQ.size ← PQ.size + 1
   3. HEAPIFY_UP(PQ, PQ.size - 1)

**Heapify Up:**

.. code-block:: text

   Algorithm: HEAPIFY_UP(PQ, index)
   // Restore heap property by moving up

   1. while index > 0 do
   2.     parent ← (index - 1) / 2
   3.     if PQ[index].priority < PQ[parent].priority then
   4.         swap(PQ[index], PQ[parent])
   5.         index ← parent
   6.     else
   7.         break
   8.     end if
   9. end while

**Dequeue (Extract Min):**

.. code-block:: text

   Algorithm: DEQUEUE(PQ)
   Input: PriorityQueue PQ
   Output: Highest priority element
   Time: O(log n)

   1. if PQ.size = 0 then
   2.     raise EmptyStructureError
   3. end if
   4. min_item ← PQ[0]
   5. PQ[0] ← PQ[PQ.size - 1]
   6. PQ.size ← PQ.size - 1
   7. HEAPIFY_DOWN(PQ, 0)
   8. return min_item

**Heapify Down:**

.. code-block:: text

   Algorithm: HEAPIFY_DOWN(PQ, index)
   // Restore heap property by moving down

   1. while 2 * index + 1 < PQ.size do
   2.     left ← 2 * index + 1
   3.     right ← 2 * index + 2
   4.     smallest ← index
   5.
   6.     if left < PQ.size and PQ[left].priority < PQ[smallest].priority then
   7.         smallest ← left
   8.     end if
   9.     if right < PQ.size and PQ[right].priority < PQ[smallest].priority then
   10.         smallest ← right
   11.     end if
   12.
   13.     if smallest ≠ index then
   14.         swap(PQ[index], PQ[smallest])
   15.         index ← smallest
   16.     else
   17.         break
   18.     end if
   19. end while

**Peek:**

.. code-block:: text

   Algorithm: PEEK(PQ)
   Input: PriorityQueue PQ
   Output: Highest priority element (without removal)
   Time: O(1)

   1. if PQ.size = 0 then
   2.     raise EmptyStructureError
   3. end if
   4. return PQ[0]

Complexity Analysis
-------------------

.. list-table::
   :header-rows: 1
   :widths: 25 20 20 20 15

   * - Operation
     - Unsorted List
     - Sorted List
     - Binary Heap
     - Best Choice
   * - **Enqueue**
     - O(1)
     - O(n)
     - O(log n)
     - Heap
   * - **Dequeue**
     - O(n)
     - O(1)
     - O(log n)
     - Heap*
   * - **Peek**
     - O(n)
     - O(1)
     - O(1)
     - Sorted/Heap
   * - **Update Priority**
     - O(n)
     - O(n)
     - O(log n)**
     - Heap
   * - **Space**
     - O(n)
     - O(n)
     - O(n)
     - Tie

\* Heap provides best **amortized** performance for mixed operations

\** With additional index tracking

Practical Usage
===============

Basic Operations
----------------

.. code-block:: python

   from sds.linear import PriorityQueue

   # Create priority queue
   pq = PriorityQueue()

   # Enqueue with priorities (lower = higher priority)
   pq.enqueue("Critical bug", priority=1)
   pq.enqueue("Feature request", priority=5)
   pq.enqueue("Urgent hotfix", priority=2)
   pq.enqueue("Documentation", priority=8)

   # Dequeue in priority order
   print(pq.dequeue())  # Output: "Critical bug" (priority 1)
   print(pq.dequeue())  # Output: "Urgent hotfix" (priority 2)
   print(pq.dequeue())  # Output: "Feature request" (priority 5)

Using Custom Priority Function
-------------------------------

.. code-block:: python

   from sds.linear import PriorityQueue

   # Create with custom comparison (higher number = higher priority)
   pq = PriorityQueue(reverse=True)

   pq.enqueue("Low", 1)
   pq.enqueue("High", 10)
   pq.enqueue("Medium", 5)

   print(pq.dequeue())  # Output: "High" (10)
   print(pq.dequeue())  # Output: "Medium" (5)
   print(pq.dequeue())  # Output: "Low" (1)

Priority Items
--------------

.. code-block:: python

   from sds.linear import PriorityQueue, PriorityItem

   # Using PriorityItem wrapper
   pq = PriorityQueue()

   pq.enqueue(PriorityItem(data="Task A", priority=3))
   pq.enqueue(PriorityItem(data="Task B", priority=1))
   pq.enqueue(PriorityItem(data="Task C", priority=2))

   while not pq.is_empty():
       item = pq.dequeue()
       print(f"{item.data} (priority: {item.priority})")

Checking State
--------------

.. code-block:: python

   # Check before operations
   if not pq.is_empty():
       next_item = pq.peek()
       print(f"Next: {next_item}")

   # Get size
   print(f"Queue size: {len(pq)}")

Real-World Applications
=======================

Application 1: Task Scheduler with Priorities
----------------------------------------------

.. code-block:: python

   from sds.linear import PriorityQueue
   import time

   class Task:
       def __init__(self, name, priority, duration):
           self.name = name
           self.priority = priority
           self.duration = duration

       def execute(self):
           print(f"Executing {self.name} (priority {self.priority})...")
           time.sleep(self.duration)
           print(f"  Completed {self.name}")

       def __repr__(self):
           return f"Task({self.name}, p={self.priority})"

   class PriorityTaskScheduler:
       def __init__(self):
           self.queue = PriorityQueue()

       def add_task(self, name, priority, duration=0.1):
           """Add task with priority."""
           task = Task(name, priority, duration)
           self.queue.enqueue(task, priority)
           print(f"Added: {task}")

       def run_all(self):
           """Execute all tasks in priority order."""
           print("\nExecuting tasks by priority:")
           while not self.queue.is_empty():
               task = self.queue.dequeue()
               task.execute()

   # Usage
   scheduler = PriorityTaskScheduler()

   scheduler.add_task("Update database", priority=2)
   scheduler.add_task("Fix critical bug", priority=1)
   scheduler.add_task("Send email", priority=5)
   scheduler.add_task("Generate report", priority=3)
   scheduler.add_task("System backup", priority=4)

   scheduler.run_all()

   # Output order:
   # 1. Fix critical bug
   # 2. Update database
   # 3. Generate report
   # 4. System backup
   # 5. Send email

Application 2: Dijkstra's Shortest Path
----------------------------------------

.. code-block:: python

   from sds.linear import PriorityQueue
   import math

   def dijkstra(graph, start):
       """
       Find shortest paths from start to all vertices.

       Time: O((V + E) log V) with binary heap
       Space: O(V)
       """
       # Initialize distances
       distances = {vertex: math.inf for vertex in graph}
       distances[start] = 0

       # Priority queue: (distance, vertex)
       pq = PriorityQueue()
       pq.enqueue(start, priority=0)

       visited = set()

       while not pq.is_empty():
           current = pq.dequeue()

           if current in visited:
               continue

           visited.add(current)
           current_dist = distances[current]

           # Check neighbors
           for neighbor, weight in graph[current].items():
               distance = current_dist + weight

               # Found shorter path
               if distance < distances[neighbor]:
                   distances[neighbor] = distance
                   pq.enqueue(neighbor, priority=distance)

       return distances

   # Test graph
   graph = {
       'A': {'B': 4, 'C': 2},
       'B': {'A': 4, 'C': 1, 'D': 5},
       'C': {'A': 2, 'B': 1, 'D': 8, 'E': 10},
       'D': {'B': 5, 'C': 8, 'E': 2},
       'E': {'C': 10, 'D': 2}
   }

   distances = dijkstra(graph, 'A')
   print("Shortest distances from A:")
   for vertex, dist in sorted(distances.items()):
       print(f"  {vertex}: {dist}")

   # Output:
   # A: 0
   # B: 3  (A → C → B)
   # C: 2  (A → C)
   # D: 8  (A → C → B → D)
   # E: 10 (A → C → B → D → E)

Application 3: Event-Driven Simulation
---------------------------------------

.. code-block:: python

   from sds.linear import PriorityQueue

   class Event:
       def __init__(self, time, name, handler):
           self.time = time
           self.name = name
           self.handler = handler

       def execute(self):
           print(f"[T={self.time}] {self.name}")
           self.handler()

   class EventSimulator:
       """
       Discrete event simulator using priority queue.
       Events are processed in chronological order.
       """

       def __init__(self):
           self.queue = PriorityQueue()
           self.current_time = 0

       def schedule(self, time, name, handler):
           """Schedule event at specific time."""
           event = Event(time, name, handler)
           self.queue.enqueue(event, priority=time)

       def run(self, until_time=None):
           """Run simulation."""
           while not self.queue.is_empty():
               event = self.queue.dequeue()

               if until_time and event.time > until_time:
                   # Re-queue and stop
                   self.queue.enqueue(event, priority=event.time)
                   break

               self.current_time = event.time
               event.execute()

   # Bank simulation example
   def customer_arrival():
       print("  → Customer arrived")

   def customer_served():
       print("  → Customer served")

   def customer_departed():
       print("  → Customer departed")

   sim = EventSimulator()

   # Schedule events
   sim.schedule(0, "Bank opens", lambda: print("  🏦 Opening"))
   sim.schedule(1, "Customer 1 arrives", customer_arrival)
   sim.schedule(3, "Customer 2 arrives", customer_arrival)
   sim.schedule(4, "Customer 1 served", customer_served)
   sim.schedule(6, "Customer 1 departs", customer_departed)
   sim.schedule(8, "Customer 2 served", customer_served)
   sim.schedule(10, "Customer 2 departs", customer_departed)
   sim.schedule(12, "Bank closes", lambda: print("  🔒 Closing"))

   print("=== Bank Simulation ===")
   sim.run()

Application 4: Merge K Sorted Lists
------------------------------------

.. code-block:: python

   from sds.linear import PriorityQueue

   def merge_k_sorted_lists(lists):
       """
       Merge k sorted lists into one sorted list.

       Time: O(N log k) where N = total elements, k = number of lists
       Space: O(k) for the priority queue
       """
       pq = PriorityQueue()
       result = []

       # Initialize: add first element from each list
       for i, lst in enumerate(lists):
           if lst:  # Non-empty list
               # Priority: (value, list_index, element_index)
               pq.enqueue((i, 0), priority=lst[0])

       # Process until queue empty
       while not pq.is_empty():
           list_idx, elem_idx = pq.dequeue()
           value = lists[list_idx][elem_idx]
           result.append(value)

           # Add next element from same list
           next_idx = elem_idx + 1
           if next_idx < len(lists[list_idx]):
               next_value = lists[list_idx][next_idx]
               pq.enqueue((list_idx, next_idx), priority=next_value)

       return result

   # Test
   lists = [
       [1, 4, 7, 10],
       [2, 5, 8, 11],
       [3, 6, 9, 12]
   ]

   merged = merge_k_sorted_lists(lists)
   print("Merged list:", merged)
   # Output: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

Application 5: Huffman Coding
------------------------------

.. code-block:: python

   from sds.linear import PriorityQueue

   class HuffmanNode:
       def __init__(self, char, freq, left=None, right=None):
           self.char = char
           self.freq = freq
           self.left = left
           self.right = right

       def is_leaf(self):
           return self.left is None and self.right is None

   def build_huffman_tree(frequencies):
       """
       Build Huffman tree from character frequencies.

       Time: O(n log n)
       """
       pq = PriorityQueue()

       # Add all characters to priority queue
       for char, freq in frequencies.items():
           node = HuffmanNode(char, freq)
           pq.enqueue(node, priority=freq)

       # Build tree bottom-up
       while len(pq) > 1:
           # Get two minimum frequency nodes
           left = pq.dequeue()
           right = pq.dequeue()

           # Create parent node
           parent = HuffmanNode(
               char=None,
               freq=left.freq + right.freq,
               left=left,
               right=right
           )

           pq.enqueue(parent, priority=parent.freq)

       return pq.dequeue()  # Root

   def generate_codes(root, code="", codes=None):
       """Generate Huffman codes from tree."""
       if codes is None:
           codes = {}

       if root.is_leaf():
           codes[root.char] = code
           return codes

       if root.left:
           generate_codes(root.left, code + "0", codes)
       if root.right:
           generate_codes(root.right, code + "1", codes)

       return codes

   # Example
   text = "hello world"
   frequencies = {}
   for char in text:
       frequencies[char] = frequencies.get(char, 0) + 1

   tree = build_huffman_tree(frequencies)
   codes = generate_codes(tree)

   print("Huffman Codes:")
   for char, code in sorted(codes.items()):
       freq = frequencies[char]
       print(f"  '{char}': {code} (freq={freq})")

Best Practices
==============

Do's
----

✅ **Use for priority-based processing**

.. code-block:: python

   # Good: Process by importance
   pq = PriorityQueue()
   pq.enqueue("critical", priority=1)
   pq.enqueue("normal", priority=5)
   pq.enqueue("low", priority=10)

✅ **Choose appropriate priority scale**

.. code-block:: python

   # Good: Clear priority levels
   CRITICAL = 1
   HIGH = 2
   MEDIUM = 5
   LOW = 10

   pq.enqueue(task, priority=CRITICAL)

✅ **Check empty before dequeue**

.. code-block:: python

   # Good: Safe dequeue
   if not pq.is_empty():
       item = pq.dequeue()

Don'ts
------

❌ **Don't use for FIFO order**

.. code-block:: python

   # Bad: Just use regular Queue
   pq = PriorityQueue()
   pq.enqueue(item, priority=time)  # Overkill

   # Good: Use Queue
   queue = Queue()
   queue.enqueue(item)

❌ **Don't confuse priority direction**

.. code-block:: python

   # Bad: Unclear
   pq.enqueue("urgent", priority=100)  # Is 100 high or low?

   # Good: Document convention
   # Lower number = higher priority
   pq.enqueue("urgent", priority=1)

❌ **Don't forget about equal priorities**

.. code-block:: python

   # Consider what happens with ties
   pq.enqueue("A", priority=5)
   pq.enqueue("B", priority=5)
   # Order of A and B is undefined

When to Use Priority Queue
===========================

**Use priority queue when:**
   * Processing by importance, not arrival order
   * Implementing graph algorithms (Dijkstra, Prim, A*)
   * Event-driven simulations
   * Scheduling with priorities
   * Finding k-smallest/largest elements
   * Huffman coding

**Don't use priority queue when:**
   * Need strict FIFO order (use Queue)
   * Need strict LIFO order (use Stack)
   * All items have equal priority
   * Frequent arbitrary access needed

Common Pitfalls
===============

1. **Priority confusion**

   .. code-block:: python

      # Always document: lower = higher or vice versa
      # Default: lower number = higher priority

2. **Not handling ties**

   .. code-block:: python

      # Elements with same priority have undefined order
      # Add timestamp as tiebreaker if needed

3. **Wrong use case**

   .. code-block:: python

      # Don't use PQ when simple Queue suffices

4. **Performance misconceptions**

   .. code-block:: python

      # Binary heap: O(log n) enqueue/dequeue
      # Not O(1) like simple queue

See Also
========

* :doc:`/api/linear/queue` - API reference
* :doc:`queue` - FIFO structure
* :doc:`dequeue` - Double-ended queue
* :doc:`/guide/tree_structures/heap` - Heap implementation details