.. _api_advanced_interfaces:

===================
Abstract Interfaces
===================

.. currentmodule:: sds.advanced.interfaces

All abstract classes in ``sds.advanced`` inherit from
:class:`~sds.core.interfaces.Collection`, enforcing a shared base contract
(``__len__``, ``is_empty``, ``clear``, ``__iter__``, ``__contains__``,
``__bool__``) across every advanced structure.

Class Hierarchy
===============

.. mermaid::

   classDiagram
       class Collection {
           <<abstract — sds.core>>
           +__len__() int
           +is_empty() bool
           +clear()
           +__iter__() Iterator
           +__contains__(item) bool
           +__bool__() bool
       }

       class AbstractDisjointSet {
           <<abstract>>
           +make_set(element)
           +find(element) Any
           +union(x, y) bool
           +connected(x, y) bool
           +get_sets() List
           +count_sets() int
           +size(element) int
       }

       class AbstractProbabilisticSet {
           <<abstract>>
           +add(item)
           +estimated_fill_ratio() float
       }

       class AbstractSkipList {
           <<abstract>>
           +insert(key, value)
           +delete(key) bool
           +search(key) Any
       }

       class AbstractHashTable {
           <<abstract>>
           +put(key, value)
           +get(key) Any
           +delete(key) bool
       }

       class AbstractLRUCache {
           <<abstract>>
           +get(key) Any
           +put(key, value)
       }

       class AbstractFenwickTree {
           <<abstract>>
           +update(i, delta)
           +prefix_sum(i) float
           +range_sum(l, r) float
       }

       Collection <|-- AbstractDisjointSet
       Collection <|-- AbstractProbabilisticSet
       Collection <|-- AbstractSkipList
       Collection <|-- AbstractHashTable
       Collection <|-- AbstractLRUCache
       Collection <|-- AbstractFenwickTree

.. autoclass:: AbstractDisjointSet
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: AbstractProbabilisticSet
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: AbstractSkipList
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: AbstractHashTable
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: AbstractLRUCache
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: AbstractFenwickTree
   :members:
   :undoc-members:
   :show-inheritance:
