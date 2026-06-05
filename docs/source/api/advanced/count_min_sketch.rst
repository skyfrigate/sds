.. _api_advanced_count_min_sketch:

================
Count-Min Sketch
================

.. currentmodule:: sds.advanced.count_min_sketch

.. autoclass:: CountMinSketch
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __contains__, __len__, __repr__, __str__

   .. rubric:: Complexity Summary

   .. list-table::
      :header-rows: 1
      :widths: 30 20 50

      * - Operation
        - Complexity
        - Notes
      * - ``add(item, count)``
        - O(d)
        - d = depth (number of rows)
      * - ``frequency(item)``
        - O(d)
        - Upper bound on true count
      * - ``__contains__(item)``
        - O(d)
        - True iff frequency > 0
      * - ``merge(other)``
        - O(d × w)
        - Element-wise sum
      * - ``clear()``
        - O(d × w)
        - Resets all counters
      * - ``from_dimensions(w, d)``
        - O(d × w)
        - Class method constructor
      * - Space
        - O(d × w)
        - d rows × w columns of integers

   .. note::

      ``frequency(x)`` is always ≥ the true count of *x* (no false
      negatives). The additive error is bounded by :math:`\varepsilon \cdot N`
      with probability :math:`\geq 1 - \delta`, where *N* is the total
      number of items added.

      ``__iter__`` raises :exc:`TypeError` — individual items cannot be
      recovered from the counter matrix.
