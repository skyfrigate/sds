# Copyright 2024-2025, skyfrigate, biface
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Advanced data structures module.

This module provides advanced data structures that go beyond basic collections,
including disjoint sets, probabilistic structures, and specialized trees optimized
for specific use cases.

Submodules
----------
interfaces
    Abstract base classes for advanced structures.
disjoint_set
    Union-Find data structure for disjoint set operations.

Classes
-------
DisjointSet
    Union-Find with path compression and union by rank.

Abstract Interfaces
-------------------
AbstractDisjointSet
    Interface for disjoint set structures.
AbstractProbabilisticSet
    Interface for probabilistic membership structures.

Examples
--------
Using DisjointSet for connected components:

>>> from sds.advanced import DisjointSet
>>> ds = DisjointSet()
>>> for i in range(5):
...     ds.make_set(i)
>>> ds.union(0, 1)
True
>>> ds.union(2, 3)
True
>>> ds.union(1, 2)
True
>>> ds.count_sets()
2
>>> ds.connected(0, 3)
True

Detect cycles in a graph:

>>> ds = DisjointSet()
>>> edges = [(0, 1), (1, 2), (2, 0)]  # Triangle
>>> nodes = {0, 1, 2}
>>> for node in nodes:
...     ds.make_set(node)
>>> has_cycle = False
>>> for u, v in edges:
...     if ds.connected(u, v):
...         has_cycle = True
...         break
...     ds.union(u, v)
>>> has_cycle
True

Notes
-----
Advanced data structures are designed for specialized use cases where
standard structures (lists, trees, graphs) are insufficient:

**DisjointSet (Union-Find)**
- Use for: Connected components, cycle detection, MST algorithms
- Complexity: O(α(n)) amortized for all operations
- Space: O(n)

**Future Structures** (to be implemented):
- BloomFilter: Space-efficient probabilistic set membership
- SkipList: Probabilistic balanced search structure
- FenwickTree: Efficient range sum queries
- SegmentTree: Range queries with lazy propagation
- LRUCache: Cache with least-recently-used eviction
- CountMinSketch: Frequency estimation for streaming data

Performance Considerations
--------------------------
These structures trade off different properties:
- **Disjoint Set**: Near-constant time, permanent unions
- **Bloom Filter**: Space efficiency, probabilistic answers
- **Skip List**: Simplicity, good average case
- **Segment Tree**: Flexibility, O(log n) guarantees

Choose based on your specific requirements for time, space, and accuracy.

See Also
--------
sds.core : Core collection interfaces.
sds.linear : Linear data structures.
sds.tree : Tree data structures.
sds.graph : Graph data structures.
sds.algorithms : Algorithms using these structures.

References
----------
.. [1] Cormen, T. H., et al. (2009). "Introduction to Algorithms", 3rd ed.
.. [2] Sedgewick, R., & Wayne, K. (2011). "Algorithms", 4th ed.
.. [3] Tarjan, R. E. (1975). "Efficiency of a Good But Not Linear Set
       Union Algorithm".
"""

from .disjoint_set import DisjointSet
from .interfaces import AbstractDisjointSet, AbstractProbabilisticSet

__all__ = [
    # Concrete implementations
    "DisjointSet",
    # Abstract interfaces
    "AbstractDisjointSet",
    "AbstractProbabilisticSet",
]

__version__ = "0.1.0"
