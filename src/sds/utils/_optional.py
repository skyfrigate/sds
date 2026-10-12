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

"""Lazy import of optional dependencies.

The base install of ``pysds-tools`` has no dependency (#100). Modules of
``sds.utils`` that need a third-party package import it through
:func:`import_optional` inside the function that uses it, so that
importing the module itself never fails on a base install.
"""

import importlib
from types import ModuleType

from .exceptions import OptionalDependencyError

__all__ = ["import_optional"]


def import_optional(module: str, extra: str) -> ModuleType:
    """Import an optional dependency, naming its extra if it is missing.

    Parameters
    ----------
    module : str
        Dotted name of the module to import (``"matplotlib.pyplot"``).
    extra : str
        Extra of ``pysds-tools`` that installs it (``"image"``).

    Returns
    -------
    ModuleType
        The imported module.

    Raises
    ------
    OptionalDependencyError
        If the top-level package of ``module`` is not installed. The error
        names the package and the extra to install.
    ModuleNotFoundError
        If the package is installed but one of its own dependencies is not.

    Examples
    --------
    >>> json = import_optional("json", "unused")
    >>> json.dumps([1])
    '[1]'
    """
    package = module.partition(".")[0]
    try:
        return importlib.import_module(module)
    except ModuleNotFoundError as exc:
        # Only the optional package itself being absent calls for the extra;
        # a broken install (one of its own dependencies missing) or any other
        # ImportError propagates unchanged.
        if exc.name is None or exc.name.partition(".")[0] != package:
            raise
        raise OptionalDependencyError(package, extra) from exc
