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
       B --> G[ElementNotFoundError]
       B --> H[DuplicateElementError]
       B --> I[InvalidParameterError]
       B --> J[StructureTypeError]
       K[IndexError] --> F
       L[ValueError] --> G
       L --> H
       L --> I
       M[TypeError] --> J

       style A fill:#f9f,stroke:#333
       style B fill:#bbf,stroke:#333
       style C fill:#bfb,stroke:#333
       style D fill:#bfb,stroke:#333
       style E fill:#bfb,stroke:#333
       style F fill:#bfb,stroke:#333
       style G fill:#bfb,stroke:#333
       style H fill:#bfb,stroke:#333
       style I fill:#bfb,stroke:#333
       style J fill:#bfb,stroke:#333
       style K fill:#fdd,stroke:#333
       style L fill:#fdd,stroke:#333
       style M fill:#fdd,stroke:#333

Classes that report a problem with an argument also derive from the built-in
exception Python code would expect (``ValueError``, ``TypeError``,
``IndexError``), so an ``except ValueError`` clause still catches them.
Classes that report a problem with the state of the structure
(``EmptyStructureError``, ``FullStructureError``, ``InvalidOperationError``)
derive from ``DataStructureError`` only.

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

Reserved for structures with a bounded capacity.

**Common Scenarios:**

* Adding a node to an ``AdjacencyMatrixGraph`` that already holds
  ``max_nodes`` nodes

**Example:**

.. code-block:: python

   from sds.core.exceptions import FullStructureError
   from sds.graph import AdjacencyMatrixGraph, GraphNode

   graph = AdjacencyMatrixGraph(max_nodes=5)
   try:
       for i in range(10):
           graph.add_node(GraphNode(i, f"n{i}"))
   except FullStructureError as e:
       print(f"Error: {e.message}")
       # Output: Error: Graph is full. Maximum 5 nodes allowed

InvalidOperationError
---------------------

.. autoclass:: InvalidOperationError
   :members:
   :show-inheritance:

Raised when the arguments are valid but the current state of the structure
forbids the operation.

**Common Scenarios:**

* An edge that would close a cycle in a Bayesian network
* A Markov random field factor whose scope is not a clique
* A hidden Markov model component set twice, or read before being set
* Removing the root of a general tree without a replacement

**Example:**

.. code-block:: python

   from sds.core.exceptions import InvalidOperationError
   from sds.probabilistic import BayesianNetwork, RandomVariable

   rain = RandomVariable("Rain", ("yes", "no"))
   wet = RandomVariable("WetGrass", ("yes", "no"))
   bn = BayesianNetwork()
   bn.add_variable(rain)
   bn.add_variable(wet)
   bn.add_edge(rain, wet)

   try:
       bn.add_edge(wet, rain)
   except InvalidOperationError as e:
       print(f"Error: {e.message}")
       # Output: Error: Adding edge 'WetGrass' -> 'Rain' would introduce a cycle

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

ElementNotFoundError
--------------------

.. autoclass:: ElementNotFoundError
   :members:
   :show-inheritance:

Raised when the element designated by an argument is not in the structure:
a list item, a tree key, a graph node or edge, a model variable or state.
Also a ``ValueError``.

**Example:**

.. code-block:: python

   from sds.core.exceptions import ElementNotFoundError
   from sds.tree import BinarySearchTree

   bst = BinarySearchTree()
   bst.insert(10)
   bst.insert(5)

   try:
       bst.remove(42)
   except ElementNotFoundError as e:
       print(f"Error: {e.message}")
       # Output: Error: Item 42 not found in tree

DuplicateElementError
---------------------

.. autoclass:: DuplicateElementError
   :members:
   :show-inheritance:

Raised when adding an element that a structure rejecting duplicates already
holds (graph nodes and edges, model variables, disjoint-set elements). A
duplicate *inside an argument* is an :class:`InvalidParameterError`. Also a
``ValueError``.

**Example:**

.. code-block:: python

   from sds.core.exceptions import DuplicateElementError
   from sds.graph import Graph, GraphNode

   graph = Graph()
   node = GraphNode("A", "n1")
   graph.add_node(node)

   try:
       graph.add_node(node)
   except DuplicateElementError as e:
       print(f"Error: {e.message}")
       # Output: Error: Node n1 already exists in graph

InvalidParameterError
---------------------

.. autoclass:: InvalidParameterError
   :members:
   :show-inheritance:

Raised when an argument is invalid in itself, whatever the state of the
structure: a bound out of range, an empty input, incompatible dimensions,
evidence with probability zero under a model. Also a ``ValueError``.

**Example:**

.. code-block:: python

   from sds.advanced import BloomFilter
   from sds.core.exceptions import InvalidParameterError

   try:
       BloomFilter(size=0, num_hashes=3)
   except InvalidParameterError as e:
       print(f"Error: {e.message}")
       # Output: Error: size must be a positive integer, got 0

StructureTypeError
------------------

.. autoclass:: StructureTypeError
   :members:
   :show-inheritance:

Raised by explicit type checks on an argument: a node, an edge, a weight, or
the structure an algorithm expects. Also a ``TypeError``. Python protocols
keep their own exceptions: iterating a ``BloomFilter`` raises a plain
``TypeError``, and a missing key in a hash table raises ``KeyError``.

**Example:**

.. code-block:: python

   from sds.core.exceptions import StructureTypeError
   from sds.graph import Graph

   graph = Graph()

   try:
       graph.add_node("A")
   except StructureTypeError as e:
       print(f"Error: {e.message}")
       # Output: Error: Expected GraphNode, got str

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
     - Also catchable as
     - Reports
   * - ``EmptyStructureError``
     - —
     - Operation on an empty structure
   * - ``FullStructureError``
     - —
     - Addition beyond a bounded capacity
   * - ``InvalidOperationError``
     - —
     - Operation forbidden by the structure's state
   * - ``IndexStructureError``
     - ``IndexError``
     - Index out of range
   * - ``ElementNotFoundError``
     - ``ValueError``
     - Element absent from the structure
   * - ``DuplicateElementError``
     - ``ValueError``
     - Element already in the structure
   * - ``InvalidParameterError``
     - ``ValueError``
     - Argument invalid in itself
   * - ``StructureTypeError``
     - ``TypeError``
     - Argument of the wrong type

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