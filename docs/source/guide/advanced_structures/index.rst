.. _guide_advanced_structures:

====================
Advanced Structures
====================

Introduction
============

Advanced data structures solve specialised computational problems with
remarkable efficiency guarantees. They go beyond standard collections by
exploiting probabilistic techniques, internal algorithmic optimisations, and
hybrid designs to achieve near-constant time complexity, compact space usage,
or bounded-error estimation.

.. mermaid::

   graph TB
       DS["DisjointSet<br/>O(α(n)) ≈ O(1)"]
       BF["BloomFilter<br/>O(m) bits"]
       SL["SkipList<br/>O(log n)*"]
       HT["HashTable<br/>O(1)*"]
       LRU["LRUCache<br/>O(1)"]
       FT["FenwickTree<br/>O(log n)"]
       CMS["CountMinSketch<br/>O(d)"]

       DS --> G[Graph Algorithms]
       BF --> DB[Databases / Caches]
       SL --> IDX[Ordered Indexes]
       HT --> SYM[Symbol Tables]
       LRU --> CACHE[Bounded Caches]
       FT --> STAT[Prefix Statistics]
       CMS --> STREAM[Stream Analytics]

       style DS fill:#90ee90,stroke:#27ae60,color:#000
       style BF fill:#ffb6b6,stroke:#c0392b,color:#000
       style SL fill:#b6b6ff,stroke:#2980b9,color:#000
       style HT fill:#fff8dc,stroke:#f39c12,color:#000
       style LRU fill:#ffd700,stroke:#b8860b,color:#000
       style FT fill:#e6e6fa,stroke:#6a5acd,color:#000
       style CMS fill:#ffe4b5,stroke:#cd853f,color:#000

Structure Overview
==================

.. list-table::
   :header-rows: 1
   :widths: 22 20 18 40

   * - Structure
     - Key Operation
     - Complexity
     - Primary Use Case
   * - :ref:`DisjointSet <guide_advanced_disjoint_set>`
     - union / connected
     - O(α(n))
     - Dynamic connectivity (Kruskal, components)
   * - :ref:`BloomFilter <guide_advanced_bloom_filter>`
     - add / __contains__
     - O(k)
     - Compact membership, deduplication
   * - :ref:`SkipList <guide_advanced_skip_list>`
     - insert / search
     - O(log n)\*
     - Sorted dictionary, order book
   * - :ref:`HashTable <guide_advanced_hash_table>`
     - put / get
     - O(1)\*
     - Symbol table, key-value cache
   * - :ref:`LRUCache <guide_advanced_lru_cache>`
     - get / put
     - O(1)
     - Bounded cache with LRU eviction
   * - :ref:`FenwickTree <guide_advanced_fenwick_tree>`
     - update / prefix_sum
     - O(log n)
     - Prefix sums, rank statistics
   * - :ref:`CountMinSketch <guide_advanced_count_min_sketch>`
     - add / frequency
     - O(d)
     - Frequency estimation over streams

\* Expected / amortised — k = hash functions, d = depth

Shared ``Collection`` Interface
================================

All structures inherit from :class:`~sds.core.interfaces.Collection`:

.. code-block:: python

   from sds.core.interfaces import Collection
   from sds.advanced import SkipList, LRUCache, FenwickTree

   structures = [SkipList(), LRUCache(10), FenwickTree(100)]

   for s in structures:
       assert isinstance(s, Collection)
       assert s.is_empty()       # True on a new structure
       assert not s              # bool(s) == False when empty

Every structure implements:

* ``is_empty()`` — O(1) emptiness check
* ``clear()`` — reset to initial state
* ``__len__()`` — number of stored elements (or stream size)
* ``__contains__(item)`` — membership test
* ``__bool__()`` — truthiness (delegates to ``not is_empty()``)

.. note::

   ``BloomFilter`` and ``CountMinSketch`` raise ``TypeError`` on
   ``__iter__`` — individual items cannot be recovered from a probabilistic
   structure's internal counters.

Deterministic vs Probabilistic
================================

.. list-table::
   :header-rows: 1
   :widths: 35 35 30

   * - Deterministic (exact results)
     - Probabilistic (approximate results)
     - Hybrid
   * - DisjointSet, HashTable, LRUCache, FenwickTree
     - BloomFilter, CountMinSketch
     - SkipList (random levels, exact results)

For probabilistic structures:

* **No false negatives**: a ``False`` or ``0`` result is always exact.
* **Possible false positives**: a ``True`` or ``> 0`` result may carry a
  bounded error.

Choosing a Structure
=====================

.. mermaid::

   graph TD
       A{What is your need?}

       A -->|Track connectivity| DS[DisjointSet]
       A -->|Compact membership| BF[BloomFilter]
       A -->|Sorted key-value| SL[SkipList]
       A -->|Fast key-value| HT[HashTable]
       A -->|Bounded cache| LRU[LRUCache]
       A -->|Prefix sums| FT[FenwickTree]
       A -->|Stream frequencies| CMS[CountMinSketch]

       style DS fill:#90ee90
       style BF fill:#ffb6b6
       style SL fill:#b6b6ff
       style HT fill:#fff8dc
       style LRU fill:#ffd700
       style FT fill:#e6e6fa
       style CMS fill:#ffe4b5

.. toctree::
   :maxdepth: 2

   disjoint_set
   bloom_filter
   skip_list
   hash_table
   lru_cache
   fenwick_tree
   count_min_sketch
