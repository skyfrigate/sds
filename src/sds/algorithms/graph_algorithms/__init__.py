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

"""Algorithms on graphs.

- :func:`bfs` and :func:`dfs` (any ``AbstractGraph``): the nodes reachable
  from a source, in breadth-first or depth-first order.

Every function reads the graph through its public interface only
(``neighbors()``, ``outgoing_edges()``, ``edges()``) and never modifies it.
Neighbors are visited in the order the graph yields them, which is edge
insertion order (#91), so every result is reproducible.

The traversals are lazy generators: the graph must not be modified until
they are exhausted.
"""

from .bfs import bfs
from .dfs import dfs

__all__ = ["bfs", "dfs"]
