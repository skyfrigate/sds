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

"""Tests for the Mermaid rendering of the visualiser (#65).

The expected sources were checked with ``mermaid.parse`` (Mermaid 11).
"""

from typing import Any

import pytest

from sds.core.exceptions import StructureTypeError
from sds.graph import Graph
from sds.linear import CircularLinkedList, DoublyLinkedList, LinkedList, Queue, Stack
from sds.tree import BinarySearchTree, BTree, MinHeap, Tree
from sds.utils.visualizer import to_mermaid
from sds.utils.visualizer._mermaid import escape


class TestEscape:
    """Label escaping."""

    @pytest.mark.parametrize(
        "raw, escaped",
        [
            ("plain", "plain"),
            ('say "hi"', "say #quot;hi#quot;"),
            ("a|b", "a#124;b"),
            ("#1", "#35;1"),
            ("two\nlines", "two<br>lines"),
        ],
    )
    def test_escape(self, raw: str, escaped: str) -> None:
        """Quotes, pipes, hashes and newlines are escaped."""
        assert escape(raw) == escaped

    def test_label_with_quote_in_node(self) -> None:
        """A quote inside a label cannot close the node shape."""
        structure = LinkedList()
        structure.append('a"b')
        assert to_mermaid(structure) == 'flowchart LR\n    n0["a#quot;b"]'


class TestLinearMermaid:
    """to_mermaid() on linear structures."""

    def test_linked_list(self) -> None:
        """A chain of nodes, left to right."""
        structure = LinkedList()
        for item in (1, 2, 3):
            structure.append(item)
        assert to_mermaid(structure) == (
            "flowchart LR\n"
            '    n0["1"]\n'
            '    n1["2"]\n'
            '    n2["3"]\n'
            "    n0 --> n1\n"
            "    n1 --> n2"
        )

    def test_doubly_linked_list(self) -> None:
        """Doubly linked lists use two-way links."""
        structure = DoublyLinkedList()
        for item in (1, 2):
            structure.append(item)
        assert to_mermaid(structure).endswith("    n0 <--> n1")

    def test_circular_list_loops_back(self) -> None:
        """The last node links back to the first."""
        structure = CircularLinkedList()
        for item in (1, 2):
            structure.append(item)
        assert to_mermaid(structure).endswith("    n0 --> n1\n    n1 --> n0")

    def test_stack_top(self) -> None:
        """The top of a stack is a rounded node linked to the first item."""
        stack = Stack()
        for item in (1, 2):
            stack.push(item)
        assert to_mermaid(stack).endswith('    head(["top"]) --- n0')

    def test_queue_ends(self) -> None:
        """A queue gets front and rear nodes."""
        queue = Queue()
        for item in (1, 2):
            queue.enqueue(item)
        lines = to_mermaid(queue).splitlines()
        assert lines[-2:] == ['    head(["front"]) --- n0', '    n1 --- tail(["rear"])']

    def test_empty(self) -> None:
        """An empty structure gives the flowchart line alone, ends included."""
        assert to_mermaid(Stack()) == "flowchart LR"


class TestTreeMermaid:
    """to_mermaid() on trees."""

    def test_bst(self, bst: BinarySearchTree) -> None:
        """Nodes in preorder, binary children tagged L/R."""
        assert to_mermaid(bst) == (
            "flowchart TD\n"
            '    n0["50"]\n'
            '    n1["30"]\n'
            '    n2["20"]\n'
            "    n1 -->|L| n2\n"
            '    n3["40"]\n'
            "    n1 -->|R| n3\n"
            "    n0 -->|L| n1\n"
            '    n4["70"]\n'
            "    n0 -->|R| n4"
        )

    def test_general_tree(self, general_tree: Tree) -> None:
        """General-tree children carry no side label."""
        assert to_mermaid(general_tree) == (
            "flowchart TD\n"
            '    n0["r"]\n'
            '    n1["a"]\n'
            '    n2["c"]\n'
            "    n1 --> n2\n"
            "    n0 --> n1\n"
            '    n3["b"]\n'
            "    n0 --> n3"
        )

    def test_btree_nodes_show_keys(self, btree: BTree) -> None:
        """B-tree nodes show their keys."""
        lines = to_mermaid(btree).splitlines()
        assert lines[1] == '    n0["[4]"]'
        assert '    n4["[6 #124; 8]"]' in lines

    def test_empty(self) -> None:
        """An empty tree gives the flowchart line alone."""
        assert to_mermaid(BinarySearchTree()) == "flowchart TD"


class TestGraphMermaid:
    """to_mermaid() on graphs."""

    def test_weighted_directed(self, weighted_digraph: Any) -> None:
        """Nodes first, then edges with their weights."""
        assert to_mermaid(weighted_digraph) == (
            "flowchart LR\n"
            '    n0["A"]\n'
            '    n1["B"]\n'
            '    n2["C"]\n'
            '    n3["D"]\n'
            "    n0 -->|4.0| n1\n"
            "    n0 -->|1.0| n2\n"
            "    n2 -->|2.0| n1\n"
            "    n1 -->|1.0| n3"
        )

    def test_undirected(self, undirected: Any) -> None:
        """Undirected edges are drawn without arrow heads, once each."""
        lines = to_mermaid(undirected).splitlines()
        assert lines[-2:] == ["    n0 --- n1", "    n1 --- n2"]

    def test_weighted_undirected(self, weighted_undirected: Any) -> None:
        """Undirected weights are edge labels too."""
        assert to_mermaid(weighted_undirected).endswith("    n0 ---|2.5| n1")

    def test_empty(self) -> None:
        """An empty graph gives the flowchart line alone."""
        assert to_mermaid(Graph()) == "flowchart LR"


class TestUnsupported:
    """Structures outside the visualiser's scope."""

    def test_unsupported_structure(self) -> None:
        """Unsupported structures raise StructureTypeError."""
        with pytest.raises(StructureTypeError):
            to_mermaid(MinHeap())
