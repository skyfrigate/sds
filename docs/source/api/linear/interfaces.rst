.. _api_linear_interfaces:

======================
Linked List Interfaces
======================

.. currentmodule:: sds.linear.interfaces

Overview
========

This module provides the abstract base class for linked list implementations.
All concrete linked list types (singly, doubly, circular) inherit from this
base class to ensure a consistent interface.

.. mermaid::

   classDiagram
       LinearCollection <|-- AbstractLinkedList
       AbstractLinkedList <|-- LinkedList
       AbstractLinkedList <|-- DoublyLinkedList
       AbstractLinkedList <|-- CircularLinkedList
       
       class LinearCollection {
           <<abstract>>
           +add(item)
           +remove(item)
           +clear()
           +is_empty()
       }
       
       class AbstractLinkedList {
           <<abstract>>
           +size: int
           +prepend(item)
           +append(item)
           +insert_at(index, item)
           +remove_first()
           +remove_last()
           +remove_at(index)
           +find(item)
           +reverse()
           +__getitem__(index)
           +__setitem__(index, value)
       }

Classes
=======

.. autosummary::
   :toctree: _autosummary
   :nosignatures:

   AbstractLinkedList

Detailed Documentation
======================

AbstractLinkedList
------------------

.. autoclass:: AbstractLinkedList
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__, __len__, __getitem__, __setitem__

   .. rubric:: Constructor

   .. automethod:: __init__

   .. rubric:: Properties

   .. autoproperty:: size

   .. rubric:: Abstract Methods (must be implemented)

   .. automethod:: prepend
   .. automethod:: append
   .. automethod:: insert_at
   .. automethod:: remove_first
   .. automethod:: remove_last
   .. automethod:: remove_at
   .. automethod:: find
   .. automethod:: reverse
   .. automethod:: __getitem__
   .. automethod:: __setitem__

   .. rubric:: Concrete Methods (provided)

   .. automethod:: __len__
   .. automethod:: is_empty
   .. automethod:: add

Usage Examples
==============

Implementing Custom Linked Lists
---------------------------------

Using AbstractLinkedList as a base:

.. code-block:: python

   from sds.linear.interfaces import AbstractLinkedList
   from sds.linear.node import SimpleNode
   from typing import Any, Iterator

   class MyCustomList(AbstractLinkedList):
       """Custom linked list implementation."""
       
       def __init__(self):
           super().__init__()  # Initialize _size
           self._head = None
       
       def prepend(self, item: Any) -> None:
           """Add item to beginning."""
           new_node = SimpleNode(item, self._head)
           self._head = new_node
           self._size += 1
       
       def append(self, item: Any) -> None:
           """Add item to end."""
           new_node = SimpleNode(item)
           
           if self._head is None:
               self._head = new_node
           else:
               current = self._head
               while current.next is not None:
                   current = current.next
               current.next = new_node
           
           self._size += 1
       
       def insert_at(self, index: int, item: Any) -> None:
           """Insert item at index."""
           if index < 0 or index > self._size:
               raise IndexError(f"Index {index} out of range")
           
           if index == 0:
               self.prepend(item)
               return
           
           current = self._head
           for _ in range(index - 1):
               current = current.next
           
           new_node = SimpleNode(item, current.next)
           current.next = new_node
           self._size += 1
       
       def remove_first(self) -> Any:
           """Remove and return first item."""
           if self.is_empty():
               raise IndexError("Cannot remove from empty list")
           
           data = self._head.data
           self._head = self._head.next
           self._size -= 1
           return data
       
       def remove_last(self) -> Any:
           """Remove and return last item."""
           if self.is_empty():
               raise IndexError("Cannot remove from empty list")
           
           if self._size == 1:
               return self.remove_first()
           
           current = self._head
           while current.next.next is not None:
               current = current.next
           
           data = current.next.data
           current.next = None
           self._size -= 1
           return data
       
       def remove_at(self, index: int) -> Any:
           """Remove and return item at index."""
           if index < 0 or index >= self._size:
               raise IndexError(f"Index {index} out of range")
           
           if index == 0:
               return self.remove_first()
           
           current = self._head
           for _ in range(index - 1):
               current = current.next
           
           data = current.next.data
           current.next = current.next.next
           self._size -= 1
           return data
       
       def find(self, item: Any) -> int:
           """Find index of item."""
           current = self._head
           index = 0
           
           while current is not None:
               if current.data == item:
                   return index
               current = current.next
               index += 1
           
           return -1
       
       def reverse(self) -> None:
           """Reverse the list in place."""
           prev = None
           current = self._head
           
           while current is not None:
               next_node = current.next
               current.next = prev
               prev = current
               current = next_node
           
           self._head = prev
       
       def __getitem__(self, index: int) -> Any:
           """Get item at index."""
           if index < 0 or index >= self._size:
               raise IndexError(f"Index {index} out of range")
           
           current = self._head
           for _ in range(index):
               current = current.next
           
           return current.data
       
       def __setitem__(self, index: int, value: Any) -> None:
           """Set item at index."""
           if index < 0 or index >= self._size:
               raise IndexError(f"Index {index} out of range")
           
           current = self._head
           for _ in range(index):
               current = current.next
           
           current.data = value
       
       def __iter__(self) -> Iterator[Any]:
           """Iterate over items."""
           current = self._head
           while current is not None:
               yield current.data
               current = current.next

   # Usage
   my_list = MyCustomList()
   my_list.append(1)
   my_list.append(2)
   my_list.prepend(0)
   print(list(my_list))  # [0, 1, 2]

Polymorphic List Operations
----------------------------

Working with any linked list type:

.. code-block:: python

   from sds.linear.interfaces import AbstractLinkedList
   from typing import List

   def list_statistics(lst: AbstractLinkedList) -> dict:
       """Get statistics for any linked list type."""
       return {
           'size': lst.size,
           'is_empty': lst.is_empty(),
           'first': lst[0] if not lst.is_empty() else None,
           'last': lst[-1] if not lst.is_empty() else None
       }
   
   def reverse_copy(lst: AbstractLinkedList) -> List[Any]:
       """Create reversed copy of any linked list."""
       items = list(lst)
       return list(reversed(items))
   
   def find_all(lst: AbstractLinkedList, item: Any) -> List[int]:
       """Find all occurrences of item."""
       indices = []
       for i, value in enumerate(lst):
           if value == item:
               indices.append(i)
       return indices

Type-Safe List Processing
--------------------------

Using type hints with interfaces:

.. code-block:: python

   from sds.linear.interfaces import AbstractLinkedList
   from typing import TypeVar, Generic, Callable

   T = TypeVar('T')

   class ListProcessor(Generic[T]):
       """Process linked lists in a type-safe manner."""
       
       def __init__(self, lst: AbstractLinkedList):
           self.lst = lst
       
       def map(self, func: Callable[[T], T]) -> List[T]:
           """Apply function to all elements."""
           return [func(item) for item in self.lst]
       
       def filter(self, predicate: Callable[[T], bool]) -> List[T]:
           """Filter elements by predicate."""
           return [item for item in self.lst if predicate(item)]
       
       def reduce(self, func: Callable[[T, T], T], initial: T) -> T:
           """Reduce list to single value."""
           result = initial
           for item in self.lst:
               result = func(result, item)
           return result
       
       def partition(self, predicate: Callable[[T], bool]) -> tuple[List[T], List[T]]:
           """Partition list into two lists."""
           true_items = []
           false_items = []
           
           for item in self.lst:
               if predicate(item):
                   true_items.append(item)
               else:
                   false_items.append(item)
           
           return true_items, false_items

   # Usage
   from sds.linear import LinkedList
   
   lst = LinkedList()
   for i in range(1, 6):
       lst.append(i)
   
   processor = ListProcessor(lst)
   
   # Map
   doubled = processor.map(lambda x: x * 2)
   print(doubled)  # [2, 4, 6, 8, 10]
   
   # Filter
   evens = processor.filter(lambda x: x % 2 == 0)
   print(evens)  # [2, 4]
   
   # Reduce
   total = processor.reduce(lambda a, b: a + b, 0)
   print(total)  # 15

Interface Contract
==================

Method Requirements
-------------------

All concrete linked list classes **must** implement:

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Method
     - Required
     - Purpose
   * - ``prepend(item)``
     - Yes
     - Add item to beginning
   * - ``append(item)``
     - Yes
     - Add item to end
   * - ``insert_at(index, item)``
     - Yes
     - Insert item at index
   * - ``remove_first()``
     - Yes
     - Remove first item
   * - ``remove_last()``
     - Yes
     - Remove last item
   * - ``remove_at(index)``
     - Yes
     - Remove item at index
   * - ``find(item)``
     - Yes
     - Find index of item
   * - ``reverse()``
     - Yes
     - Reverse list in place
   * - ``__getitem__(index)``
     - Yes
     - Get item at index
   * - ``__setitem__(index, value)``
     - Yes
     - Set item at index
   * - ``size`` (property)
     - No
     - Inherited from base
   * - ``is_empty()``
     - No
     - Inherited from base
   * - ``add(item)``
     - No
     - Inherited, calls append()

Property Guarantees
-------------------

The abstract class guarantees:

* **Size tracking**: ``_size`` is automatically maintained if you update it in methods
* **Empty check**: ``is_empty()`` works based on ``_size``
* **Length**: ``len(lst)`` returns ``_size``
* **Generic add**: ``add(item)`` delegates to ``append(item)``

Implementation must guarantee:

* **Consistent size**: Update ``_size`` in all add/remove methods
* **Index bounds**: Validate indices in all indexed operations
* **Negative indexing**: Support Python-style negative indices
* **Iterator**: Implement ``__iter__`` for iteration

Design Patterns
===============

Template Method Pattern
-----------------------

The abstract class defines the template:

.. code-block:: python

   # Template methods (in AbstractLinkedList)
   def __len__(self) -> int:
       """Always works the same way."""
       return self._size
   
   def is_empty(self) -> bool:
       """Built on __len__."""
       return self._size == 0
   
   def add(self, item: Any) -> None:
       """Default behavior: append."""
       self.append(item)
   
   # Concrete classes implement specifics
   class LinkedList(AbstractLinkedList):
       def append(self, item: Any) -> None:
           """LinkedList-specific append (O(n))."""
           # Implementation...
   
   class DoublyLinkedList(AbstractLinkedList):
       def append(self, item: Any) -> None:
           """DoublyLinkedList-specific append (O(1))."""
           # Different implementation!

Strategy Pattern
----------------

Different implementations for different needs:

.. code-block:: python

   from enum import Enum

   class ListType(Enum):
       SINGLY = "singly"
       DOUBLY = "doubly"
       CIRCULAR = "circular"
   
   def create_list(list_type: ListType) -> AbstractLinkedList:
       """Factory for creating appropriate list type."""
       from sds.linear import LinkedList, DoublyLinkedList, CircularLinkedList
       
       strategies = {
           ListType.SINGLY: LinkedList,
           ListType.DOUBLY: DoublyLinkedList,
           ListType.CIRCULAR: CircularLinkedList
       }
       
       return strategies[list_type]()
   
   # Usage
   # Need O(1) append → use doubly
   lst = create_list(ListType.DOUBLY)
   
   # Need rotation → use circular
   lst = create_list(ListType.CIRCULAR)

Best Practices
==============

Interface Implementation
------------------------

✅ **Always call super().__init__()**

.. code-block:: python

   class MyList(AbstractLinkedList):
       def __init__(self):
           super().__init__()  # Initialize _size
           # Your initialization

✅ **Update size consistently**

.. code-block:: python

   def prepend(self, item):
       # ... add node ...
       self._size += 1  # Don't forget!
   
   def remove_first(self):
       # ... remove node ...
       self._size -= 1  # Don't forget!

✅ **Implement all abstract methods**

.. code-block:: python

   # Type checkers will catch missing methods
   class IncompleteList(AbstractLinkedList):
       # Missing prepend(), append(), etc.
       pass  # Type error!

Using Interfaces
----------------

✅ **Program to interfaces, not implementations**

.. code-block:: python

   # Good: Flexible, works with any list
   def process_list(lst: AbstractLinkedList):
       if not lst.is_empty():
           # Process...
           pass
   
   # Less flexible: Tied to specific type
   def process_linked(lst: LinkedList):
       # Only works with LinkedList
       pass

✅ **Use type hints for clarity**

.. code-block:: python

   from typing import Optional
   
   def find_in_list(lst: AbstractLinkedList, 
                    item: Any) -> Optional[int]:
       """Type-safe list search."""
       index = lst.find(item)
       return index if index != -1 else None

Common Patterns
===============

Iterator Pattern
----------------

.. code-block:: python

   class ListIterator:
       """Custom iterator for lists with filtering."""
       
       def __init__(self, lst: AbstractLinkedList,
                    predicate=lambda x: True):
           self.lst = lst
           self.predicate = predicate
           self._iter = iter(lst)
       
       def __iter__(self):
           return self
       
       def __next__(self):
           while True:
               item = next(self._iter)
               if self.predicate(item):
                   return item
   
   # Usage
   lst = LinkedList()
   for i in range(10):
       lst.append(i)
   
   # Iterate over even numbers only
   evens = ListIterator(lst, lambda x: x % 2 == 0)
   print(list(evens))  # [0, 2, 4, 6, 8]

Adapter Pattern
---------------

.. code-block:: python

   class ListStack:
       """Adapt any linked list to stack interface."""
       
       def __init__(self, lst: AbstractLinkedList):
           self._lst = lst
       
       def push(self, item):
           """Push onto stack (prepend)."""
           self._lst.prepend(item)
       
       def pop(self):
           """Pop from stack (remove first)."""
           return self._lst.remove_first()
       
       def peek(self):
           """Peek at top of stack."""
           return self._lst[0]
       
       def is_empty(self):
           """Check if stack is empty."""
           return self._lst.is_empty()
   
   # Usage with any list type
   from sds.linear import DoublyLinkedList
   
   stack = ListStack(DoublyLinkedList())
   stack.push(1)
   stack.push(2)
   print(stack.pop())  # 2

See Also
========

* :doc:`node` - Node implementations
* :doc:`list` - Concrete linked list implementations
* :doc:`../../guide/linear_structures/linked_list` - Linked list theory and guide

References
==========

.. [1] Gamma, E., et al. "Design Patterns: Elements of Reusable Object-Oriented Software", 1994
.. [2] Martin, R. C. "Clean Architecture", Chapter 11: DIP
.. [3] Liskov, B. "Data Abstraction and Hierarchy", OOPSLA '87
.. [4] Knuth, D. E. "The Art of Computer Programming, Volume 1", Section 2.2
