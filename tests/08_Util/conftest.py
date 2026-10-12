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

"""Structures shared by the visualiser tests (#65)."""

from typing import Tuple

import pytest

from sds.graph import (
    DirectedGraph,
    Graph,
    GraphNode,
    WeightedDirectedEdge,
    WeightedDirectedGraph,
    WeightedEdge,
    WeightedGraph,
)
from sds.graph.edge import DirectedEdge, Edge
from sds.tree import BinarySearchTree, BTree, Tree


@pytest.fixture
def nodes() -> Tuple[GraphNode, ...]:
    """Four nodes A..D with ids n1..n4."""
    return tuple(GraphNode(data, f"n{i}") for i, data in enumerate("ABCD", 1))


@pytest.fixture
def weighted_digraph(nodes: Tuple[GraphNode, ...]) -> WeightedDirectedGraph:
    """A -> B (4), A -> C (1), C -> B (2), B -> D (1)."""
    a, b, c, d = nodes
    graph = WeightedDirectedGraph()
    for node in nodes:
        graph.add_node(node)
    for src, dst, weight in ((a, b, 4.0), (a, c, 1.0), (c, b, 2.0), (b, d, 1.0)):
        graph.add_edge(WeightedDirectedEdge(src, dst, weight))
    return graph


@pytest.fixture
def undirected(nodes: Tuple[GraphNode, ...]) -> Graph:
    """A -- B, B -- C, isolated D."""
    a, b, c, _ = nodes
    graph = Graph()
    for node in nodes:
        graph.add_node(node)
    graph.add_edge(Edge(a, b))
    graph.add_edge(Edge(b, c))
    return graph


@pytest.fixture
def weighted_undirected(nodes: Tuple[GraphNode, ...]) -> WeightedGraph:
    """A -- B (2.5)."""
    a, b, _, _ = nodes
    graph = WeightedGraph()
    graph.add_node(a)
    graph.add_node(b)
    graph.add_edge(WeightedEdge(a, b, 2.5))
    return graph


@pytest.fixture
def digraph(nodes: Tuple[GraphNode, ...]) -> DirectedGraph:
    """A -> B, B -> A."""
    a, b, _, _ = nodes
    graph = DirectedGraph()
    graph.add_node(a)
    graph.add_node(b)
    graph.add_edge(DirectedEdge(a, b))
    graph.add_edge(DirectedEdge(b, a))
    return graph


@pytest.fixture
def bst() -> BinarySearchTree:
    """50 / (30 / 20, 40), 70."""
    tree = BinarySearchTree()
    for key in (50, 30, 70, 20, 40):
        tree.insert(key)
    return tree


@pytest.fixture
def general_tree() -> Tree:
    """r / (a / c), b."""
    tree = Tree("r")
    a = tree.add_child("a", tree.root)
    tree.add_child("b", tree.root)
    tree.add_child("c", a)
    return tree


@pytest.fixture
def btree() -> BTree:
    """Minimum degree 2, keys 1..10."""
    tree = BTree(2)
    for key in range(1, 11):
        tree.insert(key)
    return tree
