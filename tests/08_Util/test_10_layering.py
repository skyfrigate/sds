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

"""sds.utils is the top layer: no other module of sds imports it (#99).

The check reads the sources with :mod:`ast` instead of importing them, so
an import hidden inside a function body is caught as well as a top-level
one. Relative imports are resolved against the module that holds them.
"""

import ast
from importlib.util import resolve_name
from pathlib import Path
from typing import Iterator, List

import pytest

import sds

ROOT = Path(sds.__file__).resolve().parent

#: The top layer, and the entry point of ``python -m sds`` that runs it.
ALLOWED = ("utils", "__main__.py")


def _module_name(path: Path, root: Path) -> str:
    parts = ("sds", *path.relative_to(root).with_suffix("").parts)
    return ".".join(parts[:-1] if parts[-1] == "__init__" else parts)


def _imports(source: str, module: str, is_package: bool) -> Iterator[str]:
    """Yield the absolute name of every module ``source`` imports."""
    package = module if is_package else module.rpartition(".")[0]
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            yield from (alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                base = resolve_name("." * node.level + (node.module or ""), package)
            else:
                base = node.module or ""
            yield base
            # ``from . import utils`` names the module in the imported names.
            yield from (f"{base}.{alias.name}" for alias in node.names)


def _is_utils(name: str) -> bool:
    return name == "sds.utils" or name.startswith("sds.utils.")


def _violations(path: Path, root: Path = ROOT) -> List[str]:
    module = _module_name(path, root)
    source = path.read_text(encoding="utf-8")
    names = _imports(source, module, path.name == "__init__.py")
    return sorted({f"{module} imports {name}" for name in names if _is_utils(name)})


def _structure_modules() -> List[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.py")
        if path.relative_to(ROOT).parts[0] not in ALLOWED
    )


def test_no_module_below_utils_imports_it() -> None:
    """Every module outside sds.utils loads without it."""
    modules = _structure_modules()
    assert len(modules) > 50  # the walk found the package
    violations = [line for path in modules for line in _violations(path)]
    assert violations == []


@pytest.mark.parametrize(
    "relative, source",
    [
        ("graph/edge.py", "from sds.utils import visualizer"),
        ("graph/edge.py", "import sds.utils.cli"),
        ("graph/edge.py", "from ..utils import OptionalDependencyError"),
        ("graph/edge.py", "from .. import utils"),
        ("graph/__init__.py", "from ..utils.visualizer import render"),
        ("__init__.py", "from .utils import cli"),
        ("graph/edge.py", "def f():\n    from ..utils import cli\n"),
    ],
)
def test_the_check_sees_each_form(tmp_path: Path, relative: str, source: str) -> None:
    """Absolute, relative and function-level imports are all detected."""
    path = tmp_path / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")
    assert _violations(path, tmp_path) != []


@pytest.mark.parametrize(
    "relative, source",
    [
        ("graph/edge.py", "from ..core.exceptions import DataStructureError"),
        ("graph/edge.py", "from . import utilities"),
        ("graph/edge.py", "import sds.utilsx"),
    ],
)
def test_the_check_ignores_other_imports(
    tmp_path: Path, relative: str, source: str
) -> None:
    """Neighbouring names are not mistaken for sds.utils."""
    path = tmp_path / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")
    assert _violations(path, tmp_path) == []
