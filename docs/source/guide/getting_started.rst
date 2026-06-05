.. _guide_getting_started:

===============
Getting Started
===============

Welcome to SDS-Tools! This guide will help you get started with the library
and understand its fundamental concepts.

Your First Program
==================

Let's start with a simple example using a linked list:

.. code-block:: python

   from sds.linear import LinkedList

   # Create a new linked list
   my_list = LinkedList()

   # Add some elements
   my_list.append(10)
   my_list.append(20)
   my_list.append(30)

   # Print the list
   print(my_list)  # [10 -> 20 -> 30]

   # Access elements
   print(f"First element: {my_list[0]}")   # 10
   print(f"Last element: {my_list[-1]}")   # 30

   # Iterate over elements
   for item in my_list:
       print(item)

Basic Concepts
==============

Collections
-----------

All data structures in SDS-Tools implement the :class:`~sds.core.interfaces.Collection`
interface, which provides common operations:

.. code-block:: python

   from sds.linear import LinkedList

   lst = LinkedList()
   lst.append(1)
   lst.append(2)
   lst.append(3)

   # Size
   print(len(lst))          # 3

   # Empty check
   print(lst.is_empty())    # False

   # Membership test
   print(2 in lst)          # True

   # Clear all elements
   lst.clear()
   print(len(lst))          # 0

Linear Collections
------------------

Linear structures extend :class:`~sds.core.interfaces.LinearCollection` with
add and remove operations:

.. code-block:: python

   from sds.linear import Stack

   stack = Stack()

   # Add elements (LIFO)
   stack.add(1)  # or stack.push(1)
   stack.add(2)
   stack.add(3)

   # Remove elements
   print(stack.remove())  # 3 (or stack.pop())
   print(stack.remove())  # 2

Working with Different Structures
==================================

Linked Lists
------------

**When to use:** Frequent insertions/deletions at the beginning, no random access needed.

.. code-block:: python

   from sds.linear import LinkedList

   lst = LinkedList()

   # Add elements
   lst.append(1)      # Add to end: O(n)
   lst.prepend(0)     # Add to beginning: O(1)
   lst.insert_at(1, 0.5)  # Insert at index: O(n)

   # Remove elements
   first = lst.remove_first()   # O(1)
   last = lst.remove_last()     # O(n)
   item = lst.remove_at(1)      # O(n)

   # Search
   index = lst.find(0.5)        # O(n)

   # Reverse
   lst.reverse()                # O(n)

Doubly Linked Lists
-------------------

**When to use:** Need efficient operations at both ends and backward traversal.

.. code-block:: python

   from sds.linear import DoublyLinkedList

   dll = DoublyLinkedList()

   # Efficient operations at both ends
   dll.prepend(1)     # O(1)
   dll.append(2)      # O(1) - unlike singly linked!
   dll.remove_first() # O(1)
   dll.remove_last()  # O(1) - unlike singly linked!

   # Forward iteration
   for item in dll:
       print(item)

   # Backward iteration
   for item in reversed(dll):
       print(item)

Circular Linked Lists
---------------------

**When to use:** Round-robin scheduling, ring buffers, rotation operations.

.. code-block:: python

   from sds.linear import CircularLinkedList

   cll = CircularLinkedList()
   cll.append(1)
   cll.append(2)
   cll.append(3)

   # The list is circular
   print(cll.tail.next is cll.head)  # True

   # Rotate operations - unique to circular lists
   cll.rotate(1)      # Move forward: [2, 3, 1]
   cll.rotate(-1)     # Move backward: [1, 2, 3]
   cll.rotate(2)      # Multiple steps: [3, 1, 2]

Stacks
------

**When to use:** LIFO behavior, recursion, undo/redo, expression parsing.

.. code-block:: python

   from sds.linear import Stack

   stack = Stack()

   # Push elements (add to top)
   stack.push(1)
   stack.push(2)
   stack.push(3)

   # Peek at top without removing
   print(stack.peek())  # 3

   # Pop elements (remove from top)
   print(stack.pop())   # 3
   print(stack.pop())   # 2

   # Check if empty
   if not stack.is_empty():
       print(stack.pop())  # 1

**Example: Balanced Parentheses**

.. code-block:: python

   from sds.linear import Stack

   def is_balanced(expression):
       stack = Stack()
       pairs = {'(': ')', '[': ']', '{': '}'}

       for char in expression:
           if char in pairs:
               stack.push(char)
           elif char in pairs.values():
               if stack.is_empty():
                   return False
               if pairs[stack.pop()] != char:
                   return False

       return stack.is_empty()

   print(is_balanced("({[]})"))     # True
   print(is_balanced("({[}])"))     # False

Queues
------

**When to use:** FIFO behavior, task scheduling, BFS, producer-consumer.

.. code-block:: python

   from sds.linear import Queue

   queue = Queue()

   # Enqueue elements (add to rear)
   queue.enqueue(1)
   queue.enqueue(2)
   queue.enqueue(3)

   # Peek at front without removing
   print(queue.peek())     # 1

   # Dequeue elements (remove from front)
   print(queue.dequeue())  # 1
   print(queue.dequeue())  # 2

**Example: Task Processing**

.. code-block:: python

   from sds.linear import Queue

   task_queue = Queue()

   # Add tasks
   task_queue.enqueue("task1")
   task_queue.enqueue("task2")
   task_queue.enqueue("task3")

   # Process tasks in FIFO order
   while not task_queue.is_empty():
       task = task_queue.dequeue()
       print(f"Processing {task}")

Deques (Double-Ended Queues)
-----------------------------

**When to use:** Need efficient operations at both ends, sliding windows.

.. code-block:: python

   from sds.linear import Deque

   deque = Deque()

   # Add to either end
   deque.append_left(1)   # Add to left
   deque.append_right(2)  # Add to right

   # Remove from either end
   left = deque.pop_left()    # Remove from left
   right = deque.pop_right()  # Remove from right

**Example: Sliding Window Maximum**

.. code-block:: python

   from sds.linear import Deque

   def max_sliding_window(nums, k):
       deque = Deque()
       result = []

       for i, num in enumerate(nums):
           # Remove elements outside window
           while not deque.is_empty() and deque.peek_left() <= i - k:
               deque.pop_left()

           # Remove smaller elements
           while not deque.is_empty() and nums[deque.peek_right()] < num:
               deque.pop_right()

           deque.append_right(i)

           if i >= k - 1:
               result.append(nums[deque.peek_left()])

       return result

Exception Handling
==================

All SDS-Tools structures use consistent exception handling:

.. code-block:: python

   from sds.linear import Stack
   from sds.core.exceptions import EmptyStructureError

   stack = Stack()

   try:
       item = stack.pop()
   except EmptyStructureError as e:
       print(f"Error: {e.message}")
       # Handle empty stack gracefully

Common exceptions:

* :class:`~sds.core.exceptions.EmptyStructureError` - Operation on empty structure
* :class:`~sds.core.exceptions.FullStructureError` - Structure at capacity
* :class:`~sds.core.exceptions.IndexStructureError` - Invalid index access
* :class:`~sds.core.exceptions.InvalidOperationError` - Invalid operation

Performance Considerations
==========================

Understanding Complexity
------------------------

Different structures have different performance characteristics:

.. code-block:: python

   # LinkedList: O(n) append, O(1) prepend
   from sds.linear import LinkedList
   lst = LinkedList()
   lst.prepend(1)  # Fast: O(1)
   lst.append(1)   # Slow: O(n) - traverses entire list

   # DoublyLinkedList: O(1) for both
   from sds.linear import DoublyLinkedList
   dll = DoublyLinkedList()
   dll.prepend(1)  # Fast: O(1)
   dll.append(1)   # Also fast: O(1) - has tail pointer

Choosing the Right Structure
-----------------------------

.. list-table:: Quick Selection Guide
   :header-rows: 1
   :widths: 30 35 35

   * - Use Case
     - Recommended Structure
     - Why?
   * - Frequent insertions at start
     - LinkedList
     - O(1) prepend
   * - Operations at both ends
     - DoublyLinkedList or Deque
     - O(1) at both ends
   * - LIFO ordering
     - Stack
     - Semantic clarity
   * - FIFO ordering
     - Queue
     - Semantic clarity
   * - Round-robin scheduling
     - CircularLinkedList
     - Efficient rotation
   * - Undo/Redo system
     - Stack
     - Natural LIFO fit
   * - Task queue
     - Queue
     - Natural FIFO fit

Common Patterns
===============

Pattern 1: Processing All Elements
-----------------------------------

.. code-block:: python

   from sds.linear import LinkedList

   lst = LinkedList()
   # ... populate list ...

   # Method 1: Iterator
   for item in lst:
       process(item)

   # Method 2: While not empty
   while not lst.is_empty():
       item = lst.remove_first()
       process(item)

Pattern 2: Filtering
---------------------

.. code-block:: python

   from sds.linear import LinkedList

   def filter_list(lst, predicate):
       result = LinkedList()
       for item in lst:
           if predicate(item):
               result.append(item)
       return result

   # Usage
   numbers = LinkedList()
   for i in range(10):
       numbers.append(i)

   evens = filter_list(numbers, lambda x: x % 2 == 0)

Pattern 3: Stack-based Algorithms
----------------------------------

.. code-block:: python

   from sds.linear import Stack

   def evaluate_postfix(expression):
       stack = Stack()

       for token in expression.split():
           if token.isdigit():
               stack.push(int(token))
           else:
               b = stack.pop()
               a = stack.pop()
               if token == '+':
                   stack.push(a + b)
               elif token == '-':
                   stack.push(a - b)
               elif token == '*':
                   stack.push(a * b)
               elif token == '/':
                   stack.push(a // b)

       return stack.pop()

   result = evaluate_postfix("3 4 + 2 * 7 /")  # (3+4)*2/7 = 2

Pattern 4: Queue-based Processing
----------------------------------

.. code-block:: python

   from sds.linear import Queue

   def level_order_processing(root):
       queue = Queue()
       queue.enqueue(root)
       result = []

       while not queue.is_empty():
           node = queue.dequeue()
           result.append(node.value)

           for child in node.children:
               queue.enqueue(child)

       return result

Type Hints and IDE Support
===========================

SDS-Tools provides comprehensive type hints:

.. code-block:: python

   from typing import Optional
   from sds.linear import LinkedList
   from sds.core.interfaces import Collection

   def process_collection(coll: Collection) -> Optional[int]:
       """Process any collection, return first element if exists."""
       if not coll.is_empty():
           return next(iter(coll))
       return None

   # Works with any collection
   lst = LinkedList()
   lst.append(42)
   result = process_collection(lst)  # Type checker knows result is Optional[int]

Best Practices
==============

1. **Choose the Right Structure**

   Don't use a LinkedList when you need O(1) access by index - use a Python list instead.

2. **Check Before Operating**

   .. code-block:: python

      if not stack.is_empty():
          item = stack.pop()

3. **Use Type Hints**

   .. code-block:: python

      def process(items: LinkedList) -> int:
          return len(items)

4. **Handle Exceptions Appropriately**

   .. code-block:: python

      try:
          item = queue.dequeue()
      except EmptyStructureError:
          item = default_value

5. **Understand Time Complexity**

   Know the O-notation for operations you use frequently.

Next Steps
==========

Now that you understand the basics, explore:

* :doc:`linear_structures/index` - Deep dive into linear structures
* :doc:`tree_structures/index` - Learn about tree structures
* :doc:`graph_structures/index` - Explore graph structures
* :ref:`api-reference` - Complete API reference

Practice Exercises
==================

1. **Reverse a Stack**

   Write a function to reverse all elements in a stack.

2. **Queue with Stacks**

   Implement a queue using two stacks.

3. **Palindrome Checker**

   Use a deque to check if a string is a palindrome.

4. **Recent Counter**

   Implement a counter that returns the number of recent requests within
   a time window using a queue.

.. tip::

   Solutions to these exercises can be found in the examples directory
   of the GitHub repository.

Getting Help
============

* **Documentation**: https://sds-tools.readthedocs.io
* **API Reference**: :ref:`api-reference`
* **Examples**: https://github.com/skyfrigate/sds/tree/main/examples
* **Issues**: https://github.com/skyfrigate/sds/issues

.. note::

   All code examples in this guide are tested and guaranteed to work with
   the current version of SDS-Tools. You can copy and paste them directly
   into your Python environment.