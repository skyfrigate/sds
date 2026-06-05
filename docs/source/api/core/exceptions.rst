.. _api_core_exceptions:

==========
Exceptions
==========

.. currentmodule:: sds.core.exceptions

Custom exception classes for data structures.

Module Contents
===============

.. automodule:: sds.core.exceptions
   :members:
   :undoc-members:
   :show-inheritance:

Exception Hierarchy
===================

.. mermaid::

   graph TD
       A[Exception] --> B[DataStructureError]
       B --> C[EmptyStructureError]
       B --> D[FullStructureError]
       B --> E[InvalidOperationError]
       B --> F[IndexStructureError]

       style A fill:#f9f,stroke:#333
       style B fill:#bbf,stroke:#333
       style C fill:#bfb,stroke:#333
       style D fill:#bfb,stroke:#333
       style E fill:#bfb,stroke:#333
       style F fill:#bfb,stroke:#333

Exception Classes
=================

DataStructureError
------------------

.. autoclass:: DataStructureError
   :members:
   :show-inheritance:

Base exception for all data structure errors.

**Usage:**

This is the base class for all custom exceptions in SDS-Tools. You can catch
this to handle any data structure error:

.. code-block:: python

   from sds.core.exceptions import DataStructureError
   from sds.linear import Stack

   stack = Stack()

   try:
       stack.pop()
   except DataStructureError as e:
       print(f"Data structure error: {e}")

EmptyStructureError
-------------------

.. autoclass:: EmptyStructureError
   :members:
   :show-inheritance:

Raised when attempting to access or remove from an empty structure.

**Common Scenarios:**

* Popping from an empty stack
* Dequeuing from an empty queue
* Removing from an empty list
* Accessing elements when size is 0

**Example:**

.. code-block:: python

   from sds.core.exceptions import EmptyStructureError
   from sds.linear import Stack

   stack = Stack()

   try:
       item = stack.pop()
   except EmptyStructureError as e:
       print(f"Error: {e.message}")
       # Output: Error: Cannot perform operation on empty structure

**Custom Message:**

.. code-block:: python

   try:
       item = stack.pop()
   except EmptyStructureError:
       raise EmptyStructureError("Stack is empty, cannot pop")

FullStructureError
------------------

.. autoclass:: FullStructureError
   :members:
   :show-inheritance:

Raised when attempting to add to a full structure.

**Common Scenarios:**

* Adding to a bounded queue at capacity
* Pushing to a fixed-size stack that's full
* Inserting into a structure with maximum capacity

**Example:**

.. code-block:: python

   from sds.core.exceptions import FullStructureError
   from sds.linear import BoundedStack

   stack = BoundedStack(max_size=3)
   stack.push(1)
   stack.push(2)
   stack.push(3)

   try:
       stack.push(4)
   except FullStructureError as e:
       print(f"Error: {e.message}")
       # Output: Error: Cannot add to full structure

**Custom Message:**

.. code-block:: python

   try:
       stack.push(4)
   except FullStructureError:
       raise FullStructureError(f"Stack is full (capacity: {stack.capacity})")

InvalidOperationError
---------------------

.. autoclass:: InvalidOperationError
   :members:
   :show-inheritance:

Raised when an invalid operation is attempted.

**Common Scenarios:**

* Removing a node that doesn't exist
* Invalid state transitions
* Operations not supported by the structure
* Violating structural invariants

**Example:**

.. code-block:: python

   from sds.core.exceptions import InvalidOperationError
   from sds.tree import BinarySearchTree

   bst = BinarySearchTree()

   try:
       bst.remove(42)  # Removing non-existent value
   except InvalidOperationError as e:
       print(f"Error: {e.message}")

**Custom Message:**

.. code-block:: python

   if node.is_root():
       raise InvalidOperationError("Cannot remove root without children")

IndexStructureError
-------------------

.. autoclass:: IndexStructureError
   :members:
   :show-inheritance:

Raised when an invalid index is accessed.

**Common Scenarios:**

* Index out of bounds
* Negative index beyond size
* Invalid slice parameters

**Example:**

.. code-block:: python

   from sds.core.exceptions import IndexStructureError
   from sds.linear import LinkedList

   lst = LinkedList()
   lst.append(1)
   lst.append(2)

   try:
       item = lst[10]
   except IndexStructureError as e:
       print(f"Error: {e.message}")
       # Output: Error: Index 10 out of range for list of size 2

**Custom Message:**

.. code-block:: python

   if index >= self._size:
       raise IndexStructureError(
           f"Index {index} out of range for list of size {self._size}"
       )

Usage Patterns
==============

Basic Exception Handling
-------------------------

Catch specific exceptions:

.. code-block:: python

   from sds.core.exceptions import EmptyStructureError
   from sds.linear import Queue

   queue = Queue()

   try:
       item = queue.dequeue()
   except EmptyStructureError:
       print("Queue is empty!")
       item = None

Multiple Exception Handling
----------------------------

Handle different exceptions differently:

.. code-block:: python

   from sds.core.exceptions import (
       EmptyStructureError,
       IndexStructureError
   )
   from sds.linear import LinkedList

   lst = LinkedList()

   try:
       item = lst.remove_at(5)
   except EmptyStructureError:
       print("List is empty")
   except IndexStructureError as e:
       print(f"Invalid index: {e.message}")

Catch All Data Structure Errors
--------------------------------

Use the base exception to catch any error:

.. code-block:: python

   from sds.core.exceptions import DataStructureError

   try:
       # Various data structure operations
       stack.pop()
       queue.dequeue()
       tree.remove(42)
   except DataStructureError as e:
       print(f"An error occurred: {e}")
       # Handle any data structure error

Re-raising with Context
-----------------------

Add context when re-raising:

.. code-block:: python

   from sds.core.exceptions import EmptyStructureError

   def process_stack(stack):
       try:
           return stack.pop()
       except EmptyStructureError:
           raise EmptyStructureError(
               "Cannot process: stack is empty"
           ) from None

Custom Error Messages
---------------------

All exceptions accept custom messages:

.. code-block:: python

   from sds.core.exceptions import InvalidOperationError

   def rotate_tree(node):
       if node.is_leaf():
           raise InvalidOperationError(
               f"Cannot rotate leaf node with value {node.data}"
           )

Best Practices
==============

Be Specific
-----------

Catch the most specific exception possible:

.. code-block:: python

   # Good ✓
   try:
       item = lst[index]
   except IndexStructureError:
       handle_index_error()

   # Less good ✗
   try:
       item = lst[index]
   except DataStructureError:  # Too broad
       handle_error()

Provide Context
---------------

Include helpful information in error messages:

.. code-block:: python

   if index < 0 or index >= self._size:
       raise IndexStructureError(
           f"Index {index} out of range [0, {self._size})"
       )

Don't Catch Too Broadly
-----------------------

.. code-block:: python

   # Bad ✗
   try:
       result = complex_operation()
   except Exception:  # Catches everything!
       pass

   # Good ✓
   try:
       result = complex_operation()
   except (EmptyStructureError, IndexStructureError) as e:
       handle_specific_errors(e)

Document Exceptions
-------------------

Always document which exceptions a function can raise:

.. code-block:: python

   def remove_at(self, index: int) -> Any:
       """Remove item at index.

       Parameters
       ----------
       index : int
           Position of item to remove

       Returns
       -------
       Any
           The removed item

       Raises
       ------
       EmptyStructureError
           If the list is empty
       IndexStructureError
           If index is out of range
       """
       pass

Error Recovery
--------------

Handle errors gracefully:

.. code-block:: python

   from sds.core.exceptions import EmptyStructureError
   from sds.linear import Stack

   def safe_pop(stack: Stack, default=None):
       """Pop with a default value if empty."""
       try:
           return stack.pop()
       except EmptyStructureError:
           return default

   # Usage
   result = safe_pop(my_stack, default=0)

Comparison with Built-in Exceptions
====================================

Why Not Use Built-in Exceptions?
---------------------------------

SDS-Tools uses custom exceptions for several reasons:

1. **Specificity** - Clear indication of data structure errors
2. **Consistency** - Uniform error handling across all structures
3. **Categorization** - Easy to catch all data structure errors
4. **Custom Fields** - ``message`` attribute for detailed information

Mapping to Built-ins
--------------------

.. list-table:: Exception Mapping
   :header-rows: 1
   :widths: 40 30 30

   * - SDS Exception
     - Similar Built-in
     - Why Custom?
   * - ``EmptyStructureError``
     - ``IndexError``
     - More semantic
   * - ``FullStructureError``
     - ``OverflowError``
     - More specific
   * - ``InvalidOperationError``
     - ``ValueError``
     - Clearer intent
   * - ``IndexStructureError``
     - ``IndexError``
     - Consistent naming

Performance Considerations
==========================

Exceptions are not free, but the overhead is minimal:

.. code-block:: python

   # Checking before operation (preferred for hot paths)
   if not stack.is_empty():
       item = stack.pop()

   # Exception handling (cleaner for rare errors)
   try:
       item = stack.pop()
   except EmptyStructureError:
       item = None

For operations that rarely fail, exception handling is cleaner. For hot code
paths with frequent checks, explicit validation is faster.

See Also
========

* :doc:`interfaces` - Interfaces that raise these exceptions
* :doc:`../linear/index` - Linear structures using these exceptions
* Python's :py:exc:`Exception` - Built-in exception base class

.. note::

   All exceptions in SDS-Tools inherit from ``DataStructureError``, which
   itself inherits from Python's built-in ``Exception``. This means you can
   catch them with standard Python exception handling.