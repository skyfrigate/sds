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

"""Tests for render(), the format dispatcher of the visualiser (#65)."""

from typing import Any

import pytest

from sds.core.exceptions import InvalidParameterError, StructureTypeError
from sds.utils.visualizer import FORMATS, render, to_dot, to_mermaid, to_text


class TestRender:
    """render()."""

    def test_formats(self) -> None:
        """The three text formats, in this order."""
        assert FORMATS == ("text", "mermaid", "dot")

    def test_default_is_text(self, bst: Any) -> None:
        """Without a format, render() gives text."""
        assert render(bst) == to_text(bst)

    @pytest.mark.parametrize(
        "fmt, function", [("text", to_text), ("mermaid", to_mermaid), ("dot", to_dot)]
    )
    def test_dispatch(self, fmt: str, function: Any, weighted_digraph: Any) -> None:
        """Each format gives the output of its function."""
        assert render(weighted_digraph, fmt) == function(weighted_digraph)

    def test_label_is_passed_on(self, digraph: Any) -> None:
        """The label function reaches the renderer."""
        assert render(digraph, "text", label=lambda node: node.id).startswith("n1")

    @pytest.mark.parametrize("fmt", ["svg", "TEXT", ""])
    def test_unknown_format(self, fmt: str, bst: Any) -> None:
        """An unknown format raises InvalidParameterError, a ValueError."""
        with pytest.raises(InvalidParameterError, match="use one of text"):
            render(bst, fmt)
        with pytest.raises(ValueError):
            render(bst, fmt)

    def test_dot_on_a_tree(self, bst: Any) -> None:
        """DOT on a tree raises StructureTypeError."""
        with pytest.raises(StructureTypeError, match="graphs only"):
            render(bst, "dot")
