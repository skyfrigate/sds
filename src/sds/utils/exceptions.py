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

"""Exceptions raised by the tooling of ``sds.utils``.

The structure modules raise the exceptions of :mod:`sds.core.exceptions`
(#101). This module holds only the errors of the tooling layer, all
deriving from :class:`~sds.core.exceptions.DataStructureError`.
"""

from ..core.exceptions import DataStructureError

__all__ = ["OptionalDependencyError"]


class OptionalDependencyError(DataStructureError, ImportError):
    """Exception raised when a feature needs an extra that is not installed.

    The message names the package that failed to import and the
    ``pysds-tools`` extra that provides it. Also an ``ImportError``, with
    :attr:`name` set to the missing package.

    Parameters
    ----------
    package : str
        Importable name of the missing package (``"matplotlib"``).
    extra : str
        Extra of ``pysds-tools`` that installs it (``"image"``).

    Examples
    --------
    >>> err = OptionalDependencyError("matplotlib", "image")
    >>> print(err)
    matplotlib is required for this feature: pip install "pysds-tools[image]"
    >>> err.extra
    'image'
    """

    def __init__(self, package: str, extra: str) -> None:
        self.package = package
        self.extra = extra
        self.message = (
            f"{package} is required for this feature: "
            f'pip install "pysds-tools[{extra}]"'
        )
        super().__init__(self.message)
        self.name = package
