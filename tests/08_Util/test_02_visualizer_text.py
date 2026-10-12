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

"""Tests for the plain-text rendering of the visualiser (#65)."""

from typing import Any, Type

import pytest

from sds.core.exceptions import StructureTypeError
from sds.linear import (
    CircularLinkedList,
    Deque,
    DoublyLinkedList,
    LinkedList,
    PriorityQueue,
    Queue,
    Stack,
)
from sds.tree import AVLTree, BinarySearchTree, BTree, MinHeap, RedBlackTree, Tree
from sds.utils.visualizer import to_text


class TestLinearText:
    """to_text() on linear structures."""

    @pytest.mark.parametrize(
        "cls, expected",
        [
            (LinkedList, "1 -> 2 -> 3"),
            (DoublyLinkedList, "1 <-> 2 <-> 3"),
            (CircularLinkedList, "1 -> 2 -> 3 -> (1)"),
        ],
    )
    def test_lists(self, cls: Type[Any], expected: str) -> None:
        """Lists render as a chain; circular lists loop back to the head."""
        structure = cls()
        for item in (1, 2, 3):
            structure.append(item)
        assert to_text(structure) == expected

    def test_stack_names_its_top(self) -> None:
        """A stack iterates from its top, which is named."""
        stack = Stack()
        for item in (1, 2, 3):
            stack.push(item)
        assert to_text(stack) == "top: 3 -> 2 -> 1"

    def test_queue_names_both_ends(self) -> None:
        """A queue names its front and rear."""
        queue = Queue()
        for item in (1, 2, 3):
            queue.enqueue(item)
        assert to_text(queue) == "front: 1 -> 2 -> 3 :rear"

    def test_deque_names_both_ends(self) -> None:
        """A deque names its front and rear."""
        deque = Deque()
        deque.add_rear(1)
        deque.add_rear(2)
        deque.add_front(0)
        assert to_text(deque) == "front: 0 -> 1 -> 2 :rear"

    def test_priority_queue_in_priority_order(self) -> None:
        """A priority queue renders in its iteration (priority) order."""
        queue = PriorityQueue()
        for item in (3, 1, 2):
            queue.enqueue(item)
        assert to_text(queue) == "1 -> 2 -> 3"

    @pytest.mark.parametrize("cls", [LinkedList, Stack, Queue])
    def test_empty(self, cls: Type[Any]) -> None:
        """An empty structure renders as (empty)."""
        assert to_text(cls()) == "(empty)"

    def test_label_receives_items(self) -> None:
        """For linear structures the label function receives each item."""
        structure = LinkedList()
        for item in (1, 2):
            structure.append(item)
        assert to_text(structure, label=lambda item: f"<{item}>") == "<1> -> <2>"


class TestBinaryTreeText:
    """to_text() on binary trees."""

    def test_bst(self, bst: BinarySearchTree) -> None:
        """Children are tagged L/R, last child drawn with a corner."""
        assert to_text(bst) == (
            "50\n" "├── L: 30\n" "│   ├── L: 20\n" "│   └── R: 40\n" "└── R: 70"
        )

    def test_single_child_keeps_its_side(self) -> None:
        """A lone child still says which side it is on."""
        tree = BinarySearchTree()
        for key in (5, 7, 6):
            tree.insert(key)
        assert to_text(tree) == "5\n└── R: 7\n    └── L: 6"

    def test_red_black_hides_sentinels(self) -> None:
        """The NIL sentinel of a red-black tree is never rendered."""
        tree = RedBlackTree()
        for key in (1, 2, 3, 4):
            tree.insert(key)
        text = to_text(tree, label=lambda node: f"{node.data} {node.color}")
        assert text == (
            "2 BLACK\n" "├── L: 1 BLACK\n" "└── R: 3 BLACK\n" "    └── R: 4 RED"
        )

    def test_avl(self) -> None:
        """AVL trees render through the same interface."""
        tree = AVLTree()
        for key in (1, 2, 3):
            tree.insert(key)
        assert to_text(tree) == "2\n├── L: 1\n└── R: 3"

    def test_empty(self) -> None:
        """An empty tree renders as (empty)."""
        assert to_text(BinarySearchTree()) == "(empty)"


class TestGeneralTreeText:
    """to_text() on general trees."""

    def test_tree(self, general_tree: Tree) -> None:
        """Children appear in insertion order, without sides."""
        assert to_text(general_tree) == "r\n├── a\n│   └── c\n└── b"

    def test_empty(self) -> None:
        """A tree without root renders as (empty)."""
        assert to_text(Tree()) == "(empty)"


class TestBTreeText:
    """to_text() on B-trees."""

    def test_btree(self, btree: BTree) -> None:
        """Each node shows its keys separated by bars."""
        assert to_text(btree) == (
            "[4]\n"
            "├── [2]\n"
            "│   ├── [1]\n"
            "│   └── [3]\n"
            "└── [6 | 8]\n"
            "    ├── [5]\n"
            "    ├── [7]\n"
            "    └── [9 | 10]"
        )

    def test_label_receives_keys(self, btree: BTree) -> None:
        """For B-trees the label function receives each key."""
        first_line = to_text(btree, label=lambda key: f"k{key}").splitlines()[0]
        assert first_line == "[k4]"

    def test_empty(self) -> None:
        """An empty B-tree renders as (empty)."""
        assert to_text(BTree(2)) == "(empty)"


class TestGraphText:
    """to_text() on graphs."""

    def test_weighted_directed(self, weighted_digraph: Any) -> None:
        """Successors in edge order, weights in parentheses."""
        assert to_text(weighted_digraph) == (
            "A -> B (4.0), C (1.0)\n" "B -> D (1.0)\n" "C -> B (2.0)\n" "D"
        )

    def test_undirected_lists_both_ends(self, undirected: Any) -> None:
        """An undirected edge appears at both ends; an isolated node alone."""
        assert to_text(undirected) == "A -- B\nB -- A, C\nC -- B\nD"

    def test_weighted_undirected(self, weighted_undirected: Any) -> None:
        """Weights of undirected edges appear at both ends."""
        assert to_text(weighted_undirected) == "A -- B (2.5)\nB -- A (2.5)"

    def test_label_receives_nodes(self, digraph: Any) -> None:
        """For graphs the label function receives the node."""
        assert to_text(digraph, label=lambda node: node.id) == "n1 -> n2\nn2 -> n1"

    def test_empty(self) -> None:
        """An empty graph renders as (empty)."""
        from sds.graph import Graph

        assert to_text(Graph()) == "(empty)"


class TestUnsupported:
    """Structures outside the visualiser's scope."""

    @pytest.mark.parametrize("structure", [MinHeap(), [1, 2], 42])
    def test_unsupported_structure(self, structure: Any) -> None:
        """Anything unsupported raises StructureTypeError, a TypeError."""
        with pytest.raises(StructureTypeError, match="does not support"):
            to_text(structure)
        with pytest.raises(TypeError):
            to_text(structure)
