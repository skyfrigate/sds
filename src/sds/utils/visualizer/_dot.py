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

"""Graphviz DOT rendering of graph views.

The output is a DOT source string; producing it needs no Graphviz
install (#102). Nodes are identified by their graph id, which is unique,
and labelled with the user label.
"""

from ._views import GraphView

INDENT = "    "


def quote(text: str) -> str:
    """Return ``text`` as a quoted DOT string."""
    escaped = text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{escaped}"'


def graph_dot(view: GraphView) -> str:
    """Render a graph view as a ``digraph`` or a ``graph``."""
    keyword, arrow = ("digraph", "->") if view.directed else ("graph", "--")
    lines = [f"{keyword} {{"]
    lines.extend(
        f"{INDENT}{quote(node_id)} [label={quote(label)}];"
        for node_id, label in view.nodes
    )
    for first, second, weight in view.edges:
        attributes = "" if weight is None else f" [label={quote(weight)}]"
        lines.append(f"{INDENT}{quote(first)} {arrow} {quote(second)}{attributes};")
    lines.append("}")
    return "\n".join(lines)
