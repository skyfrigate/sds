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

"""Format-neutral views of the structures the visualiser renders.

Each supported structure is turned once into one of three views, built
from its public accessors only (#102): a chain for linear structures, a
rooted tree, or a node-and-edge graph. Every output format then renders a
view, so the per-structure logic lives in this module alone and each
format handles three shapes, not one per class.

Dispatch is on the abstract interfaces (``LinearCollection``,
``AbstractBinaryTree``, ``AbstractGraph``), and on the concrete ``Tree``
and ``BTree`` classes, whose common interface ``AbstractTree`` exposes
neither a root nor children (#86).
"""

from dataclasses import dataclass, field
from functools import singledispatch
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from ...core.exceptions import StructureTypeError
from ...core.interfaces import LinearCollection
from ...graph.edge import DirectedEdge, Edge, WeightedDirectedEdge, WeightedEdge
from ...graph.interfaces import AbstractDirectedGraph, AbstractGraph
from ...graph.node import GraphNode
from ...linear.list import CircularLinkedList, DoublyLinkedList
from ...linear.queue import Deque, Queue
from ...linear.stack import Stack
from ...tree.btree import BTree
from ...tree.general import Tree
from ...tree.interfaces import AbstractBinaryTree
from ...tree.node import BTreeNode, TreeNode

#: User-supplied labelling function. It receives the node for trees and
#: graphs, the item for linear structures and the key for B-trees.
Label = Optional[Callable[[Any], str]]


@dataclass(frozen=True, slots=True)
class ChainView:
    """A linear structure: items in iteration order."""

    items: List[str]
    link: str = "->"
    circular: bool = False
    head: Optional[str] = None
    tail: Optional[str] = None


@dataclass(slots=True)
class TreeItem:
    """A tree node with its children, each tagged with an optional side."""

    label: str
    children: List[Tuple[Optional[str], "TreeItem"]] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class TreeView:
    """A rooted tree; ``binary`` marks children tagged ``L``/``R``."""

    root: Optional[TreeItem]
    binary: bool = False


@dataclass(frozen=True, slots=True)
class GraphView:
    """A graph: nodes as ``(id, label)``, edges as ``(id1, id2, weight)``."""

    nodes: List[Tuple[str, str]]
    edges: List[Tuple[str, str, Optional[str]]]
    directed: bool


View = Union[ChainView, TreeView, GraphView]


def _item_label(label: Label, item: Any) -> str:
    return label(item) if label is not None else str(item)


def _node_label(label: Label, node: Any) -> str:
    return label(node) if label is not None else str(node.data)


@singledispatch
def build_view(structure: Any, label: Label = None) -> View:
    """Return the view of ``structure``.

    Raises
    ------
    StructureTypeError
        If the visualiser does not support the structure.
    """
    raise StructureTypeError(
        f"The visualiser does not support {type(structure).__name__}"
    )


@build_view.register
def _(structure: LinearCollection, label: Label = None) -> View:
    items = [_item_label(label, item) for item in structure]
    if isinstance(structure, DoublyLinkedList):
        return ChainView(items, link="<->")
    if isinstance(structure, CircularLinkedList):
        return ChainView(items, circular=True)
    if isinstance(structure, Stack):
        return ChainView(items, head="top")
    if isinstance(structure, (Queue, Deque)):
        return ChainView(items, head="front", tail="rear")
    return ChainView(items)


@build_view.register
def _(structure: AbstractBinaryTree, label: Label = None) -> View:
    root = structure.root
    if root is None:
        return TreeView(None, binary=True)

    def visit(node: Any) -> TreeItem:
        item = TreeItem(_node_label(label, node))
        left, right = structure.children(node)
        for side, child in (("L", left), ("R", right)):
            if child is not None:
                item.children.append((side, visit(child)))
        return item

    return TreeView(visit(root), binary=True)


@build_view.register
def _(structure: Tree, label: Label = None) -> View:
    def visit(node: TreeNode) -> TreeItem:
        item = TreeItem(_node_label(label, node))
        item.children.extend((None, visit(child)) for child in node.children)
        return item

    root = structure.root
    return TreeView(None if root is None else visit(root))


@build_view.register
def _(structure: BTree, label: Label = None) -> View:
    def visit(node: BTreeNode) -> TreeItem:
        keys = " | ".join(_item_label(label, key) for key in node.keys)
        item = TreeItem(f"[{keys}]")
        item.children.extend((None, visit(child)) for child in node.children)
        return item

    root = structure.root
    if root is None or not root.keys:
        return TreeView(None)
    return TreeView(visit(root))


def _endpoints(edge: Edge) -> Tuple[GraphNode, GraphNode]:
    if isinstance(edge, DirectedEdge):
        return edge.source, edge.target
    return edge.node1, edge.node2


def _weight(edge: Edge) -> Optional[str]:
    if isinstance(edge, (WeightedEdge, WeightedDirectedEdge)):
        return str(edge.weight)
    return None


@build_view.register
def _(structure: AbstractGraph, label: Label = None) -> View:
    nodes = [(str(node.id), _node_label(label, node)) for node in structure.nodes()]
    edges: List[Tuple[str, str, Optional[str]]] = []
    for edge in structure.edges():
        first, second = _endpoints(edge)
        edges.append((str(first.id), str(second.id), _weight(edge)))
    return GraphView(nodes, edges, isinstance(structure, AbstractDirectedGraph))


def neighbours(view: GraphView) -> Dict[str, List[Tuple[str, Optional[str]]]]:
    """Adjacency of a graph view, in edge order, keyed by node id.

    Directed graphs list successors only; undirected graphs list each edge
    at both ends, a self-loop once.
    """
    adjacency: Dict[str, List[Tuple[str, Optional[str]]]] = {
        node_id: [] for node_id, _ in view.nodes
    }
    for first, second, weight in view.edges:
        adjacency[first].append((second, weight))
        if not view.directed and first != second:
            adjacency[second].append((first, weight))
    return adjacency
