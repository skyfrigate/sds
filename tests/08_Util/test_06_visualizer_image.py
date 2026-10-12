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

"""Tests for the image output of the visualiser (#65)."""

import sys
from pathlib import Path
from typing import Any

import pytest

from sds.core.exceptions import InvalidParameterError, StructureTypeError
from sds.linear import CircularLinkedList, Stack
from sds.tree import BinarySearchTree, MinHeap
from sds.utils import OptionalDependencyError
from sds.utils.visualizer import save_image
from sds.utils.visualizer._image import label_position

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


class TestMissingExtra:
    """save_image() without matplotlib."""

    def test_names_the_image_extra(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, bst: Any
    ) -> None:
        """Without matplotlib, the error names the image extra."""
        monkeypatch.setitem(sys.modules, "matplotlib", None)
        monkeypatch.delitem(sys.modules, "matplotlib.figure", raising=False)
        with pytest.raises(OptionalDependencyError, match=r"pysds-tools\[image\]"):
            save_image(bst, tmp_path / "tree.png")
        assert not (tmp_path / "tree.png").exists()


class TestLabelPosition:
    """Placement of edge labels (pure geometry)."""

    def test_straight_edge(self) -> None:
        """On a straight edge, the label sits at 40 % from the start."""
        assert label_position(0.0, 0.0, 10.0, 0.0, 0.0) == (4.0, 0.0)

    def test_bent_edge_moves_off_the_chord(self) -> None:
        """On a bent edge, the label leaves the chord."""
        _, y = label_position(0.0, 0.0, 10.0, 0.0, 0.2)
        assert y != 0.0


class TestSaveImage:
    """save_image() with matplotlib installed."""

    @pytest.fixture(autouse=True)
    def _needs_matplotlib(self) -> None:
        pytest.importorskip("matplotlib")

    @pytest.mark.parametrize(
        "fixture", ["bst", "general_tree", "btree", "weighted_digraph", "undirected"]
    )
    def test_png(self, fixture: str, request: Any, tmp_path: Path) -> None:
        """Trees and graphs are written as PNG files."""
        path = tmp_path / "out.png"
        save_image(request.getfixturevalue(fixture), path)
        assert path.read_bytes().startswith(PNG_SIGNATURE)

    def test_linear_and_markers(self, tmp_path: Path) -> None:
        """A stack, with its top marker, is written."""
        stack = Stack()
        for item in (1, 2, 3):
            stack.push(item)
        save_image(stack, tmp_path / "stack.png")
        assert (tmp_path / "stack.png").stat().st_size > 0

    def test_circular_list(self, tmp_path: Path) -> None:
        """The bent back edge of a circular list draws."""
        structure = CircularLinkedList()
        for item in (1, 2, 3):
            structure.append(item)
        save_image(structure, str(tmp_path / "circular.png"))
        assert (tmp_path / "circular.png").exists()

    def test_self_loop(self, tmp_path: Path, nodes: Any) -> None:
        """A self-loop is drawn as a loop mark next to its node."""
        from sds.graph import Graph
        from sds.graph.edge import Edge

        graph = Graph()
        graph.add_node(nodes[0])
        graph.add_edge(Edge(nodes[0], nodes[0], allow_self_loop=True))
        save_image(graph, tmp_path / "loop.png")
        assert (tmp_path / "loop.png").read_bytes().startswith(PNG_SIGNATURE)

    def test_format_from_extension(self, tmp_path: Path, bst: Any) -> None:
        """The extension selects the format."""
        save_image(bst, tmp_path / "tree.svg")
        assert (tmp_path / "tree.svg").read_text().lstrip().startswith("<?xml")

    def test_label(self, tmp_path: Path, bst: Any) -> None:
        """A label function is accepted."""
        save_image(bst, tmp_path / "tree.png", label=lambda node: f"k={node.data}")
        assert (tmp_path / "tree.png").exists()

    def test_empty_structure(self, tmp_path: Path) -> None:
        """An empty structure gives an empty but valid image."""
        save_image(BinarySearchTree(), tmp_path / "empty.png")
        assert (tmp_path / "empty.png").read_bytes().startswith(PNG_SIGNATURE)

    @pytest.mark.parametrize("name", ["tree.xyz", "tree"])
    def test_unknown_format(self, name: str, tmp_path: Path, bst: Any) -> None:
        """An unknown or missing extension raises InvalidParameterError."""
        with pytest.raises(InvalidParameterError, match="use one of"):
            save_image(bst, tmp_path / name)

    def test_unsupported_structure(self, tmp_path: Path) -> None:
        """Unsupported structures raise StructureTypeError."""
        with pytest.raises(StructureTypeError):
            save_image(MinHeap(), tmp_path / "heap.png")
