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

"""Tests for the DOT rendering of the visualiser (#65)."""

import shutil
import subprocess
from typing import Any

import pytest

from sds.core.exceptions import StructureTypeError
from sds.graph import Graph, GraphNode, WeightedEdge, WeightedGraph
from sds.linear import LinkedList
from sds.tree import BinarySearchTree, MinHeap
from sds.utils.visualizer import to_dot
from sds.utils.visualizer._dot import quote


class TestQuote:
    """DOT string quoting."""

    @pytest.mark.parametrize(
        "raw, quoted",
        [
            ("A", '"A"'),
            ('say "hi"', '"say \\"hi\\""'),
            ("back\\slash", '"back\\\\slash"'),
            ("two\nlines", '"two\\nlines"'),
        ],
    )
    def test_quote(self, raw: str, quoted: str) -> None:
        """Quotes, backslashes and newlines are escaped."""
        assert quote(raw) == quoted


class TestGraphDot:
    """to_dot() on graphs."""

    def test_weighted_directed(self, weighted_digraph: Any) -> None:
        """A digraph, nodes by id, weights as edge labels."""
        assert to_dot(weighted_digraph) == (
            "digraph {\n"
            '    "n1" [label="A"];\n'
            '    "n2" [label="B"];\n'
            '    "n3" [label="C"];\n'
            '    "n4" [label="D"];\n'
            '    "n1" -> "n2" [label="4.0"];\n'
            '    "n1" -> "n3" [label="1.0"];\n'
            '    "n3" -> "n2" [label="2.0"];\n'
            '    "n2" -> "n4" [label="1.0"];\n'
            "}"
        )

    def test_undirected(self, undirected: Any) -> None:
        """An undirected graph uses graph and --, each edge once."""
        lines = to_dot(undirected).splitlines()
        assert lines[0] == "graph {"
        assert lines[-3:] == ['    "n1" -- "n2";', '    "n2" -- "n3";', "}"]

    def test_label(self, digraph: Any) -> None:
        """The label function sets the node labels, not the ids."""
        lines = to_dot(digraph, label=lambda node: f"node {node.id}").splitlines()
        assert lines[1] == '    "n1" [label="node n1"];'

    def test_empty(self) -> None:
        """An empty graph is an empty graph block."""
        assert to_dot(Graph()) == "graph {\n}"

    @pytest.mark.skipif(shutil.which("dot") is None, reason="Graphviz not installed")
    def test_accepted_by_graphviz(self) -> None:
        """Graphviz parses the output, awkward ids and labels included."""
        graph = WeightedGraph()
        first = GraphNode('a "quoted"\\ label\non two lines', "id with spaces")
        second = GraphNode("B", "n2")
        graph.add_node(first)
        graph.add_node(second)
        graph.add_edge(WeightedEdge(first, second, 2.5))
        result = subprocess.run(
            ["dot", "-Tsvg"],
            input=to_dot(graph),
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr


class TestNotAGraph:
    """DOT is offered for graphs only."""

    @pytest.mark.parametrize("structure", [LinkedList(), BinarySearchTree()])
    def test_supported_non_graph(self, structure: Any) -> None:
        """A linear structure or a tree raises StructureTypeError."""
        with pytest.raises(StructureTypeError, match="graphs only"):
            to_dot(structure)

    def test_unsupported_structure(self) -> None:
        """An unsupported structure raises StructureTypeError."""
        with pytest.raises(StructureTypeError, match="does not support"):
            to_dot(MinHeap())
