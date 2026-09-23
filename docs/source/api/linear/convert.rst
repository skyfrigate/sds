.. _api_linear_convert:

==========
Conversion
==========

.. currentmodule:: sds.linear.convert

Overview
========

This module converts between a Python ``list`` and any linear structure of
``sds.linear``. Its main use is to sort the content of a structure with the
``list``-based functions of ``sds.algorithms.sorting`` and get a structure
back.

Both functions are generic: they rely only on ``__iter__`` and ``add()``,
which every :class:`~sds.core.interfaces.LinearCollection` implements with its
own semantics. No class-specific code is involved.

.. mermaid::

   graph LR
       A["Linear structure"] -->|"to_list()"| B["list"]
       B -->|"sorted() / quick_sort()"| C["sorted list"]
       C -->|"from_list(cls, ...)"| D["Linear structure"]

       style A fill:#3498db,color:#fff
       style D fill:#2ecc71,color:#fff

Round-trip behaviour
====================

``to_list(from_list(cls, items))`` returns ``items`` unchanged only for the
structures that iterate in insertion order.

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - Structure
     - Round trip
     - Why
   * - ``LinkedList``, ``DoublyLinkedList``, ``CircularLinkedList``
     - Identity
     - ``add()`` appends; iteration goes head to tail
   * - ``Queue``
     - Identity
     - ``add()`` enqueues; iteration goes front to rear
   * - ``Deque``
     - Identity
     - ``add()`` adds at the rear; iteration goes front to rear
   * - ``Stack``
     - Reversed
     - ``add()`` pushes; iteration goes top to bottom
   * - ``PriorityQueue``
     - Sorted by priority
     - ``add()`` inserts at the item's priority

Example
=======

.. code-block:: python

   from sds.linear import Queue, Stack, from_list, to_list

   queue = from_list(Queue, [3, 1, 2])
   ordered = from_list(Queue, sorted(to_list(queue)))
   print(to_list(ordered))                     # [1, 2, 3]

   print(to_list(from_list(Stack, [1, 2, 3]))) # [3, 2, 1] - LIFO

   # Constructor arguments are forwarded
   from sds.linear import PriorityQueue
   pq = from_list(PriorityQueue, ["pear", "fig", "banana"], key=len)
   print(to_list(pq))                          # ['fig', 'pear', 'banana']

Complexity
==========

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Function
     - Time
     - Notes
   * - ``to_list(structure)``
     - O(n)
     - One pass over the structure
   * - ``from_list(cls, items)``
     - n × cost of ``cls.add()``
     - O(n) for ``DoublyLinkedList``, ``CircularLinkedList``, ``Stack``,
       ``Deque``; O(n²) for ``LinkedList``, ``Queue``, ``PriorityQueue``

Detailed Documentation
======================

.. autofunction:: to_list

.. autofunction:: from_list
