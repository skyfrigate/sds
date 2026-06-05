.. _guide_advanced_skip_list:

========================
Skip List — User Guide
========================


Introduction
============

A **Skip List** is a probabilistic alternative to balanced trees. It maintains
a sorted linked list (level 0) augmented with several express-lane linked lists,
enabling O(log n) average-case search, insertion, and deletion without
deterministic rotations or rebalancing.

Mathematical Foundations
========================

Multi-Level Structure
---------------------

A Skip List of maximum height :math:`L` is a family of linked lists
:math:`S_0 \supseteq S_1 \supseteq \cdots \supseteq S_L` where:

* :math:`S_0` — base list containing all elements (sorted)
* :math:`S_i` — subset of :math:`S_{i-1}`; each element is promoted with
  probability :math:`p`

.. mermaid::

   graph LR
       subgraph "Level 2 (express)"
           H2[head] --> N2_1[1] --> N2_10[10] --> T2[tail]
       end
       subgraph "Level 1"
           H1[head] --> N1_1[1] --> N1_4[4] --> N1_10[10] --> N1_15[15] --> T1[tail]
       end
       subgraph "Level 0 (base)"
           H0[head] --> N0_1[1] --> N0_4[4] --> N0_7[7] --> N0_10[10] --> N0_15[15] --> T0[tail]
       end

Expected Complexity
-------------------

With promotion probability :math:`p` and :math:`n` elements:

* Expected height: :math:`E[L] = O(\log_{1/p} n)`
* Expected space: :math:`O(n / (1-p))` — i.e. :math:`O(2n)` for :math:`p = 0.5`

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - Operation
     - Complexity
     - Notes
   * - ``insert(key)``
     - O(log n)\*
     - Updates value if key exists
   * - ``delete(key)``
     - O(log n)\*
     - Returns False if absent
   * - ``search(key)``
     - O(log n)\*
     - Returns None if absent
   * - ``min_key()``
     - O(1)
     - First node in base list
   * - ``max_key()``
     - O(n)
     - Traverses base list
   * - ``__iter__``
     - O(n)
     - Level-0 traversal

\* Expected — p = promotion probability

Level Randomisation
-------------------

The height of a new node is drawn by successive Bernoulli trials:

.. code-block:: python

   level = 0
   while random() < p and level < max_level:
       level += 1

This follows a truncated geometric distribution:
:math:`P(\text{level} = k) = p^k (1-p)`.

SDS Implementation
==================

.. mermaid::

   classDiagram
       class _SkipListNode {
           +key: Any
           +value: Any
           +forward: list
       }
       class SkipList {
           -_max_level: int
           -_probability: float
           -_level: int
           -_length: int
           -_head: _SkipListNode
           +insert(key, value)
           +delete(key) bool
           +search(key) Any
           +min_key() Any
           +max_key() Any
           +items() Iterator
       }
       SkipList --> _SkipListNode

Usage
=====

Construction
------------

.. code-block:: python

   from sds.advanced import SkipList

   # Default: max_level=16, probability=0.5
   sl = SkipList()

   # Custom parameters
   sl = SkipList(max_level=8, probability=0.25)

Basic Operations
----------------

.. code-block:: python

   sl = SkipList()

   # Insert with value
   sl.insert(3, "three")
   sl.insert(1, "one")
   sl.insert(2, "two")

   # Search
   print(sl.search(2))       # "two"
   print(sl.search(99))      # None

   # Membership
   assert 1 in sl
   assert 99 not in sl

   # Delete
   assert sl.delete(2) is True
   assert sl.delete(99) is False

   # Sorted iteration
   for key in sl:
       print(key)            # 1, 3

   # Key-value pairs
   for key, val in sl.items():
       print(key, val)

   # Bounds
   print(sl.min_key())       # 1
   print(sl.max_key())       # 3

   # Update (duplicate key)
   sl.insert(1, "ONE")
   assert sl.search(1) == "ONE"
   assert len(sl) == 2       # no duplicate created

Range Queries
-------------

.. code-block:: python

   sl = SkipList()
   for k in range(20):
       sl.insert(k, k * 2)

   # Range [5, 10]
   result = [(k, v) for k, v in sl.items() if 5 <= k <= 10]

Real-World Use Cases
====================

Order Book
----------

.. code-block:: python

   from sds.advanced import SkipList

   order_book = SkipList()
   # Prices as keys (automatically sorted)
   order_book.insert(101.5, {"qty": 100, "side": "bid"})
   order_book.insert(99.0,  {"qty": 200, "side": "ask"})

   best_bid = order_book.min_key()    # lowest price
   best_ask = order_book.max_key()    # highest price

Leaderboard
-----------

.. code-block:: python

   scores = SkipList()
   for player, score in [("Alice", 1500), ("Bob", 1200), ("Carol", 1800)]:
       scores.insert(score, player)

   # Ascending ranking
   for rank, (score, name) in enumerate(scores.items(), 1):
       print(f"{rank}. {name}: {score}")

Best Practices
==============

✅ Set ``max_level = ceil(log(n) / log(1/p))`` to match the expected
number of elements.

✅ Prefer ``p = 0.5`` (O(log₂ n) behaviour) unless memory is constrained.

✅ Use ``insert(k, v)`` to update values — no duplicate node is created.

❌ Avoid calling ``max_key()`` in tight loops — it is O(n). Maintain a
tail pointer if frequent maximum access is required.

References
==========

.. [1] Pugh, W. (1990). "Skip Lists: A Probabilistic Alternative to
   Balanced Trees". *Communications of the ACM*, 33(6), 668-676.
   DOI: `10.1145/78973.78977 <https://doi.org/10.1145/78973.78977>`_

.. [2] OpenDSA — Skip Lists.
   https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/SkipList.html

See Also
========

* :ref:`api_advanced_skip_list` — API Reference
* :ref:`guide_advanced_hash_table` — O(1) key-value lookup
