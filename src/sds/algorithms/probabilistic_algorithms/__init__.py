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

"""Inference algorithms for probabilistic graphical models.

The structures of :mod:`sds.probabilistic` only store a model; answering a
question about it is the job of the algorithms below (#84).

On Bayesian networks and Markov random fields (any ``AbstractGraphicalModel``):

- :func:`variable_elimination`: the exact distribution of one or more
  variables given evidence.
- :func:`belief_propagation`: the marginal of every variable given
  evidence, by message passing; exact on tree-shaped models, approximate
  (loopy) otherwise.

On hidden Markov models (any ``AbstractHiddenMarkovModel``):

- :func:`forward`: the log-likelihood of an observation sequence and the
  filtered state distributions.
- :func:`viterbi`: the most likely sequence of hidden states.

``Factor`` has no product or marginalization operation. The algorithms
copy each factor into a private working table, compute there, and return
plain ``Factor`` objects.
"""

from .belief_propagation import belief_propagation
from .forward import forward
from .variable_elimination import variable_elimination
from .viterbi import viterbi

__all__ = ["variable_elimination", "belief_propagation", "forward", "viterbi"]
