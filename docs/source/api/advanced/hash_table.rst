.. _api_advanced_hash_table:

===========
Hash Tables
===========

.. currentmodule:: sds.advanced.hash_table

Two concrete hash table implementations share the
:class:`~sds.advanced.interfaces.AbstractHashTable` interface and differ only
in their collision-resolution strategy.

.. list-table:: Strategy Comparison
   :header-rows: 1
   :widths: 30 35 35

   * - Aspect
     - ``HashTableChaining``
     - ``HashTableOpenAddressing``
   * - Collision handling
     - Per-slot linked list
     - Linear probing + tombstones
   * - Load factor constraint
     - Any positive value
     - Must be < 1.0
   * - Deletion
     - Direct list removal
     - Tombstone (``_DELETED``)
   * - Resize clears tombstones
     - N/A
     - Yes — full rehash

----

HashTableChaining
=================

.. autoclass:: HashTableChaining
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __contains__, __len__, __iter__, __getitem__, __setitem__, __repr__, __str__

   .. rubric:: Complexity Summary

   .. list-table::
      :header-rows: 1
      :widths: 30 20 50

      * - Operation
        - Complexity
        - Notes
      * - ``put(key, value)``
        - O(1)*
        - O(n) on resize
      * - ``get(key)``
        - O(1)*
        - Returns None if absent
      * - ``delete(key)``
        - O(1)*
        - Returns False if absent
      * - ``__contains__``
        - O(1)*
        - \* average case
      * - ``__iter__``
        - O(capacity + n)
        - Unspecified order
      * - ``clear()``
        - O(capacity)
        - Resets all buckets
      * - Space
        - O(n)
        - Plus bucket overhead

----

HashTableOpenAddressing
=======================

.. autoclass:: HashTableOpenAddressing
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __contains__, __len__, __iter__, __getitem__, __setitem__, __repr__, __str__

   .. rubric:: Complexity Summary

   .. list-table::
      :header-rows: 1
      :widths: 30 20 50

      * - Operation
        - Complexity
        - Notes
      * - ``put(key, value)``
        - O(1)*
        - O(n) on resize
      * - ``get(key)``
        - O(1)*
        - Returns None if absent
      * - ``delete(key)``
        - O(1)*
        - Leaves tombstone
      * - ``__contains__``
        - O(1)*
        - \* average case
      * - ``__iter__``
        - O(capacity)
        - Skips tombstones
      * - ``clear()``
        - O(capacity)
        - Removes tombstones
      * - Space
        - O(n)
        - Compact array
