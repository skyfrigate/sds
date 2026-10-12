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

"""Tests for the optional-dependency helper of sds.utils, per #105."""

import sys
import textwrap
from pathlib import Path

import pytest

from sds.core.exceptions import DataStructureError
from sds.utils import OptionalDependencyError
from sds.utils._optional import import_optional


class TestOptionalDependencyError:
    """Tests for OptionalDependencyError."""

    def test_hierarchy(self) -> None:
        """The error is a DataStructureError and an ImportError."""
        err = OptionalDependencyError("matplotlib", "image")
        assert isinstance(err, DataStructureError)
        assert isinstance(err, ImportError)

    def test_message_names_package_and_extra(self) -> None:
        """The message gives the package and the install command."""
        err = OptionalDependencyError("yaml", "yaml")
        assert err.message == (
            'yaml is required for this feature: pip install "pysds-tools[yaml]"'
        )
        assert str(err) == err.message

    def test_attributes(self) -> None:
        """package, extra and ImportError.name are set."""
        err = OptionalDependencyError("matplotlib", "image")
        assert err.package == "matplotlib"
        assert err.extra == "image"
        assert err.name == "matplotlib"


class TestImportOptional:
    """Tests for import_optional()."""

    def test_returns_installed_module(self) -> None:
        """An installed module is returned as is."""
        import json

        assert import_optional("json", "unused") is json

    def test_returns_submodule(self) -> None:
        """A dotted name returns the submodule."""
        import os.path

        assert import_optional("os.path", "unused") is os.path

    def test_missing_package_names_extra(self) -> None:
        """A missing package raises OptionalDependencyError naming the extra."""
        with pytest.raises(OptionalDependencyError, match=r"pysds-tools\[image\]"):
            import_optional("sds_absent_package_105", "image")

    def test_missing_package_of_submodule(self) -> None:
        """For a dotted name, the error names the top-level package."""
        with pytest.raises(OptionalDependencyError) as info:
            import_optional("sds_absent_package_105.pyplot", "image")
        assert info.value.package == "sds_absent_package_105"
        assert isinstance(info.value.__cause__, ModuleNotFoundError)

    @pytest.mark.parametrize(
        "module, extra",
        [("matplotlib.pyplot", "image"), ("yaml", "yaml")],
    )
    def test_blocked_extra_package(
        self, monkeypatch: pytest.MonkeyPatch, module: str, extra: str
    ) -> None:
        """With the package unimportable, the error names its real extra."""
        package = module.partition(".")[0]
        monkeypatch.setitem(sys.modules, package, None)
        if module != package:
            monkeypatch.delitem(sys.modules, module, raising=False)
        with pytest.raises(OptionalDependencyError, match=rf"\[{extra}\]"):
            import_optional(module, extra)

    def _make_package(self, root: Path, name: str, body: str) -> None:
        """Write a one-module package under root."""
        package = root / name
        package.mkdir()
        (package / "__init__.py").write_text(textwrap.dedent(body))

    def test_broken_install_is_not_masked(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A missing dependency of an installed package propagates."""
        self._make_package(
            tmp_path, "sds_broken_105", "import sds_absent_dependency_105\n"
        )
        monkeypatch.syspath_prepend(str(tmp_path))
        with pytest.raises(ModuleNotFoundError) as info:
            import_optional("sds_broken_105", "image")
        assert not isinstance(info.value, OptionalDependencyError)
        assert info.value.name == "sds_absent_dependency_105"

    def test_other_import_error_propagates(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """An ImportError raised inside the package propagates."""
        self._make_package(
            tmp_path, "sds_failing_105", "raise ImportError('broken on import')\n"
        )
        monkeypatch.syspath_prepend(str(tmp_path))
        with pytest.raises(ImportError, match="broken on import") as info:
            import_optional("sds_failing_105", "image")
        assert not isinstance(info.value, OptionalDependencyError)
