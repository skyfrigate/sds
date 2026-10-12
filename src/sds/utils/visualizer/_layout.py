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

"""Node placement for the image output of the visualiser.

matplotlib draws but computes no layout (#102), so the visualiser places
nodes itself. Every layout here is a direct, deterministic placement,
with no search or optimisation (which would belong to ``sds.algorithms``
under #99):

- chain: one row, left to right;
- binary tree: x is the in-order rank, y the depth, so no two nodes
  overlap;
- other trees: leaves left to right, each parent centred over its
  children;
- graph: a circle, in ``nodes()`` order, starting at the top and turning
  clockwise.

This module is pure Python; it is tested without matplotlib.
"""

import math
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from ._views import ChainView, GraphView, TreeItem, TreeView, View


@dataclass(frozen=True, slots=True)
class PlacedNode:
    """A node to draw: its text and centre. Markers are drawn unboxed."""

    label: str
    x: float
    y: float
    marker: bool = False


@dataclass(frozen=True, slots=True)
class PlacedEdge:
    """A link between two placed nodes, by index."""

    start: int
    end: int
    label: Optional[str] = None
    arrow: str = "-"  # matplotlib arrow style: "-", "-|>" or "<|-|>"
    bend: float = 0.0  # arc3 radius; 0 for a straight line


@dataclass(slots=True)
class Drawing:
    """Placed nodes and edges, ready for a renderer."""

    nodes: List[PlacedNode] = field(default_factory=list)
    edges: List[PlacedEdge] = field(default_factory=list)

    def bounds(self) -> Tuple[float, float, float, float]:
        """Return ``(xmin, xmax, ymin, ymax)`` over all nodes."""
        xs = [node.x for node in self.nodes] or [0.0]
        ys = [node.y for node in self.nodes] or [0.0]
        return min(xs), max(xs), min(ys), max(ys)


#: Horizontal and vertical spacing between tree and chain nodes.
STEP_X = 1.0
STEP_Y = 1.0


def chain_layout(view: ChainView) -> Drawing:
    """Place a chain on one row; named ends sit above their end node."""
    drawing = Drawing()
    for index, item in enumerate(view.items):
        drawing.nodes.append(PlacedNode(item, index * STEP_X, 0.0))
    arrow = "<|-|>" if view.link == "<->" else "-|>"
    for index in range(len(view.items) - 1):
        drawing.edges.append(PlacedEdge(index, index + 1, arrow=arrow))
    count = len(view.items)
    if count and view.circular:
        drawing.edges.append(PlacedEdge(count - 1, 0, arrow=arrow, bend=0.3))
    if count and view.head is not None:
        drawing.nodes.append(PlacedNode(view.head, 0.0, 0.6 * STEP_Y, marker=True))
    if count and view.tail is not None:
        drawing.nodes.append(
            PlacedNode(view.tail, (count - 1) * STEP_X, 0.6 * STEP_Y, marker=True)
        )
    return drawing


def tree_layout(view: TreeView) -> Drawing:
    """Place a tree top-down, root at y = 0 and one level per STEP_Y."""
    drawing = Drawing()
    if view.root is None:
        return drawing
    next_x = [0.0]

    def place(item: TreeItem, depth: int) -> int:
        """Place ``item`` and its subtree; return the index of ``item``."""
        index = len(drawing.nodes)
        drawing.nodes.append(PlacedNode(item.label, 0.0, 0.0))  # fixed below
        children: List[Tuple[Optional[str], int]] = []
        if view.binary:
            # In-order: left subtree, node, right subtree.
            for side, child in item.children:
                if side == "L":
                    children.append((side, place(child, depth + 1)))
            x = next_x[0]
            next_x[0] += STEP_X
            for side, child in item.children:
                if side == "R":
                    children.append((side, place(child, depth + 1)))
        else:
            children = [
                (side, place(child, depth + 1)) for side, child in item.children
            ]
            if children:
                first = drawing.nodes[children[0][1]].x
                last = drawing.nodes[children[-1][1]].x
                x = (first + last) / 2
            else:
                x = next_x[0]
                next_x[0] += STEP_X
        drawing.nodes[index] = PlacedNode(item.label, x, -depth * STEP_Y)
        drawing.edges.extend(PlacedEdge(index, child) for _, child in children)
        return index

    place(view.root, 0)
    return drawing


def graph_layout(view: GraphView) -> Drawing:
    """Place a graph on a circle, in node order, clockwise from the top.

    Directed edges get arrow heads; when both ``a -> b`` and ``b -> a``
    exist, each is bent so the two do not overlap. A self-loop is kept in
    the edge list with ``start == end``; the renderer draws it apart.
    """
    drawing = Drawing()
    count = len(view.nodes)
    radius = max(1.0, count * 1.2 / (2 * math.pi))
    index_of = {}
    for position, (node_id, label) in enumerate(view.nodes):
        angle = math.pi / 2 - 2 * math.pi * position / max(count, 1)
        x = 0.0 if count == 1 else round(radius * math.cos(angle), 9)
        y = 0.0 if count == 1 else round(radius * math.sin(angle), 9)
        drawing.nodes.append(PlacedNode(label, x, y))
        index_of[node_id] = position
    pairs = {(first, second) for first, second, _ in view.edges}
    for first, second, weight in view.edges:
        reverse = view.directed and first != second and (second, first) in pairs
        drawing.edges.append(
            PlacedEdge(
                index_of[first],
                index_of[second],
                label=weight,
                arrow="-|>" if view.directed else "-",
                bend=0.2 if reverse else 0.0,
            )
        )
    return drawing


def layout(view: View) -> Drawing:
    """Place the nodes of any view."""
    if isinstance(view, ChainView):
        return chain_layout(view)
    if isinstance(view, TreeView):
        return tree_layout(view)
    return graph_layout(view)
