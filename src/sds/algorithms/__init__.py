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

"""Algorithms operating on the data structures of ``sds``.

Algorithmic logic (searching, sorting, traversing, optimizing) lives here,
never inside the structure classes (#14). Each function takes the
structure it works on as a parameter, typed against the broadest abstract
interface that provides what the algorithm needs (#86).

Subpackages
-----------
sorting
    Comparison sorts on Python lists.
tree_algorithms
    Traversals of binary trees.
graph_algorithms
    Traversals, shortest paths and minimum spanning trees on graphs.
probabilistic_algorithms
    Inference on Bayesian networks, Markov random fields and hidden Markov
    models.
"""
