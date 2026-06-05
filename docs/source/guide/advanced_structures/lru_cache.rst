.. _guide_advanced_lru_cache:

=========================
LRU Cache — User Guide
=========================


Introduction
============

An **LRU Cache** (Least Recently Used) is a bounded-capacity key-value store
that evicts the least recently used entry when full. Every call to ``get``
or ``put`` moves the accessed entry to the most-recently-used (MRU) position.

Foundations
===========

LRU Eviction Policy
--------------------

Entries are ordered from least recently used (LRU) to most recently used
(MRU). When capacity is reached, the head of the list (LRU) is evicted.

.. mermaid::

   graph LR
       subgraph "Before get(B)"
           LRU1["A (LRU)"] --> B1["B"] --> C1["C (MRU)"]
       end
       subgraph "After get(B)"
           LRU2["A (LRU)"] --> C2["C"] --> B2["B (MRU)"]
       end

O(1) Implementation
--------------------

The combination of a **doubly-linked list** and a **hash map** achieves O(1)
for both ``get`` and ``put``:

* The linked list maintains LRU → MRU order
* The hash map maps each key to its node in the list
* O(1) node access via hash map + O(1) move to head/tail

.. mermaid::

   graph TB
       subgraph "Hash Map"
           HM["key → node"]
       end
       subgraph "Doubly-Linked List (LRU → MRU)"
           HEAD["head (sentinel)"] --> N1["A"] --> N2["B"] --> N3["C"] --> TAIL["tail (sentinel)"]
           N3 --> N2
           N2 --> N1
           N1 --> HEAD
           TAIL --> N3
       end
       HM -.-> N1
       HM -.-> N2
       HM -.-> N3

Sentinel Nodes
--------------

The implementation uses two fixed sentinel nodes ``_head`` and ``_tail``,
eliminating edge cases when inserting or removing at the list boundaries.

Usage
=====

.. code-block:: python

   from sds.advanced import LRUCache

   cache = LRUCache(capacity=3)

   cache.put(1, "one")
   cache.put(2, "two")
   cache.put(3, "three")

   # get() promotes to MRU
   print(cache.get(1))      # "one" — 1 becomes MRU
   # Order: 2(LRU), 3, 1(MRU)

   cache.put(4, "four")     # evicts 2 (LRU)
   print(cache.get(2))      # None — evicted

   # peek() without promotion
   print(cache.peek(3))     # "three" — 3 stays LRU

   # Inspect order
   print(cache.keys())      # [3, 1, 4] (LRU → MRU)

   # Eviction counter
   print(cache.evictions_count)   # 1

   # Manual deletion (does not increment evictions_count)
   cache.delete(3)
   assert 3 not in cache

   # LRU → MRU iteration
   for key, val in cache.items():
       print(key, val)

   # Reset (does not increment evictions_count)
   cache.clear()
   assert cache.is_empty()

``get`` vs ``peek`` vs ``__contains__``
----------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Method
     - Returns value
     - Updates recency
   * - ``get(key)``
     - ✅
     - ✅ (moves to MRU)
   * - ``peek(key)``
     - ✅
     - ❌ (order unchanged)
   * - ``key in cache``
     - ❌ (bool only)
     - ❌

Real-World Use Cases
====================

Database Query Cache
--------------------

.. code-block:: python

   from sds.advanced import LRUCache

   query_cache = LRUCache(capacity=500)

   def execute_query(sql):
       result = query_cache.get(sql)
       if result is None:
           result = db.execute(sql)
           query_cache.put(sql, result)
       return result

Memoisation
-----------

.. code-block:: python

   cache = LRUCache(capacity=256)

   def fib(n):
       if n <= 1:
           return n
       cached = cache.get(n)
       if cached is not None:
           return cached
       result = fib(n - 1) + fib(n - 2)
       cache.put(n, result)
       return result

Browser Page Cache
------------------

.. code-block:: python

   browser_cache = LRUCache(capacity=50)

   def load_page(url):
       page = browser_cache.get(url)   # promotes to MRU
       if page is None:
           page = fetch_from_network(url)
           browser_cache.put(url, page)
       return page

Best Practices
==============

✅ Use ``peek()`` to inspect a value without disturbing the eviction order.

✅ Monitor ``evictions_count`` to detect an under-sized cache.

✅ Use ``key in cache`` to distinguish a stored ``None`` value from a
cache miss before calling ``get()``.

❌ Do not use ``__contains__`` as a substitute for ``get()`` — it does
not promote the entry, and ``get()`` can return ``None`` for two distinct
reasons (absent key vs stored ``None`` value).

References
==========

.. [1] LeetCode problem 146 — LRU Cache (canonical interview problem).
   https://leetcode.com/problems/lru-cache/

.. [2] Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.),
   Chapter 11. MIT Press.

See Also
========

* :ref:`api_advanced_lru_cache` — API Reference
* :ref:`guide_advanced_hash_table` — Underlying hash tables
