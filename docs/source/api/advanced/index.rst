.. _api_advanced:

==================================
Advanced Structures (sds.advanced)
==================================

.. currentmodule:: sds.advanced

Advanced data structures provide specialised solutions for complex computational
problems: dynamic connectivity tracking, space-efficient membership testing,
probabilistic frequency estimation, ordered probabilistic access, bounded caching,
and prefix-sum queries.

.. toctree::
   :maxdepth: 2

   interfaces
   disjoint
   bloom_filter
   skip_list
   hash_table
   lru_cache
   fenwick_tree
   count_min_sketch

Module Contents
===============

Structure Type Comparison
--------------------------

.. list-table::
   :header-rows: 1
   :widths: 22 14 14 14 36

   * - Structure
     - Add / Update
     - Query
     - Space
     - Best Use Case
   * - ``DisjointSet``
     - O(α(n))
     - O(α(n))
     - O(n)
     - Dynamic connectivity
   * - ``BloomFilter``
     - O(k)
     - O(k)
     - O(m) bits
     - Approximate membership
   * - ``SkipList``
     - O(log n)\*
     - O(log n)\*
     - O(n log n)\*
     - Ordered key-value store
   * - ``HashTableChaining``
     - O(1)\*
     - O(1)\*
     - O(n)
     - Key-value lookup (chaining)
   * - ``HashTableOpenAddressing``
     - O(1)\*
     - O(1)\*
     - O(n)
     - Key-value lookup (probing)
   * - ``LRUCache``
     - O(1)
     - O(1)
     - O(capacity)
     - Bounded cache with eviction
   * - ``FenwickTree``
     - O(log n)
     - O(log n)
     - O(n)
     - Prefix-sum queries
   * - ``CountMinSketch``
     - O(d)
     - O(d)
     - O(d × w)
     - Frequency estimation

\* Expected / amortised — k = hash functions, m = bits, d = depth, w = width

Operation Support Matrix
-------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 10 10 10 10 10 10 10 10

   * - Operation
     - DisjointSet
     - BloomFilter
     - SkipList
     - HT Chaining
     - HT Open
     - LRUCache
     - FenwickTree
     - CMS
   * - **Add**
     - make_set
     - add
     - insert
     - put
     - put
     - put
     - update
     - add
   * - **Query**
     - find/connected
     - __contains__
     - search
     - get
     - get
     - get
     - prefix_sum
     - frequency
   * - **Delete**
     - ❌
     - ❌
     - ✅
     - ✅
     - ✅
     - ✅
     - ❌
     - ❌
   * - **Ordered**
     - ❌
     - ❌
     - ✅
     - ❌
     - ❌
     - ❌
     - ❌
     - ❌
   * - **Merge**
     - union
     - union()
     - ❌
     - ❌
     - ❌
     - ❌
     - ❌
     - merge()
   * - **Iterable**
     - ✅
     - ❌\*
     - ✅
     - ✅
     - ✅
     - ✅
     - ✅
     - ❌\*

\* ``__iter__`` raises ``TypeError`` — items cannot be recovered from
probabilistic structures.

Class Hierarchy
================

.. mermaid::

   classDiagram
       class Collection {
           <<abstract>>
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

       AbstractDisjointSet <|.. DisjointSet
       AbstractProbabilisticSet <|.. BloomFilter
       AbstractSkipList <|.. SkipList
       AbstractHashTable <|.. HashTableChaining
       AbstractHashTable <|.. HashTableOpenAddressing
       AbstractLRUCache <|.. LRUCache
       AbstractFenwickTree <|.. FenwickTree
       Collection <|.. CountMinSketch

Related Modules
===============

* :doc:`../core/index` — Core abstractions and exception hierarchy
* :doc:`../linear/index` — Linear data structures
* :doc:`../tree/index` — Tree structures
* :doc:`../graph/index` — Graph structures (uses DisjointSet)
