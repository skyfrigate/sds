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

"""Tests for the pysds command (#106).

main(argv) returns the exit status, so the command runs in-process: no
subprocess, and coverage sees every line.
"""

import io
import json
import runpy
import sys
from importlib import metadata
from pathlib import Path
from typing import Any, Dict, List

import pytest

from sds.utils import cli
from sds.utils.cli import main

GRAPH: Dict[str, Any] = {
    "type": "WeightedDirectedGraph",
    "nodes": [{"id": "a"}, {"id": "b"}],
    "edges": [["a", "b", 2.5]],
}

STACK: Dict[str, Any] = {"type": "Stack", "items": [1, 2, 3]}


def _json_file(tmp_path: Path, document: Any, name: str = "input.json") -> str:
    path = tmp_path / name
    path.write_text(json.dumps(document), encoding="utf-8")
    return str(path)


def _error_line(capsys: pytest.CaptureFixture[str]) -> str:
    """Return standard error, checked to be a single pysds error line."""
    captured = capsys.readouterr()
    assert captured.out == ""
    lines = captured.err.splitlines()
    assert len(lines) == 1, captured.err
    assert lines[0].startswith("pysds: error: ")
    return lines[0]


class TestVersion:
    """pysds --version."""

    def test_prints_the_installed_version(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """The version comes from the pysds-tools distribution."""
        monkeypatch.setattr(metadata, "version", lambda name: "9.9.9")
        with pytest.raises(SystemExit) as info:
            main(["--version"])
        assert info.value.code == 0
        assert capsys.readouterr().out == "pysds 9.9.9\n"

    def test_unknown_outside_an_installed_distribution(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Run from a source tree, the version is unknown."""

        def missing(name: str) -> str:
            raise metadata.PackageNotFoundError(name)

        monkeypatch.setattr(metadata, "version", missing)
        with pytest.raises(SystemExit):
            main(["--version"])
        assert capsys.readouterr().out == "pysds unknown\n"


class TestShow:
    """pysds show: text output."""

    def test_text_by_default(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Without --format, the text view is printed."""
        assert main(["show", _json_file(tmp_path, STACK)]) == 0
        assert capsys.readouterr().out == "top: 3 -> 2 -> 1\n"

    def test_mermaid(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """--format mermaid prints a Mermaid flowchart."""
        assert main(["show", _json_file(tmp_path, GRAPH), "--format", "mermaid"]) == 0
        assert capsys.readouterr().out.startswith("flowchart")

    def test_dot(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """--format dot prints a DOT digraph for a directed graph."""
        assert main(["show", _json_file(tmp_path, GRAPH), "--format", "dot"]) == 0
        out = capsys.readouterr().out
        assert out.startswith("digraph {")
        assert '"a" -> "b" [label="2.5"];' in out

    def test_standard_input(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """FILE - reads JSON on standard input."""
        monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(STACK)))
        assert main(["show", "-"]) == 0
        assert capsys.readouterr().out == "top: 3 -> 2 -> 1\n"

    def test_output_file(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """--output writes the text, newline-terminated, and prints nothing."""
        target = tmp_path / "stack.txt"
        assert main(["show", _json_file(tmp_path, STACK), "--output", str(target)]) == 0
        assert capsys.readouterr().out == ""
        assert target.read_text(encoding="utf-8") == "top: 3 -> 2 -> 1\n"


class TestYaml:
    """YAML input, through the yaml extra."""

    @pytest.mark.parametrize("name", ["queue.yaml", "queue.yml", "QUEUE.YML"])
    def test_yaml_suffixes(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str], name: str
    ) -> None:
        """.yaml and .yml, in any case, are read as YAML."""
        pytest.importorskip("yaml")
        path = tmp_path / name
        path.write_text("type: Queue\nitems: [a, b]\n", encoding="utf-8")
        assert main(["show", str(path)]) == 0
        assert capsys.readouterr().out == "front: a -> b :rear\n"

    def test_invalid_yaml(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """A YAML syntax error is an input error."""
        pytest.importorskip("yaml")
        path = tmp_path / "broken.yaml"
        path.write_text("type: [Stack\n", encoding="utf-8")
        assert main(["show", str(path)]) == 1
        assert _error_line(capsys) == (
            f"pysds: error: {path}: invalid YAML: "
            "expected ',' or ']', but got '<stream end>': line 2 column 1"
        )

    def test_yaml_error_without_position(self) -> None:
        """A PyYAML error with no mark is flattened to one line."""
        yaml = pytest.importorskip("yaml")
        exc = yaml.YAMLError("first line\n  second line")
        assert cli._yaml_problem(exc) == "first line second line"

    def test_missing_yaml_extra(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Without PyYAML, the error names the extra to install."""
        monkeypatch.setitem(sys.modules, "yaml", None)
        path = tmp_path / "stack.yaml"
        path.write_text("type: Stack\n", encoding="utf-8")
        assert main(["show", str(path)]) == 1
        assert 'pip install "pysds-tools[yaml]"' in _error_line(capsys)


class TestImage:
    """--image, through the image extra."""

    def test_saves_a_png(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """The drawing is saved in the format of the extension."""
        pytest.importorskip("matplotlib")
        target = tmp_path / "graph.png"
        assert main(["show", _json_file(tmp_path, GRAPH), "--image", str(target)]) == 0
        assert capsys.readouterr().out == ""
        assert target.read_bytes().startswith(b"\x89PNG")

    def test_unknown_image_format(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """An extension matplotlib cannot write is an error, not a trace."""
        pytest.importorskip("matplotlib")
        target = tmp_path / "graph.xyz"
        assert main(["show", _json_file(tmp_path, GRAPH), "--image", str(target)]) == 1
        assert "xyz" in _error_line(capsys)

    def test_missing_image_extra(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Without matplotlib, the error names the extra to install."""
        monkeypatch.setitem(sys.modules, "matplotlib", None)
        monkeypatch.delitem(sys.modules, "matplotlib.figure", raising=False)
        target = tmp_path / "graph.png"
        assert main(["show", _json_file(tmp_path, GRAPH), "--image", str(target)]) == 1
        assert 'pip install "pysds-tools[image]"' in _error_line(capsys)
        assert not target.exists()


class TestErrors:
    """Exit status 1: one error line on standard error, no trace."""

    @pytest.mark.parametrize(
        "document, message",
        [
            ({"type": "MinHeap"}, "unsupported type 'MinHeap'"),
            ({"type": "Stack", "items": 3}, "items: expected a list"),
            (
                {"type": "Graph", "edges": [["a", "b"]]},
                r"edges[0]: unknown node 'a'",
            ),
        ],
    )
    def test_invalid_document(
        self,
        tmp_path: Path,
        capsys: pytest.CaptureFixture[str],
        document: Dict[str, Any],
        message: str,
    ) -> None:
        """A document the loader rejects gives its message."""
        assert main(["show", _json_file(tmp_path, document)]) == 1
        assert message in _error_line(capsys)

    def test_invalid_json(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """A JSON syntax error names the file."""
        path = tmp_path / "broken.json"
        path.write_text("[1", encoding="utf-8")
        assert main(["show", str(path)]) == 1
        assert f"{path}: invalid JSON" in _error_line(capsys)

    def test_invalid_json_on_standard_input(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Standard input is named <stdin>."""
        monkeypatch.setattr(sys, "stdin", io.StringIO("{"))
        assert main(["show", "-"]) == 1
        assert "<stdin>: invalid JSON" in _error_line(capsys)

    def test_not_utf8(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """A file that is not UTF-8 text is reported as such."""
        path = tmp_path / "latin1.json"
        path.write_bytes('{"type": "é"}'.encode("latin-1"))
        assert main(["show", str(path)]) == 1
        assert _error_line(capsys) == f"pysds: error: {path}: not UTF-8 text"

    def test_missing_file(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """An unreadable file gives the system message, with its name."""
        path = tmp_path / "absent.json"
        assert main(["show", str(path)]) == 1
        assert _error_line(capsys) == (
            f"pysds: error: {path}: No such file or directory"
        )

    def test_unwritable_output(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """An output path in a missing directory is reported."""
        target = tmp_path / "absent" / "out.txt"
        assert main(["show", _json_file(tmp_path, STACK), "--output", str(target)]) == 1
        assert str(target) in _error_line(capsys)

    def test_dot_for_a_non_graph(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """DOT output is for graphs only."""
        assert main(["show", _json_file(tmp_path, STACK), "--format", "dot"]) == 1
        assert "graphs only" in _error_line(capsys)


class TestDescribe:
    """Messages for system errors without a file name."""

    def test_strerror_without_filename(self) -> None:
        """The system message alone is kept."""
        assert cli._describe(OSError(28, "No space left on device")) == (
            "No space left on device"
        )

    def test_plain_os_error(self) -> None:
        """An OSError without strerror falls back to str()."""
        assert cli._describe(OSError("disk detached")) == "disk detached"


class TestUsage:
    """Exit status 2: usage errors reported by argparse."""

    @pytest.mark.parametrize(
        "argv",
        [
            [],
            ["show"],
            ["show", "f.json", "--format", "png"],
            ["show", "f.json", "--image", "f.png", "--format", "dot"],
            ["show", "f.json", "--image", "f.png", "--output", "f.txt"],
        ],
    )
    def test_usage_error(
        self, argv: List[str], capsys: pytest.CaptureFixture[str]
    ) -> None:
        """argparse exits with 2 and prints the usage."""
        with pytest.raises(SystemExit) as info:
            main(argv)
        assert info.value.code == 2
        assert "usage: pysds" in capsys.readouterr().err

    def test_help_lists_supported_types(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """show --help names the types the loader accepts."""
        with pytest.raises(SystemExit) as info:
            main(["show", "--help"])
        assert info.value.code == 0
        out = " ".join(capsys.readouterr().out.split())
        assert "WeightedDirectedGraph" in out


class TestModule:
    """python -m sds runs the same command."""

    def test_python_dash_m(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """The exit status of main() becomes the process exit status."""
        monkeypatch.setattr(sys, "argv", ["sds", "show", _json_file(tmp_path, STACK)])
        with pytest.raises(SystemExit) as info:
            runpy.run_module("sds", run_name="__main__", alter_sys=True)
        assert info.value.code == 0
        assert capsys.readouterr().out == "top: 3 -> 2 -> 1\n"
