.. _guide_advanced_hash_table:

==========================
Hash Tables — User Guide
==========================


Introduction
============

A **hash table** maps keys to values via a hash function. SDS-Tools provides
two implementations with different collision-resolution strategies, both
sharing the :class:`~sds.advanced.interfaces.AbstractHashTable` interface.

Mathematical Foundations
========================

Hash Function
-------------

A hash function :math:`h : U \to [0, m)` maps the universe of keys :math:`U`
to :math:`m` slots. Python's built-in ``hash()`` is used internally, composed
with ``% m``.

Load Factor
-----------

.. math::

   \alpha = \frac{n}{m}

where :math:`n` = stored entries, :math:`m` = capacity. Higher :math:`\alpha`
increases the probability of collision.

Strategy 1 — Separate Chaining
================================

Each slot holds a list of ``(key, value)`` pairs. Collisions are resolved by
appending to the list.

.. mermaid::

   graph LR
       subgraph "Bucket array (m=4)"
           B0["slot 0"] --> L0["[('apple', 1)]"]
           B1["slot 1"] --> L1["[('dog', 3), ('cat', 2)]"]
           B2["slot 2"] --> L2["[]"]
           B3["slot 3"] --> L3["[('egg', 4)]"]
       end

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - Operation
     - Complexity
     - Notes
   * - ``put``
     - O(1)\*
     - O(n) on resize
   * - ``get``
     - O(1)\*
     - O(n) worst case (all in one slot)
   * - ``delete``
     - O(1)\*
     - Direct list removal
   * - Load factor
     - Any value > 0
     - May exceed 1.0

\* Average case with uniform distribution

Strategy 2 — Open Addressing (Linear Probing)
==============================================

All entries reside in the primary array. On collision, the algorithm probes
successive slots ``(h + 1) % m``, ``(h + 2) % m``, etc. Deleted slots are
marked with a **tombstone** (``_DELETED``) to preserve probing chains.

.. mermaid::

   graph LR
       subgraph "Array (m=8)"
           S0["0: apple→1"]
           S1["1: ∅"]
           S2["2: cat→2"]
           S3["3: _DELETED"]
           S4["4: dog→3"]
           S5["5: ∅"]
           S6["6: ∅"]
           S7["7: egg→4"]
       end

.. list-table::
   :header-rows: 1
   :widths: 30 25 45

   * - Operation
     - Complexity
     - Notes
   * - ``put``
     - O(1)\*
     - O(n) on resize
   * - ``get``
     - O(1)\*
     - Traverses tombstones
   * - ``delete``
     - O(1)\*
     - Leaves tombstone sentinel
   * - Load factor
     - Must be < 1.0
     - Default: 0.6

\* Average case; O(n) worst case with primary clustering

Automatic Resizing
==================

Both classes double capacity and rehash all live entries when the load factor
exceeds ``max_load_factor``. Rehashing also clears all tombstones (open
addressing).

SDS Implementation
==================

.. mermaid::

   classDiagram
       class AbstractHashTable {
           <<abstract>>
           +put(key, value)
           +get(key) Any
           +delete(key) bool
           +__contains__(key) bool
           +__len__() int
           +__iter__() Iterator
       }
       class HashTableChaining {
           -_buckets: list~list~
           -_capacity: int
           -_max_load_factor: float
           +put(key, value)
           +get(key) Any
           +items() Iterator
       }
       class HashTableOpenAddressing {
           -_slots: list
           -_capacity: int
           -_max_load_factor: float
           +put(key, value)
           +get(key) Any
           +items() Iterator
       }
       AbstractHashTable <|.. HashTableChaining
       AbstractHashTable <|.. HashTableOpenAddressing

Usage
=====

Chaining
--------

.. code-block:: python

   from sds.advanced import HashTableChaining

   ht = HashTableChaining(capacity=16, max_load_factor=0.75)

   # Insert / update
   ht.put("name", "Alice")
   ht.put("age", 30)
   ht.put("name", "Bob")    # update

   # Lookup
   print(ht.get("name"))    # "Bob"
   print(ht.get("city"))    # None

   # Bracket syntax
   ht["score"] = 100
   print(ht["score"])       # 100

   # Membership
   assert "age" in ht
   assert "city" not in ht

   # Delete
   ht.delete("age")

   # Iteration
   for key, val in ht.items():
       print(key, val)

Open Addressing
---------------

.. code-block:: python

   from sds.advanced import HashTableOpenAddressing

   ht = HashTableOpenAddressing(capacity=16, max_load_factor=0.6)

   for i in range(100):
       ht.put(i, i ** 2)

   assert ht.get(42) == 1764
   assert len(ht) == 100

Choosing a Strategy
--------------------

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Criterion
     - Chaining
     - Open Addressing
   * - Load factor > 1
     - ✅ Possible
     - ❌ Forbidden
   * - Memory locality
     - ❌ (scattered lists)
     - ✅ (compact array)
   * - Frequent deletions
     - ✅ (direct removal)
     - ⚠️ (tombstones accumulate)
   * - Unknown key distribution
     - ✅ (chains absorb)
     - ⚠️ (clustering risk)

Real-World Use Cases
====================

Word Frequency Counter
----------------------

.. code-block:: python

   from sds.advanced import HashTableChaining

   ht = HashTableChaining()
   words = ["the", "cat", "the", "dog", "the"]
   for word in words:
       ht.put(word, (ht.get(word) or 0) + 1)

   print(ht.get("the"))     # 3
   print(ht.get("cat"))     # 1

Symbol Table (Compiler)
-----------------------

.. code-block:: python

   symbols = HashTableOpenAddressing(capacity=256)
   symbols.put("x", {"type": "int", "addr": 0x100})
   symbols.put("y", {"type": "float", "addr": 0x108})

   if "x" in symbols:
       info = symbols.get("x")

Best Practices
==============

✅ Use ``HashTableChaining`` when load factor may exceed 1 or key
distribution is unknown.

✅ Use ``HashTableOpenAddressing`` for better memory locality with
well-distributed keys.

✅ Tune ``max_load_factor``: 0.5–0.7 for open addressing, 0.75–1.0 for
chaining.

❌ Do not use unhashable keys (lists, dicts).

References
==========

.. [1] Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.),
   Chapter 11. MIT Press.

.. [2] OpenDSA — Hashing.
   https://opendsa-server.cs.vt.edu/ODSA/Books/Everything/html/HashIntro.html

See Also
========

* :ref:`api_advanced_hash_table` — API Reference
* :ref:`guide_advanced_lru_cache` — LRU Cache built on a hash map
