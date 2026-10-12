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

"""Tests for the node placement of the visualiser's image output (#65).

Pure geometry: these tests do not need matplotlib.
"""

import math
from typing import Any, List, Tuple

import pytest

from sds.linear import CircularLinkedList, DoublyLinkedList, LinkedList, Queue
from sds.tree import BinarySearchTree, BTree, Tree
from sds.utils.visualizer._layout import Drawing, layout
from sds.utils.visualizer._views import build_view


def placed(drawing: Drawing) -> List[Tuple[str, float, float]]:
    """Labels and positions of the boxed nodes."""
    return [(n.label, n.x, n.y) for n in drawing.nodes if not n.marker]


class TestChainLayout:
    """Placement of linear structures."""

    def test_row(self) -> None:
        """Items sit on one row, linked left to right with arrow heads."""
        structure = LinkedList()
        for item in (1, 2, 3):
            structure.append(item)
        drawing = layout(build_view(structure))
        assert placed(drawing) == [("1", 0.0, 0.0), ("2", 1.0, 0.0), ("3", 2.0, 0.0)]
        assert [(e.start, e.end, e.arrow) for e in drawing.edges] == [
            (0, 1, "-|>"),
            (1, 2, "-|>"),
        ]

    def test_doubly_linked_arrows(self) -> None:
        """Doubly linked lists get two-headed arrows."""
        structure = DoublyLinkedList()
        for item in (1, 2):
            structure.append(item)
        assert layout(build_view(structure)).edges[0].arrow == "<|-|>"

    def test_circular_back_edge_is_bent(self) -> None:
        """The edge back to the head is bent over the row."""
        structure = CircularLinkedList()
        for item in (1, 2, 3):
            structure.append(item)
        back = layout(build_view(structure)).edges[-1]
        assert (back.start, back.end) == (2, 0)
        assert back.bend != 0

    def test_named_ends_are_markers(self) -> None:
        """Front and rear are unboxed markers above their end nodes."""
        queue = Queue()
        for item in (1, 2, 3):
            queue.enqueue(item)
        markers = [(n.label, n.x) for n in layout(build_view(queue)).nodes if n.marker]
        assert markers == [("front", 0.0), ("rear", 2.0)]

    def test_empty(self) -> None:
        """An empty chain places nothing."""
        drawing = layout(build_view(Queue()))
        assert drawing.nodes == [] and drawing.edges == []


class TestTreeLayout:
    """Placement of trees."""

    def test_binary_in_order_columns(self, bst: BinarySearchTree) -> None:
        """x is the in-order rank, y minus the depth."""
        assert sorted(placed(layout(build_view(bst)))) == [
            ("20", 0.0, -2.0),
            ("30", 1.0, -1.0),
            ("40", 2.0, -2.0),
            ("50", 3.0, 0.0),
            ("70", 4.0, -1.0),
        ]

    def test_binary_single_child_keeps_its_side(self) -> None:
        """A lone right child sits to the right of its parent."""
        tree = BinarySearchTree()
        for key in (5, 7):
            tree.insert(key)
        positions = {label: x for label, x, _ in placed(layout(build_view(tree)))}
        assert positions["7"] > positions["5"]

    def test_general_parent_centred(self, general_tree: Tree) -> None:
        """Leaves left to right; each parent centred over its children."""
        tree = general_tree
        tree.add_child("d", tree.root.children[0])
        assert placed(layout(build_view(tree))) == [
            ("r", 1.25, 0.0),
            ("a", 0.5, -1.0),
            ("c", 0.0, -2.0),
            ("d", 1.0, -2.0),
            ("b", 2.0, -1.0),
        ]

    def test_btree_edges(self, btree: BTree) -> None:
        """Every non-root node has one incoming edge, without arrow head."""
        drawing = layout(build_view(btree))
        assert len(drawing.edges) == len(drawing.nodes) - 1
        assert {e.arrow for e in drawing.edges} == {"-"}

    def test_no_overlap(self) -> None:
        """No two nodes of a binary tree share a position."""
        tree = BinarySearchTree()
        for key in (8, 3, 10, 1, 6, 14, 4, 7, 13):
            tree.insert(key)
        positions = [(x, y) for _, x, y in placed(layout(build_view(tree)))]
        assert len(set(positions)) == len(positions)

    def test_empty(self) -> None:
        """An empty tree places nothing."""
        assert layout(build_view(BinarySearchTree())).nodes == []


class TestGraphLayout:
    """Placement of graphs."""

    def test_circle_from_the_top_clockwise(self, weighted_digraph: Any) -> None:
        """Nodes on a circle, first at the top, then clockwise."""
        nodes = layout(build_view(weighted_digraph)).nodes
        assert nodes[0].x == pytest.approx(0.0) and nodes[0].y > 0
        assert nodes[1].x > 0 and nodes[1].y == pytest.approx(0.0)
        radii = {round(math.hypot(n.x, n.y), 6) for n in nodes}
        assert len(radii) == 1

    def test_directed_edges_have_heads(self, weighted_digraph: Any) -> None:
        """Directed edges are arrows and keep their weights."""
        edges = layout(build_view(weighted_digraph)).edges
        assert {e.arrow for e in edges} == {"-|>"}
        assert [e.label for e in edges] == ["4.0", "1.0", "2.0", "1.0"]

    def test_opposite_edges_are_bent(self, digraph: Any) -> None:
        """a -> b and b -> a are bent so they do not overlap."""
        assert [e.bend for e in layout(build_view(digraph)).edges] == [0.2, 0.2]

    def test_undirected_edges_are_lines(self, undirected: Any) -> None:
        """Undirected edges are plain, straight lines."""
        edges = layout(build_view(undirected)).edges
        assert {(e.arrow, e.bend) for e in edges} == {("-", 0.0)}

    def test_single_node_at_origin(self, nodes: Any) -> None:
        """A lone node sits at the origin."""
        from sds.graph import Graph

        graph = Graph()
        graph.add_node(nodes[0])
        drawing = layout(build_view(graph))
        assert placed(drawing) == [("A", 0.0, 0.0)]


class TestBounds:
    """Drawing.bounds()."""

    def test_bounds(self, bst: BinarySearchTree) -> None:
        """Bounds span all nodes."""
        assert layout(build_view(bst)).bounds() == (0.0, 4.0, -2.0, 0.0)

    def test_empty_bounds(self) -> None:
        """An empty drawing is bounded at the origin."""
        assert Drawing().bounds() == (0.0, 0.0, 0.0, 0.0)
