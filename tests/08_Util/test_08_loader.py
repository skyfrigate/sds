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

"""Tests for the structure loader of the command line (#106)."""

from typing import Any, Dict

import pytest

from sds.core.exceptions import InvalidParameterError, StructureTypeError
from sds.graph import (
    AdjacencyMatrixGraph,
    DirectedEdge,
    DirectedGraph,
    Edge,
    Graph,
    WeightedDirectedEdge,
    WeightedDirectedGraph,
    WeightedEdge,
    WeightedGraph,
)
from sds.linear import PriorityQueue, Queue, Stack, to_list
from sds.tree import AVLTree, BTree, Tree
from sds.utils._loader import SUPPORTED, build
from sds.utils.visualizer import to_text


class TestLinear:
    """Linear structures are filled from items, in order."""

    def test_stack_pushes_items_in_order(self) -> None:
        """The last item ends on top."""
        stack = build({"type": "Stack", "items": [1, 2, 3]})
        assert isinstance(stack, Stack)
        assert stack.peek() == 3

    def test_queue(self) -> None:
        """A queue keeps the order of items."""
        queue = build({"type": "Queue", "items": ["a", "b"]})
        assert isinstance(queue, Queue)
        assert to_list(queue) == ["a", "b"]

    def test_options_reach_the_constructor(self) -> None:
        """options are passed to the constructor through from_list()."""
        queue = build(
            {"type": "PriorityQueue", "items": [2, 5, 1], "options": {"reverse": True}}
        )
        assert isinstance(queue, PriorityQueue)
        assert queue.dequeue() == 5

    def test_missing_items_gives_an_empty_structure(self) -> None:
        """items may be left out."""
        assert len(build({"type": "Stack"})) == 0


class TestTrees:
    """Keyed trees from items, general trees from root."""

    def test_keyed_tree_inserts_items(self) -> None:
        """Each item is inserted; the tree balances itself."""
        tree = build({"type": "AVLTree", "items": [1, 2, 3]})
        assert isinstance(tree, AVLTree)
        assert tree.root is not None and tree.root.data == 2

    def test_btree_options(self) -> None:
        """The minimum degree of a B-tree is an option."""
        tree = build({"type": "BTree", "items": [1, 2, 3], "options": {"t": 2}})
        assert isinstance(tree, BTree)
        assert tree.t == 2

    def test_general_tree(self) -> None:
        """root is a nested data/children object."""
        tree = build(
            {
                "type": "Tree",
                "root": {
                    "data": "r",
                    "children": [
                        {"data": "a", "children": [{"data": "c"}]},
                        {"data": "b"},
                    ],
                },
            }
        )
        assert isinstance(tree, Tree)
        assert to_text(tree) == "r\n├── a\n│   └── c\n└── b"

    def test_general_tree_without_root_is_empty(self) -> None:
        """A missing or null root gives an empty tree."""
        assert build({"type": "Tree"}).is_empty()
        assert build({"type": "Tree", "root": None}).is_empty()


class TestGraphs:
    """Nodes by id, edges as lists of ids, edge class from the graph."""

    @pytest.mark.parametrize(
        "name, edge_cls",
        [
            ("Graph", Edge),
            ("DirectedGraph", DirectedEdge),
            ("WeightedGraph", WeightedEdge),
            ("WeightedDirectedGraph", WeightedDirectedEdge),
        ],
    )
    def test_edge_class_follows_the_graph(self, name: str, edge_cls: type) -> None:
        """Each graph class gets the edge class it accepts."""
        graph = build(
            {"type": name, "nodes": [{"id": "a"}, {"id": "b"}], "edges": [["a", "b"]]}
        )
        (edge,) = graph.edges()
        assert type(edge) is edge_cls

    def test_weights(self) -> None:
        """A third element is the weight."""
        graph = build(
            {
                "type": "WeightedDirectedGraph",
                "nodes": [{"id": "a"}, {"id": "b"}],
                "edges": [["a", "b", 2.5]],
            }
        )
        assert isinstance(graph, WeightedDirectedGraph)
        (edge,) = graph.edges()
        assert edge.weight == 2.5

    def test_weighted_edge_without_weight_takes_the_default(self) -> None:
        """A weighted graph accepts [source, target]."""
        graph = build(
            {
                "type": "WeightedGraph",
                "nodes": [{"id": "a"}, {"id": "b"}],
                "edges": [["a", "b"]],
            }
        )
        assert isinstance(graph, WeightedGraph)
        (edge,) = graph.edges()
        assert edge.weight == 1.0

    def test_data_defaults_to_the_id(self) -> None:
        """A node without data shows its id."""
        graph = build(
            {"type": "Graph", "nodes": [{"id": "a"}, {"id": "b", "data": "B"}]}
        )
        assert [node.data for node in graph.nodes()] == ["a", "B"]

    def test_integer_ids(self) -> None:
        """Integer ids, frequent in YAML, become strings."""
        graph = build(
            {
                "type": "DirectedGraph",
                "nodes": [{"id": 1}, {"id": 2}],
                "edges": [[1, 2]],
            }
        )
        assert isinstance(graph, DirectedGraph)
        assert [node.id for node in graph.nodes()] == ["1", "2"]

    def test_graph_options(self) -> None:
        """Constructor options such as max_nodes apply."""
        graph = build({"type": "AdjacencyMatrixGraph", "options": {"max_nodes": 3}})
        assert isinstance(graph, AdjacencyMatrixGraph)

    def test_empty_graph(self) -> None:
        """nodes and edges may be left out."""
        graph = build({"type": "Graph"})
        assert isinstance(graph, Graph)
        assert list(graph.nodes()) == []


class TestSupported:
    """The list of supported types."""

    def test_every_supported_type_builds_empty(self) -> None:
        """A document with type alone builds each supported class."""
        for name in SUPPORTED:
            assert type(build({"type": name})).__name__ == name

    def test_sorted_without_case(self) -> None:
        """SUPPORTED is in case-insensitive alphabetical order."""
        assert list(SUPPORTED) == sorted(SUPPORTED, key=str.lower)


class TestErrors:
    """Malformed documents name the place of the problem."""

    @pytest.mark.parametrize(
        "document, message",
        [
            ([1, 2], "expected an object with a 'type' key"),
            ({"items": []}, "'type' must name a structure class"),
            ({"type": "Stack", "options": []}, "options: expected an object"),
            ({"type": "Stack", "items": 3}, "items: expected a list"),
            ({"type": "Stack", "item": [1]}, "unknown key 'item' for Stack"),
            ({"type": "BTree", "items": "abc"}, "items: expected a list"),
            ({"type": "Tree", "options": {"x": 1}}, "Tree takes no options"),
            ({"type": "Tree", "root": "r"}, "root: expected an object"),
            ({"type": "Tree", "root": {"children": []}}, "root: missing 'data'"),
            (
                {"type": "Tree", "root": {"data": 1, "kids": []}},
                "root: unknown key 'kids'",
            ),
            (
                {
                    "type": "Tree",
                    "root": {"data": 1, "children": [{"data": 2, "children": 3}]},
                },
                r"root.children\[0\]: expected a list",
            ),
            ({"type": "Graph", "nodes": [{"data": 1}]}, r"nodes\[0\]: missing 'id'"),
            ({"type": "Graph", "nodes": [{"id": 1.5}]}, r"nodes\[0\]: a node id is"),
            ({"type": "Graph", "nodes": [{"id": True}]}, r"nodes\[0\]: a node id is"),
            (
                {"type": "Graph", "nodes": [{"id": "a", "label": "x"}]},
                r"nodes\[0\]: unknown key 'label'",
            ),
            ({"type": "Graph", "nodes": ["a"]}, r"nodes\[0\]: expected an object"),
            ({"type": "Graph", "edges": [["a", "b"]]}, r"edges\[0\]: unknown node 'a'"),
            ({"type": "Graph", "edges": ["ab"]}, r"edges\[0\]: expected \[source"),
            ({"type": "Graph", "edges": [["a"]]}, r"edges\[0\]: expected \[source"),
        ],
    )
    def test_malformed(self, document: Any, message: str) -> None:
        """Each malformed document raises InvalidParameterError."""
        with pytest.raises(InvalidParameterError, match=message):
            build(document)

    def test_weight_on_an_unweighted_graph(self) -> None:
        """An unweighted graph rejects a weight."""
        document: Dict[str, Any] = {
            "type": "DirectedGraph",
            "nodes": [{"id": "a"}, {"id": "b"}],
            "edges": [["a", "b", 2]],
        }
        with pytest.raises(
            InvalidParameterError, match="DirectedGraph is not weighted"
        ):
            build(document)

    def test_weight_must_be_a_number(self) -> None:
        """A weight is an int or a float, not a string or a bool."""
        for weight in ("2", True):
            document = {
                "type": "WeightedGraph",
                "nodes": [{"id": "a"}, {"id": "b"}],
                "edges": [["a", "b", weight]],
            }
            with pytest.raises(
                InvalidParameterError, match="the weight must be a number"
            ):
                build(document)

    def test_structure_errors_are_located(self) -> None:
        """An error raised by the structure is prefixed with its place."""
        document = {"type": "Graph", "nodes": [{"id": "a"}, {"id": "a"}]}
        with pytest.raises(
            InvalidParameterError, match=r"nodes\[1\]: Node a already exists"
        ):
            build(document)

    def test_self_loop(self) -> None:
        """The edge's own rejection of a self-loop is located."""
        document = {"type": "Graph", "nodes": [{"id": "a"}], "edges": [["a", "a"]]}
        with pytest.raises(InvalidParameterError, match=r"edges\[0\]: Self-loops"):
            build(document)

    def test_incomparable_items(self) -> None:
        """Items a search tree cannot compare are reported, not raised raw."""
        with pytest.raises(
            InvalidParameterError, match=r"items\[1\]: '<' not supported"
        ):
            build({"type": "BinarySearchTree", "items": [1, "a"]})

    def test_incomparable_linear_items(self) -> None:
        """from_list() errors are located at items."""
        with pytest.raises(InvalidParameterError, match="items: "):
            build({"type": "PriorityQueue", "items": [1, "a"]})

    def test_bad_option_name(self) -> None:
        """An option the constructor does not take is reported."""
        with pytest.raises(
            InvalidParameterError,
            match=r"^options: BTree\(\) got an unexpected keyword argument 'degree'",
        ):
            build({"type": "BTree", "options": {"degree": 2}})

    def test_bad_option_name_of_a_linear_structure(self) -> None:
        """from_list() builds linear structures; options keep their place."""
        with pytest.raises(
            InvalidParameterError,
            match=r"^options: Stack\(\) got an unexpected keyword argument 'bogus'",
        ):
            build({"type": "Stack", "items": [1], "options": {"bogus": 1}})

    def test_option_of_the_wrong_type(self) -> None:
        """A TypeError raised by the constructor is reported at options."""
        with pytest.raises(InvalidParameterError, match="^options: '<' not supported"):
            build({"type": "BTree", "options": {"t": "x"}})

    def test_bad_option_value_keeps_the_structure_error(self) -> None:
        """A value the constructor rejects raises the constructor's error."""
        with pytest.raises(InvalidParameterError, match="t"):
            build({"type": "BTree", "options": {"t": 1}})

    def test_unsupported_type(self) -> None:
        """An unknown type lists the supported ones."""
        with pytest.raises(
            StructureTypeError,
            match="unsupported type 'MinHeap': use one of AdjacencyListGraph",
        ):
            build({"type": "MinHeap"})
