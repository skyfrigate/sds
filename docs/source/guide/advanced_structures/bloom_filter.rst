.. _guide_advanced_bloom_filter:

===========================
Bloom Filter — User Guide
===========================


Introduction
============

A **Bloom Filter** is a space-efficient probabilistic data structure that tests
whether an element is a member of a set. It stores only a compact bit array and
guarantees:

* **No false negatives**: if ``x not in bf``, *x* is definitely absent.
* **Possible false positives**: if ``x in bf``, *x* is *probably* (but not
  certainly) present.

Mathematical Foundations
========================

Formal Definition
-----------------

A Bloom Filter for universe :math:`U` is a triple :math:`(m, k, h)` where:

* :math:`m` — size of the bit array
* :math:`k` — number of hash functions :math:`h_1, \ldots, h_k : U \to [0, m)`
* A bit array :math:`B[0..m-1]`, initialised to 0

**Insert** :math:`x \in U`:

.. math::

   \forall i \in [1, k] : B[h_i(x)] \leftarrow 1

**Test** membership of :math:`x`:

.. math::

   x \in S \iff \forall i \in [1, k] : B[h_i(x)] = 1

False Positive Rate
-------------------

For :math:`n` elements inserted into a filter of :math:`m` bits with :math:`k`
hash functions:

.. math::

   P_{fp} \approx \left(1 - e^{-kn/m}\right)^k

Optimal Parameters
------------------

For :math:`n` elements and target false positive rate :math:`p`:

.. math::

   m^* = \left\lceil \frac{-n \ln p}{(\ln 2)^2} \right\rceil
   \qquad
   k^* = \left\lfloor \frac{m}{n} \ln 2 \right\rfloor

Double Hashing
--------------

Instead of :math:`k` independent hash functions, the implementation uses
**double hashing** (Kirsch & Mitzenmacher, 2006):

.. math::

   h_i(x) = (h_1(x) + i \cdot h_2(x)) \bmod m

where :math:`h_1` = SHA-256 and :math:`h_2` = MD5 (non-cryptographic use).

SDS Implementation
==================

.. mermaid::

   classDiagram
       class Collection {
           <<abstract — sds.core>>
           +is_empty() bool
           +clear()
       }
       class AbstractProbabilisticSet {
           <<abstract>>
           +add(item)
           +__contains__(item) bool
           +estimated_fill_ratio() float
       }
       class BloomFilter {
           -_size: int
           -_num_hashes: int
           -_bit_array: bytearray
           -_count: int
           +add(item)
           +__contains__(item) bool
           +estimated_fill_ratio() float
           +estimated_fp_rate() float
           +union(other) BloomFilter
           +intersection(other) BloomFilter
           +optimal_params(n, fp_rate)$
       }
       Collection <|-- AbstractProbabilisticSet
       AbstractProbabilisticSet <|.. BloomFilter

Usage
=====

Construction
------------

Using optimal parameters (recommended):

.. code-block:: python

   from sds.advanced import BloomFilter

   # Compute parameters for 10 000 elements and 1% false positive rate
   size, k = BloomFilter.optimal_params(n=10_000, fp_rate=0.01)
   bf = BloomFilter(size=size, num_hashes=k)
   print(f"Size: {size} bits, hash functions: {k}")

With explicit parameters:

.. code-block:: python

   bf = BloomFilter(size=9586, num_hashes=7)

Basic Operations
----------------

.. code-block:: python

   # Adding elements
   bf.add("apple")
   bf.add("banana")
   bf.add(42)           # integers accepted
   bf.add((1, 2, 3))    # tuples accepted

   # Membership test
   assert "apple" in bf          # True (no false negatives)
   assert "cherry" not in bf     # False → definitely absent

   # Metrics
   print(f"Items added : {len(bf)}")
   print(f"Fill ratio  : {bf.estimated_fill_ratio():.2%}")
   print(f"FP rate est.: {bf.estimated_fp_rate():.4%}")

   # Reset
   bf.clear()
   assert bf.is_empty()

Set Operations
--------------

.. code-block:: python

   bf1 = BloomFilter(size=1000, num_hashes=3)
   bf2 = BloomFilter(size=1000, num_hashes=3)
   bf1.add("alpha")
   bf2.add("beta")

   # Union — contains anything either filter contains
   union = bf1.union(bf2)
   assert "alpha" in union
   assert "beta" in union

   # Intersection (over-approximation)
   bf1.add("common")
   bf2.add("common")
   inter = bf1.intersection(bf2)
   assert "common" in inter

Real-World Use Cases
====================

Stream Deduplication
--------------------

.. code-block:: python

   from sds.advanced import BloomFilter

   size, k = BloomFilter.optimal_params(n=1_000_000, fp_rate=0.001)
   seen = BloomFilter(size=size, num_hashes=k)

   def process_stream(items):
       for item in items:
           if item not in seen:
               process(item)    # process only new items
               seen.add(item)

Cache Pre-Filter
----------------

.. code-block:: python

   # Avoid expensive database lookups
   bf = BloomFilter(size=500_000, num_hashes=7)
   cache = {}

   def get(key):
       if key not in bf:
           return None        # definitely absent
       return cache.get(key) or db.query(key)

Distributed Filter Merge
-------------------------

.. code-block:: python

   # Distributed nodes — identical configuration required
   node1 = BloomFilter(size=100_000, num_hashes=5)
   node2 = BloomFilter(size=100_000, num_hashes=5)
   # ... each node processes its portion of the stream ...
   merged = node1.union(node2)

Best Practices
==============

✅ Use ``optimal_params`` to size the filter correctly for your workload.

✅ Monitor ``estimated_fill_ratio()`` — beyond 0.5, the false positive rate
rises sharply.

✅ Use ``x not in bf`` as a fast guard before an expensive exact lookup.

❌ Do not assume a ``True`` result is exact — it is probabilistic.

❌ Do not use for deletions — the standard Bloom Filter does not support
``delete``.

References
==========

.. [1] Bloom, B. H. (1970). "Space/time trade-offs in hash coding with
   allowable errors". *Communications of the ACM*, 13(7), 422-426.
   DOI: `10.1145/362686.362692 <https://doi.org/10.1145/362686.362692>`_

.. [2] Broder, A., & Mitzenmacher, M. (2004). "Network Applications of
   Bloom Filters: A Survey". *Internet Mathematics*, 1(4), 485-509.
   https://www.eecs.harvard.edu/~michaelm/postscripts/im2005b.pdf

.. [3] Kirsch, A., & Mitzenmacher, M. (2006). "Less Hashing, Same
   Performance: Building a Better Bloom Filter". *ESA 2006*.
   https://www.eecs.harvard.edu/~kirsch/pubs/bbbf/esa06.pdf

.. [4] Shaffer, C. A., et al. *OpenDSA: Open Data Structures and Algorithms*.
   https://opendsa-server.cs.vt.edu/

See Also
========

* :ref:`api_advanced_bloom_filter` — API Reference
* :ref:`guide_advanced_count_min_sketch` — Frequency estimation over streams
