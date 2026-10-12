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

"""Tooling built on top of the data structures of ``sds``.

``sds.utils`` is the top layer of the package (#99): it may import any
structure module and ``sds.algorithms``, and no structure module imports
it. It holds what is neither algorithmic nor part of a domain's public
contract: presentation, command line, input and output.

Features that need third-party packages install them through optional
extras of the ``pysds-tools`` distribution (#100), for instance
``pip install "pysds-tools[image]"``. A missing extra raises
:class:`OptionalDependencyError` when the feature is used, never at import.
"""

from .exceptions import OptionalDependencyError

__all__ = ["OptionalDependencyError"]
