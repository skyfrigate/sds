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

"""Plain-text rendering of the visualiser views."""

from typing import List

from ._views import ChainView, GraphView, TreeItem, TreeView, View, neighbours

EMPTY = "(empty)"


def chain_text(view: ChainView) -> str:
    """Render a chain on one line: ``top: 3 -> 2 -> 1``."""
    if not view.items:
        return EMPTY
    text = f" {view.link} ".join(view.items)
    if view.circular:
        text += f" {view.link} ({view.items[0]})"
    if view.head is not None:
        text = f"{view.head}: {text}"
    if view.tail is not None:
        text = f"{text} :{view.tail}"
    return text


def tree_text(view: TreeView) -> str:
    """Render a tree with box-drawing branches, one node per line."""
    if view.root is None:
        return EMPTY
    lines = [view.root.label]

    def visit(item: TreeItem, prefix: str) -> None:
        for index, (side, child) in enumerate(item.children):
            last = index == len(item.children) - 1
            tag = f"{side}: " if side is not None else ""
            lines.append(f"{prefix}{'└── ' if last else '├── '}{tag}{child.label}")
            visit(child, prefix + ("    " if last else "│   "))

    visit(view.root, "")
    return "\n".join(lines)


def graph_text(view: GraphView) -> str:
    """Render a graph as an adjacency list, one node per line."""
    if not view.nodes:
        return EMPTY
    labels = dict(view.nodes)
    arrow = "->" if view.directed else "--"
    lines: List[str] = []
    for node_id, adjacent in neighbours(view).items():
        targets = ", ".join(
            labels[other] if weight is None else f"{labels[other]} ({weight})"
            for other, weight in adjacent
        )
        lines.append(
            f"{labels[node_id]} {arrow} {targets}" if targets else labels[node_id]
        )
    return "\n".join(lines)


def view_text(view: View) -> str:
    """Render any view as plain text."""
    if isinstance(view, ChainView):
        return chain_text(view)
    if isinstance(view, TreeView):
        return tree_text(view)
    return graph_text(view)
