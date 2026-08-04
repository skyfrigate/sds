# Copyright 2024-2025, skyfrigate, biface
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

"""Probabilistic graphical model structures module.

This module provides structures for representing probability distributions
over discrete random variables as graphical models: Bayesian networks
(directed, acyclic) and Markov random fields (undirected, may contain
cycles). It deliberately holds no inference logic — algorithms such as
Variable Elimination or Belief Propagation belong to ``sds.algorithms`` and
operate on instances of these structures.

Submodules
----------
variable
    RandomVariable — a named, discrete, finite-domain random variable.
factor
    Factor — a non-negative potential table over a scope of variables.
interfaces
    Abstract base classes defining the graphical model contracts.

Classes
-------
RandomVariable
    A discrete random variable with a finite domain of states.
Factor
    A potential table mapping joint assignments to non-negative values.
BayesianNetwork
    Directed acyclic graphical model with per-variable CPTs.

Abstract Interfaces
-------------------
AbstractGraphicalModel
    Common base: manages variables and factors, evaluates a joint
    assignment's potential.
AbstractBayesianNetwork
    Directed, acyclic graphical model with locally normalized CPTs.
AbstractMarkovRandomField
    Undirected graphical model with (generally unnormalized) potentials.

Examples
--------
Define two variables and a factor over their joint scope:

>>> from sds.probabilistic import RandomVariable, Factor
>>> rain = RandomVariable("Rain", ("true", "false"))
>>> sprinkler = RandomVariable("Sprinkler", ("true", "false"))
>>> table = {
...     ("true", "true"): 0.01,
...     ("true", "false"): 0.99,
...     ("false", "true"): 0.4,
...     ("false", "false"): 0.6,
... }
>>> cpt = Factor((rain, sprinkler), table)
>>> cpt.value({rain: "true", sprinkler: "false"})
0.99

Build a small Bayesian network and evaluate a joint assignment (the CPT's
scope must start with the conditioned variable itself):

>>> from sds.probabilistic import BayesianNetwork
>>> bn = BayesianNetwork()
>>> bn.add_variable(rain)
>>> bn.add_variable(sprinkler)
>>> bn.add_edge(rain, sprinkler)
>>> bn.set_cpt(rain, Factor((rain,), {("true",): 0.2, ("false",): 0.8}))
>>> sprinkler_cpt = Factor((sprinkler, rain), {
...     (s, r): table[(r, s)] for r in rain.domain for s in sprinkler.domain
... })
>>> bn.set_cpt(sprinkler, sprinkler_cpt)
>>> round(bn.joint({rain: "true", sprinkler: "false"}), 4)
0.198

Notes
-----
``MarkovRandomField`` is not yet implemented in this module. ``HiddenMarkovModel``
is planned separately and is intentionally not part of the
``AbstractGraphicalModel`` hierarchy — its sequential structure (hidden
states, observations, transition/emission matrices) does not map onto a
generic scope-of-variables factor model.

``BayesianNetwork`` composes ``sds.graph.DirectedGraph`` for topology
rather than reimplementing adjacency; ``AbstractMarkovRandomField``
implementations are expected to do the same with ``sds.graph.Graph``.

See Also
--------
sds.core : Core collection interfaces.
sds.graph : Graph data structures, composed here for topology.
sds.algorithms : Algorithms (planned), including inference over these
    structures.

References
----------
.. [1] Koller, D., & Friedman, N. (2009). Probabilistic Graphical Models:
       Principles and Techniques. MIT Press.
.. [2] Murphy, K. P. (2012). Machine Learning: A Probabilistic Perspective.
       MIT Press. Chapter 10: Directed Graphical Models.
"""

from .bayesian_network import BayesianNetwork
from .factor import Factor
from .interfaces import (
    AbstractBayesianNetwork,
    AbstractGraphicalModel,
    AbstractMarkovRandomField,
)
from .variable import RandomVariable

__all__ = [
    # Building blocks
    "RandomVariable",
    "Factor",
    # Concrete structures
    "BayesianNetwork",
    # Abstract interfaces
    "AbstractGraphicalModel",
    "AbstractBayesianNetwork",
    "AbstractMarkovRandomField",
]

__version__ = "0.1.0"
