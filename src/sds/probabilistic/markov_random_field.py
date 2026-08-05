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

"""Markov random field implementation.

This module provides ``MarkovRandomField``, a concrete
``AbstractMarkovRandomField``. Topology (undirected dependency edges) is
delegated to a composed ``sds.graph.Graph`` rather than reimplemented; each
``RandomVariable`` is wrapped in a ``GraphNode`` (using the variable's name
as node id), mirroring ``BayesianNetwork``'s approach with ``DirectedGraph``.

Unlike a Bayesian network, factors here are **not** normalized and are not
assigned one-per-variable: a factor is attached over any subset of
variables that forms a **clique** of the underlying graph (the standard
Hammersley-Clifford correspondence between graph structure and
factorization). ``add_factor`` enforces this at attach-time, fail-fast,
consistent with the rest of the library (e.g. DD-007's
``UndirectedGraph``/``DirectedEdge`` rejection).

No inference lives here: ``joint()`` only multiplies the stored potentials
together, giving a value proportional to the true joint distribution — not
the true probability, since that requires dividing by the partition
function Z (an inference concern, reserved for ``sds.algorithms``).

Classes
-------
MarkovRandomField
    Undirected graphical model with potentials attached over cliques.

Examples
--------
>>> from sds.probabilistic import Factor, MarkovRandomField, RandomVariable
>>> a = RandomVariable("A", ("0", "1"))
>>> b = RandomVariable("B", ("0", "1"))
>>> mrf = MarkovRandomField()
>>> mrf.add_variable(a)
>>> mrf.add_variable(b)
>>> mrf.add_edge(a, b)
>>> potential = Factor(
...     (a, b),
...     {("0", "0"): 2.0, ("0", "1"): 0.5, ("1", "0"): 0.5, ("1", "1"): 2.0},
... )
>>> mrf.add_factor(potential)
>>> mrf.joint({a: "0", b: "0"})
2.0

See Also
--------
sds.probabilistic.interfaces.AbstractMarkovRandomField : Contract implemented here.
sds.graph.graph.Graph : Composed for topology.
"""

from typing import Any, Dict, Iterator, List, Mapping

from ..graph import Edge, Graph, GraphNode
from .factor import Factor
from .interfaces import AbstractMarkovRandomField
from .variable import RandomVariable

__all__ = ["MarkovRandomField"]


class MarkovRandomField(AbstractMarkovRandomField):
    """Undirected graphical model with potentials attached over cliques.

    Examples
    --------
    See the module-level docstring for a full worked example.

    Notes
    -----
    Each ``RandomVariable`` is stored as the ``data`` payload of a
    ``GraphNode`` whose id is the variable's name; topology is delegated
    entirely to a composed ``Graph``. Unlike ``BayesianNetwork``, there is
    no per-variable completeness requirement: ``joint()`` multiplies
    whatever potentials are attached, without checking that every variable
    participates in at least one (a variable with no potential simply does
    not constrain the (unnormalized) joint value).

    See Also
    --------
    AbstractMarkovRandomField : The interface this class implements.
    """

    __slots__ = ("_graph", "_variables", "_nodes", "_factors")

    def __init__(self) -> None:
        self._graph: Graph = Graph()
        self._variables: Dict[str, RandomVariable] = {}
        self._nodes: Dict[str, GraphNode] = {}
        self._factors: List[Factor] = []

    # ------------------------------------------------------------------
    # Collection
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        return len(self._variables)

    def is_empty(self) -> bool:
        return len(self._variables) == 0

    def clear(self) -> None:
        self._graph = Graph()
        self._variables.clear()
        self._nodes.clear()
        self._factors.clear()

    def __iter__(self) -> Iterator[RandomVariable]:
        return iter(self._variables.values())

    def __contains__(self, item: Any) -> bool:
        return isinstance(item, RandomVariable) and self.has_variable(item)

    # ------------------------------------------------------------------
    # Variables
    # ------------------------------------------------------------------

    def add_variable(self, variable: RandomVariable) -> None:
        """See AbstractGraphicalModel.add_variable."""
        if variable.name in self._variables:
            raise ValueError(f"Variable '{variable.name}' already exists")
        node = GraphNode(variable, variable.name)
        self._graph.add_node(node)
        self._variables[variable.name] = variable
        self._nodes[variable.name] = node

    def has_variable(self, variable: RandomVariable) -> bool:
        """See AbstractGraphicalModel.has_variable."""
        return self._variables.get(variable.name) == variable

    def get_variable(self, name: str) -> RandomVariable:
        """See AbstractGraphicalModel.get_variable."""
        return self._variables[name]

    def variables(self) -> Iterator[RandomVariable]:
        """See AbstractGraphicalModel.variables."""
        return iter(self._variables.values())

    # ------------------------------------------------------------------
    # Topology (delegated to the composed Graph)
    # ------------------------------------------------------------------

    def add_edge(self, first: RandomVariable, second: RandomVariable) -> None:
        """See AbstractMarkovRandomField.add_edge."""
        if not self.has_variable(first):
            raise ValueError(f"'{first.name}' is not in the field")
        if not self.has_variable(second):
            raise ValueError(f"'{second.name}' is not in the field")
        if first == second:
            raise ValueError(f"Self-loop is not allowed ('{first.name}')")

        edge = Edge(self._nodes[first.name], self._nodes[second.name])
        self._graph.add_edge(edge)

    def neighbors(self, variable: RandomVariable) -> Iterator[RandomVariable]:
        """See AbstractMarkovRandomField.neighbors."""
        node = self._nodes[variable.name]
        for neighbor in self._graph.neighbors(node):
            yield neighbor.data

    # ------------------------------------------------------------------
    # Factors / potentials
    # ------------------------------------------------------------------

    def add_factor(self, factor: Factor) -> None:
        """See AbstractGraphicalModel.add_factor.

        Raises
        ------
        ValueError
            If any variable in ``factor.scope`` is not part of the field,
            or if ``factor.scope`` is not a clique of the underlying graph
            (some pair of variables in the scope has no edge between them).
        """
        for variable in factor.scope:
            if not self.has_variable(variable):
                raise ValueError(f"'{variable.name}' is not in the field")
        self._validate_clique(factor)
        self._factors.append(factor)

    def _validate_clique(self, factor: Factor) -> None:
        """Check that every pair of variables in ``factor.scope`` is
        connected by an edge (Hammersley-Clifford correspondence)."""
        scope = factor.scope
        for i in range(len(scope)):
            for j in range(i + 1, len(scope)):
                first, second = scope[i], scope[j]
                node_first = self._nodes[first.name]
                node_second = self._nodes[second.name]
                if not self._graph.has_edge(node_first, node_second):
                    raise ValueError(
                        f"Factor scope {[v.name for v in scope]} is not a "
                        f"clique: no edge between '{first.name}' and "
                        f"'{second.name}'"
                    )

    def factors(self) -> Iterator[Factor]:
        """See AbstractGraphicalModel.factors."""
        return iter(self._factors)

    def factors_for(self, variable: RandomVariable) -> Iterator[Factor]:
        """See AbstractGraphicalModel.factors_for."""
        if not self.has_variable(variable):
            raise ValueError(f"'{variable.name}' is not in the field")
        for factor in self._factors:
            if variable in factor.scope:
                yield factor

    def joint(self, assignment: Mapping[RandomVariable, Any]) -> float:
        """See AbstractGraphicalModel.joint.

        Notes
        -----
        Unlike ``BayesianNetwork.joint``, this does not check that every
        variable participates in at least one factor: an unnormalized
        potential over a subset of variables is still well-defined even if
        some variables are unconstrained by any attached factor.
        """
        result = 1.0
        for factor in self._factors:
            result *= factor.value(assignment)
        return result

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"MarkovRandomField(variables={len(self._variables)}, "
            f"edges={self._graph.edge_count()}, factors={len(self._factors)})"
        )
