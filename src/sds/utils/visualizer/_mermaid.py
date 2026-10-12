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

"""Mermaid rendering of the visualiser views.

The output is a ``flowchart`` the user guides can embed as is (#31).
Mermaid node ids are generated (``n0``, ``n1``...) because labels and
graph node ids may hold characters Mermaid rejects in an id; labels are
quoted and escaped.
"""

from typing import Dict, List

from ._views import ChainView, GraphView, TreeItem, TreeView, View

INDENT = "    "


def escape(text: str) -> str:
    """Escape a label for a quoted Mermaid node or an edge label."""
    return (
        text.replace("#", "#35;")
        .replace('"', "#quot;")
        .replace("|", "#124;")
        .replace("\n", "<br>")
    )


def _node(node_id: str, label: str) -> str:
    return f'{node_id}["{escape(label)}"]'


def chain_mermaid(view: ChainView) -> str:
    """Render a chain left to right; named ends become rounded nodes."""
    lines = ["flowchart LR"]
    ids = [f"n{index}" for index in range(len(view.items))]
    lines.extend(INDENT + _node(i, item) for i, item in zip(ids, view.items))
    arrow = "<-->" if view.link == "<->" else "-->"
    lines.extend(f"{INDENT}{a} {arrow} {b}" for a, b in zip(ids, ids[1:]))
    if ids and view.circular:
        lines.append(f"{INDENT}{ids[-1]} {arrow} {ids[0]}")
    if ids and view.head is not None:
        lines.append(f'{INDENT}head(["{escape(view.head)}"]) --- {ids[0]}')
    if ids and view.tail is not None:
        lines.append(f'{INDENT}{ids[-1]} --- tail(["{escape(view.tail)}"])')
    return "\n".join(lines)


def tree_mermaid(view: TreeView) -> str:
    """Render a tree top-down; binary children carry an L/R edge label."""
    lines = ["flowchart TD"]
    if view.root is None:
        return lines[0]
    counter = [0]

    def visit(item: TreeItem) -> str:
        node_id = f"n{counter[0]}"
        counter[0] += 1
        lines.append(INDENT + _node(node_id, item.label))
        for side, child in item.children:
            child_id = visit(child)
            link = f"-->|{side}|" if side is not None else "-->"
            lines.append(f"{INDENT}{node_id} {link} {child_id}")
        return node_id

    visit(view.root)
    return "\n".join(lines)


def graph_mermaid(view: GraphView) -> str:
    """Render a graph left to right; weights become edge labels."""
    lines: List[str] = ["flowchart LR"]
    ids: Dict[str, str] = {}
    for index, (node_id, label) in enumerate(view.nodes):
        ids[node_id] = f"n{index}"
        lines.append(INDENT + _node(ids[node_id], label))
    arrow = "-->" if view.directed else "---"
    for first, second, weight in view.edges:
        link = arrow if weight is None else f"{arrow}|{escape(weight)}|"
        lines.append(f"{INDENT}{ids[first]} {link} {ids[second]}")
    return "\n".join(lines)


def view_mermaid(view: View) -> str:
    """Render any view as a Mermaid flowchart."""
    if isinstance(view, ChainView):
        return chain_mermaid(view)
    if isinstance(view, TreeView):
        return tree_mermaid(view)
    return graph_mermaid(view)
