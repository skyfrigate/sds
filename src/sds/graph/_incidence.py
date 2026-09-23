# Copyright 2024-2026, skyfrigate, biface
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

"""Insertion-ordered incidence index shared by the graph implementations.

This is an internal module, not part of the public API. Every
adjacency-holding graph class stores its topology in one
:class:`IncidenceIndex` (undirected) or two (directed: outgoing and
incoming), so that all of them share a single, deterministic layout:

.. code-block:: text

    node_id -> { neighbor_id -> [edge, edge, ...] }

Both mapping levels are plain ``dict`` objects, hence ordered by
insertion (#91). Keeping the edge objects themselves, rather than bare
neighbor ids, is what lets a weighted graph hand out a node's outgoing
edges in O(degree) instead of scanning every edge (#87).

Ordering rules
--------------
- Neighbors are yielded in the order their first connecting edge was
  added.
- Parallel edges to the same neighbor (multigraphs) are yielded
  consecutively, in insertion order.
- When the last edge to a neighbor is removed, the neighbor leaves the
  row; adding an edge to it again appends it at the end.
"""

from typing import Dict, Generic, Iterator, List, TypeVar

from .edge import Edge

E = TypeVar("E", bound=Edge)


class IncidenceIndex(Generic[E]):
    """Two-level, insertion-ordered ``node -> neighbor -> edges`` index.

    The index knows nothing about edge direction: callers decide which
    row an edge is linked into (both endpoints for an undirected edge,
    source row of the outgoing index and target row of the incoming
    index for a directed edge).

    Notes
    -----
    Complexities, with ``d`` the number of distinct neighbors of a node
    and ``k`` the number of parallel edges between two nodes:

    ====================  ===============
    Operation             Time
    ====================  ===============
    ``add_node``          O(1)
    ``link``              O(1) amortized
    ``unlink``            O(k)
    ``has_link``          O(1) average
    ``neighbor_ids``      O(d)
    ``edges_of``          O(degree)
    ``pop_node``          O(1)
    ``drop_node``         O(d)
    ====================  ===============
    """

    __slots__ = ("_rows",)

    def __init__(self) -> None:
        """Initialize an empty index."""
        self._rows: Dict[str, Dict[str, List[E]]] = {}

    def add_node(self, node_id: str) -> None:
        """Create an empty row for ``node_id``."""
        self._rows[node_id] = {}

    def pop_node(self, node_id: str) -> Dict[str, List[E]]:
        """Remove and return the row of ``node_id``.

        The caller is responsible for dropping ``node_id`` from the rows
        of its neighbors (see :meth:`drop_neighbor`).
        """
        return self._rows.pop(node_id)

    def drop_neighbor(self, node_id: str, neighbor_id: str) -> None:
        """Forget every edge from ``node_id``'s row to ``neighbor_id``."""
        self._rows[node_id].pop(neighbor_id, None)

    def link(self, node_id: str, neighbor_id: str, edge: E) -> None:
        """Record ``edge`` in ``node_id``'s row, under ``neighbor_id``."""
        self._rows[node_id].setdefault(neighbor_id, []).append(edge)

    def unlink(self, node_id: str, neighbor_id: str, edge: E) -> None:
        """Remove ``edge`` (by identity) from ``node_id``'s row.

        The neighbor leaves the row once its last edge is removed.
        Identity rather than equality matters for multigraphs: parallel
        edges compare equal (same endpoints) but are distinct objects.
        """
        row = self._rows[node_id]
        bucket = row[neighbor_id]
        for position, candidate in enumerate(bucket):
            if candidate is edge:
                del bucket[position]
                break
        if not bucket:
            del row[neighbor_id]

    def link_undirected(self, edge: E) -> None:
        """Record an undirected ``edge`` in the rows of both endpoints.

        A self-loop is recorded once, in its own row.
        """
        n1_id, n2_id = edge.node1.id, edge.node2.id
        self.link(n1_id, n2_id, edge)
        if n1_id != n2_id:
            self.link(n2_id, n1_id, edge)

    def unlink_undirected(self, edge: E) -> None:
        """Remove an undirected ``edge`` from the rows of both endpoints."""
        n1_id, n2_id = edge.node1.id, edge.node2.id
        self.unlink(n1_id, n2_id, edge)
        if n1_id != n2_id:
            self.unlink(n2_id, n1_id, edge)

    def drop_node(self, node_id: str) -> None:
        """Remove ``node_id``'s row and every reference to it.

        Only valid for an undirected index, where each link has a mirror
        entry in the neighbor's row. A directed graph must use
        :meth:`pop_node` / :meth:`drop_neighbor` across its two indexes.
        """
        for neighbor_id in self._rows.pop(node_id):
            if neighbor_id != node_id:
                self._rows[neighbor_id].pop(node_id, None)

    def has_link(self, node_id: str, neighbor_id: str) -> bool:
        """Return True if at least one edge links the two nodes in this row."""
        return neighbor_id in self._rows[node_id]

    def neighbor_ids(self, node_id: str) -> Iterator[str]:
        """Yield the distinct neighbor ids of ``node_id``, in order."""
        yield from self._rows[node_id]

    def neighbor_count(self, node_id: str) -> int:
        """Return the number of distinct neighbors of ``node_id``."""
        return len(self._rows[node_id])

    def edges_of(self, node_id: str) -> Iterator[E]:
        """Yield every edge recorded in ``node_id``'s row, in order."""
        for bucket in self._rows[node_id].values():
            yield from bucket

    def clear(self) -> None:
        """Remove every row."""
        self._rows.clear()
