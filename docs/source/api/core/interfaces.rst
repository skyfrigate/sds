.. _api_core_interfaces:

==========
Interfaces
==========

.. currentmodule:: sds.core.interfaces

Abstract base classes defining interfaces for data structures.

Module Contents
===============

.. automodule:: sds.core.interfaces
   :members:
   :undoc-members:
   :show-inheritance:

Classes
=======

Collection
----------

.. autoclass:: Collection
   :members:
   :special-members: __len__, __iter__, __contains__, __bool__
   :member-order: bysource

Base interface for all collections.

**Key Features:**

* Size querying (``__len__``, ``is_empty``)
* Iteration support (``__iter__``)
* Membership testing (``__contains__``)
* Boolean conversion (``__bool__``)
* Clearing all elements (``clear``)

**Usage Example:**

.. code-block:: python

   from sds.core.interfaces import Collection

   class SimpleList(Collection):
       def __init__(self):
           self._data = []

       def __len__(self):
           return len(self._data)

       def is_empty(self):
           return len(self._data) == 0

       def clear(self):
           self._data.clear()

       def __iter__(self):
           return iter(self._data)

       def __contains__(self, item):
           return item in self._data

       def add(self, item):
           self._data.append(item)

LinearCollection
----------------

.. autoclass:: LinearCollection
   :members:
   :special-members: __len__, __iter__, __contains__, __bool__
   :member-order: bysource

Extended interface for linear data structures.

**Extends:** :class:`Collection`

**Additional Features:**

* Generic add operation (``add``)
* Generic remove operation (``remove``)

**Usage Example:**

.. code-block:: python

   from sds.core.interfaces import LinearCollection

   class SimpleStack(LinearCollection):
       def __init__(self):
           self._data = []

       # Implement Collection methods
       def __len__(self):
           return len(self._data)

       def is_empty(self):
           return len(self._data) == 0

       def clear(self):
           self._data.clear()

       def __iter__(self):
           return iter(self._data)

       def __contains__(self, item):
           return item in self._data

       # Implement LinearCollection methods
       def add(self, item):
           self._data.append(item)  # Stack: add to top

       def remove(self, item):
           if self.is_empty():
               raise EmptyStructureError()
           return self._data.pop()  # Stack: remove from top

Interface Hierarchy
===================

.. mermaid::

   classDiagram
       class Collection {
           <<abstract>>
           +__len__()
           +is_empty()
           +clear()
           +__iter__()
           +__contains__()
           +__bool__()
       }

       class LinearCollection {
           <<abstract>>
           +add(item)
           +remove(item)
       }

       class AbstractLinkedList {
           <<abstract>>
           +prepend(item)
           +append(item)
           +insert_at(index, item)
           +remove_first()
           +remove_last()
           +remove_at(index)
           +find(item)
           +reverse()
       }

       Collection <|-- LinearCollection
       LinearCollection <|-- AbstractLinkedList

       note for Collection "Base interface:\nsize, iteration,\nmembership"
       note for LinearCollection "Adds generic:\nadd/remove operations"
       note for AbstractLinkedList "Specific to lists:\nindexed operations"

Method Reference
================

Collection Interface
--------------------

__len__()
~~~~~~~~~

.. automethod:: Collection.__len__

Return the number of elements in the collection.

**Returns:** ``int``

**Time Complexity:** O(1)

**Example:**

.. code-block:: python

   collection = MyCollection()
   collection.add(1)
   collection.add(2)
   print(len(collection))  # 2

is_empty()
~~~~~~~~~~

.. automethod:: Collection.is_empty

Check if the collection contains no elements.

**Returns:** ``bool``

**Time Complexity:** O(1)

**Example:**

.. code-block:: python

   collection = MyCollection()
   print(collection.is_empty())  # True
   collection.add(1)
   print(collection.is_empty())  # False

clear()
~~~~~~~

.. automethod:: Collection.clear

Remove all elements from the collection.

**Returns:** ``None``

**Time Complexity:** O(1) ideally

**Example:**

.. code-block:: python

   collection = MyCollection()
   collection.add(1)
   collection.add(2)
   collection.clear()
   print(len(collection))  # 0

__iter__()
~~~~~~~~~~

.. automethod:: Collection.__iter__

Return an iterator over the collection elements.

**Returns:** ``Iterator[Any]``

**Example:**

.. code-block:: python

   collection = MyCollection()
   collection.add(1)
   collection.add(2)
   collection.add(3)

   for item in collection:
       print(item)

   # Or convert to list
   items = list(collection)

__contains__()
~~~~~~~~~~~~~~

.. automethod:: Collection.__contains__

Check if an item is in the collection.

**Parameters:**

* ``item`` (Any) - The item to search for

**Returns:** ``bool``

**Time Complexity:** O(n) typically

**Example:**

.. code-block:: python

   collection = MyCollection()
   collection.add(42)

   print(42 in collection)  # True
   print(99 in collection)  # False

__bool__()
~~~~~~~~~~

.. automethod:: Collection.__bool__

Return True if the collection is not empty.

**Returns:** ``bool``

**Time Complexity:** O(1)

**Example:**

.. code-block:: python

   collection = MyCollection()

   if not collection:
       print("Collection is empty")

   collection.add(1)

   if collection:
       print("Collection has items")

LinearCollection Interface
---------------------------

add()
~~~~~

.. automethod:: LinearCollection.add

Add an item to the collection.

**Parameters:**

* ``item`` (Any) - The item to add

**Returns:** ``None``

**Raises:** ``FullStructureError`` if collection has maximum capacity

**Example:**

.. code-block:: python

   collection = MyLinearCollection()
   collection.add(1)
   collection.add(2)
   collection.add(3)

remove()
~~~~~~~~

.. automethod:: LinearCollection.remove

Remove and return an item from the collection.

**Parameters:**

* ``item`` (Any) - Context depends on implementation

**Returns:** ``Any`` - The removed item

**Raises:**

* ``EmptyStructureError`` if collection is empty
* ``ValueError`` if item not found (for some implementations)

**Example:**

.. code-block:: python

   collection = MyLinearCollection()
   collection.add(1)
   collection.add(2)

   item = collection.remove(1)
   print(item)  # 1

Implementation Guidelines
=========================

Creating a New Collection Type
-------------------------------

When implementing a new collection:

1. **Inherit from the appropriate interface**

   .. code-block:: python

      from sds.core.interfaces import Collection

      class MyCollection(Collection):
          pass

2. **Implement all abstract methods**

   The Python interpreter will raise ``TypeError`` if you try to instantiate
   without implementing all abstract methods.

3. **Follow the contract**

   Each method has expected behavior (see docstrings). Implementations should
   respect these contracts for consistency.

4. **Consider performance**

   Document time complexity for your implementations. Users rely on this
   information to choose the right data structure.

Example Implementation
----------------------

Complete example of a simple collection:

.. code-block:: python

   from typing import Any, Iterator
   from sds.core.interfaces import LinearCollection
   from sds.core.exceptions import EmptyStructureError

   class SimpleQueue(LinearCollection):
       """A simple FIFO queue implementation."""

       def __init__(self):
           self._items = []

       def __len__(self) -> int:
           """O(1) - Return size."""
           return len(self._items)

       def is_empty(self) -> bool:
           """O(1) - Check if empty."""
           return len(self._items) == 0

       def clear(self) -> None:
           """O(1) - Clear all items."""
           self._items.clear()

       def __iter__(self) -> Iterator[Any]:
           """O(n) - Iterate over items."""
           return iter(self._items)

       def __contains__(self, item: Any) -> bool:
           """O(n) - Check membership."""
           return item in self._items

       def add(self, item: Any) -> None:
           """O(1) - Add to rear."""
           self._items.append(item)

       def remove(self, item: Any) -> Any:
           """O(n) - Remove from front."""
           if self.is_empty():
               raise EmptyStructureError("Cannot dequeue from empty queue")
           return self._items.pop(0)

Best Practices
==============

Consistency
-----------

All implementations of the same interface should behave consistently:

.. code-block:: python

   def process_any_collection(coll: Collection):
       """Works with ANY Collection implementation."""
       if not coll.is_empty():
           for item in coll:
               print(item)

Documentation
-------------

Always document:

* **Time complexity** for each operation
* **Space complexity** if relevant
* **Exceptions** that can be raised
* **Specific behavior** (LIFO, FIFO, etc.)

Type Hints
----------

Use abstract classes for type hints to accept any implementation:

.. code-block:: python

   from sds.core.interfaces import Collection, LinearCollection

   def count_items(coll: Collection) -> int:
       """Count items in any collection."""
       return len(coll)

   def add_multiple(coll: LinearCollection, *items) -> None:
       """Add multiple items to any linear collection."""
       for item in items:
           coll.add(item)

See Also
========

* :doc:`node` - Abstract node base class
* :doc:`exceptions` - Exception hierarchy
* :doc:`../linear/interfaces` - Extended linear interfaces
* :doc:`../../guide/index` - Architecture overview

.. note::

   The interface design follows the **Liskov Substitution Principle**:
   any implementation can be used wherever the interface is expected,
   ensuring polymorphic behavior across all data structures.