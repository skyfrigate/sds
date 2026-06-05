.. _api_advanced_bloom_filter:

============
Bloom Filter
============

.. currentmodule:: sds.advanced.bloom_filter

.. autoclass:: BloomFilter
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
      * - ``add(item)``
        - O(k)
        - k = number of hash functions
      * - ``__contains__(item)``
        - O(k)
        - No false negatives
      * - ``estimated_fill_ratio()``
        - O(m/8)
        - m = bit array size in bits
      * - ``estimated_fp_rate()``
        - O(m/8)
        - fill_ratio^k
      * - ``union(other)``
        - O(m/8)
        - Bitwise OR of arrays
      * - ``intersection(other)``
        - O(m/8)
        - Bitwise AND of arrays
      * - ``optimal_params(n, fp_rate)``
        - O(1)
        - Static method
      * - ``clear()``
        - O(m/8)
        - Resets bit array and count
      * - Space
        - O(m)
        - m bits regardless of n
