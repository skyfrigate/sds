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

"""Every subpackage of sds imports on a base install, per #100 and #105."""

import os
import subprocess
import sys
import textwrap
from pathlib import Path

import sds

#: Packages installed only by extras of pysds-tools.
EXTRA_PACKAGES = ("matplotlib", "yaml")

SCRIPT = textwrap.dedent("""
    import importlib.abc
    import pkgutil
    import sys

    BLOCKED = set(sys.argv[1:])

    class BlockExtras(importlib.abc.MetaPathFinder):
        def find_spec(self, fullname, path, target=None):
            if fullname.partition(".")[0] in BLOCKED:
                raise ModuleNotFoundError(f"blocked: {fullname}", name=fullname)
            return None

    sys.meta_path.insert(0, BlockExtras())

    import sds

    failed = []
    for info in pkgutil.walk_packages(sds.__path__, "sds."):
        try:
            importlib.import_module(info.name)
        except Exception as exc:
            failed.append(f"{info.name}: {type(exc).__name__}: {exc}")
    print("\\n".join(failed))
    sys.exit(1 if failed else 0)
    """)


def test_every_module_imports_without_extras() -> None:
    """No module of sds needs an extra at import time."""
    src = str(Path(sds.__file__).resolve().parent.parent)
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(
        p for p in (src, env.get("PYTHONPATH", "")) if p
    )
    result = subprocess.run(
        [sys.executable, "-c", SCRIPT, *EXTRA_PACKAGES],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
