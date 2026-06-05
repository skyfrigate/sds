.. _guide_advanced_count_min_sketch:

================================
Count-Min Sketch — User Guide
================================


Introduction
============

A **Count-Min Sketch** (CMS) estimates the frequency of elements in a data
stream using a compact :math:`d \times w` counter matrix. Like the Bloom
Filter, it may **overestimate** but never underestimates a true frequency.

Mathematical Foundations
========================

Counter Matrix
--------------

A CMS is a matrix :math:`C[d][w]` of non-negative integer counters,
initialised to 0, with :math:`d` hash functions
:math:`h_1, \ldots, h_d : U \to [0, w)`.

**Add** element :math:`x`:

.. math::

   \forall i \in [1, d] : C[i][h_i(x)] \mathrel{+}= 1

**Estimate** frequency of :math:`x`:

.. math::

   \hat{f}(x) = \min_{i=1}^{d} C[i][h_i(x)]

Probabilistic Guarantee
-----------------------

Let :math:`N` be the total number of elements added. With probability
:math:`\geq 1 - \delta`:

.. math::

   f(x) \leq \hat{f}(x) \leq f(x) + \varepsilon \cdot N

Optimal dimensions:

.. math::

   w = \left\lceil \frac{e}{\varepsilon} \right\rceil
   \qquad
   d = \left\lceil \ln\frac{1}{\delta} \right\rceil

**No false negatives**: :math:`\hat{f}(x) \geq f(x)` always holds.

Double Hashing
--------------

As with the Bloom Filter, the CMS uses double hashing to avoid computing
:math:`d` fully independent hash functions:

.. math::

   h_i(x) = (h_1(x) + i \cdot h_2(x)) \bmod w

Comparison with Bloom Filter
-----------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Aspect
     - Bloom Filter
     - Count-Min Sketch
   * - Stored information
     - Membership (0/1)
     - Frequency (counter)
   * - False negatives
     - ❌ Impossible
     - ❌ Impossible
   * - False positives
     - ✅ Possible
     - ✅ Overestimation possible
   * - Space
     - O(m) bits
     - O(d × w) integers
   * - Merge
     - ``union()``
     - ``merge()``

Usage
=====

Construction
------------

Using error parameters (recommended):

.. code-block:: python

   from sds.advanced import CountMinSketch

   # ε = 1% additive error, δ = 1% failure probability
   cms = CountMinSketch(epsilon=0.01, delta=0.01)
   print(f"Matrix: {cms.depth} × {cms.width}")

Using explicit dimensions:

.. code-block:: python

   cms = CountMinSketch.from_dimensions(width=500, depth=5)

Basic Operations
----------------

.. code-block:: python

   # Add (count=1 by default)
   cms.add("apple")
   cms.add("apple")
   cms.add("banana", count=5)

   # Frequency estimate
   print(cms.frequency("apple"))     # ≥ 2
   print(cms.frequency("banana"))    # ≥ 5
   print(cms.frequency("cherry"))    # 0

   # Membership
   assert "apple" in cms
   assert "cherry" not in cms

   # Total items added
   print(len(cms))                   # 7

   # Reset
   cms.clear()
   assert cms.is_empty()

Merging Sketches
-----------------

.. code-block:: python

   # Both sketches must share the same dimensions
   cms1 = CountMinSketch.from_dimensions(width=200, depth=5)
   cms2 = CountMinSketch.from_dimensions(width=200, depth=5)

   cms1.add("stream_A", count=100)
   cms2.add("stream_A", count=50)

   combined = cms1.merge(cms2)
   assert combined.frequency("stream_A") >= 150
   assert combined.total == 150

Real-World Use Cases
====================

Word Frequency (NLP)
--------------------

.. code-block:: python

   from sds.advanced import CountMinSketch

   cms = CountMinSketch(epsilon=0.001, delta=0.01)

   with open("corpus.txt") as f:
       for line in f:
           for word in line.split():
               cms.add(word.lower())

   for word in ["the", "a", "of", "in"]:
       print(f"{word}: ~{cms.frequency(word)}")

Heavy Hitter Detection (Network)
----------------------------------

.. code-block:: python

   # Detect IPs sending > 1% of traffic
   cms = CountMinSketch(epsilon=0.005, delta=0.01)
   total_packets = 0

   for packet in network_stream():
       cms.add(packet.src_ip)
       total_packets += 1

   threshold = 0.01 * total_packets
   suspicious = [ip for ip in known_ips if cms.frequency(ip) > threshold]

Distributed Aggregation
------------------------

.. code-block:: python

   # Distributed nodes — identical dimensions required
   w, d = 1000, 7
   node_sketches = [CountMinSketch.from_dimensions(w, d) for _ in range(10)]

   # Each node processes its partition
   for i, node in enumerate(node_sketches):
       for event in get_partition(i):
           node.add(event)

   # Merge results
   from functools import reduce
   global_sketch = reduce(lambda a, b: a.merge(b), node_sketches)

Real-Time Metrics
-----------------

.. code-block:: python

   cms = CountMinSketch(epsilon=0.01, delta=0.05)

   def record(name, value=1):
       cms.add(name, count=value)

   def get_metric(name):
       return cms.frequency(name)

   record("requests", 1)
   record("errors", 1)
   record("latency_ms", 42)

Best Practices
==============

✅ Use ``epsilon`` and ``delta`` to size the sketch — the formulas
provide theoretical guarantees.

✅ Use ``len(cms)`` (total added) to interpret relative frequencies.

✅ For distributed merging, all sketches must have identical dimensions.

❌ Do not call ``list(cms)`` — raises ``TypeError``. Individual items
cannot be recovered from the counter matrix.

❌ Do not assume ``frequency(x) == 0`` means certain absence — it only
means no hash collision occurred across all rows for *x*.

References
==========

.. [1] Cormode, G., & Muthukrishnan, S. (2005). "An improved data stream
   summary: The count-min sketch and its applications". *Journal of
   Algorithms*, 55(1), 58-75.
   DOI: `10.1016/j.jalgor.2003.12.001 <https://doi.org/10.1016/j.jalgor.2003.12.001>`_

.. [2] Cormode, G. (2009). "Count-Min Sketch". *Encyclopedia of Database Systems*.
   https://dimacs.rutgers.edu/~graham/pubs/papers/cmencyc.pdf

See Also
========

* :ref:`api_advanced_count_min_sketch` — API Reference
* :ref:`guide_advanced_bloom_filter` — Probabilistic membership testing
