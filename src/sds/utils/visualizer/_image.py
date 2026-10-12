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

"""Image output of the visualiser, through matplotlib (extra ``image``).

matplotlib is imported here only, inside :func:`save_drawing`, through
:func:`~sds.utils._optional.import_optional`: importing the visualiser
never needs the extra (#100). The figure is built with the object API
(``matplotlib.figure.Figure``), which needs no pyplot, no GUI backend and
leaves the user's matplotlib state untouched.
"""

import os
from pathlib import Path
from typing import Any, List, Tuple, Union

from ...core.exceptions import InvalidParameterError
from .._optional import import_optional
from ._layout import Drawing

#: Margin, in layout units, around the outermost nodes.
MARGIN = 0.8
#: Figure inches per layout unit, and minimum figure size.
SCALE = 1.1
MIN_SIZE = 2.5


def label_position(
    x1: float, y1: float, x2: float, y2: float, bend: float
) -> Tuple[float, float]:
    """Return where to write an edge label.

    The label sits at 40 % of the way from the start, so that the labels
    of two edges crossing at their middles do not overlap, and is moved
    off a bent edge's chord onto the arc.
    """
    t = 0.4
    x = x1 + t * (x2 - x1)
    y = y1 + t * (y2 - y1)
    if bend:
        # arc3 bends the edge by ``bend`` times the chord, to the left of
        # the direction of travel at the middle; 4t(1-t) scales the
        # offset of a quadratic curve away from its middle.
        offset = bend * 4 * t * (1 - t) / 2
        x += offset * (y2 - y1)
        y -= offset * (x2 - x1)
    return x, y


def save_drawing(drawing: Drawing, path: Union[str, "os.PathLike[str]"]) -> None:
    """Draw ``drawing`` with matplotlib and save it to ``path``.

    The format follows the file extension; it must be one matplotlib can
    write (``png``, ``svg``, ``pdf``...).

    Raises
    ------
    OptionalDependencyError
        If matplotlib is not installed.
    InvalidParameterError
        If the extension names no format matplotlib can write.
    """
    figure_module = import_optional("matplotlib.figure", "image")
    xmin, xmax, ymin, ymax = drawing.bounds()
    width = max(MIN_SIZE, (xmax - xmin + 2 * MARGIN) * SCALE)
    height = max(MIN_SIZE, (ymax - ymin + 2 * MARGIN) * SCALE)
    figure = figure_module.Figure(figsize=(width, height))

    suffix = Path(path).suffix.lower().lstrip(".")
    supported = figure.canvas.get_supported_filetypes()
    if suffix not in supported:
        raise InvalidParameterError(
            f"Cannot write {suffix or 'a file without extension'!r}: "
            f"use one of {', '.join(sorted(supported))}"
        )

    axes = figure.subplots()
    axes.set_axis_off()
    axes.set_xlim(xmin - MARGIN, xmax + MARGIN)
    axes.set_ylim(ymin - MARGIN, ymax + MARGIN)
    axes.set_aspect("equal")

    boxes: List[Any] = []
    for node in drawing.nodes:
        if node.marker:
            text = axes.text(
                node.x, node.y, node.label, ha="center", va="center", style="italic"
            )
        else:
            text = axes.text(
                node.x,
                node.y,
                node.label,
                ha="center",
                va="center",
                bbox={"boxstyle": "round,pad=0.3", "fc": "white", "ec": "black"},
                zorder=3,
            )
        boxes.append(text)

    for edge in drawing.edges:
        start, end = drawing.nodes[edge.start], drawing.nodes[edge.end]
        if edge.start == edge.end:
            loop = "\u21ba" if edge.label is None else f"\u21ba {edge.label}"
            axes.text(start.x, start.y + 0.35, loop, ha="center", va="bottom")
            continue
        axes.annotate(
            "",
            xy=(end.x, end.y),
            xytext=(start.x, start.y),
            arrowprops={
                "arrowstyle": edge.arrow,
                "connectionstyle": f"arc3,rad={edge.bend}",
                "patchA": boxes[edge.start].get_bbox_patch(),
                "patchB": boxes[edge.end].get_bbox_patch(),
                "shrinkA": 2,
                "shrinkB": 2,
                "color": "black",
            },
            # Above the boxes: matplotlib positions a text box while drawing
            # the text, so drawing edges afterwards clips them to the boxes'
            # current borders, where the arrow heads land.
            zorder=4,
        )
        if edge.label is not None:
            x, y = label_position(start.x, start.y, end.x, end.y, edge.bend)
            axes.text(
                x,
                y,
                edge.label,
                ha="center",
                va="center",
                fontsize="small",
                bbox={"boxstyle": "round,pad=0.15", "fc": "white", "ec": "none"},
                zorder=5,
            )

    figure.savefig(path, format=suffix, bbox_inches="tight")
