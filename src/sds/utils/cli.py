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

"""The ``pysds`` command (#106).

``pysds show FILE`` reads a structure described in a JSON file, or a YAML
file with the ``yaml`` extra, and prints it with the visualiser::

    pysds show tree.json                      # plain text on stdout
    pysds show graph.yaml --format mermaid    # Mermaid flowchart
    pysds show graph.json --format dot --output graph.dot
    pysds show tree.json --image tree.png     # needs the image extra
    cat stack.json | pysds show -             # JSON on standard input

``python -m sds`` runs the same command. The input document names the
class in ``type`` and gives the content in ``items`` (linear structures
and keyed trees), ``root`` (general trees) or ``nodes`` and ``edges``
(graphs); ``options`` are passed to the constructor. For example::

    {"type": "WeightedDirectedGraph",
     "nodes": [{"id": "a"}, {"id": "b"}],
     "edges": [["a", "b", 2.5]]}

Exit status: 0 on success; 1 when the input cannot be read or describes
no valid structure, or a needed extra is missing, with a one-line
``pysds: error: ...`` message on standard error; 2 on a usage error.
"""

import argparse
import json
import sys
from importlib import metadata
from pathlib import Path
from typing import Any, Optional, Sequence, Tuple

from ..core.exceptions import DataStructureError, InvalidParameterError
from ._loader import SUPPORTED, build
from ._optional import import_optional
from .visualizer import FORMATS, render, save_image

__all__ = ["main"]

PROG = "pysds"

#: File suffixes read as YAML; any other file is read as JSON.
YAML_SUFFIXES = (".yaml", ".yml")


def _version() -> str:
    try:
        return metadata.version("pysds-tools")
    except metadata.PackageNotFoundError:  # running from a source tree
        return "unknown"


def _parsers() -> Tuple[argparse.ArgumentParser, argparse.ArgumentParser]:
    """Return the ``pysds`` parser and its ``show`` subparser."""
    parser = argparse.ArgumentParser(
        prog=PROG,
        description="Display the data structures of pysds-tools.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {_version()}")
    commands = parser.add_subparsers(dest="command", required=True)

    show = commands.add_parser(
        "show",
        help="display a structure described in a JSON or YAML file",
        description=(
            "Build the structure described in FILE and display it. "
            f"Supported types: {', '.join(SUPPORTED)}."
        ),
    )
    show.add_argument(
        "file",
        metavar="FILE",
        help="JSON file, YAML file (.yaml, .yml; yaml extra), or - for "
        "JSON on standard input",
    )
    show.add_argument(
        "--format",
        choices=FORMATS,
        help="text output format (default: text); dot is for graphs only",
    )
    show.add_argument(
        "--output",
        metavar="PATH",
        help="write the text output to PATH instead of standard output",
    )
    show.add_argument(
        "--image",
        metavar="PATH",
        help="save a drawing to PATH, format from its extension (image extra)",
    )
    return parser, show


def _parse_json(text: str, source: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise InvalidParameterError(f"{source}: invalid JSON: {exc}") from exc


def _yaml_problem(exc: Exception) -> str:
    """Return a one-line message for a PyYAML error.

    ``str()`` of a PyYAML error spans several lines (context, excerpt,
    caret); keep the problem and its position, in the form the
    :mod:`json` messages use.
    """
    problem = getattr(exc, "problem", None)
    mark = getattr(exc, "problem_mark", None)
    if problem and mark is not None:
        return f"{problem}: line {mark.line + 1} column {mark.column + 1}"
    return " ".join(str(exc).split())


def _parse_yaml(text: str, source: str) -> Any:
    yaml = import_optional("yaml", "yaml")
    try:
        return yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise InvalidParameterError(
            f"{source}: invalid YAML: {_yaml_problem(exc)}"
        ) from exc


def _read(source: str) -> Any:
    """Decode the document at ``source``, ``-`` being standard input."""
    if source == "-":
        return _parse_json(sys.stdin.read(), "<stdin>")
    path = Path(source)
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise InvalidParameterError(f"{source}: not UTF-8 text") from exc
    if path.suffix.lower() in YAML_SUFFIXES:
        return _parse_yaml(text, source)
    return _parse_json(text, source)


def _write(text: str, output: Optional[str]) -> None:
    if output is None:
        print(text)
    else:
        Path(output).write_text(text + "\n", encoding="utf-8")


def _describe(exc: Exception) -> str:
    if isinstance(exc, OSError) and exc.strerror:
        return f"{exc.filename}: {exc.strerror}" if exc.filename else exc.strerror
    return str(exc)


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Run the ``pysds`` command.

    Parameters
    ----------
    argv : sequence of str, optional
        Command-line arguments without the program name; ``sys.argv[1:]``
        by default.

    Returns
    -------
    int
        0 on success, 1 on an input, structure or missing-extra error.

    Raises
    ------
    SystemExit
        Raised by :mod:`argparse`: code 2 on a usage error, 0 after
        ``--help`` or ``--version``.

    Examples
    --------
    >>> main(["--version"])  # doctest: +SKIP
    pysds 0.8.0
    """
    parser, show = _parsers()
    args = parser.parse_args(argv)
    if args.image is not None and (args.format is not None or args.output is not None):
        show.error("--image cannot be combined with --format or --output")

    try:
        structure = build(_read(args.file))
        if args.image is not None:
            save_image(structure, args.image)
        else:
            _write(render(structure, args.format or "text"), args.output)
    except (DataStructureError, OSError) as exc:
        print(f"{PROG}: error: {_describe(exc)}", file=sys.stderr)
        return 1
    return 0
