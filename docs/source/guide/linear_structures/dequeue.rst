.. _guide_linear_deque:

===========
Deque Guide
===========

.. currentmodule:: sds.linear

Introduction
============

A **deque** (double-ended queue, pronounced "deck") is a linear data structure
that allows insertion and deletion at **both ends**. Unlike stacks (LIFO) and
queues (FIFO), deques provide maximum flexibility for element access.

.. mermaid::

   graph LR
       A[Front] --> B[Element 1]
       B --> C[Element 2]
       C --> D[Element 3]
       D --> E[Rear]

       F[add_front/remove_front] -.->|Both ends accessible| A
       E -.->|Both ends accessible| G[add_rear/remove_rear]

       style A fill:#e74c3c,stroke:#c0392b,color:#fff
       style E fill:#3498db,stroke:#2980b9,color:#fff
       style C fill:#f39c12

.. note::

   Deques are particularly useful for sliding window algorithms, work-stealing
   schedulers, and any scenario requiring efficient operations at both ends.

Mathematical Model
==================

Formal Definition
-----------------

A deque :math:`D` is an ordered collection:

.. math::

   D = \langle e_1, e_2, \ldots, e_n \rangle

where both :math:`e_1` (front) and :math:`e_n` (rear) are accessible for
insertion and removal.

Operations
----------

Front Operations
^^^^^^^^^^^^^^^^

**Add to front:**

.. math::

   add\_front(D, x) = \langle x, e_1, e_2, \ldots, e_n \rangle

**Remove from front:**

.. math::

   remove\_front(\langle e_1, e_2, \ldots, e_n \rangle) = (e_1, \langle e_2, \ldots, e_n \rangle)

Rear Operations
^^^^^^^^^^^^^^^

**Add to rear:**

.. math::

   add\_rear(D, x) = \langle e_1, e_2, \ldots, e_n, x \rangle

**Remove from rear:**

.. math::

   remove\_rear(\langle e_1, \ldots, e_{n-1}, e_n \rangle) = (e_n, \langle e_1, \ldots, e_{n-1} \rangle)

Properties
^^^^^^^^^^

1. **Bidirectional access**: Operations at both ends in :math:`O(1)`
2. **Generalization**: Subsumes both stack and queue behavior
3. **Size preservation**:

   .. math::

      |add\_rear(remove\_front(D))| = |D|

Deque Invariants
----------------

1. **Size constraint**: :math:`|D| \geq 0`
2. **Front/rear accessibility**: If :math:`|D| > 0`, both :math:`front(D)` and :math:`rear(D)` are defined
3. **Order preservation**: Elements maintain insertion order between operations

Algorithmic Model
=================

Deque ADT
---------

.. code-block:: text

   ADT Deque:
       Data:
           - elements: sequence
           - front: reference to first element
           - rear: reference to last element
           - size: number of elements

       Operations:
           - Deque(): create empty deque
           - add_front(item): insert at front O(1)
           - add_rear(item): insert at rear O(1)
           - remove_front(): remove from front O(1)
           - remove_rear(): remove from rear O(1)
           - peek_front(): view front element O(1)
           - peek_rear(): view rear element O(1)
           - is_empty(): check if empty O(1)
           - size(): get number of elements O(1)

Implementation Strategies
-------------------------

Doubly Linked List Implementation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. mermaid::

   graph LR
       F[Front] --> A[Node 1]
       A <--> B[Node 2]
       B <--> C[Node 3]
       C --> N[None]
       R[Rear] -.-> C

       style F fill:#e74c3c
       style R fill:#3498db

**Advantages:**
   * True :math:`O(1)` for all operations
   * No reallocation needed
   * Dynamic size

**Disadvantages:**
   * Extra memory for prev/next pointers
   * Less cache-friendly than array

Circular Array Implementation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. mermaid::

   graph TD
       A["Array [0,1,2,3,4,5]"]
       B[front = 2]
       C[rear = 5]
       D["[-, -, A, B, C, D]"]

       style A fill:#3498db
       style D fill:#f39c12

**Advantages:**
   * Better cache locality
   * Less memory overhead
   * :math:`O(1)` amortized operations

**Disadvantages:**
   * Reallocation on growth
   * Wrap-around complexity

Algorithm Pseudocode
--------------------

Add to Front
^^^^^^^^^^^^

.. code-block:: text

   Algorithm: ADD_FRONT(D, item)
   Input: Deque D, element item
   Output: Modified deque D
   Time: O(1)

   1. new_node ← Node(item, next=D.head)
   2. if D.head ≠ null then
   3.     D.head.prev ← new_node
   4. else
   5.     D.tail ← new_node
   6. end if
   7. D.head ← new_node
   8. D.size ← D.size + 1

Add to Rear
^^^^^^^^^^^

.. code-block:: text

   Algorithm: ADD_REAR(D, item)
   Input: Deque D, element item
   Output: Modified deque D
   Time: O(1)

   1. new_node ← Node(item, prev=D.tail)
   2. if D.tail ≠ null then
   3.     D.tail.next ← new_node
   4. else
   5.     D.head ← new_node
   6. end if
   7. D.tail ← new_node
   8. D.size ← D.size + 1

Remove from Front
^^^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: REMOVE_FRONT(D)
   Input: Deque D
   Output: Front element
   Time: O(1)

   1. if D.head = null then
   2.     raise EmptyStructureError
   3. end if
   4. item ← D.head.data
   5. D.head ← D.head.next
   6. if D.head ≠ null then
   7.     D.head.prev ← null
   8. else
   9.     D.tail ← null
   10. end if
   11. D.size ← D.size - 1
   12. return item

Remove from Rear
^^^^^^^^^^^^^^^^

.. code-block:: text

   Algorithm: REMOVE_REAR(D)
   Input: Deque D
   Output: Rear element
   Time: O(1)

   1. if D.tail = null then
   2.     raise EmptyStructureError
   3. end if
   4. item ← D.tail.data
   5. D.tail ← D.tail.prev
   6. if D.tail ≠ null then
   7.     D.tail.next ← null
   8. else
   9.     D.head ← null
   10. end if
   11. D.size ← D.size - 1
   12. return item

Complexity Analysis
-------------------

.. list-table::
   :header-rows: 1
   :widths: 30 20 20 30

   * - Operation
     - Linked List
     - Circular Array
     - Notes
   * - **add_front**
     - O(1)
     - O(1)*
     - * Amortized for array
   * - **add_rear**
     - O(1)
     - O(1)*
     - * Amortized for array
   * - **remove_front**
     - O(1)
     - O(1)
     - Always constant
   * - **remove_rear**
     - O(1)
     - O(1)
     - Always constant
   * - **peek_front/rear**
     - O(1)
     - O(1)
     - Just read access
   * - **Random access**
     - O(n)
     - O(1)
     - Array advantage
   * - **Space**
     - O(n)
     - O(n)
     - Proportional to size

Practical Usage
===============

Basic Operations
----------------

.. code-block:: python

   from sds.linear import Deque

   # Create deque
   deque = Deque()

   # Add to both ends
   deque.add_rear(2)      # [2]
   deque.add_front(1)     # [1, 2]
   deque.add_rear(3)      # [1, 2, 3]
   deque.add_front(0)     # [0, 1, 2, 3]

   print(list(deque))     # Output: [0, 1, 2, 3]

Peek Operations
---------------

.. code-block:: python

   # View without removing
   print(deque.peek_front())  # Output: 0
   print(deque.peek_rear())   # Output: 3

   # Deque unchanged
   print(len(deque))          # Output: 4

Remove Operations
-----------------

.. code-block:: python

   # Remove from either end
   print(deque.remove_front())  # Output: 0
   print(deque.remove_rear())   # Output: 3

   print(list(deque))           # Output: [1, 2]

Iteration
---------

.. code-block:: python

   deque = Deque()
   for i in [1, 2, 3, 4, 5]:
       deque.add_rear(i)

   # Forward iteration
   for item in deque:
       print(item)  # Output: 1, 2, 3, 4, 5

   # Reverse iteration (if supported)
   for item in reversed(deque):
       print(item)  # Output: 5, 4, 3, 2, 1

Real-World Applications
=======================

Application 1: Sliding Window Maximum
--------------------------------------

Find the maximum element in each sliding window of size k.

.. code-block:: python

   from sds.linear import Deque

   def sliding_window_max(nums, k):
       """
       Find maximum in each window of size k.

       Time: O(n), each element added/removed once
       Space: O(k) for the deque
       """
       if not nums or k <= 0:
           return []

       deque = Deque()  # Stores indices
       result = []

       for i, num in enumerate(nums):
           # Remove indices outside current window
           while (not deque.is_empty() and
                  deque.peek_front() <= i - k):
               deque.remove_front()

           # Remove indices of smaller elements
           # (they won't be max in any future window)
           while (not deque.is_empty() and
                  nums[deque.peek_rear()] < num):
               deque.remove_rear()

           deque.add_rear(i)

           # Add to result once window is full
           if i >= k - 1:
               result.append(nums[deque.peek_front()])

       return result

   # Test
   nums = [1, 3, -1, -3, 5, 3, 6, 7]
   k = 3
   print(sliding_window_max(nums, k))
   # Output: [3, 3, 5, 5, 6, 7]

   # Explanation:
   # Window [1, 3, -1]    → max = 3
   # Window [3, -1, -3]   → max = 3
   # Window [-1, -3, 5]   → max = 5
   # Window [-3, 5, 3]    → max = 5
   # Window [5, 3, 6]     → max = 6
   # Window [3, 6, 7]     → max = 7

Application 2: Palindrome Checker
----------------------------------

Check if a sequence is a palindrome using deque.

.. code-block:: python

   from sds.linear import Deque

   def is_palindrome(text):
       """
       Check if text is a palindrome.

       Time: O(n)
       Space: O(n)
       """
       # Clean text: remove spaces, lowercase
       text = ''.join(text.split()).lower()

       deque = Deque()
       for char in text:
           deque.add_rear(char)

       # Compare from both ends
       while len(deque) > 1:
           if deque.remove_front() != deque.remove_rear():
               return False

       return True

   # Test
   print(is_palindrome("A man a plan a canal Panama"))  # True
   print(is_palindrome("race a car"))                   # False
   print(is_palindrome("Was it a rat I saw"))           # True

Application 3: Work-Stealing Scheduler
---------------------------------------

Implement a work-stealing task scheduler where workers can take tasks
from either end of their deque.

.. code-block:: python

   from sds.linear import Deque
   import random

   class WorkStealingScheduler:
       """
       Task scheduler with work stealing.

       - Owner takes from rear (newest tasks)
       - Thieves steal from front (oldest tasks)
       """

       def __init__(self):
           self.deque = Deque()

       def add_task(self, task):
           """Add new task (owner operation)."""
           self.deque.add_rear(task)

       def get_own_task(self):
           """Get own task from rear (LIFO for cache locality)."""
           if not self.deque.is_empty():
               return self.deque.remove_rear()
           return None

       def steal_task(self):
           """Steal task from front (FIFO for fairness)."""
           if not self.deque.is_empty():
               return self.deque.remove_front()
           return None

       def has_work(self):
           """Check if tasks available."""
           return not self.deque.is_empty()

   # Simulation
   class Worker:
       def __init__(self, name):
           self.name = name
           self.scheduler = WorkStealingScheduler()

       def execute_tasks(self, workers):
           """Execute tasks, steal if needed."""
           while True:
               # Try own queue first
               task = self.scheduler.get_own_task()

               if task:
                   print(f"{self.name} executing own task: {task}")
               else:
                   # Try to steal
                   for other in workers:
                       if other != self and other.scheduler.has_work():
                           task = other.scheduler.steal_task()
                           if task:
                               print(f"{self.name} stole task from {other.name}: {task}")
                               break

                   if not task:
                       break  # No more work

   # Test
   w1 = Worker("Worker-1")
   w2 = Worker("Worker-2")

   # Worker-1 gets many tasks
   for i in range(5):
       w1.scheduler.add_task(f"Task-{i}")

   w1.execute_tasks([w1, w2])
   w2.execute_tasks([w1, w2])

Application 4: Browser History Navigation
------------------------------------------

Implement browser-like forward/back navigation.

.. code-block:: python

   from sds.linear import Deque

   class BrowserHistory:
       """
       Browser history with forward/back navigation.

       Current page is at the rear of back_history.
       """

       def __init__(self, homepage):
           self.back_history = Deque()
           self.forward_history = Deque()
           self.back_history.add_rear(homepage)

       def visit(self, url):
           """Visit new URL."""
           self.back_history.add_rear(url)
           # Clear forward history on new visit
           self.forward_history = Deque()

       def back(self, steps=1):
           """Go back in history."""
           while steps > 0 and len(self.back_history) > 1:
               current = self.back_history.remove_rear()
               self.forward_history.add_rear(current)
               steps -= 1

           return self.current_url()

       def forward(self, steps=1):
           """Go forward in history."""
           while steps > 0 and not self.forward_history.is_empty():
               page = self.forward_history.remove_rear()
               self.back_history.add_rear(page)
               steps -= 1

           return self.current_url()

       def current_url(self):
           """Get current URL."""
           if not self.back_history.is_empty():
               return self.back_history.peek_rear()
           return None

   # Test
   browser = BrowserHistory("homepage.com")
   browser.visit("page1.com")
   browser.visit("page2.com")
   browser.visit("page3.com")

   print(browser.current_url())     # page3.com
   print(browser.back(2))           # page1.com
   print(browser.forward(1))        # page2.com
   browser.visit("page4.com")
   print(browser.back(1))           # page2.com
   print(browser.forward(1))        # page4.com

Best Practices
==============

Do's
----

✅ **Use for bidirectional access**

.. code-block:: python

   # Good: Deque shines with operations at both ends
   deque = Deque()
   deque.add_front(1)   # O(1)
   deque.add_rear(2)    # O(1)
   deque.remove_front() # O(1)
   deque.remove_rear()  # O(1)

✅ **Choose deque for sliding windows**

.. code-block:: python

   # Good: Efficient for window algorithms
   def process_sliding_window(data, k):
       window = Deque()
       # Use add_rear/remove_front for sliding
       ...

✅ **Use as both stack and queue**

.. code-block:: python

   # Stack behavior
   deque.add_rear(x)    # push
   deque.remove_rear()  # pop

   # Queue behavior
   deque.add_rear(x)      # enqueue
   deque.remove_front()   # dequeue

Don'ts
------

❌ **Don't use for random access**

.. code-block:: python

   # Bad: O(n) access
   item = deque[5]

   # Good: Use list for random access
   items = list(deque)
   item = items[5]  # O(1)

❌ **Don't ignore which end matters**

.. code-block:: python

   # Bad: Inconsistent usage
   deque.add_front(x)
   item = deque.remove_rear()  # Wrong end!

   # Good: Be deliberate
   deque.add_rear(x)
   item = deque.remove_rear()  # Same end

❌ **Don't use when simple queue/stack suffices**

.. code-block:: python

   # Bad: Overkill
   deque = Deque()
   deque.add_rear(x)
   deque.remove_front()  # Just need a queue

   # Good: Use appropriate structure
   queue = Queue()
   queue.enqueue(x)
   queue.dequeue()

When to Use Deque
=================

**Use deque when:**
   * Need efficient operations at **both ends**
   * Implementing sliding window algorithms
   * Building work-stealing schedulers
   * Need both stack and queue behavior
   * Implementing palindrome checks or similar bidirectional algorithms

**Don't use deque when:**
   * Only need FIFO (use Queue instead)
   * Only need LIFO (use Stack instead)
   * Need frequent random access (use list/array)
   * Operations are only at one end

Comparison with Alternatives
=============================

Deque vs Queue
--------------

.. code-block:: python

   # Queue: Only rear/front
   queue.enqueue(x)      # rear only
   queue.dequeue()       # front only

   # Deque: Both ends
   deque.add_rear(x)     # rear
   deque.add_front(x)    # front
   deque.remove_rear()   # rear
   deque.remove_front()  # front

Deque vs Stack
--------------

.. code-block:: python

   # Stack: Only top
   stack.push(x)   # top only
   stack.pop()     # top only

   # Deque: Both ends
   deque.add_rear(x)     # like push
   deque.remove_rear()   # like pop
   deque.add_front(x)    # bonus!
   deque.remove_front()  # bonus!

Deque vs List
-------------

.. list-table::
   :header-rows: 1
   :widths: 30 20 20 30

   * - Operation
     - Deque
     - List
     - Winner
   * - Add/remove front
     - O(1)
     - O(n)
     - **Deque**
   * - Add/remove rear
     - O(1)
     - O(1)*
     - Tie
   * - Random access
     - O(n)
     - O(1)
     - **List**
   * - Memory
     - O(n)
     - O(n)
     - Tie

\* Amortized for list

Common Pitfalls
===============

1. **Forgetting which end is which**

   .. code-block:: python

      # Remember: front = left, rear = right
      # [front] ... [rear]

2. **Using wrong structure**

   .. code-block:: python

      # If only using one end, use Stack or Queue

3. **Empty deque operations**

   .. code-block:: python

      # Always check before removing
      if not deque.is_empty():
          item = deque.remove_front()

4. **Performance expectations**

   .. code-block:: python

      # Random access is O(n), not O(1)
      # Convert to list if needed

See Also
========

* :doc:`/api/linear/queue` - API reference
* :doc:`queue` - FIFO structure
* :doc:`stack` - LIFO structure
* :doc:`linked_list` - Implementation details